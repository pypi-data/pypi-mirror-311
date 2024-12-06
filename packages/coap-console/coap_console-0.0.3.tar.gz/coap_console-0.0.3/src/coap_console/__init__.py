import argparse
import asyncio
from asyncio import Queue, wait_for, create_task, Future
import io
from pathlib import Path
import sys
import threading
import time
from typing import Optional, Union
import urllib.parse

# just for the side effect
import readline

import aiocoap
import cbor2
import cbor_diag
from aiocoap.util.vendored import link_header

class AutoDiscoveryError(Exception):
    """Error with a user friendly message raised when autodiscovery does not succeed"""

class UriWithRemote:
    """URI with an aiocoap remote attached

    The remote needs to encode the URI's Origin when queried back."""

    uri: str
    remote: Optional[aiocoap.interfaces.EndpointAddress]

    def __init__(self, uri: Union[str, "UriWithRemote"], remote: aiocoap.interfaces.EndpointAddress = None):
        if isinstance(uri, UriWithRemote):
            self.uri = uri.uri
            self.remote = uri.remote
        else:
            self.uri = uri
            self.remote = None
        if remote is not None:
            self.remote = remote

    def __repr__(self):
        return f"<{type(self).__name__} {self.uri}" + (">" if self.remote is None else f" via {self.remote}>")

    def set_on_request(self, message: aiocoap.Message):
        """Modify message to use self as URI, asserting the correctness of the remote"""

        message.set_request_uri(self.uri)
        if self.remote is not None:
            message.remote = self.remote
            assert message.get_request_uri() == self.uri, "Remote did not fit the URI"

    def learn_from_response(self, message: aiocoap.Message):
        """Modify self to store the remote from a response message"""
        assert urllib.parse.urljoin(message.get_request_uri(), "/") == urllib.parse.urljoin(self.uri, "/"), "Message was for another URI"
        self.remote = message.remote

def clip_to_i32(n: int):
    n = n & 0xffffffff
    if n >= 0x80000000:
        n -= 2 ** 32
    return n

def cbor_stream_to_list(stream: bytes) -> list:
    full = len(stream)
    stream = io.BytesIO(stream)
    items = []
    while stream.tell() < full:
        items.append(cbor2.load(stream))
    return items

async def read_stream_to_console(ctx, uri: Union[str, UriWithRemote], *, waker: Optional[Queue[None]] = None, max_poll: float = 10):
    """Read data from a stream URI that is a variant of
    <https://forum.riot-os.org/t/coap-remote-shell/3340/5>. This is (for lack
    of implementations) not yet expecting to use observation. Consequently, it
    will never see recoverable gaps.

    (If the polling fails due to overflows, it's already too late; if the
    polling fails due to simultaneous writing, it'll get an error, and recover
    from the start of the available data. Only an observation with lost
    messages, or one where the server decides to rather send out the latest
    data, would result in recoverable gaps.)

    The polling will usually apply poll in intervals, exponentially backing off
    from the RTT to at most the given `max_poll` value in seconds. but if data
    arrives at the waker, eg. because the user has triggered something, the
    waker can be used to speed things up.
    """
    uri = UriWithRemote(uri)

    printed = None
    printed_available = False

    current_interval = max_poll

    while True:
        if printed_available:
            message = aiocoap.Message(code=aiocoap.FETCH, payload=cbor2.dumps(printed))
        else:
            message = aiocoap.Message(code=aiocoap.GET)
        uri.set_on_request(message)
        req_start = time.time()
        req = ctx.request(message)
        res = await req.response
        uri.learn_from_response(res)
        req_rtt = time.time() - req_start

        if res.code == aiocoap.SERVICE_UNAVAILABLE:
            printed_available = False
            max_age = res.opt.max_age
            if max_age is None:
                max_age = 60
            await asyncio.sleep(max(req_rtt, max_age))
            continue
        elif res.code != aiocoap.CONTENT:
            raise RuntimeError("Unexpected response from stdin endpoint: %s", res)

        items = cbor_stream_to_list(res.payload)
        [start, data] = items

        if printed is None:
            printed = start
        else:
            delta = clip_to_i32(start - printed)
            if delta == 0:
                pass
            elif delta > 0:
                print(f"(lost {delta} bytes)", end="", flush=True)
                printed += delta
            else:
                # This case should only ever be reached after recovering with a GET
                repeated = -delta
                if repeated > len(data):
                    continue # ignore complete duplicate
                else:
                    # ignore the missing start parts
                    start += repeated
                    data = data[repeated:]

        if len(data) != 0:
            current_interval = 0
        else:
            current_interval = min(current_interval * 2 + req_rtt, max_poll)

        assert printed == start
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
        printed = start + len(data)
        printed_available = True

        if waker is not None:
            try:
                await wait_for(waker.get(), current_interval)
            except TimeoutError:
                pass
            else:
                current_interval = 0
        else:
            time.sleep(current_interval)

async def post_commands_from_stdin(ctx, uri: UriWithRemote, wake_out: Optional[Queue[None]] = None):
    loop = asyncio.get_running_loop()
    while True:
        try:
            line = await loop.run_in_executor(None, lambda: input())
        except EOFError:
            break
        except asyncio.CancelledError:
            # happens at ^C (but only goes through when ^D or return is pressed after it)
            break

        # input() strips the newline
        line = line + '\n'

        reqmsg = aiocoap.Message(code=aiocoap.POST, payload=line.encode('utf8'))
        uri.set_on_request(reqmsg)
        req = ctx.request(reqmsg)
        res = await req.response_raising
        uri.learn_from_response(res)

        if wake_out is not None:
            await wake_out.put(None)

async def autodiscover(ctx, host: str) -> (UriWithRemote, Optional[UriWithRemote]):
    """Given a host URI, read /.well-known/core to discover stdout (eg. by its
    if="tag:riot-os.org,2021:ser-out") and stdin
    (if="tag:riot-os.org,2021:ser-out"), or more precise attributes (which are
    currently not implemented)"""

    wkc = urllib.parse.urljoin(host, '/.well-known/core?if=tag:riot-os.org,2021:ser-*')

    req = ctx.request(aiocoap.Message(uri=wkc, code=aiocoap.GET))
    res = await req.response_raising

    # Starting from `res` matters here if a multicast address was given --
    # then, we get the unicast address the response came from
    origin = urllib.parse.urljoin(res.get_request_uri(), '/')

    SO_IF = 'tag:riot-os.org,2021:ser-out'
    SI_IF = 'tag:riot-os.org,2021:ser-in'
    so_candidates = []
    si_candidates = []

    for link in link_header.parse(res.payload.decode('utf8')).links:
        if 'anchor' in link:
            continue
        if_on_link = " ".join(getattr(link, 'if')).split(' ')
        target = urllib.parse.urljoin(origin, link.href)
        if SO_IF in if_on_link:
            so_candidates.append(target)
        if SI_IF in if_on_link:
            si_candidates.append(target)

    if not so_candidates:
        raise AutoDiscoveryError('No resource with if="tag:riot-os.org,2021:ser-out" found')
    if len(so_candidates) > 1:
        raise AutoDiscoveryError(f'Multiple candidate stdout resources, please specify explicitly one of: {so_candidates}')
    if len(si_candidates) > 1:
        raise AutoDiscoveryError(f'Multiple candidate stdin resources, please specify explicitly one of: {si_candidates}')

    so, si = (so_candidates[0], si_candidates[0] if si_candidates else None)

    requested_origin = urllib.parse.urljoin(host, '/')
    so_origin = urllib.parse.urljoin(so, '/')
    si_origin = urllib.parse.urljoin(si, '/')

    if so is not None:
        so = UriWithRemote(so)
    if si is not None:
        si = UriWithRemote(si)

    if so_origin != requested_origin:
        print(f"Discovery yielded a stdout resource on a different host than requested: {so_origin}", file=sys.stderr)
    else:
        so.learn_from_response(res)
    if si is not None:
        if si_origin != requested_origin and si_origin != so_origin:
            print(f"Discovery yielded a stdin resource on a different host than requested: {si_origin}", file=sys.stderr)
        else:
            si.learn_from_response(res)

    return (so, si)

async def main():
    p = argparse.ArgumentParser(
            description="CoAP remote console",
            epilog="""Instead of stdout and stdin, a single URI without path
            can given; in that case, paths are auto-discovered. A multicast
            address can be used in that case; the first device that responds
            will be connected to.""",
            )
    p.add_argument("stdout", help="URI of a stdout-style resource.")
    p.add_argument("stdin", help="URI of a stdin-style resource", nargs='?')
    p.add_argument("--max-poll", default=10, type=float, help="Maximum time (in seconds) between polling requests", metavar="T")
    p.add_argument("--credentials", type=Path, help="aiocoap credentials JSON / CBOR EDN file to load", metavar="C")
    args = p.parse_args()

    ctx = await aiocoap.Context.create_client_context()
    if args.credentials:
        ctx.client_credentials.load_from_dict(cbor2.loads(cbor_diag.diag2cbor(args.credentials.open().read())))

    wake_queue = Queue()

    stdout_parsed = urllib.parse.urlparse(args.stdout)
    if not stdout_parsed.scheme:
        p.error("stdout must be a full URI (eg. `coap://hostname`).")

    if stdout_parsed.path in ('', '/'):
        (stdout, discovered_stdin) = await autodiscover(ctx, args.stdout)
    else:
        stdout = UriWithRemote(args.stdout)
        discovered_stdin = None

    if args.stdin is not None:
        stdin = UriWithRemote(urllib.parse.urljoin(stdout.uri, args.stdin))
        if urllib.parse.urljoin(stdin.uri, "/") == urllib.parse.urljoin(stdout.uri, "/"):
            stdin.remote = stdout.remote
    else:
        stdin = None

    if not stdin:
        stdin = discovered_stdin

    jobs = {}
    jobs['get stdout'] = read_stream_to_console(ctx, stdout, waker=wake_queue, max_poll=args.max_poll)

    if stdin:
        jobs['get stdin'] = post_commands_from_stdin(ctx, stdin, wake_out=wake_queue)

    try:
        await next(asyncio.as_completed(jobs.values()))
    finally:
        await ctx.shutdown()

async def aiocoap_errors_are_pretty(awaitable):
    try:
        await awaitable
    except aiocoap.error.Error as e:
        print(e, file=sys.stderr)
        sys.exit(1)

def outer_main():
    asyncio.run(aiocoap_errors_are_pretty(main()))

if __name__ == "__main__":
    outer_main()

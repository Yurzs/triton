#  Copyright (c) Yurzs 2020.

import asyncio
from triton.dns.core import DnsMessage
from triton.protocols.exception import TimeoutError


class UdpClient:
    def __init__(self, loop, message: DnsMessage, on_con_lost, timeout=5):
        self.loop = loop
        self.message = message
        self.transport = None
        self.on_con_lost = on_con_lost
        self.task = loop.create_task(self.timeout_task(timeout))

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message.pack())

    def datagram_received(self, data, addr):
        message = DnsMessage.unpack(data)
        self.on_con_lost.set_result(message)

    def error_received(self, exc):
        self.on_con_lost.set_exception(exc)

    def connection_lost(self, exc):
        return self.message

    async def timeout_task(self, time):
        await asyncio.sleep(time)
        try:
            if not self.on_con_lost.result():
                self.on_con_lost.set_exception(TimeoutError)
                self.on_con_lost.exception()
        except asyncio.base_futures.InvalidStateError:
            self.on_con_lost.set_exception(TimeoutError)
            self.on_con_lost.exception()

    @classmethod
    async def send_message(cls, message, host, port=53, timeout=1, retries=5, loop=None):
        on_con_lost = loop.create_future()
        try:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: cls(loop, message, on_con_lost, timeout),
                remote_addr=(str(host), port))
            for _ in range(retries):
                try:
                    message = await on_con_lost
                    return message
                except TimeoutError:
                    continue
                except ConnectionRefusedError:
                    protocol.task.cancel()
                    raise Exception("cannot connect")
                finally:
                    transport.close()
        except ConnectionRefusedError:
            pass


class UdpServer(asyncio.DatagramProtocol):

    def __init__(self, dns_server, *args, **kwargs):
        self.dns_server = dns_server
        super().__init__(*args, **kwargs)

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def datagram_received(self, data, addr) -> None:
        message = DnsMessage.unpack(data)
        task = asyncio.Task(self.to_async(message, addr))

    @asyncio.coroutine
    def to_async(self, message, addr):
        reply_message = yield from self.dns_server.proceed_request(message)
        self.transport.sendto(reply_message.pack(), addr)

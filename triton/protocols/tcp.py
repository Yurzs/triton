import asyncio
import triton
from triton.dns.core import DnsMessage


class TcpClient(asyncio.Protocol):

    def __init__(self, loop, message: DnsMessage, on_con_lost, timeout=5):
        self.loop = loop
        self.message = message
        self.transport = None
        self.on_con_lost = on_con_lost
        loop.create_task(self.timeout_task(timeout))

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message.Binary.full)

    def data_received(self, data: bytes) -> None:
        task = asyncio.Task(self.to_async(data))

    @asyncio.coroutine
    def to_async(self, data):
        message = DnsMessage.unpack(data)
        self.on_con_lost.set_result(message)

    def connection_lost(self, exc):
        return self.message

    async def timeout_task(self, time):
        await asyncio.sleep(time)
        self.on_con_lost.set_exception(TimeoutError)
        self.on_con_lost.exception()

    @classmethod
    async def send_message(cls, message, host, port=53, timeout=5):

        loop = triton.loop
        on_con_lost = loop.create_future()
        transport, protocol = await loop.create_connection(
            lambda: cls(loop, message, on_con_lost, timeout),
            host, port)
        try:
            message = await on_con_lost
            return message
        finally:
            transport.close()


class TcpServer(asyncio.Protocol):

    def __init__(self, dns_server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dns_server = dns_server

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data) -> None:
        data = data[2:]
        message = DnsMessage.unpack(data)
        task = asyncio.Task(self.to_async(message))

    @asyncio.coroutine
    def to_async(self, message):
        reply_message = yield from self.dns_server.proceed_request(message)
        packed_message = reply_message.pack()
        data = len(packed_message).to_bytes(2, "big") + packed_message
        self.transport.write(data)

#  Copyright (c) Yurzs 2020.
import asyncio
import logging
import yaml

from .glob import global_loop
from .database import DatabaseConnection

from triton.dns.core import DnsMessage, parts
from triton.protocols import udp, tcp

log = logging.getLogger("triton")


class Server:
    class Protocols:
        tcp = tcp.TcpServer
        udp = udp.UdpServer

    class Servers:
        def __init__(self):
            self.tcp = None
            self.udp = None

    class Tasks:
        def __init__(self):
            self.tcp = None
            self.udp = None

    def __init__(self, config, host="127.0.0.1", port=53, loop=global_loop, recursion=False):
        with open(config, "r") as config_file:
            self.config = yaml.load(config_file, yaml.FullLoader)
            if not self.config.get("database"):
                raise Exception("No database config provided.")
        self.servers = Server.Servers()
        self.host = host
        self.port = port
        self.loop = loop
        self.tasks = Server.Tasks()
        self.recursion = recursion
        self.database = DatabaseConnection(self.loop, self.config["database"])
        asyncio.set_event_loop(self.loop)

    async def _start_tcp(self):
        """Helper for starting TCP server."""

        log.info(f"Starting TCP server on port {self.port}.")
        print(f"Starting TCP server on port {self.port}.")
        self.servers.tcp = await self.loop.create_server(
            lambda: self.Protocols.tcp(self),
            self.host, self.port)

    async def _start_udp(self):
        """Helper for starting UDP server."""

        log.info(f"Starting UDP server on port {self.port}.")
        print(f"Starting UDP server on port {self.port}.")
        self.servers.udp = await self.loop.create_datagram_endpoint(
            lambda: self.Protocols.udp(self),
            local_addr=(self.host, self.port)
        )

        try:
            await asyncio.sleep(99999999999999)
        finally:
            self.servers.udp.close()

    def start(self, asynchronously=False):
        """Starts coroutine for TCP and UDP servers."""

        self.tasks.tcp = self.loop.create_task(self._start_tcp())
        self.tasks.udp = self.loop.create_task(self._start_udp())

        if not asynchronously:
            self.loop.run_forever()

    def stop(self):
        """Cancels tasks for TCP and UDP server coroutines."""

        if self.tasks.tcp:
            self.tasks.tcp.cancel()
        if self.tasks.udp:
            self.tasks.udp.cancel()

    async def proceed_request(self, message: DnsMessage):
        """Proceed request received from protocols."""

        if not message.question:
            return message
        question = message.question[0]
        domain = await self.database.find_one({"domain": str(question.qname)})
        if not domain:
            return message

        for rr in filter(
            lambda rr: rr["type"] == question.qtype and rr["class"] == question.qclass,
            domain["resource_records"]
        ):
            message.header.qr = True
            rdata = parts.rdata.Rdata.by_type(rr["type"])
            message.answer.append(
                parts.DnsMessageAnswer(
                    message, rr["label"], rr["type"], rr["class"], rr["ttl"],
                rdata(**rr["rdata"])))

        return message

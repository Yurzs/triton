#  Copyright (c) Yurzs 2019.

from .root_servers import root_nameservers
from .nameserver import Nameserver
from . import Cache
from protocols.udp import UdpClient
from triton.dns.core.message import DnsMessage
from triton.dns.core.parts import rdata


@Cache.find
@Cache.save
async def resolve(loop, dns_server, label, type, klass):
    """Helper for resolving using specified dns server."""

    message = DnsMessage.new_question(label, type, klass)
    message.header.rd = False
    return await UdpClient.send_message(message, dns_server, loop=loop)


class Resolver:

    nameservers = root_nameservers

    def __init__(self, loop, label, type, klass):
        self.loop = loop
        self.label = label
        self.type = type
        self.klass = klass

    async def resolve(self):
        """Resolves recursively from root to target."""

        for server in self.nameservers.copy():
            reply = await resolve(self.loop, server.ip4, self.label, self.type, self.klass)
            if not reply:
                continue
            if not reply.answer and reply.authority and reply.additional:

                if reply.authority.contains_type(rdata.Soa):
                    return reply

                nameservers = []
                for answer in reply.authority:
                    ns = Nameserver(answer.rdata.nsdname.label)
                    for additional in reply.additional:
                        if additional.name == ns.label:
                            if isinstance(additional.rdata, rdata.A):
                                ns.ip4 = additional.rdata.address
                            elif isinstance(additional.rdata, rdata.Aaaa):
                                ns.ip6 = additional.rdata.address
                    if not ns.ip4:
                        r = Resolver(self.loop, ns.label, 1, 1)
                        result = await r.resolve()
                        if not result:
                            return
                        ns.ip4 = result.answer[0].rdata.address
                    nameservers.append(ns)
                self.nameservers = nameservers
                return await self.resolve()
            else:
                return reply

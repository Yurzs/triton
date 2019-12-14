import struct

from triton.dns.core.parts import DnsMessagePart, rdata
from triton.dns.core.domains import DnsDomain


class DnsMessageAnswer(DnsMessagePart):

    name: DnsDomain
    type: int
    klass: int
    ttl: int
    rdlength: int
    rdata: rdata.Rdata

    def __init__(self, message, name=None, type=None, klass=None, ttl=None, rdata=None):
        self._message = message
        self.name = DnsDomain(message, label=name) if isinstance(name, str) else name
        self.type = type
        self.klass = klass
        self.ttl = ttl
        self.rdata = rdata

    @property
    def rdlength(self):
        return len(self.rdata.pack())

    @classmethod
    def unpack(cls, message, data):

        answer = cls(message)
        answer.name = DnsDomain.unpack(message, data)
        answer.type, answer.klass, answer.ttl, answer._rdlength = struct.unpack(
            "!HHLH", data.read(10)
        )
        answer.rdata = rdata.Rdata.by_type(answer.type).unpack(answer, data)
        return answer

    def pack(self):

        name = self.name.pack()
        fields = struct.pack("!HHLH", self.type, self.klass, self.ttl, self.rdlength)
        rdata_ = self.rdata.pack()
        self._message.bytestream.write(fields + rdata_)

        return name + fields + rdata_

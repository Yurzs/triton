from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Rdata


class Ns(Rdata):
    nsdname: DnsDomain
    type = 2

    @classmethod
    def unpack(cls, answer, data):

        ns = cls()
        ns.nsdname = DnsDomain.unpack(answer._message, data)
        return ns

    def pack(self):

        return self.nsdname.pack()

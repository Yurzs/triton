from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Rdata


class Ptr(Rdata):
    ptrdname: DnsDomain
    type = 12

    @classmethod
    def unpack(cls, answer, data):

        ptr = cls()
        ptr.ptrdname = DnsDomain.unpack(answer._message, data)
        return ptr

    def pack(self):

        return self.ptrdname.pack()

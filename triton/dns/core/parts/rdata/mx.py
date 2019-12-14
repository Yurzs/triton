#  Copyright (c) Yurzs 2019.

import struct

from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Rdata


class Mx(Rdata):
    preference: int
    exchange: DnsDomain
    type = 15

    @classmethod
    def unpack(cls, answer, data):

        mx = cls()
        mx.preference = struct.unpack("!H", data.read(2))[0]
        mx.exchange = DnsDomain.unpack(answer._message, data)
        return mx

    def pack(self):

        packed = struct.pack("!H", self.preference)
        packed += self.exchange.pack()
        return packed

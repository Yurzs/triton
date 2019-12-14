#  Copyright (c) Yurzs 2019.
import ipaddress
import struct

from tests.dns.core.test_dnsMessagePart import TestDnsMessagePart
from triton.dns.core.parts import DnsMessageAnswer, rdata
from triton.dns.core import bytestream, domains


class TestDnsMessageAnswer(TestDnsMessagePart):

    PART = DnsMessageAnswer

    TEST_DATA = bytestream.ByteStream(
        domains.DnsDomain(TestDnsMessagePart.MOCKED_MESSAGE(), "test.domain").pack() +
        struct.pack("!HHLH", 1, 1, 1, 4) +
        TestDnsMessagePart.MOCKED_RDATA.pack()
    )

    TEST_RESULT = {
        "name": "test.domain",
        "type": 1,
        "klass": 1,
        "ttl": 1,
        "rdata": TestDnsMessagePart.MOCKED_RDATA.to_dict()
    }

    def test_rdlength(self):
        a = DnsMessageAnswer(self.MOCKED_MESSAGE())
        a.rdata = rdata.A()
        a.rdata.address = ipaddress.IPv4Address("1.1.1.1")
        self.assertEqual(a.rdlength, 4)

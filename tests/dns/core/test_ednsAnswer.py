#  Copyright (c) Yurzs 2019.
import struct

from tests.dns.core.test_dnsMessagePart import TestDnsMessagePart
from triton.dns.extensions import edns
from triton.dns.core import ByteStream, domains


class TestEdnsAnswer(TestDnsMessagePart):

    MOCKED_RDATA = TestDnsMessagePart.MOCKED_OPT()

    PART = edns.EdnsAnswer

    TEST_DATA = ByteStream(
        domains.DnsDomain(TestDnsMessagePart.MOCKED_MESSAGE(), "test.domain").pack() +
        struct.pack("!HHLH", 41, 1, 16809984, 8) +
        TestDnsMessagePart.MOCKED_OPT().pack()
    )

    TEST_RESULT = {
        "name": "test.domain",
        "type": 41,
        "extended_rcode": 1,
        "version": 0,
        "do": True,
        "udp_payload_size": 1,
        "z": 0,
        "rdata": TestDnsMessagePart.MOCKED_OPT().to_dict()
    }

    def test_rdlength(self):
        a = self.PART(self.MOCKED_MESSAGE())
        a.rdata = self.MOCKED_OPT()
        self.assertEqual(a.rdlength, 8)

#  Copyright (c) Yurzs 2019.
import ipaddress

from tests.dns.triron_test import TritonTest
from triton.dns.core import DnsMessage, ByteStream
from triton.dns.core.parts import DnsMessagePart, rdata
from triton.dns.extensions.edns import Opt

class TestDnsMessagePart(TritonTest):

    MOCKED_RDATA = rdata.A()
    MOCKED_RDATA.address = ipaddress.IPv4Address("1.1.1.1")

    PART: DnsMessagePart

    TEST_DATA: ByteStream

    TEST_RESULT: dict

    def test_pack(self):
        if self.__class__ != TestDnsMessagePart:
            self.TEST_DATA.reset()
            message = self.MOCKED_MESSAGE()
            unpacked = self.PART.unpack(message, self.TEST_DATA)
            message.domains.clear()
            self.TEST_DATA.reset()
            self.assertEqual(self.TEST_DATA.read(), unpacked.pack())

    def test_unpack(self):
        if self.__class__ != TestDnsMessagePart:
            self.TEST_DATA.reset()
            unpacked = self.PART.unpack(self.MOCKED_MESSAGE(), self.TEST_DATA)
            for k, v in unpacked.__dict__.items():
                if not k.startswith("_"):
                    if isinstance(v, rdata.Rdata):
                        self.assertEqual(v.to_dict(), self.TEST_RESULT[k])
                    else:
                        self.assertEqual(self.TEST_RESULT[k], v)

    def test_to_dict(self):
        if self.__class__ != TestDnsMessagePart:
            self.TEST_DATA.reset()
            unpacked = self.PART.unpack(self.MOCKED_MESSAGE(), self.TEST_DATA)
            self.assertEqual(self.TEST_RESULT, unpacked.to_dict())

    @staticmethod
    def MOCKED_OPT():
        opt = Opt()
        setattr(opt, "1", b"test")
        return opt

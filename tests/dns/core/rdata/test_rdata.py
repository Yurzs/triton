#  Copyright (c) Yurzs 2019.
import ipaddress


from tests.dns.triron_test import TritonTest

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts import DnsMessageAnswer
from triton.dns.core.parts import rdata
# from tests.dns.core import rdata as rdta


class TestRdata(TritonTest):

    RDATA: rdata.Rdata
    TEST_DATA: ByteStream
    TEST_RESULT: dict

    def test_by_type(self):
        if hasattr(self, "RDATA"):
            self.assertEqual(rdata.Rdata.by_type(self.RDATA.type), self.RDATA)
        elif self.__class__.__name__ == "TestRdata":
            for subclass in rdata.Rdata.__subclasses__():
                if len([s.RDATA for s in TestRdata.__subclasses__()]) > 0:
                    self.assertTrue(subclass in [s.RDATA for s in TestRdata.__subclasses__()])
        else:
            self.fail()

    def test_pack(self):
        if hasattr(self, "TEST_RESULT") and hasattr(self, "TEST_DATA"):
            self.TEST_DATA.reset()
            answer = DnsMessageAnswer(self.MOCKED_MESSAGE())
            answer._rdlength = len(self.TEST_DATA.peek())
            rrdata = self.RDATA.unpack(answer, self.TEST_DATA)
            for k, v in self.TEST_RESULT.items():
                self.assertEqual(getattr(rrdata, k), v)

        elif self.__class__.__name__ == "TestRdata":
            pass
        else:
            self.fail()

    def test_unpack(self):
        if hasattr(self, "TEST_RESULT") and hasattr(self, "TEST_DATA"):
            self.TEST_DATA.reset()
            message = self.MOCKED_MESSAGE()
            answer = DnsMessageAnswer(message)
            answer._rdlength = len(self.TEST_DATA.peek())
            rrdata = self.RDATA.unpack(answer, self.TEST_DATA)
            message.domains.clear()
            self.TEST_DATA.reset()
            self.assertEqual(self.TEST_DATA.read(), rrdata.pack())
        elif self.__class__.__name__ == "TestRdata":
            pass
        else:
            self.fail()

    def test_to_dict(self):
        if hasattr(self, "TEST_RESULT") and hasattr(self, "TEST_DATA"):
            self.TEST_DATA.reset()
            message = self.MOCKED_MESSAGE()
            answer = DnsMessageAnswer(message)
            answer._rdlength = len(self.TEST_DATA.peek())
            rrdata = self.RDATA.unpack(answer, self.TEST_DATA)
            test_result = {}
            for k, v in self.TEST_RESULT.items():
                if isinstance(v, ipaddress.IPv6Address) or isinstance(v, ipaddress.IPv4Address):
                    test_result[k] = str(v)
                else:
                    test_result[k] = v
            self.assertEqual(test_result, rrdata.to_dict())
        elif self.__class__.__name__ == "TestRdata":
            pass
        else:
            self.fail()

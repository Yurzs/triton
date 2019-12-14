import ipaddress

from tests.dns.triron_test import TritonTest


from triton.dns.core.domains import DomainStorage, DnsDomain
from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts import DnsMessageHeader, DnsMessageQuestion, DnsMessageAnswer, rdata


class TestDomainStorage(TritonTest):
    pass


class TestDnsDomain(TritonTest):

    def test_unpack(self):
        """Tests unpacking of domain from bytes."""

        message = self.MOCKED_MESSAGE()
        test_domain = ByteStream(b"\x04test\x06domain\x00")
        domain = DnsDomain.unpack(message, test_domain)
        self.assertEqual(domain.label, "test.domain")

    def test_pack(self):
        """Tests packing of domain to bytes."""

        message = self.MOCKED_MESSAGE()
        test_domain = ByteStream(b"\x04test\x06domain\x00")
        domain = DnsDomain(message, "test.domain")
        self.assertEqual(domain.pack(), test_domain.read())

    def test_domain_shortener(self):
        """Tests if same domains in message are shortened."""

        message = self.MOCKED_MESSAGE()
        message.header = DnsMessageHeader(message, 1, 0, 0, 1, 1, 1, 1, 0, 1)
        message.question.append(DnsMessageQuestion(message, "test.domain",
                                                   1, 1))
        a = rdata.A()
        a.address = ipaddress.IPv4Address("1.1.1.1")
        message.answer.append(
            DnsMessageAnswer(message, "test.domain", 1, 1, 1,
                             a)
        )

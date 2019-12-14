import ipaddress

from unittest import TestCase
from triton.dns.core.exceptions import DnsException
from triton.dns.core.parts import storage, header, answer
from triton.dns.core.parts.rdata import A
from triton.dns.core import message


class TestDnsPartStorage(TestCase):
    def test_append(self):
        storage_ = storage.DnsPartStorage()
        self.assertRaises(DnsException, storage_.append, 1)
        self.assertEqual(len(storage_), 0)
        h = header.DnsMessageHeader(None)
        storage_.append(h)
        self.assertEqual(len(storage_), 1)
        self.assertEqual(storage_[0], h)

    def test_pack(self):
        m = message.DnsMessage()
        s = storage.DnsPartStorage()
        a = A()
        a.address = ipaddress.IPv4Address("1.1.1.1")
        s.append(
            answer.DnsMessageAnswer(m, "test.domain", 1, 1, 45, a)
        )
        self.assertEqual(
            b"\x04test\x06domain\x00\x00\x01\x00\x01\x00\x00\x00-\x00\x04\x01\x01\x01\x01",
            s.pack()
        )
        s.append(
            answer.DnsMessageAnswer(m, "mail.test.domain", 1, 1, 45, a)
        )
        m.domains.clear()
        self.assertEqual(
            (b"\x04test\x06domain\x00\x00\x01\x00\x01\x00\x00\x00-\x00\x04\x01"
             b"\x01\x01\x01\x04mail\xc0\x1b\x00\x01\x00\x01\x00\x00\x00-\x00\x04"
             b"\x01\x01\x01\x01"),
            s.pack()
        )

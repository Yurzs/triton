#  Copyright (c) Yurzs 2019.
import ipaddress
import struct

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts.rdata import A
from tests.dns.core.rdata.test_rdata import TestRdata


class TestA(TestRdata):

    RDATA = A
    TEST_DATA = ByteStream(struct.pack("!L", int(ipaddress.IPv4Address("1.1.1.1"))))
    TEST_RESULT = {"address": ipaddress.IPv4Address("1.1.1.1")}

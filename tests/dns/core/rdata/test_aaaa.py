#  Copyright (c) Yurzs 2019.

import ipaddress

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts.rdata import Aaaa
from tests.dns.core.rdata.test_rdata import TestRdata


class TestAaaa(TestRdata):

    RDATA = Aaaa
    TEST_DATA = ByteStream(int(ipaddress.IPv6Address("1:1:1:1::")).to_bytes(16, "big"))
    TEST_RESULT = {
        "address": ipaddress.IPv6Address("1:1:1:1::")
    }

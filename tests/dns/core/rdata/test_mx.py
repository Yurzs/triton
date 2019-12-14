#  Copyright (c) Yurzs 2019.

import struct

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Mx
from tests.dns.core.rdata.test_rdata import TestRdata


class TestMx(TestRdata):
    RDATA = Mx

    TEST_DATA = ByteStream(
        struct.pack("!H", 100) + DnsDomain(TestRdata.MOCKED_MESSAGE(), "test.domain").pack()
    )
    TEST_RESULT = {
        "preference": 100,
        "exchange": "test.domain"
    }

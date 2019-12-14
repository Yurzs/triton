#  Copyright (c) Yurzs 2019.

import struct

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Soa
from tests.dns.core.rdata.test_rdata import TestRdata


class TestSoa(TestRdata):
    RDATA = Soa

    TEST_DATA = ByteStream(
        DnsDomain(TestRdata.MOCKED_MESSAGE(), "test.domain").pack() +
        DnsDomain(TestRdata.MOCKED_MESSAGE(), "responsible.person").pack() +
        struct.pack("!LLLLL", 1234, 2345, 3456, 4567, 5678)
    )

    TEST_RESULT = {
        "mname": "test.domain",
        "rname": "responsible.person",
        "serial": 1234,
        "refresh": 2345,
        "retry": 3456,
        "expire": 4567,
        "minimum": 5678,
    }

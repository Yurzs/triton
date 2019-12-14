#  Copyright (c) Yurzs 2019.

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Ptr
from tests.dns.core.rdata.test_rdata import TestRdata


class TestPtr(TestRdata):
    RDATA = Ptr

    TEST_DATA = ByteStream(
        DnsDomain(TestRdata.MOCKED_MESSAGE(), "test.domain").pack()
    )

    TEST_RESULT = {
        "ptrdname": "test.domain"
    }

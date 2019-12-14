#  Copyright (c) Yurzs 2019.

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.domains import DnsDomain
from triton.dns.core.parts.rdata import Cname
from tests.dns.core.rdata.test_rdata import TestRdata


class TestCname(TestRdata):

    RDATA = Cname
    TEST_DATA = ByteStream(DnsDomain(TestRdata.MOCKED_MESSAGE(), "test.domain").pack())
    TEST_RESULT = {
        "cname": "test.domain"
    }

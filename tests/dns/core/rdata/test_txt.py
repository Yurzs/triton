#  Copyright (c) Yurzs 2019.

import struct

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts.rdata import Txt
from tests.dns.core.rdata.test_rdata import TestRdata


class TestTxt(TestRdata):
    RDATA = Txt

    TXT_DATA = "test txt record"

    TEST_DATA = ByteStream(struct.pack("!B", len(TXT_DATA.encode("ascii"))) +
                           TXT_DATA.encode("ascii"))

    TEST_RESULT = {
        "txt_data": TXT_DATA
    }

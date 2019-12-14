#  Copyright (c) Yurzs 2019.
import struct

from tests.dns.core.rdata.test_rdata import TestRdata
from triton.dns.extensions.edns import Opt
from triton.dns.core import ByteStream


class TestOpt(TestRdata):
    RDATA = Opt

    TEST_DATA = ByteStream(struct.pack("!2H", 1, 4) + b"test")

    TEST_RESULT = {
        "1": b'test'
    }


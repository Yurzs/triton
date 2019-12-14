#  Copyright (c) Yurzs 2019.

import struct

from triton.dns.core.bytestream import ByteStream
from triton.dns.core.parts.rdata import Caa
from tests.dns.core.rdata.test_rdata import TestRdata


class TestCaa(TestRdata):

    RDATA = Caa
    TEST_DATA = ByteStream(
        struct.pack("!?", 1) + b"\x05issue" + b"testing.org")
    TEST_RESULT = {"critical": True, "tag": "issue", "value": "testing.org"}

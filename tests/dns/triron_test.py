#  Copyright (c) Yurzs 2019.

from unittest import TestCase

from triton.dns.core import DnsMessage


class TritonTest(TestCase):

    @staticmethod
    def MOCKED_MESSAGE():
        return DnsMessage()

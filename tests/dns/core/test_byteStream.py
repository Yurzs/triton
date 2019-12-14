#  Copyright (c) Yurzs 2019.

from unittest import TestCase

from triton.dns.core.bytestream import ByteStream


class TestByteStream(TestCase):

    def test_init(self):
        ByteStream(b"12")
        ByteStream(b"")

    def test_init_bad(self):
        self.assertRaises(ValueError, ByteStream, 1)
        self.assertRaises(ValueError, ByteStream, 1.01)
        self.assertRaises(ValueError, ByteStream, "abc")
        self.assertRaises(ValueError, ByteStream, {"a": 1})
        self.assertRaises(ValueError, ByteStream, {"test"})

    def test_read(self):
        stream = ByteStream(b"12")
        self.assertEqual(stream.read(1), b"1")
        self.assertEqual(stream.read(1), b"2")
        self.assertRaises(MemoryError, stream.read, 1)
        self.assertRaises(MemoryError, stream.read)

    def test_peek(self):
        stream = ByteStream(b"12")
        self.assertEqual(stream.peek(), b"12")
        stream.read(1)
        self.assertEqual(stream.peek(), b"2")
        stream.read(1)
        self.assertEqual(stream.peek(), b"")

    def test_reset(self):
        stream = ByteStream(b"123")
        self.assertEqual(stream.read(1), b"1")
        self.assertEqual(stream.read(1), b"2")
        stream.reset()
        self.assertEqual(stream.read(1), b"1")
        self.assertEqual(stream.read(1), b"2")
        self.assertEqual(stream.read(1), b"3")
        self.assertRaises(MemoryError, stream.read, 1)


import json
import random

import triton.dns.core.parts as message_parts

from triton.dns.core.exceptions import DnsException
from triton.dns.core.domains import DomainStorage
from triton.dns.core.bytestream import ByteStream
from triton.dns.extensions import edns
from triton.dns.core.parts import DnsMessageQuestion, DnsMessageHeader


class DnsMessage:

    header: message_parts.DnsMessageHeader

    def __init__(self):
        self.question = message_parts.DnsPartStorage()
        self.answer = message_parts.DnsPartStorage()
        self.authority = message_parts.DnsPartStorage()
        self.additional = message_parts.DnsPartStorage()
        self.domains = DomainStorage()
        self.bytestream = ByteStream()

    def enable_edns(self, max_payload_size=4096, dnssec=False):
        """Adds OPT RR to additional section."""

        edns_answer = edns.EdnsAnswer(self, max_payload_size, 0, 0, bool(dnssec), 0)
        self.additional.append(edns_answer)

    @classmethod
    def unpack(cls, data: bytes):
        """Unpacks dns message from bytes."""

        data = ByteStream(data)
        message = cls()

        message.header = message_parts.DnsMessageHeader.unpack(message, data.read(12))
        data = message.parse_resource_record(
            message, message_parts.DnsMessageQuestion, message.question, message.header._qdcount,
            data)
        data = message.parse_resource_record(
            message, message_parts.DnsMessageAnswer, message.answer, message.header._ancount,
            data)
        data = message.parse_resource_record(
            message, message_parts.DnsMessageAnswer, message.authority, message.header._nscount,
            data)
        data = message.parse_resource_record(
            message, message_parts.DnsMessageAnswer, message.additional, message.header._arcount,
            data)
        if len(data.peek()) != 0:
            raise DnsException("some data still left")
        return message

    @staticmethod
    def parse_resource_record(message, rrtype, storage, count, data):
        """Parses resource record (answer, authority, additional) from bytes."""

        for rr in range(count):

            storage.append(
                rrtype.unpack(
                    message, data)
                )
        return data

    def pack(self):
        """Packs dns message to bytes."""

        self.bytestream.clear()
        self.domains.clear()
        result = b""
        self.header.pack()
        result += self.question.pack()
        result += self.answer.pack()
        result += self.authority.pack()
        result += self.additional.pack()
        return self.bytestream.data

    def __repr__(self):
        string = "|‾‾‾‾‾‾‾‾ DNS MESSAGE ‾‾‾‾‾‾‾|\n"
        string += f"|~~~~~~~~   HEADER   ~~~~~~~~|\n{self.header}\n"
        string += f"|~~~~~~~~  QUESTION  ~~~~~~~~|\n{self.question}"
        string += f"|~~~~~~~~   ANSWERS  ~~~~~~~~|\n{self.answer}"
        string += f"|~~~~~~~~ AUTHORITY  ~~~~~~~~|\n{self.authority}"
        string += f"|~~~~~~~~ADDITIONALS ~~~~~~~~|\n{self.additional}"
        string += f"|{'_'*28}|"
        return string

    def to_json(self):
        """Returns JSON representation of dns message."""

        return json.dumps({
            "header": self.header.to_dict(),
            "question": self.question.to_dict(),
            "answer": self.answer.to_dict(),
            "authority": self.authority.to_dict(),
            "additional": self.additional.to_dict()
        })

    @classmethod
    def new_question(cls, label, type, klass):
        """Create question message."""

        message = cls()
        header = DnsMessageHeader(message)
        header.id = random.randrange(1, 65535)
        header.qr = 0
        header.opcode = 0
        header.aa = 1
        header.tc = 0
        header.rd = 1
        header.ra = 0
        header.z = 0
        header.rcode = 0
        message.header = header
        question = DnsMessageQuestion(message, label, type, klass)
        message.question.append(question)
        message.enable_edns()
        return message

    @classmethod
    def dummy_answer(cls, answers: list, label, type, klass):
        """Creates fake answer for question."""

        message = cls.new_question(label, type, klass)

        message.header.qr = True
        message.additional.clear()

        for answer in answers:
            message.answer.append(answer)

        return message

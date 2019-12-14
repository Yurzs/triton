import json

from triton.dns.core.exceptions import DnsException
from triton.dns.core.parts import DnsMessagePart


class DnsPartStorage(list):

    def append(self, object) -> None:
        if not isinstance(object, DnsMessagePart):
            raise DnsException("Cant append anything other than dns message part.")
        super().append(object)

    def pack(self):
        result = b""
        for item in self:
            result += item.pack()
        return result

    def __repr__(self):
        string = ""
        for item in self:
            string += f"{item}\n"
        return string

    def to_dict(self):
        """Return dict representation of items in storage."""

        return [i.to_dict() for i in self]

    def contains_type(self, klass):
        return bool(list(filter(lambda item: isinstance(item.rdata, klass), self)))

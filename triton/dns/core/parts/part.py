import struct


from triton.dns.core.parts import rdata
from triton.dns.core.domains import DnsDomain


class DnsMessagePart:
    """Base part class."""

    structure: struct.Struct

    def pack(self):
        pass

    @classmethod
    def unpack(cls, message, data):
        pass

    def __repr__(self):
        string = ""  # f"##### {self.__class__.__name__.upper()} #####\n"
        for k, v in {attr: val for attr, val in self.__dict__.items()
                     if not attr.startswith("_")}.items():
            if len(f"| {k.upper()}: {v}|\n") > 31:
                if isinstance(v, rdata.Rdata):
                    for chunk in v.__repr_chunks__():
                        string += f"|{chunk}|\n"
                else:
                    string += f"| {k.upper()}: {' ' * (30 - 5 - len(k.upper()))}|\n"
                    for chunk in [str(v)[start: start + 28] for start in range(0, len(str(v)), 28)]:
                        string += f"|{chunk}|\n"
            else:
                string += f"| {k.upper()}: {v}"
                string += " " * (29 - len(f"| {k.upper()}: {v}")) + "|\n"
        string += "|" + "-" * 28 + "|"
        return string

    def to_dict(self):
        """Returns dict representation of dns message part."""

        part_dict = {}
        for k, v in {attr: val for attr, val in self.__dict__.items()
                     if not attr.startswith("_")}.items():
            if type(v) in (bool, int, dict, str):
                part_dict[k] = v
            elif isinstance(v, DnsDomain):
                part_dict[k] = v.label
            else:
                part_dict[k] = v.to_dict()
        return part_dict

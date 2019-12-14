#  Copyright (c) Yurzs 2019.
import ipaddress


class Nameserver:

    def __init__(self, label, ip4=None, ip6=None, about=None):
        self.label = label

        if ip4:
            self.ip4 = ipaddress.IPv4Address(ip4)
        else:
            self.ip4 = ip4

        if ip6:
            self.ip6 = ipaddress.IPv6Address(ip6)
        else:
            self.ip6 = ip6

        self.about = about

    @property
    def addresses(self):
        return [self.ip4, self.ip6]

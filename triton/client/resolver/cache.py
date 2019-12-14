#  Copyright (c) Yurzs 2020.
import asyncio
from triton.dns.extensions.edns import Opt
from triton.dns.core.parts import DnsMessageAnswer
from triton.dns.core import DnsMessage


class Cache:

    storage = []

    def __new__(cls, *args, **kwargs):
        """Cache is a singleton."""

        if not hasattr(cls, "__instance__"):
            cls.__instance__ = super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    def _find(self, label: str, type: int, klass: int) -> list:
        """Finds rr by attrs in storage."""

        return list(filter(lambda rr: rr.name == label and rr.type == type and
            rr.klass == klass, self.storage))

    @staticmethod
    def find(f):
        """Decorator for finding in RR in cache."""

        async def wrapper(loop: asyncio.AbstractEventLoop,
                          server: str, label: str, type: int, klass: int):
            cache = Cache()
            found = cache._find(label, type, klass)
            if found:
                return DnsMessage.dummy_answer(found, label, type, klass)
            else:
                return await f(loop, server, label, type, klass)
        return wrapper

    @staticmethod
    def save(f):
        """Decorator for saving results of query."""

        async def wrapper(loop: asyncio.AbstractEventLoop, server, label, typee, klass):

            cache = Cache()
            result = await f(loop, server, label, typee, klass)
            if result:
                for answer in result.answer:
                    cache.append(answer)
                    loop.create_task(cache.remove_after_ttl_expires(answer))
                for answer in result.authority:
                    cache.append(answer)
                    loop.create_task(cache.remove_after_ttl_expires(answer))
                for answer in result.additional:
                    if not isinstance(answer.rdata, Opt):
                        cache.append(answer)
                        loop.create_task(cache.remove_after_ttl_expires(answer))
            return result
        return wrapper

    def remove(self, rr: DnsMessageAnswer):
        """Deletes RR from cache storage."""

        return self.storage.remove(rr)

    async def remove_after_ttl_expires(self, rr: DnsMessageAnswer):
        """Removes RR from cache after its TTL expires."""

        await asyncio.sleep(rr.ttl)
        return self.remove(rr)

    def append(self, rr: DnsMessageAnswer) -> None:
        """Appends if RR not already in storage."""

        for storage_rr in self.storage:
            if rr.name == storage_rr.name and \
               rr.type == storage_rr.type and \
               rr.klass == storage_rr.klass and \
               rr.rdata == storage_rr.rdata:
                return

        rr.ttl = property()

        self.storage.append(rr)

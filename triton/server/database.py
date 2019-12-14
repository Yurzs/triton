#  Copyright (c) Yurzs 2020.

import urllib

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


class DatabaseConnection:
    __client__ = AsyncIOMotorClient
    __collection__ = "triton"
    __auth_database__ = "admin"

    def __init__(self, loop, database_config):

        if database_config.get("replica_set"):
            host = ",".join(database_config["replica_set"])
        else:
            host = "{host}:{port}".format(host=database_config["host"],
                                          port=database_config["port"])
        if not database_config.get("username") or not database_config.get("password"):
            uri = f"mongodb://{host}"
        else:
            username = urllib.parse.quote_plus(database_config['username'])
            password = urllib.parse.quote_plus(database_config['password'])
            uri = f"mongodb://{username}:{password}@{host}/{self.__auth_database__}"

        self.connection: AsyncIOMotorClient = self.__client__(uri, io_loop=loop)
        self.database: AsyncIOMotorDatabase = self.connection[database_config["database"]]
        self.collection: AsyncIOMotorCollection = self.database[self.__collection__]

    async def find(self, length, *args, **kwargs):
        """Proxy for mongo find method."""

        return await self.collection.find(*args, **kwargs).to_list(length)

    async def find_one(self, *args, **kwargs):
        """Proxy for mongo find_one method."""

        return await self.collection.find_one(*args, **kwargs)

    async def insert_one(self, *args, **kwargs):
        """Proxy for mongo insert_one method."""

        return await self.collection.insert_one(*args, **kwargs)

    async def update_one(self, *args, **kwargs):
        """Proxy for mongo update_one method."""

        return await self.collection.update_one(*args, **kwargs)

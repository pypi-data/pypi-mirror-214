import logging
from typing import Dict

# Database manager.
from dls_normsql.databases import Databases
from dls_utilpack.callsign import callsign

# Base class for generic things.
from dls_utilpack.thing import Thing

from xchembku_api.databases.database_definition import DatabaseDefinition

logger = logging.getLogger(__name__)

thing_type = "xchembku_lib.xchembku_datafaces.direct"


class DirectBase(Thing):
    """ """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):
        Thing.__init__(self, thing_type, specification)

        # For testing, caller might want to drop the database on connection.
        self.__should_drop_database = specification.get("should_drop_database")

        self.__database_definition_object = DatabaseDefinition()

        self.__database = None

    # ----------------------------------------------------------------------------------------
    async def start(self):
        # Connect to the database to create the schemas if they don't exist already.
        await self.establish_database_connection()

        # Make sure we are up to date with the latest database schema revision.
        await self.__database.apply_revisions()

    # ----------------------------------------------------------------------------------------
    async def disconnect(self):
        if self.__database is not None:
            logger.debug(f"[DISSHU] {callsign(self)} disconnecting")
            await self.__database.disconnect()
            logger.debug(f"[DISSHU] {callsign(self)} disconnected")
            self.__database = None

        # TODO: Figure out a better way to disconnect the dataface mixins.
        await self.disconnect_soakdb3_crystal_wells_mixin()

    # ----------------------------------------------------------------------------------------
    async def establish_database_connection(self):
        if self.__database is None:
            self.__database = Databases().build_object(
                self.specification()["database"],
                self.__database_definition_object,
            )

            # For testing, caller might want to drop the database on connection.
            await self.__database.connect(
                should_drop_database=self.__should_drop_database
            )

    # ----------------------------------------------------------------------------------------
    async def reinstance(self):
        """"""
        if self.__database is None:
            return

        self.__database = self.__database.reinstance()

        return self

    # ----------------------------------------------------------------------------------------
    async def backup(self):
        """"""
        await self.establish_database_connection()

        return await self.__database.backup()

    # ----------------------------------------------------------------------------------------
    async def restore(self, nth):
        """"""
        await self.establish_database_connection()

        return await self.__database.restore(nth)

    # ----------------------------------------------------------------------------------------
    async def query(self, sql, subs=None, why=None):
        """"""

        await self.establish_database_connection()

        records = await self.__database.query(sql, subs=subs, why=why)

        return records

    # ----------------------------------------------------------------------------------------
    async def execute(self, sql, subs=None, why=None):
        """"""
        await self.establish_database_connection()

        return await self.__database.execute(sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def insert(self, table_name, records, why=None) -> None:
        """"""
        await self.establish_database_connection()

        return await self.__database.insert(table_name, records, why=why)

    # ----------------------------------------------------------------------------------------
    async def update(self, table_name, record, where, subs=None, why=None) -> Dict:
        """"""
        await self.establish_database_connection()

        if why is None:
            why = f"update {table_name} record"

        # This returns the count of records changed by the update.
        return {
            "count": await self.__database.update(
                table_name, record, where, subs=subs, why=why
            )
        }

    # ----------------------------------------------------------------------------------------
    async def begin(self, why=None) -> None:
        """"""
        await self.establish_database_connection()

        return await self.__database.begin()

    # ----------------------------------------------------------------------------------------
    async def commit(self, why=None) -> None:
        """"""
        await self.establish_database_connection()

        return await self.__database.commit()

    # ----------------------------------------------------------------------------------------
    async def rollback(self, why=None) -> None:
        """"""
        await self.establish_database_connection()

        return await self.__database.rollback()

    # ----------------------------------------------------------------------------------------
    async def report_health(self):
        """"""

        report = {}

        report["alive"] = True

        return report

    # ----------------------------------------------------------------------------------------
    async def open_client_session(self):
        """"""
        # Connect to the database to create the schemas if they don't exist already.
        await self.establish_database_connection()

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""
        logger.debug(f"[DISSHU] {callsign(self)} in aexit, calling disconnect")

        await self.disconnect()

        logger.debug(f"[DISSHU] {callsign(self)} in aexit, disconnected")

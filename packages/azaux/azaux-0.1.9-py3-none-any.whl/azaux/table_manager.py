from contextlib import asynccontextmanager

from azure.core.exceptions import ResourceNotFoundError
from azure.data.tables import TableEntity
from azure.data.tables.aio import TableServiceClient

from azaux.storage_resource import (
    StorageResourceType,
    StorageResource,
)

# TODO: REVISE ASYNC CODE


class TableManager(StorageResource):
    """
    Class to manage retrieving and upsert table entities from a given table from the Table Storage account
    """

    def __init__(
        self,
        table: str,
        account: str,
        api_key: str,
        create_by_default: bool = False,
    ):
        self.table = table
        super().__init__(account, api_key)
        self.create_by_default = create_by_default

    @property
    def resource_type(self):
        return StorageResourceType.table

    @asynccontextmanager
    async def client(self):
        """Retrieve a client for the table"""
        async with TableServiceClient(
            self.endpoint, credential=self.credential
        ) as service_client:
            # NOTE: not exists() method for TableClient
            if not service_client.query_tables(self.table):
                if self.create_by_default:  # if table does not exist, create it
                    await service_client.create_table(self.table)
                else:  # if table does not exist, raise error
                    raise ResourceNotFoundError(f"Table not found: '{self.table}'")
            yield service_client.get_table_client(self.table)

    async def upsert_entity(self, entity_data: dict):
        """
        Upload a table entity to the table storage account

        :param entity_data: The data to be uploaded as a table entity.
        """
        async with self.client() as table_client:
            await table_client.upsert_entity(entity=entity_data)

    async def retrieve_table_entities(self, query: str):
        """
        Retrieve table entities from the table storage account

        :param query: The query string to filter the table entities.
        """
        table_entities_list: list[TableEntity] = []
        async with self.client() as table_client:
            async for table_ent in table_client.query_entities(query_filter=str(query)):
                table_entities_list.append(table_ent)
        return table_entities_list

    async def remove_table_entity(self, entity: TableEntity):
        """
        Remove a table entity from the table storage account

        :param entity: The table entity to be removed.
        """
        async with self.client() as table_client:
            await table_client.delete_entity(
                partition_key=entity["PartitionKey"], row_key=entity["RowKey"]
            )

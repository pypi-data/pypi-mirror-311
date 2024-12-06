from pathlib import Path
from typing import overload, TypedDict, Unpack

from anyio import open_file
import asyncer
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from azure.storage.blob.aio._blob_client_async import BlobClient

from azaux.storage_resource import StorageResource, StorageResourceType


@overload
async def download_blob(
    client: ContainerClient, blob_name: str, encoding: None = None, **kwargs
) -> bytes: ...


@overload
async def download_blob(
    client: ContainerClient, blob_name: str, encoding: str, **kwargs
) -> str: ...


async def download_blob(
    client: ContainerClient, blob_name: str, encoding: str | None = None, **kwargs
) -> bytes | str:
    """
    Retrieve data from a given blob file within the container.

    :param client: The ContainerClient.
    :param blob_name: The name of the blob file.
    :param encoding: The encoding to use for decoding the blob content.
    :param kwargs: Additional keyword arguments to pass to download_blob.
    :return: The content of the blob.
    """
    downloader = await client.download_blob(blob_name, **kwargs)
    content = await downloader.readall()
    return content.decode(encoding) if encoding else content


async def upload_blob(
    client: ContainerClient, filepath: Path, blob_path: Path | None = None, **kwargs
) -> BlobClient:
    """
    Upload a file to a blob, or get the blob client if it already exists.

    :param client: The ContainerClient.
    :param filepath: The path to the file to upload.
    :param blob_path: The path in the blob storage to upload to.
    :return: The BlobClient for the uploaded blob.
    """
    async with await open_file(filepath, mode="rb") as f:
        blob_name = str(blob_path or filepath)
        blob_client = await client.upload_blob(blob_name, f, **kwargs)
    return blob_client


async def sync_blobs(
    client: ContainerClient, filepaths: list[Path], blob_paths: list[Path] | None = None
) -> list[BlobClient]:
    """Upload files only if they don't already exist in the blob storage."""
    soon_values: list[asyncer.SoonValue[BlobClient]] = []
    async with asyncer.create_task_group() as tg:
        for i, pth in enumerate(filepaths):
            blb = blob_paths[i] if blob_paths else pth
            blob_client = client.get_blob_client(blb.as_posix())
            if not await blob_client.exists():
                soon_values.append(tg.soonify(upload_blob)(client, pth, blb))
    return [sv.value for sv in soon_values]


async def sync_folder_blobs(
    client: ContainerClient, folder: Path, pattern: str = "**/*"
) -> list[BlobClient]:
    """Sync a folder with a blob storage container."""
    existing_blobs = {blb.name async for blb in client.list_blobs(folder.name + "/")}
    tasks: list[asyncer.SoonValue[BlobClient]] = []
    async with asyncer.create_task_group() as tg:
        for filepath in folder.glob(pattern):
            if filepath.is_file():
                blob_path = filepath.relative_to(folder.parent)
                if str(blob_path) not in existing_blobs:
                    tasks.append(tg.soonify(upload_blob)(client, filepath, blob_path))
    return [t.value for t in tasks]


class ServiceKwargs(TypedDict, total=False):
    secondary_hostname: str
    max_block_size: int
    max_single_put_size: int
    min_large_block_upload_threshold: int
    use_byte_buffer: bool
    max_page_size: int
    max_single_get_size: int
    max_chunk_get_size: int
    audience: str


class ContainerManager(StorageResource):
    """
    Class to manage retrieving blob data from a given blob file.

    :param container: The name of the container.
    :param account: The name of the Azure Storage account.
    :param api_key: The API key for the Azure Storage account.
    """

    def __init__(
        self,
        container: str,
        account: str,
        api_key: str,
        **kwargs: Unpack[ServiceKwargs],
    ):
        """
        Initialize the ContainerManager class.

        :param container: The name of the container.
        :param account: The name of the Azure Storage account.
        :param api_key: The API key for the Azure Storage account.
        :param create_if_missing: Whether to create the container if it does not exist.

        """
        self.container = container
        super().__init__(account, api_key)
        self.kwargs = kwargs
        self._client_cache: ContainerClient | None = None

    @property
    def resource_type(self) -> StorageResourceType:
        return StorageResourceType.blob

    @property
    def client(self):
        """Retrieve a client for the container, using a cached client if available"""
        if not self._client_cache:
            service = BlobServiceClient(
                self.endpoint, credential=self.credential, **self.kwargs
            )
            self._client_cache = service.get_container_client(self.container)
        return self._client_cache

    async def download_blob(self, blob_path: Path, encoding: None | str = None):
        """Download a blob from the container"""
        async with self.client as client:
            return await download_blob(client, blob_path.as_posix(), encoding)

    async def upload_blob(self, filepath: Path, blob_path: Path | None = None):
        """Upload a file to a blob, or get the blob client if it already exists."""
        async with self.client as client:
            return await upload_blob(client, filepath, blob_path)

    async def try_upload_blobs(
        self, filepaths: list[Path], blob_paths: list[Path] | None = None
    ):
        """
        Upload multiple files to blobs with the filepaths as default names.

        :param filepaths: The paths to the files to upload.
        :param blob_paths: The paths in the blob storage to upload to.
        """
        async with self.client as client:
            await sync_blobs(client, filepaths, blob_paths)

    async def sync_with_folder(self, folder: Path, pattern: str = "**/*"):
        """Sync the container with a folder"""
        async with self.client as client:
            await sync_folder_blobs(client, folder, pattern)

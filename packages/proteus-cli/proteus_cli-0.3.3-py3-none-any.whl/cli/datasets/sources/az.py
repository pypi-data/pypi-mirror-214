import re

# from azure.storage.blob._models import BlobProperties as AzureBlobProperties
from io import BytesIO

from azure.storage.blob import ContainerClient
from azure.core.credentials import AzureSasCredential
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError
from azure.identity import DefaultAzureCredential

from .common import Source, SourcedItem
from ... import proteus
from cli.config import config

AZURE_SAS_TOKEN = config.AZURE_SAS_TOKEN

CONTENT_CHUNK_SIZE = 10 * 1024 * 1024


class AZSource(Source):
    URI_re = re.compile(
        r"^https:\/\/(?P<bucket_name>.*\.windows\.net)\/" r"(?P<container_name>[^\/]*)(\/)?(?P<prefix>.*)?$"
    )

    def __init__(self, uri):
        super().__init__(uri)
        match = self.URI_re.match(uri.rstrip("/"))
        assert match is not None, f"{uri} must be an s3 URI"
        container_name = match.groupdict()["container_name"]
        storage_url = f'https://{match.groupdict()["bucket_name"]}'

        auth_methods = [
            "exclude_environment_credential",
            "exclude_cli_credential",
            "exclude_shared_token_cache_credential",
            "exclude_visual_studio_code_credential",
            "exclude_interactive_browser_credential",
            "exclude_powershell_credential",
            "exclude_managed_identity_credential",
        ]

        if AZURE_SAS_TOKEN:
            self.container_client = ContainerClient(
                storage_url,
                credential=AzureSasCredential(AZURE_SAS_TOKEN),
                container_name=container_name,
            )
            return

        errors = []
        login_successful = False
        for auth_method in auth_methods:
            try:
                flags = {auth: True for auth in auth_methods}
                flags[auth_method] = False
                self.container_client = ContainerClient(
                    storage_url,
                    credential=DefaultAzureCredential(**flags),
                    container_name=container_name,
                )
                self.container_client.exists()
                login_successful = True
                break
            except ClientAuthenticationError as e:
                errors.append(e)

        if not login_successful:
            for error in errors:
                proteus.logger.error(error)
            raise RuntimeError("Cannot authenticate into azure")

    @proteus.may_insist_up_to(5, 1)
    def list_contents(self, starts_with="", ends_with=None):
        bucket_uri = self.uri
        match = self.URI_re.match(bucket_uri.rstrip("/"))
        assert match is not None, f"{bucket_uri} must be an s3 URI"
        prefix = match.groupdict()["prefix"]
        try:
            for item in self.container_client.list_blobs(name_starts_with=prefix + starts_with):
                item_name = f'/{item["name"]}'
                assert item_name.startswith(f"/{prefix}{starts_with}".replace("//", "/"))
                if ends_with is None or item_name.endswith(ends_with):
                    yield SourcedItem(item, item_name, self, item.size)
        except HttpResponseError:
            proteus.logger.error(
                "Missing Azure credentials to perform this operation, please "
                "provide a SAS token or provide another authentication method on Azure"
            )
            raise

    def open(self, reference):
        reference_path = reference.get("name")
        file_size = reference["size"]
        modified = reference["last_modified"]

        stream = BytesIO()
        streamdownloader = self.container_client.download_blob(reference.get("name"), max_concurrency=4)
        streamdownloader.download_to_stream(stream)
        stream.seek(0)
        return reference_path, file_size, modified, stream

    @proteus.may_insist_up_to(5, 1)
    def _download_blob(self, reference):
        return self.container_client.download_blob(
            reference.get("name"), max_concurrency=3, read_timeout=8000, timeout=8000
        )

    def download(self, reference):
        return self._download_blob(reference).readall()

    def chunks(self, reference):
        with AZObjectFile(
            mode="r", size=reference.size, container_client=self.container_client, reference_path=reference.get("name")
        ) as f:
            for chunk in f:
                yield chunk


class AZObjectFile:
    """An ObjectFile in object storage that can be opened and closed.
    See Objects.open()"""

    def __init__(self, mode, size, container_client=None, reference_path=None):
        """Initialize the Object object with a name and a blob_client
        mode is w or r, size is the blob size.
        """
        self.container_client = container_client
        self.reference_path = reference_path
        self.block_list = []
        self.mode = mode
        self.__open__ = True
        self.pos = 0
        self.size = size

    def close(self):
        """Finalise the object"""
        self.__open__ = False

    def __del__(self):
        if self.__open__:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__open__:
            self.close()

    def __iter__(self):
        self.pos = 0

        return self

    @proteus.may_insist_up_to(5, delay_in_secs=1)
    def __next__(self):
        data = BytesIO()
        if self.pos >= self.size:
            raise StopIteration()
        elif self.pos + CONTENT_CHUNK_SIZE > self.size:
            size = self.size - self.pos
        else:
            size = CONTENT_CHUNK_SIZE
        self.container_client.download_blob(self.reference_path, offset=self.pos, length=size).download_to_stream(
            data, max_concurrency=16
        )
        self.pos += size
        return data.getvalue()

    def read(self, size=CONTENT_CHUNK_SIZE):
        if size is None:
            return self.container_client.download_blob(self.reference_path).readall()
        else:
            if self.pos >= self.size:
                return ""
            elif self.pos + size > self.size:
                size = self.size - self.pos
            data = BytesIO()
            self.container_client.download_blob(self.reference_path, offset=self.pos, length=size).download_to_stream(
                data, max_concurrency=4
            )
            self.pos += size
            return data.getvalue()

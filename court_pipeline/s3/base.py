from abc import ABC, abstractmethod
import asyncio
import io
import os
from typing import Any

from minio import Minio


class S3MixIn(ABC):
    """
    Base Mixin class that provides S3-compatible storage capabilities.
    Focuses solely on storage responsibilities without configuration management.
    Subclasses define bucket-specific behavior.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._s3_client: Optional[Minio] = None

    @property
    @abstractmethod
    def bucket_name(self) -> str:
        """
        Return the S3 bucket name for this storage type.
        Must be implemented by concrete subclasses.
        """
        pass

    @property
    @abstractmethod
    def object_name(self, *args: Any, **kwargs: Any) -> str:
        """
        Generate object name based on parameters.
        Must be implemented by concrete subclasses.
        """
        pass

    @property
    def s3_client(self) -> Minio:
        if self._s3_client is None:
            self._s3_client = Minio(
                endpoint=os.getenv('S3_ENDPOINT', 'localhost:9000'),
                access_key=os.getenv('S3_ACCESS_KEY', 'minioadmin'),
                secret_key=os.getenv('S3_SECRET_KEY', 'minioadmin'),
                secure=os.getenv('S3_SECURE', 'false').lower() == 'true'
            )
        return self._s3_client

    async def create_bucket(self) -> None:

        def _create_bucket(client: Minio, bucket_name: str) -> None:
            is_exist = client.bucket_exists(bucket_name)
            if is_exist:
                return
            client.make_bucket(bucket_name)

        await asyncio.to_thread(
            _create_bucket,
            client=self.s3_client,
            bucket_name=self.bucket_name,
        )

    async def store_object(self, data: bytes, content_type: str) -> None:
        """
        Store object to S3-compatible storage
        """

        def _store_object(
            client: Minio,
            bucket_name: str,
            object_name: str,
            data: bytes,
            content_type: str,
        ) -> None:
            data_io = io.BytesIO(data)
            data_length = len(data)
            client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data_io,
                length=data_length,
                content_type=content_type,
            )

        await asyncio.to_thread(
            _store_object,
            client=self.s3_client,
            bucket_name=self.bucket_name,
            object_name=self.object_name,
            data=data,
            content_type=content_type,
        )

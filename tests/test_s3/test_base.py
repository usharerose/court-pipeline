import os
import pytest
from unittest.mock import Mock, patch

from court_pipeline.s3.base import S3MixIn


class SampleS3MixIn(S3MixIn):

    @property
    def bucket_name(self) -> str:
        return "test-bucket"

    @property
    def object_name(self) -> str:
        return "test-object.json"


class TestS3MixIn:

    def test_init_mixin(self):
        mixin = SampleS3MixIn()
        assert getattr(mixin, "_s3_client", None) is None

    @patch.dict(os.environ, {
        'S3_ENDPOINT': 'test-endpoint:9000',
        'S3_ACCESS_KEY': 'test-key',
        'S3_SECRET_KEY': 'test-secret',
        'S3_SECURE': 'true'
    })
    @patch('court_pipeline.s3.base.Minio')
    def test_s3_client_creation_with_env(self, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()
        client = mixin.s3_client

        assert client == mock_client
        mock_minio.assert_called_once_with(
            endpoint='test-endpoint:9000',
            access_key='test-key',
            secret_key='test-secret',
            secure=True
        )

    @patch.dict(os.environ, {}, clear=True)
    @patch('court_pipeline.s3.base.Minio')
    def test_s3_client_creation_with_defaults(self, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()
        client = mixin.s3_client

        assert client == mock_client
        mock_minio.assert_called_once_with(
            endpoint='localhost:9000',
            access_key='minioadmin',
            secret_key='minioadmin',
            secure=False
        )

    @patch('court_pipeline.s3.base.Minio')
    def test_s3_client_lazy_initialization(self, mock_minio):
        """Test that S3 client is lazily initialized"""
        mock_client = Mock()
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()

        assert getattr(mixin, "_s3_client", None) is None

        client1 = mixin.s3_client
        assert client1 == mock_client
        assert mixin._s3_client == mock_client

        client2 = mixin.s3_client
        assert client2 == client1
        mock_minio.assert_called_once()

    def test_bucket_name_is_abstract(self):
        with pytest.raises(TypeError):
            S3MixIn()

    def test_object_name_is_abstract(self):

        class IncompleteMixIn(S3MixIn):
            @property
            def bucket_name(self) -> str:
                return "test"

        with pytest.raises(TypeError):
            IncompleteMixIn()

    @patch('court_pipeline.s3.base.Minio')
    @pytest.mark.asyncio
    async def test_create_bucket_async(self, mock_minio):
        mock_client = Mock()
        mock_client.bucket_exists.return_value = False
        mock_client.make_bucket.return_value = None
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()
        await mixin.create_bucket()

        mock_client.bucket_exists.assert_called_once_with("test-bucket")
        mock_client.make_bucket.assert_called_once_with("test-bucket")

    @patch('court_pipeline.s3.base.Minio')
    @pytest.mark.asyncio
    async def test_create_bucket_already_exists(self, mock_minio):
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.make_bucket.return_value = None
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()
        await mixin.create_bucket()

        mock_client.bucket_exists.assert_called_once_with("test-bucket")
        mock_client.make_bucket.assert_not_called()

    @patch('court_pipeline.s3.base.Minio')
    @pytest.mark.asyncio
    async def test_store_object_async(self, mock_minio):
        mock_client = Mock()
        mock_client.put_object.return_value = None
        mock_minio.return_value = mock_client

        mixin = SampleS3MixIn()
        data = b'{"version": "1.0.0"}'
        content_type = "application/json"

        await mixin.store_object(data, content_type)

        mock_client.put_object.assert_called_once()
        call_args = mock_client.put_object.call_args

        assert call_args[1]['bucket_name'] == "test-bucket"
        assert call_args[1]['object_name'] == "test-object.json"
        assert call_args[1]['content_type'] == content_type

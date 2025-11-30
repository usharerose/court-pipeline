"""
Test cases for BaseExtractorMixIn
"""
import datetime
import json
from unittest.mock import Mock

import httpx
import pytest

from court_pipeline.extractors.base import BaseExtractorMixIn


class MockExtractor(BaseExtractorMixIn):

    def __init__(self):
        self.fetch_called = False
        self.fetch_args = None
        self.fetch_kwargs = None
        self.store_object_called = False
        self.store_object_data = None
        self.store_object_content_type = None

    async def fetch(self, *args, **kwargs):
        self.fetch_called = True
        self.fetch_args = args
        self.fetch_kwargs = kwargs

        mock_response = Mock(spec=httpx.Response)
        mock_response.content = json.dumps({"test": "data"}).encode()
        return mock_response

    async def store_object(self, data: bytes, content_type: str):
        self.store_object_called = True
        self.store_object_data = data
        self.store_object_content_type = content_type


class TestBaseExtractorMixIn:

    @pytest.mark.asyncio
    async def test_extract_calls_fetch_and_store_object(self):
        extractor = MockExtractor()

        await extractor.extract(game_id="0012300001")

        assert extractor.fetch_called is True
        assert extractor.fetch_args == ()
        assert extractor.fetch_kwargs == {"game_id": "0012300001"}

        assert extractor.store_object_called is True
        expected_data = json.dumps({"test": "data"}).encode()
        assert extractor.store_object_data == expected_data
        assert extractor.store_object_content_type == "application/json"

    @pytest.mark.asyncio
    async def test_extract_with_multiple_arguments(self):
        extractor = MockExtractor()

        await extractor.extract(datetime.date(2025, 11, 28), league_id="00")

        assert extractor.fetch_args == (datetime.date(2025, 11, 28),)
        assert extractor.fetch_kwargs == {"league_id": "00"}

    @pytest.mark.asyncio
    async def test_extract_content_type_is_application_json(self):
        extractor = MockExtractor()

        await extractor.extract()

        assert extractor.store_object_content_type == "application/json"

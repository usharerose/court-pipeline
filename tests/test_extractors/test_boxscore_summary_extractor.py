"""
Test cases for BoxscoreSummaryExtractor
"""
import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from court_pipeline.extractors.boxscore_summary_extractor import BoxscoreSummaryExtractor


with open("tests/fixtures/0022400001.json") as f:
    boxscore_summary_data = json.load(f)


class TestBoxscoreSummaryExtractor:

    def test_inheritance_structure(self):
        extractor = BoxscoreSummaryExtractor()

        assert hasattr(extractor, 'fetch')
        assert hasattr(extractor, 'store_object')
        assert hasattr(extractor, 'extract')

    def test_bucket_name_property(self):
        extractor = BoxscoreSummaryExtractor()
        assert extractor.bucket_name == "boxscoresummary"

    @patch('court_pipeline.extractors.boxscore_summary_extractor.BoxscoreSummaryS3MixIn.store_object')
    @patch('court_pipeline.extractors.boxscore_summary_extractor.BoxscoreSummaryProxy.fetch')
    @pytest.mark.asyncio
    async def test_extract_calls_super_extract_with_game_id(self, mock_fetch, mock_store_object):
        mock_response = Mock()
        mock_response.content = json.dumps(boxscore_summary_data).encode('utf-8')
        mock_fetch.return_value = mock_response

        extractor = BoxscoreSummaryExtractor()
        game_id = "0022400001"

        await extractor.extract(game_id)

        mock_fetch.assert_called_once_with(game_id=game_id)

        mock_store_object.assert_called_once_with(
            json.dumps(boxscore_summary_data).encode('utf-8'),
            "application/json",
        )

    @patch('court_pipeline.extractors.boxscore_summary_extractor.BoxscoreSummaryS3MixIn.store_object')
    @patch('httpx.AsyncClient') 
    @pytest.mark.asyncio
    async def test_extract_stores_game_id_internal_state(self, mocked_client, mock_store_object):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(boxscore_summary_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_store_object.return_value = None

        extractor = BoxscoreSummaryExtractor()
        game_id = "0022400001"

        await extractor.extract(game_id)
        assert extractor._game_id == game_id

    @patch('court_pipeline.extractors.boxscore_summary_extractor.BoxscoreSummaryS3MixIn.store_object')
    @patch('httpx.AsyncClient') 
    @pytest.mark.asyncio
    async def test_object_name_property_with_valid_game_id(self, mocked_client, mock_store_object):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(boxscore_summary_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_store_object.return_value = None

        extractor = BoxscoreSummaryExtractor()
        game_id = "0012300001"

        await extractor.extract(game_id)

        object_name = extractor.object_name

        expected = "/00/2023/0012300001.json"
        assert object_name == expected

    def test_game_id_is_optional_for_initialization(self):
        extractor = BoxscoreSummaryExtractor()
        assert extractor._game_id is None

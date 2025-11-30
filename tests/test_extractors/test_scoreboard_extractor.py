"""
Test cases for ScoreboardExtractor
"""
import datetime
import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from court_pipeline.extractors.scoreboard_extractor import ScoreboardExtractor


with open("tests/fixtures/2025-11-23.json") as f:
    scoreboard_data = json.load(f)


class TestScoreboardExtractor:

    def test_inheritance_structure(self):
        extractor = ScoreboardExtractor()

        assert hasattr(extractor, 'fetch')
        assert hasattr(extractor, 'store_object')
        assert hasattr(extractor, 'extract')

    def test_bucket_name_property(self):
        extractor = ScoreboardExtractor()
        assert extractor.bucket_name == "scoreboard"

    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardS3MixIn.store_object')
    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardProxy.fetch')
    @pytest.mark.asyncio
    async def test_extract_calls_super_extract_with_parameters(self, mock_fetch, mock_store_object):
        mock_response = Mock()
        mock_response.content = json.dumps(scoreboard_data).encode('utf-8')
        mock_fetch.return_value = mock_response

        extractor = ScoreboardExtractor()
        game_date = datetime.date(2025, 11, 23)
        league_id = "00"

        await extractor.extract(game_date, league_id)

        mock_fetch.assert_called_once_with(game_date=game_date, league_id=league_id)

        mock_store_object.assert_called_once_with(
            json.dumps(scoreboard_data).encode('utf-8'),
            "application/json",
        )

    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardS3MixIn.store_object')
    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardProxy.fetch')
    @pytest.mark.asyncio
    async def test_extract_with_default_league_id(self, mock_fetch, mock_store_object):
        mock_response = Mock()
        mock_response.content = json.dumps(scoreboard_data).encode('utf-8')
        mock_fetch.return_value = mock_response

        extractor = ScoreboardExtractor()
        game_date = datetime.date(2025, 11, 23)

        await extractor.extract(game_date)

        mock_fetch.assert_called_once_with(game_date=game_date, league_id="00")

        mock_store_object.assert_called_once_with(
            json.dumps(scoreboard_data).encode('utf-8'),
            "application/json",
        )

    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardS3MixIn.store_object')
    @patch('httpx.AsyncClient') 
    @pytest.mark.asyncio
    async def test_extract_stores_internal_state(self, mocked_client, mock_store_object):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(scoreboard_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_store_object.return_value = None

        extractor = ScoreboardExtractor()
        game_date = datetime.date(2025, 11, 23)
        await extractor.extract(game_date)

        assert extractor._game_date == game_date
        assert extractor._league_id == "00"

    @patch('court_pipeline.extractors.scoreboard_extractor.ScoreboardS3MixIn.store_object')
    @patch('httpx.AsyncClient') 
    @pytest.mark.asyncio
    async def test_object_name_property_with_valid_date(self, mocked_client, mock_store_object):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(scoreboard_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response
        mock_store_object.return_value = None

        extractor = ScoreboardExtractor()
        game_date = datetime.date(2025, 11, 23)
        league_id = "00"

        await extractor.extract(game_date, league_id)

        object_name = extractor.object_name

        expected = "/00/2025/11/23.json"
        assert object_name == expected

    def test_internal_state_is_optional_for_initialization(self):
        extractor = ScoreboardExtractor()
        assert extractor._game_date is None
        assert extractor._league_id is None

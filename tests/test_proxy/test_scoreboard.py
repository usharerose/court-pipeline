"""
Test cases for ScoreboardProxy
"""
import datetime
import json
import pytest
from unittest.mock import AsyncMock, patch

from court_pipeline.proxy.scoreboard import ScoreboardProxy


with open("tests/fixtures/2025-11-23.json") as f:
    scoreboard_data = json.load(f)


class TestScoreboardProxy:

    def setup_method(self):
        self.proxy = ScoreboardProxy()

    def test_path(self):
        expected = "scoreboardv3"
        actual = self.proxy.path
        assert actual == expected

    def test_build_http_params(self):
        expected = {
            "GameDate": "2025-11-23",
            "LeagueID": "00",
        }
        actual = self.proxy.build_http_params(game_date=datetime.date(2025, 11, 23))
        assert actual == expected

    def test_build_http_params_with_league_id(self):
        expected = {
            "GameDate": "2025-11-23",
            "LeagueID": "20",
        }
        actual = self.proxy.build_http_params(
            game_date=datetime.date(2025, 11, 23),
            league_id="20",
        )
        assert actual == expected

    def test_build_http_params_with_invalid_keyword(self):
        with pytest.raises(TypeError):
            self.proxy.build_http_params(game_id="0022400001")

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_fetch_success(self, mocked_client):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(scoreboard_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response

        response = await self.proxy.fetch(game_date=datetime.date(2025, 11, 23))

        actual = json.loads(response.content.decode('utf-8'))
        expected = scoreboard_data
        assert actual == expected

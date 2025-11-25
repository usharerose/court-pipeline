"""
Test cases for BoxscoreSummaryProxy
"""
import json
import pytest
from unittest.mock import AsyncMock, patch

from court_pipeline.proxy.boxscore_summary import BoxscoreSummaryProxy


with open("tests/fixtures/0022400001.json") as f:
    boxscore_summary_data = json.load(f)


class TestBoxscoreSummaryProxy:

    def setup_method(self):
        self.proxy = BoxscoreSummaryProxy()

    def test_path(self):
        expected = "boxscoresummaryv3"
        actual = self.proxy.path
        assert actual == expected

    def test_build_http_params(self):
        expected = {
            "GameID": "0022400001",
        }
        actual = self.proxy.build_http_params(game_id="0022400001")
        assert actual == expected

    def test_build_http_params_with_invalid_keyword(self):
        with pytest.raises(TypeError):
            self.proxy.build_http_params(gameID="0022400001")

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_fetch_success(self, mocked_client):
        mock_response = AsyncMock()
        mock_response.content = json.dumps(boxscore_summary_data).encode('utf-8')
        mocked_client.return_value.__aenter__.return_value.get.return_value = mock_response

        response = await self.proxy.fetch(game_id="0022400001")

        actual = json.loads(response.content.decode('utf-8'))
        expected = boxscore_summary_data
        assert actual == expected

import datetime
from typing import Any, Dict

import httpx

from .base import NBAProxy


class ScoreboardProxy(NBAProxy):

    @property
    def path(self) -> str:
        return 'scoreboardv3'

    def build_http_params(
        self,
        game_date: datetime.date,
        league_id: str = "00",
    ) -> Dict[str, Any]:
        """
        :param game_date: game date in format YYYY-MM-DD
        :type game_date: datetime.date
        :param league_id: Identifier of league, default is '00' for National Basketball Association
        :type league_id: str
        """
        return {
            'GameDate': game_date.strftime('%Y-%m-%d'),
            'LeagueID': league_id,
        }

    async def fetch(
        self,
        game_date: datetime.date,
        league_id: str = "00",
    ) -> httpx.Response:
        """
        :param game_date: game date in format YYYY-MM-DD
        :type game_date: datetime.date
        :param league_id: Identifier of league, default is '00' for National Basketball Association
        :type league_id: str
        """
        return await super().fetch(
            game_date=game_date,
            league_id=league_id,
        )

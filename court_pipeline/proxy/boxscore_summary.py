from typing import Any, Dict, Optional

import httpx

from .base import NBAProxy


class BoxscoreSummaryProxy(NBAProxy):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._game_id: Optional[str] = None

    @property
    def path(self) -> str:
        return 'boxscoresummaryv3'

    def build_http_params(self, game_id: str) -> Dict[str, Any]:
        """
        :param game_id: Identifier of game
        :type game_id: str
        """
        return {
            'GameID': game_id,
        }

    async def fetch(self, game_id: str) -> httpx.Response:
        """
        :param game_id: Identifier of game
        :type game_id: str
        """
        self._game_id = game_id
        return await super().fetch(game_id=game_id)

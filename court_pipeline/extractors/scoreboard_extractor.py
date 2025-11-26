import datetime
import logging

from .base import BaseExtractorMixIn
from ..proxy.scoreboard import ScoreboardProxy
from ..s3.scoreboard import ScoreboardS3MixIn


logger = logging.getLogger(__name__)


class ScoreboardExtractor(
    ScoreboardProxy,
    ScoreboardS3MixIn,
    BaseExtractorMixIn
):
    async def extract(
        self,
        game_date: datetime.date,
        league_id: str = "00",
    ) -> None:
        """
        :param game_date: game date in format YYYY-MM-DD
        :type game_date: datetime.date
        :param league_id: Identifier of league, default is '00' for National Basketball Association
        :type league_id: str
        """
        await super().extract(game_date=game_date, league_id=league_id)

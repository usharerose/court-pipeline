import logging

from .base import BaseExtractorMixIn
from ..proxy.boxscore_summary import BoxscoreSummaryProxy
from ..s3.boxscore_summary import BoxscoreSummaryS3MixIn


logger = logging.getLogger(__name__)


class BoxscoreSummaryExtractor(
    BoxscoreSummaryProxy,
    BoxscoreSummaryS3MixIn,
    BaseExtractorMixIn
):
    async def extract(self, game_id: str) -> None:
        """
        :param game_id: Identifier of game
        :type game_id: str
        """
        await super().extract(game_id=game_id)

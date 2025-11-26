from typing import Optional, Protocol

from .base import S3MixIn
from ..utils.game_id import GameId


class BoxscoreSummaryProtocol(Protocol):

    _game_id: Optional[str]


class BoxscoreSummaryS3MixIn(S3MixIn):

    @property
    def bucket_name(self) -> str:
        return "boxscoresummary"

    @property
    def object_name(self: BoxscoreSummaryProtocol) -> str:
        game_id_obj = GameId(self._game_id)
        pattern = '/{league_id}/{season_year:04d}/{game_id}.json'
        return pattern.format(
            league_id=game_id_obj.league_id,
            season_year=game_id_obj.season_year,
            game_id=game_id_obj.value,
        )

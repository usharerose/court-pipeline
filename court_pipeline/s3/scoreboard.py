import datetime
from typing import Any, Dict, Optional, Protocol

from .base import S3MixIn


class ScoreboardProtocol(Protocol):

    _game_date: Optional[datetime.date]
    _league_id: Optional[str]


class ScoreboardS3MixIn(S3MixIn):

    @property
    def bucket_name(self) -> str:
        return "scoreboard"

    @property
    def object_name(self: ScoreboardProtocol) -> str:
        pattern = '/{league_id}/{year:04d}/{month:02d}/{day:02d}.json'
        return pattern.format(
            league_id=self._league_id,
            year=self._game_date.year,
            month=self._game_date.month,
            day=self._game_date.day,
        )

import re


GAME_ID_PATTERN = re.compile(r'^(\d{2})(\d{1})(\d{2})(\d{5})$')
LEAGUE_MAPPING = {
    "00": "NBA",
    "01": "WNBA",
    "10": "G-League",
}
GAME_TYPE_MAPPING = {
    1: "Pre-season",
    2: "Regular Season",
    3: "All-Star Game",
    4: "Playoffs",
    5: "Play-in Tournament",
}


class GameId:

    def __init__(self, game_id: str) -> None:
        self._game_id = game_id
        self._parse()

    @property
    def value(self) -> str:
        return self._game_id

    def _validate(self) -> None:
        if not isinstance(self._game_id, str):
            raise TypeError("game_id should be a string")
        if not self._game_id.isdigit():
            raise ValueError("game_id should be a numeric string")
        if len(self._game_id) != 10:
            raise ValueError("game_id should be 10 digits")

    def _parse(self) -> None:
        self._validate()
        match = GAME_ID_PATTERN.match(self._game_id)
        league_str, game_type_str, season_str, game_seq_str = match.groups()
        self._league_id = league_str
        self._game_type_id = int(game_type_str)
        self._season_id = season_str
        self._game_seq_id = int(game_seq_str)

    @property
    def league_id(self) -> str:
        return self._league_id

    @property
    def league_code(self) -> str:
        if self._league_id not in LEAGUE_MAPPING:
            return "unknown"
        return LEAGUE_MAPPING[self._league_id]

    @property
    def game_type_id(self) -> int:
        return self._game_type_id

    @property
    def game_type_name(self) -> str:
        if self._game_type_id not in GAME_TYPE_MAPPING:
            return "unknown"
        return GAME_TYPE_MAPPING[self._game_type_id]

    @property
    def season_id(self) -> str:
        return self._season_id

    @property
    def season_year(self) -> int:
        year_suffix = int(self._season_id)
        year_prefix = 19
        if year_suffix < 46:  # first game is in 1946-11-01
            year_prefix = 20
        return int(f'{year_prefix}{year_suffix}')

    @property
    def game_seq_id(self) -> int:
        return self._game_seq_id

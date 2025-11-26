import pytest

from court_pipeline.utils.game_id import GameId


class TestGameId:

    def test_init_valid_game_id(self):
        game_id = "0022400001"
        game_id_obj = GameId(game_id)

        assert game_id_obj.value == game_id
        assert game_id_obj.league_id == game_id[:2]
        assert game_id_obj.game_type_id == int(game_id[2])
        assert game_id_obj.season_id == game_id[3:5]
        assert game_id_obj.game_seq_id == int(game_id[5:])

    def test_init_non_numeric_game_id(self):
        game_id = "ABCDEFGHIJ"
        with pytest.raises(ValueError):
            GameId(game_id)

    def test_init_too_short_game_id(self):
        game_id = "123"
        with pytest.raises(ValueError):
            GameId(game_id)

    def test_init_too_long_game_id(self):
        game_id = "12345678901"
        with pytest.raises(ValueError):
            GameId(game_id)

    def test_league_id_property(self):
        """Test league_id property"""
        test_cases = [
            ("0022400001", "00"),  # NBA
            ("0122300005", "01"),  # WNBA
            ("1022500002", "10"),  # G-League
        ]

        for game_id, expected in test_cases:
            game_id_obj = GameId(game_id)
            assert game_id_obj.league_id == expected

    def test_league_code_property(self):
        """Test league_code property"""
        test_cases = [
            ("0022400001", "NBA"),     # NBA
            ("0122300005", "WNBA"),   # WNBA
            ("1022500002", "G-League"),  # G-League
            ("9922400001", "unknown"), # Unknown league
        ]

        for game_id, expected in test_cases:
            game_id_obj = GameId(game_id)
            assert game_id_obj.league_code == expected

    def test_game_type_id_property(self):
        """Test game_type_id property"""
        test_cases = [
            ("0012400001", 1),  # Pre-season
            ("0022400001", 2),  # Regular season
            ("0032400001", 3),  # All-star
            ("0042400001", 4),  # Playoffs
            ("0052400001", 5),  # Play-in tournament
        ]

        for game_id, expected in test_cases:
            game_id_obj = GameId(game_id)
            assert game_id_obj.game_type_id == expected

    def test_game_type_name_property(self):
        game_id = "0042400001"
        game_id_obj = GameId(game_id)
        assert game_id_obj.game_type_name == "Playoffs"

    def test_season_year_edge_case(self):
        game_id = "0024600001"
        game_id_obj = GameId(game_id)
        assert game_id_obj.season_year == 1946

    def test_season_year_property(self):
        game_id = "0022400001"
        game_id_obj = GameId("0022400001")
        assert game_id_obj.season_year == 2024

import datetime

from court_pipeline.s3.scoreboard import ScoreboardS3MixIn


class TestScoreboardS3MixIn:

    def test_bucket_name(self):
        mixin = ScoreboardS3MixIn()
        assert mixin.bucket_name == "scoreboard"

    def test_object_name_property(self):
        mixin = ScoreboardS3MixIn()
        mixin._game_date = datetime.date(2025, 11, 26)
        mixin._league_id = "00"

        object_name = mixin.object_name
        expected = "/00/2025/11/26.json"
        assert object_name == expected

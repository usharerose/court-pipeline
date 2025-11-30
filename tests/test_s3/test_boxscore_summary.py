from court_pipeline.s3.boxscore_summary import BoxscoreSummaryS3MixIn


class TestBoxscoreSummaryS3MixIn:

    def test_bucket_name(self):
        mixin = BoxscoreSummaryS3MixIn()
        assert mixin.bucket_name == "boxscoresummary"

    def test_object_name_property(self):
        mixin = BoxscoreSummaryS3MixIn()
        mixin._game_id = "0022400001"

        object_name = mixin.object_name
        expected = "/00/2024/0022400001.json"
        assert object_name == expected

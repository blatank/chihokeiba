import unittest
from race import Race

test_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f03%2f10&k_raceNo=10&k_babaCode=32"

class TestKeiba(unittest.TestCase):
  # 解析機能を含めたテスト
  # keiba.pyのテスト
  def test_integration(self):
    # 解析するレースをセットして解析
    # 24/03/10 佐賀10R 右1400
    race = Race(test_url)
    race.analyzeUrl()

    # 参考にしたいレース条件①レースと同条件
    thisConditionData = race.analyzeThisCondition()
    self.assertTrue(len(thisConditionData) > 0)

    # 参考にしたいレース条件②レースに近い条件
    # 佐賀 右1300
    nearlyConditionData = race.analyzeNearlyCondition()
    self.assertTrue(len(nearlyConditionData) > 0)

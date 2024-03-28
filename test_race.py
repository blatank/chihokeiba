import unittest
from race import Race
from history import History
from racecourse import RaceCourse

test_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f03%2f10&k_raceNo=10&k_babaCode=32"
invalid_url = "https://blatan.info/"

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")

class TestRace(unittest.TestCase):

  # 解析機能を含めたテスト
  def test_integration(self):
    # 解析するレースをセット
    # 24/03/10 佐賀10R 右1400
    race = Race(test_url)

    # 参考にしたいレース条件①レースと同条件
    thisConditionData = race.analyzeThisCondition()
    self.assertTrue(len(thisConditionData) > 0)

    # 参考にしたいレース条件②レースに近い条件
    nearlyConditionData = race.analyzeNearlyCondition()
    self.assertTrue(len(thisConditionData) > 0)   

  def test_race(self):
    # 正しいURLを与えた場合
    race = Race(test_url)
    self.assertTrue(race.analyzeUrl())

    # 正しくないURLを与えた場合
    race = Race(invalid_url)
    self.assertFalse(race.analyzeUrl())

  def test_history(self):
    # 適当に戦績を追加
    history = History(saga1400, "1:30:0")

    # 問合せテスト
    self.assertTrue(history.hasHistory(saga1400))
    self.assertFalse(history.hasHistory(kouchi1400))
    self.assertFalse(history.hasHistory(saga1300))

  def test_raceouse(self):
    # レース条件比較
    self.assertTrue(saga1400.equal(RaceCourse("佐賀", "右1400")))
    self.assertFalse(saga1400.equal(kouchi1400))
    self.assertFalse(saga1400.equal(saga1300))

  def test_estimate_distance(self):
    # 近い距離のデータを取得
    eCourse = saga1400.esitimateCourse()

    # 近い距離は1つ
    self.assertEqual(1, len(eCourse))

    # その1つは佐賀・右1300m
    self.assertEqual("佐賀", eCourse[0].getCourse())
    self.assertEqual("右1300", eCourse[0].getDistance())

    # あり合えないデータを設定
    saga3200 = RaceCourse("佐賀", "右3200")

    # 近い距離のデータを取得
    eCourse = saga3200.esitimateCourse()

    # 近い距離のデータ無し
    self.assertEqual(0, len(eCourse))
    

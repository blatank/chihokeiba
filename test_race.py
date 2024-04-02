import unittest
from race import Race
from racecourse import RaceCourse

test_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f03%2f10&k_raceNo=10&k_babaCode=32"
invalid_url = "https://blatan.info/"

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")

class TestRace(unittest.TestCase):
  def test_race(self):
    # 正しいURLを与えた場合
    race = Race(test_url)
    self.assertTrue(race.analyzeUrl())

    # 正しくないURLを与えた場合
    race = Race(invalid_url)
    self.assertFalse(race.analyzeUrl())

  def test_estimate_couse(self):
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
    

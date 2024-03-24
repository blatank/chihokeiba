import unittest
from race import Race
from history import History

test_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f03%2f13&k_raceNo=12&k_babaCode=24"
invalid_url = "https://blatan.info/"

class TestRace(unittest.TestCase):

  def test_race(self):
    # 正しいURLを与えた場合
    race = Race(test_url)
    self.assertTrue(race.analyzeUrl())

    # 正しくないURLを与えた場合
    race = Race(invalid_url)
    self.assertFalse(race.analyzeUrl())

  def test_history(self):
    # 適当に戦績を追加
    history = History("佐賀", "右1400", "1:30:0")

    # 問合せテスト
    self.assertTrue(history.hasHistory("佐賀", "右1400"))
    self.assertFalse(history.hasHistory("高知", "右1400"))
    self.assertFalse(history.hasHistory("佐賀", "右1300"))
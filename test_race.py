import unittest
import race

test_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f03%2f13&k_raceNo=12&k_babaCode=24"

class TestRace(unittest.TestCase):

  def test_race(self):
    # 正しいURLを与えた場合
    race = Race(test_url)
    self.assertTrue(race.analyze())

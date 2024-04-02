import unittest
from racecourse import RaceCourse

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")

class TestRaceCouse(unittest.TestCase):
  def test_raceouse(self):
    # レース条件比較
    self.assertEqual(saga1400, RaceCourse("佐賀", "右1400"))
    self.assertNotEqual(saga1400, kouchi1400)
    self.assertNotEqual(saga1400, saga1300)
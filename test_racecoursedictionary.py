import unittest
from racercoursedictionary import RaceCourseDictionary

raceCourseNo_Kouchi = 31
raceCourseNo_Saga = 32
raceCourseNo_Ng = 99
class TestRaceCourseDictionary(unittest.TestCase):
  
  # Noから競馬場名を取得
  def test_inquireRaceCourseName(self):
    dictionary = RaceCourseDictionary("racecoursedictionary.json")
    self.assertEqual("高知", dictionary.inquireRaceCourseName(raceCourseNo_Kouchi))
    self.assertNotEqual("高知", dictionary.inquireRaceCourseName(raceCourseNo_Saga))

    # 存在しない馬場コード
    self.assertEqual("", dictionary.inquireRaceCourseName(raceCourseNo_Ng))

import unittest
from racecoursedictionary import RaceCourseDictionary

raceCourseNo_Kouchi = 31
raceCourseNo_Saga = 32
raceCourseNo_Ng = 99
raceCourseName = ["園田","姫路","高知","佐賀","金沢"]
class TestRaceCourseDictionary(unittest.TestCase):
  
  # Noから競馬場名を取得
  def test_inquireRaceCourseName(self):
    dictionary = RaceCourseDictionary("test_racecoursedictionary.json")
    self.assertEqual("高知", dictionary.inquireRaceCourseName(raceCourseNo_Kouchi))
    self.assertNotEqual("高知", dictionary.inquireRaceCourseName(raceCourseNo_Saga))

    # 存在しない馬場コード
    self.assertEqual("", dictionary.inquireRaceCourseName(raceCourseNo_Ng))

    # 全競馬場のテータを取得するテスト
    alldata = dictionary.getAllRaceCourseName()
    self.assertEqual(len(alldata), len(raceCourseName))
    self.assertEqual(alldata, raceCourseName)


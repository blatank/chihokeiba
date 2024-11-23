import unittest
from history import History
from racecourse import RaceCourse
import datetime

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")
testdate = datetime.datetime(2024, 4, 16)
testdata_invalid = datetime.datetime(2023, 4, 16)

class TestHistory(unittest.TestCase):
  def test_history(self):
    # 適当に戦績を追加
    history = History(saga1400, "1:30:0")

    # 問合せテスト
    self.assertTrue(history.hasHistory(saga1400))
    self.assertFalse(history.hasHistory(kouchi1400))
    self.assertFalse(history.hasHistory(saga1300))

    # getTimeStrのテスト
    self.assertEqual("1:30:0", history.getTimeStr())
    self.assertNotEqual("1:30:1", history.getTimeStr())
    
    # getDateのテスト
    # 空白時は1999/1/1扱い
    self.assertEqual(datetime.datetime(1999, 1, 1), history.getDate())
    self.assertNotEqual(datetime.datetime(2024, 4, 16), history.getDate())
    
    # 適当に戦績を追加(日付付き)
    history = History(saga1400, "1:30:0", "24.04.16")

    # getDateのテスト
    self.assertEqual(testdate, history.getDate())
    self.assertNotEqual(testdata_invalid, history.getDate())

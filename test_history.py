import unittest
from history import History
from racecourse import RaceCourse

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")

class TestHistory(unittest.TestCase):
  def test_history(self):
    # 適当に戦績を追加
    history = History(saga1400, "1:30:0")

    # 問合せテスト
    self.assertTrue(history.hasHistory(saga1400))
    self.assertFalse(history.hasHistory(kouchi1400))
    self.assertFalse(history.hasHistory(saga1300))

    # getTimeのテスト
    self.assertEqual("1:30:0", history.getTime())
    self.assertNotEqual("1:30:1", history.getTime())

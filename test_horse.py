import unittest
import datetime
from history import History
from racecourse import RaceCourse
from horse import Horse

saga1300 = RaceCourse("佐賀", "右1300")
saga1400 = RaceCourse("佐賀", "右1400")
kouchi1400 = RaceCourse("高知", "右1400")
h1 = History(saga1400, "1:30:0", "24.12.1", "良", "12", "1", "40.0", "飛騨")
h2 = History(saga1400, "1:31:0", "24.12.2", "良", "12", "1", "40.0", "飛騨")
h3 = History(saga1400, "1:32:0", "24.12.3", "良", "12", "1", "40.0", "飛騨")
h4 = History(saga1400, "1:33:0", "24.12.4", "良", "12", "1", "40.0", "飛騨")
h5 = History(saga1400, "1:34:0", "24.12.5", "良", "12", "1", "40.0", "飛騨")

class TestHoese(unittest.TestCase):
  def test_horse(self):
    # 適当に戦績を追加
    horse = Horse("テイエム野郎", "10")

    horse.addHistory(h1)
    horse.addHistory(h2)
    horse.addHistory(h3)
    horse.addHistory(h4)
    horse.addHistory(h5)

    time = horse.getTopTime(saga1400, datetime.datetime(2024,11,30))
    self.assertEqual("1:30:0 [40.0]  (2024.12.01 良 1/12)", time)

    time = horse.getTopTime(saga1400, datetime.datetime(2024,12,2))
    self.assertEqual("1:31:0 [40.0]  (2024.12.02 良 1/12)", time)



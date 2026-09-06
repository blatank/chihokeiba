from history import History
from racecourse import RaceCourse
import datetime

class Horse:
  def __init__(self, name, no):
    self.__name = name
    self.__no = no
    self.__histories = []

  def getName(self):
    return self.__name
  
  def getNo(self):
    return self.__no
  
  def getPreviousJockey(self):
    if not self.__histories:
      return ""
    return self.__histories[0].getJockey()

  def addHistory(self, history):
    self.__histories.append(history)

  def getTopTime(self, racecourse, date = datetime.datetime(2000, 1, 1)):
    best_history = None
    best_time = 9999
    for history in self.__histories:
      if history.hasHistory(racecourse) and history.getDate() >= date:
        time_int = history.getTimeInt()
        if time_int < best_time:
          best_time = time_int
          best_history = history

    return best_history.getTime() if best_history else ""
  
  def getTopTimeInt(self, racecourse, date = datetime.datetime(2000, 1, 1)):
    best = 9999
    for history in self.__histories:
      if history.hasHistory(racecourse) and history.getDate() >= date:
        time = history.getTimeInt()
        if time < best:
          best = time

    return best
  
  def getTopTimeByWeek(self, racecourse, week_start, week_end):
    """指定した週の期間内で最速タイムを取得
    
    :param racecourse: RaceCourseオブジェクト
    :param week_start: 週の開始日時（日曜日）
    :param week_end: 週の終了日時（土曜日）
    :return: (タイム文字列, タイム整数値) のタプル、データなしの場合は ("", 9999)
    """
    best_history = None
    best_time = 9999
    for history in self.__histories:
      if history.hasHistory(racecourse) and week_start <= history.getDate() <= week_end:
        time_int = history.getTimeInt()
        if time_int < best_time:
          best_time = time_int
          best_history = history
    
    if best_history:
      return best_history.getTime(), best_time
    return "", 9999
  
  def getTopTimeIntByWeek(self, racecourse, week_start, week_end):
    """指定した週の期間内で最速タイム（整数値）を取得
    
    :param racecourse: RaceCourseオブジェクト
    :param week_start: 週の開始日時（日曜日）
    :param week_end: 週の終了日時（土曜日）
    :return: タイム整数値、データなしの場合は 9999
    """
    best = 9999
    for history in self.__histories:
      if history.hasHistory(racecourse) and week_start <= history.getDate() <= week_end:
        time = history.getTimeInt()
        if time < best:
          best = time
    
    return best

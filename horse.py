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
    return self.__histories[0].getJockey()

  
  def addHistory(self, history):
    self.__histories.append(history)

  def getTopTime(self, racecourse, date = datetime.datetime(2000, 1, 1)):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(racecourse)):
        t = history.getTime()

        #最初の履歴、またはより早い時計を見つけた場合
        if (time == "" or time > t) and t != "" and history.getDate() >= date:
          time = t

    return time
  
  def getTopTimeInt(self, racecourse, date = datetime.datetime(2000, 1, 1)):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(racecourse)):
        t = history.getTime()

        #最初の履歴、またはより早い時計を見つけた場合
        if (time == "" or time > t) and t != "" and history.getDate() >= date:
          time = t
          h = history

    if time != "":
      return h.getTimeInt()

    return 9999

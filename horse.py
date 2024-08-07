from history import History
from racecourse import RaceCourse

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

  def addHistory(self, racecourse, time, date, baba, parts, gate, last3F, jockey):
    self.__histories.append(History(racecourse, time, date, baba, parts, gate, last3F, jockey))

  def getTopTime(self, racecourse):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(racecourse)):
        t = history.getTime()

        #最初の履歴、またはより早い時計を見つけた場合
        if (time == "" or time > t) and t != "":
          time = t

    return time
  
  def getTopTimeInt(self, racecourse):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(racecourse)):
        t = history.getTime()

        #最初の履歴、またはより早い時計を見つけた場合
        if (time == "" or time > t) and t != "":
          time = t
          h = history

    if time != "":
      return h.getTimeInt()

    return 9999

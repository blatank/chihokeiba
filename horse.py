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

  def addHistory(self, racecourse, time):
    self.__histories.append(History(racecourse, time))

  def getTopTime(self, racecourse):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(racecourse)):
        t = history.getTime()

        if (time == "" or time > t) and t != "":
          time = t

    return time

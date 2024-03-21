from history import History

class Horse:
  def __init__(self, name, no):
    self.__name = name
    self.__no = no
    self.__histories = []

  def getName(self):
    return self.__name
  
  def getNo(self):
    return self.__no

  def addHistory(self, course, distance, time):
    self.__histories.append(History(course, distance, time))

  def getTopTime(self, course, distance):
    time = ""
    for history in self.__histories:
      if (history.hasHistory(course, distance)):
        t = history.getTime()

        if time == "" or time > t:
          time = t

    return time

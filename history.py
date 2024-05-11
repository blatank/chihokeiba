from racecourse import RaceCourse

class History:
  def __init__(self, racecourse, time, date=""):
    self.__racecourse = racecourse
    self.__time = time
    self.__date = date

  def getTime(self):
    return self.__time
  
  def getDate(self):
    return self.__date
  
  def hasHistory(self, racecouse):
    if (self.__racecourse == racecouse):
      return True
    else:
      return False
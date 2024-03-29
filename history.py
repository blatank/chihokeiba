from racecourse import RaceCourse

class History:
  def __init__(self, racecourse, time):
    self.__racecourse = racecourse
    self.__time = time

  def getTime(self):
    return self.__time
  
  def hasHistory(self, racecouse):
    if (self.__racecourse == racecouse):
      return True
    else:
      return False
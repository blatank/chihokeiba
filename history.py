from racecourse import RaceCourse

class History:
  def __init__(self, racecourse, time, date, baba, parts, gate, last3F):
    self.__racecourse = racecourse
    self.__time = time
    self.__date = date
    self.__baba = baba
    self.__parts = parts
    self.__gate = gate
    self.__last3F = last3F


  def getTime(self):
    if len(self.__time) > 0:
      return self.__time + " [" +  self.__last3F + "]  (" + self.__date + " " + self.__baba + " " + self.__gate + "/" + self.__parts + ")"
    else:
      return ""
  
  def getDate(self):
    return self.__date
  
  def hasHistory(self, racecouse):
    if (self.__racecourse == racecouse):
      return True
    else:
      return False
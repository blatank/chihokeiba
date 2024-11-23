from racecourse import RaceCourse
import re
import datetime

class History:
  def __init__(self, racecourse, time, date="", baba="", parts="", gate="", last3F="", jockey=""):
    self.__racecourse = racecourse
    self.__time = time
    if date != "":
      d =  re.split(r'\.', date)
      self.__date = datetime.datetime(int("20" + d[0]),int(d[1]),int(d[2]))
    else:
      self.__date = datetime.datetime(1999, 1, 1)
    self.__baba = baba
    self.__parts = parts
    self.__gate = gate
    self.__last3F = last3F
    self.__jockey = jockey
    # self.setTimeInt()
    self.__timeInt = 0

  def getTimeInt(self):
    splited_str = re.split(r':', self.__time)
    m = int(splited_str[0]) * 600
    s = float(splited_str[1]) * 10
    self.__timeInt = int(m + s)
    return self.__timeInt

  def getTimeStr(self):
    return self.__time

  def getTime(self):
    if len(self.__time) > 0:
      return self.__time + " [" +  self.__last3F + "]  (" + self.getDateStr() + " " + self.__baba + " " + self.__gate + "/" + self.__parts + ")"
    else:
      return ""
  
  def getDateStr(self):
    return self.__date.strftime('%Y.%m.%d')

  def getDate(self):
    return self.__date
  
  def getJockey(self):
    return self.__jockey
  
  def hasHistory(self, racecouse):
    if (self.__racecourse == racecouse):
      return True
    else:
      return False
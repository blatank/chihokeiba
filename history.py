class History:
  def __init__(self, course, distance, time):
    self.__course = course
    self.__distance = distance
    self.__time = time

  def getTime(self):
    return self.__time
  
  def hasHistory(self, course, distance):
    if (self.__course == course and self.__distance == distance):
      return True
    else:
      return False
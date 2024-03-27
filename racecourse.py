class RaceCourse:
  def __init__(self, course, distance):
    self.__course = course
    self.__distance = distance

  def getCourse(self):
    return self.__course
  
  def getDistance(self):
    return self.__distance
  
  def equal(self, another):
    return (self.__course == another.getCourse() and self.__distance == another.getDistance())
  
  # 設定された競馬場・距離に近い競馬場・距離を返す
  def esitimateCourse(self):
    eCourses = []

    if self.__course == "佐賀":
      if self.__distance == "右1400":
        eCourses.append(RaceCourse("佐賀", "右1300"))
      elif self.__distance == "右1300":
        eCourses.append(RaceCourse("佐賀", "右1400"))

    return eCourses
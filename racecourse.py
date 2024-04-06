import csv

class RaceCourse:
  def __init__(self, course, distance):
    self.__course = course
    self.__distance = distance

  def getCourse(self):
    return self.__course
  
  def getDistance(self):
    return self.__distance
  
  def __eq__(self, __value):
    return (self.__course == __value.__course and self.__distance == __value.__distance)
  
  # 設定された競馬場・距離に近い競馬場・距離を返す
  def esitimateCourse(self):
    eCourses = []

    # 今のコースのファイルを読み出す
    # 読み出したら1行ずつ読み出す
    with open(self.__course + '_' + self.__distance + '.txt') as f:
      reader = csv.reader(f)
      # 競馬場,距離となっているため、データを取り出す
      for row in reader:
        # 取り出したデータを近い条件として登録
        eCourses.append(RaceCourse(row[0],row[1]))

    return eCourses
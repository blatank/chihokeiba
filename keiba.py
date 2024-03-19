from bs4 import BeautifulSoup

import requests
import re
import sys

class Keiba:
  def __init__(self, url):
    self.__url = url
    self.__courses = []
    self.__distances = []

    self.analyze()
  
  def setcourse(self, course):
    self.__courses.append(course)

  def setDistance(self, distance):
    self.__distances.append(distance)

  def analyze(self):

    res = requests.get(self.__url)
    soup = BeautifulSoup(res.text, "html.parser")

    self.__names = soup.find_all("a", class_="horseName")
    self.__races = soup.find_all("div", class_="raceInfo")
    self.__card = soup.find_all("section", class_="cardTable")
    self.__tokei = soup.select("tbody > tr")#名前変更予定

    self.__bamei = []
    self.__keibajou = []
    self.__kyori = []
    self.__baba = []
    self.__time = []

    #馬名取り出し処理
    for horse in self.__names:
      self.__bamei.append(horse.get_text())#OK
      self.__time.append([])#OK
      self.__keibajou.append([])#OK
      self.__kyori.append([])#OK
      self.__baba.append([])

    #走破時計取り出し処理
    for i in range(len(self.__names)):
      t2 = re.split(r'</td>',str(self.__tokei[i * 5 + 5]))
      for j in range(5):
        tokei2 = re.findall(r'\d:\d\d\.\d', t2[2+j])
        if len(tokei2) > 0:
          self.__time[i].append(tokei2[0])
        else:
          self.__time[i].append("")

    #競馬場取り出し処理
    for i in range(len(self.__names)):
      for j in range(5):
        k2 = re.split(r'<br/>', str(self.__races[i * 5 +j]))
        if len(k2) > 1:
          keibajou2 = re.findall(r'\w+　\w+　\w+', k2[1])
          if len(keibajou2) > 0:
            keibajou3 = re.split(r'　', keibajou2[0])
            place = keibajou3[0]
            dis = keibajou3[1]
          else:
            place = ""
            dis = ""
        else:
            place = ""
            dis = ""

        self.__keibajou[i].append(place)
        self.__kyori[i].append(dis)

  # 時計順で出力
  def outputHourseTime(self):
    # 設定した条件の分だけ検索して出力
    for i in range(len(self.__courses)):
      for j in range(len(self.__distances)):
        print("-----------------------------")
        print(self.__courses[i] + " " + self.__distances[j])

        self.print_sorted_data(self.__courses[i], self.__distances[j])
  
  def print_sorted_data(self, course, distance):
    top_time = []

    # 該当データ検索
    for i in range(len(self.__names)):
      moti = ""

      # 過去5走から検索する
      for j in range(5):
        if self.__keibajou[i][j] == course and self.__kyori[i][j] == distance:
          if moti == "" or moti > self.__time[i][j]:
            # 除外・取消を除く
            if self.__time[i][j] != "":
              # 持ち時計-馬番の形で一時保存
              moti = self.__time[i][j] + "-" + str(i+1)
      
      # その馬の最速タイムとして登録
      top_time.append(moti)
    
    # ソートして出力する
    top_time.sort()
    for s in top_time:
      if s != "":
        # 持ちタイムと馬番を分離して、馬番を前に出して出力
        s2 = re.split(r'-', s)
        print(s2[1] + "番" + self.__bamei[int(s2[1]) - 1] +"：" + s2[0])

# test(あとで別ファイルにする)
race = Keiba(sys.argv[1])
race.setcourse("高知")
race.setDistance("右1400")
race.setDistance("右1300")
race.setDistance("右1600")
race.outputHourseTime()

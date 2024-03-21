from bs4 import BeautifulSoup

import requests
import re
import sys

from horse import Horse
from history import History

class Keiba:
  def __init__(self, url):
    self.__url = url
    self.__courses = []
    self.__distances = []
    self.__horses = []

    self.analyze()
  
  # データ抽出に使いたい競馬場をセットする
  def setcourse(self, course):
    self.__courses.append(course)

  # データ抽出に使いたい距離を定義する
  # 例)右1400
  def setDistance(self, distance):
    self.__distances.append(distance)

  # URL解析
  def analyze(self):

    res = requests.get(self.__url)
    soup = BeautifulSoup(res.text, "html.parser")

    self.__names = soup.find_all("a", class_="horseName")
    self.__races = soup.find_all("div", class_="raceInfo")
    self.__card = soup.find_all("section", class_="cardTable")
    self.__tokei = soup.select("tbody > tr")#名前変更予定

    names = []
    time = []
    # self.__keibajou = []
    # self.__kyori = []
    # self.__baba = []
    # self.__time = []

    #馬名取り出し処理
    no = 1
    for horse in self.__names:
      self.__horses.append(Horse(horse.get_text(), no))
      no += 1
      time.append([])
      # self.__time.append([])#OK
      # self.__keibajou.append([])#OK
      # self.__kyori.append([])#OK
      # self.__baba.append([])

    #走破時計取り出し処理
    for i in range(len(self.__horses)):
      # TODO:何を目的としているかコメントに残す
      t2 = re.split(r'</td>',str(self.__tokei[i * 5 + 5]))

      # 馬柱に載っているのは過去5走
      # そのデータを分解し、Horseにセットする
      for j in range(5):
        tokei2 = re.findall(r'\d:\d\d\.\d', t2[2+j])

        # データが空(出走数が少ない場合など)ではない？
        if len(tokei2) > 0:
          time[i].append(tokei2[0])
        else:
          time[i].append("")

    #競馬場取り出し処理
    for i in range(len(self.__horses)):
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

        # self.__keibajou[i].append(place)
        # self.__kyori[i].append(dis)
        self.__horses[i].addHistory(place, dis, time[i][j])

  # 時計順で出力
  def outputHourseTime(self):
    # 設定した条件の分だけ検索して出力
    for i in range(len(self.__courses)):
      for j in range(len(self.__distances)):
        print("-----------------------------")
        print(self.__courses[i] + " " + self.__distances[j])

        self.print_sorted_data(self.__courses[i], self.__distances[j])
  
  # 条件内をソートして出力
  def print_sorted_data(self, course, distance):
    top_time = []

    # 該当データ検索
    for horse in self.__horses:
      time = horse.getTopTime(course, distance)
      if time != "":
        top_time.append(time + "-" + str(horse.getNo()))
    
    # ソートして出力する
    top_time.sort()
    for time_str in top_time:
      if time_str != "":
        # 持ちタイムと馬番を分離して、馬番を前に出して出力
        # splited_str[0]：タイム
        # splited_str[1]：馬番
        splited_str = re.split(r'-', time_str)
        h = self.__horses[int(splited_str[1]) - 1]
        print(splited_str[1] + "番" + h.getName() +"：" + splited_str[0])


  

# test(あとで別ファイルにする)
race = Keiba(sys.argv[1])
race.setcourse("高知")
race.setDistance("右1400")
race.setDistance("右1300")
race.setDistance("右1600")
race.outputHourseTime()

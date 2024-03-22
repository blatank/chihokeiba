from bs4 import BeautifulSoup

import requests
import re

from horse import Horse
from history import History

class Race:
  def __init__(self, url):
    self.__url = url
    self.__courses = []
    self.__distances = []
    self.__horses = []
  
  # データ抽出に使いたい競馬場をセットする
  def setCourse(self, course):
    self.__courses.append(course)

  # データ抽出に使いたい距離を定義する
  # 例)右1400
  def setDistance(self, distance):
    self.__distances.append(distance)

  # URL解析
  def analyzeUrl(self):

    res = requests.get(self.__url)
    soup = BeautifulSoup(res.text, "html.parser")

    names = soup.find_all("a", class_="horseName")
    if len(names) == 0:
      return False

    races = soup.find_all("div", class_="raceInfo")
    times = soup.select("tbody > tr")

    time = []

    #馬名取り出し処理
    no = 1
    for horse in names:
      self.__horses.append(Horse(horse.get_text(), no))
      no += 1
      time.append([])

    #走破時計取り出し処理
    for i in range(len(self.__horses)):
      # TODO:何を目的としているかコメントに残す
      t2 = re.split(r'</td>',str(times[i * 5 + 5]))

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
        k2 = re.split(r'<br/>', str(races[i * 5 +j]))
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
    
    # ここまで来れば正常終了
    return True

  # 時計順で出力
  def outputHourseTime(self):
    # 設定した条件の分だけ検索して出力
    for i in range(len(self.__courses)):
      for j in range(len(self.__distances)):
        print("-----------------------------")
        print(self.__courses[i] + " " + self.__distances[j])

        self.printSortedData(self.__courses[i], self.__distances[j])
  
  # 条件内をソートして出力
  def printSortedData(self, course, distance):
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
from bs4 import BeautifulSoup

import requests
import re
from urllib.parse import urlparse

from horse import Horse
from history import History
from racecourse import RaceCourse

class Race:
  def __init__(self, url):
    self.__url = url
    self.__courses = []
    self.__distances = []
    self.__horses = []
    self.__raceCourse = ""
    self.__raceDistance = ""
    self.__reaceNo = ""
  
  # データ抽出に使いたい競馬場をセットする
  def setCourse(self, course):
    self.__courses.append(course)

  # データ抽出に使いたい距離を定義する
  # 例)右1400
  def setDistance(self, distance):
    self.__distances.append(distance)

  def getRaceDistance(self):
    return self.__raceDistance
  
  def getRaceCourse(self):
    return self.__raceCourse
  
  def getRaceNo(self):
    return self.__reaceNo

  # URL解析
  def analyzeUrl(self):

    res = requests.get(self.__url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 馬名の抽出
    names = soup.find_all("a", class_="horseName")
    
    # 抽出がうまく行かなかった場合はURLが間違っていると思われる
    if len(names) == 0:
      return False

    # レース施行条件の抽出
    # ul.dataAreaのliを抽出し、その中を全角スペース→ｍで分割すると距離と回りが取り出せる
    dataArea = soup.select("ul.dataArea > li")
    # 全角スペースで分割した2番目が取り出したいもの
    # 1番目はダート。盛岡の芝が解析したくなったら考える
    zenkaku_splitted = re.split(r'　',str(dataArea[0]))

    # race_info[0]：距離
    # race_info[1]：（右）or（左）
    race_info = re.split(r'ｍ',zenkaku_splitted[1])
    if race_info[1] == "（右）":
      self.__raceDistance = "右" + race_info[0]
    else:
      self.__raceDistance = "左" + race_info[0]

    # URL自体からレース情報の解析
    url = urlparse(self.__url)
    query = re.split(r'&',url.query)
    for q in query:
      jouhou = re.split(r'=',q)

      # k_babaCode=32は佐賀
      # TODO：調査用のクラスを作る
      if jouhou[0] == "k_babaCode" and jouhou[1] == "32":
        self.__raceCourse = "佐賀"
      
      # k_raceNoはレースNo.
      if jouhou[0] == "k_raceNo":
        self.__reaceNo = jouhou[1]
    
    # TODO：このレースの施行条件取得する

    # 過去のレース情報取得(競馬場・距離用)
    races = soup.find_all("div", class_="raceInfo")

    # 過去のレース情報取得(時計用)
    history_table = soup.select("tbody > tr")

    # 走破時計保存用一時配列初期化(二次元配列で使用)
    time = []

    #馬名取り出し処理
    no = 1
    for horse in names:
      # 馬名・馬番取得とともにHorseインスタンス追加
      self.__horses.append(Horse(horse.get_text(), no))
      no += 1
      time.append([])

    #走破時計取り出し処理
    for i in range(len(self.__horses)):
      # TODO:何を目的としているかコメントに残す
      t2 = re.split(r'</td>',str(history_table[i * 5 + 5]))

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
        self.__horses[i].addHistory(RaceCourse(place, dis), time[i][j])
    
    # ここまで来れば正常終了
    return True

  # 時計順で出力
  def outputHourseTime(self):
    # 今はダート決め打ち
    print(self.getRaceCourse() + self.getRaceNo() + "R" + " ダート" + self.getRaceDistance() + "m")

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
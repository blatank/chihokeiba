from bs4 import BeautifulSoup

import requests
import re
import os
import csv
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
    self.__jockeys = []
    self.__reaceNo = ""
  
  # データ抽出に使いたい競馬場をセットする
  def setCourse(self, course):
    self.__courses.append(course)

  # データ抽出に使いたい距離を定義する
  # 例)右1400
  def setDistance(self, distance):
    self.__distances.append(distance)
  
  def getRaceCourse(self):
    return self.__raceCourse
  
  def getRaceNo(self):
    return self.__reaceNo
  
  # このレースの条件での時計を出力
  def analyzeThisCondition(self):
    return self.analyzeCondtion(self.__raceCourse)

  # このレースに似た条件での時計を出力
  def analyzeNearlyCondition(self):
    results = ""

    # 該当データ検索
    nearlyRaces = self.__raceCourse.esitimateCourse()
    for race in nearlyRaces:
      results += self.analyzeCondtion(race)
    
    return results
  
  # 条件に近いデータの補正値を出力
  def getAjustedTime(thisCourse, nearlyCourse):
    ajustedTime = 0

    # 今のコースのファイルを読み出す
    datafile = "data/" + thisCourse.getCourse() + "_" + thisCourse.getDistance() + ".txt"
    if os.path.isfile(datafile):
      with open(datafile, encoding='UTF-8') as f:
        reader = csv.reader(f)
  
        # 読み出したら1行ずつ読み出す
        for row in reader:
          # 競馬場,距離となっているため、データを取り出す
          # 取り出したデータを近い条件として登録
          if row[0] == nearlyCourse.getCourse() and\
             row[1] == nearlyCourse.getDistance():
            ajustedTime = int(row[2])
            break

    return ajustedTime
  
  def analyzeEsitimateTime(self):
    top_time = []

    #今の条件の時計を拾う
    times = self.analyzeTime(self.__raceCourse)
    top_time.append(times)

    #似た条件の時計を拾う
    nearlyRaces = self.__raceCourse.esitimateCourse()
    for race in nearlyRaces:
      nearlyTimes = self.analyzeTime(race)
      top_time.append(nearlyTimes)
    
    #似た条件の時計を補正する
    i = 0
    nodata = ""
    tops = []

    for horse in self.__horses:
      k = 1
      # 補正実施
      for nearlyRace in nearlyRaces:
        if(top_time[k][i] != 9999):
          top_time[k][i] += Race.getAjustedTime(self.__raceCourse, nearlyRace)
        k += 1

      # 補正した分も含めて最速タイムを算出する
      t = 9999
      for j in range(len(nearlyRaces)+1):
        if top_time[j][i] < t:
          t = top_time[j][i]

      if t != 9999:
        tops.append(Race.convTime(t) + "-" + str(horse.getNo()))
      else:
        nodata += " " + str(horse.getNo()) + "番"
      i += 1

    tops.sort()

    result = ""
    i = 0
    j = 0
    for time_str in tops:
      # ソート用の文字列を出力用の文字列に変換
      r = self._formattedTimeStr(time_str)

      time_str = re.sub(r'-\d+', '', time_str)
      r = re.sub(r'\n', '', r)
      
      splited_str = re.split(r':', time_str)
      m = int(splited_str[0]) * 600
      s = float(splited_str[1]) * 10
      t = int(m + s)

      #１回目の時間を保存
      if i == 0:
        fast = t
      #最速タイムとの差を確認
      diff = t - fast

      if diff > 10 and j == 0:
        result += "*******************************\n"
        j = 1
      
      result += r + " (+" + Race.convTime(diff) + ")\n"
      i += 1
    
    if len(nodata) > 0:
      result += "\nデータなし:"  + nodata
    
    return result
  
  def analyzeTime(self, racecourse):
    top_time = []
    nodata = ""
    # 該当データ検索
    for horse in self.__horses:
      time = horse.getTopTimeInt(racecourse)
      if time != 0:
        top_time.append(time)
      else:
        top_time.append(0)
    return top_time
  
  def convTime(time):
    m = int(time / 600)
    s = int((time - (m * 600)) / 10)
    if s < 10:
      str_s = "0" + str(s)
    else:
      str_s = str(s)
    ms = time % 10

    convertedTime = str(m) + ":" + str_s + "." + str(ms)

    return convertedTime
  
  # 条件に合う時計をソートして文字列にする
  def analyzeCondtion(self, racecourse):
    top_time = []
    nodata = ""
    # 該当データ検索
    for horse in self.__horses:
      time = horse.getTopTime(racecourse)
      if time != "":
        top_time.append(time + "-" + str(horse.getNo()))
      else:
        nodata += " " + str(horse.getNo()) + "番"
    
    # ソートして出力する
    top_time.sort()
    result = ""
    for time_str in top_time:
      # ソート用の文字列を出力用の文字列に変換
      result += self._formattedTimeStr(time_str)

    # データあるならタイトル付加する
    if len(result) > 0:
      if len(nodata) > 0:
        result += "\nデータなし:"  + nodata
      prefix = racecourse.getCourse() + " " + racecourse.getDistance() + "\n"
      prefix += "----------------------------\n"
      result = prefix + result + "\n"
    
    return result

  # 持ちタイムと馬番の文字列から結果としてふさわしい文字列にする
  def _formattedTimeStr(self, time_str):
    result = ""

    if time_str != "":
      # 持ちタイムと馬番を分離して、馬番を前に出して出力
      # splited_str[0]：タイム
      # splited_str[1]：馬番
      splited_str = re.split(r'-', time_str)
      no = splited_str[1]
      index = int(no) - 1
      if len(no) == 1:
        no = " " + no
      
      h = self.__horses[int(splited_str[1]) - 1]
      name = h.getName()
      if len(name) < 9:
        n = 9 - len(name)
        for i in range(n):
          name = name + "  "
      
      jk = self.__jockeys[index]
      if jk == h.getPreviousJockey() :
        change = " "
      else :
        change = "*"

      result = no + "番" + name + "(" + jk + change + ") " + splited_str[0] + "\n"
    
    return result

  # URL解析
  def analyzeUrl(self):

    res = requests.get(self.__url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 馬名の抽出
    names = soup.find_all("a", class_="horseName")
    
    # 抽出がうまく行かなかった場合はURLが間違っていると思われる
    if len(names) == 0:
      return False
    
    # 騎手名の抽出
    jockeynames = soup.find_all("a", class_="jockeyName")
    
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
      distance = "右" + race_info[0]
    else:
      distance = "左" + race_info[0]

    # URL自体からレース情報の解析
    url = urlparse(self.__url)
    query = re.split(r'&',url.query)
    course = ""
    for q in query:
      jouhou = re.split(r'=',q)

      # k_babaCode=32は佐賀
      # TODO：調査用のクラスを作る
      # TODO：racecousedictionaryに置き換える
      if jouhou[0] == "k_babaCode":
        if jouhou[1] == "32":
          course = "佐賀"
        elif jouhou[1] == "31":
          course = "高知"
        elif jouhou[1] == "27":
          course = "園田"
        else:
          print("該当する競馬場が有りません！")
      
      # k_raceNoはレースNo.
      if jouhou[0] == "k_raceNo":
        self.__reaceNo = jouhou[1]
    
    # エラーチェックとこのレース情報登録
    if distance != "" and course != "":
      self.__raceCourse = RaceCourse(course, distance)
    else:
      return False

    # 過去のレース情報取得(競馬場・距離用)
    races = soup.find_all("div", class_="raceInfo")

    # 過去のレース情報取得(時計用)
    history_table = soup.select("tbody > tr")

    # 走破時計保存用一時配列初期化(二次元配列で使用)
    time = []
    last3F = []
    jockeys = []

    #馬名取り出し処理
    no = 1
    for horse in names:
      # 馬名・馬番取得とともにHorseインスタンス追加
      self.__horses.append(Horse(horse.get_text(), no))
      no += 1
      time.append([])
      last3F.append([])
      jockeys.append([])

    #騎手名取り出し処理
    # no = 1
    for jockey in jockeynames:
      st = re.split(r'\n',jockey.get_text())
      st2 = re.split(r'（',st[1])
      self.__jockeys.append(st2[0])

    #走破時計取り出し処理
    for i in range(len(self.__horses)):
      # TODO:何を目的としているかコメントに残す
      t2 = re.split(r'</td>',str(history_table[i * 5 + 5]))
      t4 = re.split(r'</td>',str(history_table[i * 5 + 4]))
      
      # 馬柱に載っているのは過去5走
      # そのデータを分解し、Horseにセットする
      for j in range(5):
        tokei2 = re.findall(r'\d:\d\d\.\d', t2[2+j])

        # 騎手名とりだし
        st4 = re.split(r'　',t4[3+j])
        if len(st4) >= 3: # データあり？
          st42 = re.split(r' ',st4[2])
          l = len(st42[0])

          # ☆とかあれば取り除く
          if l >= 3 :
            # TODO:武豊など、3文字以内の騎手がいる場合バグ有
            jk = st42[0][l-3:l]
          else:
            jk = st42[0]
          jockeys[i].append(jk)
        else:
          jockeys[i].append("")

        # データが空(出走数が少ない場合など)ではない？
        if len(tokei2) > 0:
          time[i].append(tokei2[0])
        else:
          time[i].append("")

        t3 = re.split(r'　', t2[2+j])
        if len(t3) >= 3:
          last3F[i].append(t3[2].replace("\n", ""))
        else:
          last3F[i].append("")

    #競馬場取り出し処理
    for i in range(len(self.__horses)):
      for j in range(5):
        k2 = re.split(r'<br/>', str(races[i * 5 +j]))
        if len(k2) > 1:
          hiduke = re.findall(r'[\w|\.]+　\w+　\w+', k2[0])

          if len(hiduke) > 0:
            hiduke2 = re.split(r'　', hiduke[0])
            date = hiduke2[0]
            baba = hiduke2[1]
            parts = hiduke2[2]
          else:
            date = ""
            baba = ""
            parts = ""
          
          keibajou2 = re.findall(r'\w+　\w+　\w+', k2[1])
          if len(keibajou2) > 0:
            keibajou3 = re.split(r'　', keibajou2[0])
            place = keibajou3[0]
            dis = keibajou3[1]
            gate = keibajou3[2]
            
          else:
            place = ""
            dis = ""
            gate = ""
        else:
            place = ""
            dis = ""
            date = ""
            baba = ""
            parts = ""
            gate = ""

        # self.__keibajou[i].append(place)
        # self.__kyori[i].append(dis)
        self.__horses[i].addHistory(RaceCourse(place, dis), time[i][j], date, baba, parts, gate, last3F[i][j], jockeys[i][j])
    
    # ここまで来れば正常終了
    return True

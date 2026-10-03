from bs4 import BeautifulSoup

import requests
import re
import os
import csv
import datetime
from urllib.parse import urlparse

from horse import Horse
from history import History
from racecourse import RaceCourse
from racecoursedictionary import RaceCourseDictionary


class Race:
  NO_TIME = 9999

  def __init__(self, url, period = False, start = datetime.datetime(2000, 1, 1)):
    self.__url = url
    self.__courses = []
    self.__distances = []
    self.__horses = []
    self.__jockeys = []
    self.__reaceNo = ""
    self.__raceCourse = None
    # self.__date = self.getDate(url)
    self.__periodflag = period

    # 指定した日付までをレースを検索対象にする
    if self.__periodflag == True:
      self.__c_date = start
      # if self.__date.month <= 2 :
      #   self.__c_date = datetime.datetime(self.__date.year - 1,self.__date.month + 12 - 2,1)
      # else:
      #   self.__c_date = datetime.datetime(self.__date.year,self.__date.month - 2,1)
    else:
      self.__c_date = datetime.datetime(2000, 1, 1)


  
  # def getDate(self, url):
  #   u1 = re.split(r'&', url)
  #   u2 = re.split(r'k_raceDate=', u1[0])
  #   u3 = re.split(r'%2f', u2[1])
  #   return datetime.datetime(int(u3[0]),int(u3[1]),int(u3[2]))

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
  
  def analyzeByWeek(self, num_weeks=12, start_date=None, end_date=None):
    """週ごとに分析結果を出力
    
    :param num_weeks: start_date が未指定のときのみ使う週数
    :param start_date: 分析開始日（含む）
    :param end_date: 分析終了日（含む、未指定時は現在日）
    :return: 週ごとの分析結果を含む文字列
    """
    result = ""

    # 終了日は現在日またはレース日を使う
    if end_date is None:
      end_date = datetime.datetime.now()
    elif isinstance(end_date, datetime.date) and not isinstance(end_date, datetime.datetime):
      end_date = datetime.datetime.combine(end_date, datetime.time.min)

    if start_date is None:
      start_date = end_date - datetime.timedelta(weeks=num_weeks)
    elif isinstance(start_date, datetime.date) and not isinstance(start_date, datetime.datetime):
      start_date = datetime.datetime.combine(start_date, datetime.time.min)

    if start_date > end_date:
      start_date, end_date = end_date, start_date

    # 開始日から終了日までの週を列挙
    weeks_data = []
    reference_monday = end_date - datetime.timedelta(days=end_date.weekday())
    week_num = 0
    while True:
      week_start = reference_monday - datetime.timedelta(weeks=week_num)
      week_end = week_start + datetime.timedelta(days=6)
      if week_end < start_date:
        break
      if week_start <= end_date:
        weeks_data.append((week_num, week_start, week_end))
      week_num += 1

    # 古い順に処理
    weeks_data.reverse()

    # 各週の分析を実施（補正後のタイムで比較）
    for week_num, week_start, week_end in weeks_data:
      result += f"\n{'='*50}\n"
      result += f"週{week_num + 1}の分析 ({week_start.strftime('%Y.%m.%d')} ～ {week_end.strftime('%Y.%m.%d')})\n"
      result += f"{'='*50}\n"

      # 各コース（本コース + 類似コース）ごとの週内最速タイム（整数値）を収集
      top_time_matrix = []  # [コース索引][馬索引] = time_int

      # 本コースの週内最速タイム
      this_week_times = []
      for horse in self.__horses:
        this_week_times.append(horse.getTopTimeIntByWeek(self.__raceCourse, week_start, week_end))
      top_time_matrix.append(this_week_times)

      # 類似コースの週内最速タイム
      nearlyRaces = self.__raceCourse.esitimateCourse()
      for nr in nearlyRaces:
        times_nearly = []
        for horse in self.__horses:
          times_nearly.append(horse.getTopTimeIntByWeek(nr, week_start, week_end))
        top_time_matrix.append(times_nearly)

      # 馬ごとに補正を適用して最速タイムを選定
      tops = []
      nodata = ""
      for i, horse in enumerate(self.__horses):
        # 類似コースに対して補正を適用
        for k in range(1, len(top_time_matrix)):
          if top_time_matrix[k][i] != Race.NO_TIME:
            adj = Race.getAjustedTime(self.__raceCourse, nearlyRaces[k-1])
            top_time_matrix[k][i] += adj

        # 最小値を探す
        t = Race.NO_TIME
        for j in range(len(top_time_matrix)):
          if top_time_matrix[j][i] < t:
            t = top_time_matrix[j][i]

        if t != Race.NO_TIME:
          tops.append(Race.convTime(t) + "-" + str(horse.getNo()))
        else:
          nodata += " " + str(horse.getNo()) + "番"

      tops.sort()

      # 出力整形（最速との差分表示など）
      i = 0
      j = 0
      if len(tops) == 0:
        result += "この週のデータがありません\n"
      else:
        fast = None
        for time_str in tops:
          r = self._formattedTimeStr(time_str)

          time_only = re.sub(r'-\d+', '', time_str)
          r = re.sub(r'\n', '', r)

          splited_str = re.split(r':', time_only)
          m = int(splited_str[0]) * 600
          s = float(splited_str[1]) * 10
          t_int = int(m + s)

          if i == 0:
            fast = t_int
          diff = t_int - fast

          if diff > 10 and j == 0:
            result += "*******************************\n"
            j = 1

          result += r + " (+" + Race.convTime(diff) + ")\n"
          i += 1

      if len(nodata) > 0:
        result += "\nデータなし:" + nodata + "\n"

    return result
  
  # 条件に近いデータの補正値を出力
  @staticmethod
  def getAdjustedTime(thisCourse, nearlyCourse):
    ajustedTime = 0

    # 今のコースのファイルを読み出す
    datafile = os.path.join("data", f"{thisCourse.getCourse()}_{thisCourse.getDistance()}.txt")
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

  getAjustedTime = getAdjustedTime
  
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

    # 該当データ検索
    for horse in self.__horses:
      top_time.append(horse.getTopTimeInt(racecourse, self.__c_date))
    return top_time
  
  @staticmethod
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
      time = horse.getTopTime(racecourse, self.__c_date)
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

    if(zenkaku_splitted[0] == "<li>芝"):
      distance = "芝" + distance

    # URL自体からレース情報の解析
    url = urlparse(self.__url)
    query = re.split(r'&',url.query)
    course = ""
    for q in query:
      jouhou = re.split(r'=',q)

      # k_babaCode=32は佐賀
      if jouhou[0] == "k_babaCode":
        dictionary = RaceCourseDictionary("racecoursedictionary.json")
        course = dictionary.inquireRaceCourseName(int(jouhou[1]))
        if course == "":
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
    # # ファイルに文字列を書き込む
    # with open("output.txt", "w", encoding="utf-8") as f:
    #   for g in history_table:
    #     f.write(str(g))


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
      st2 = re.split(r'（',st[0])
      self.__jockeys.append(st2[0])

    #走破時計取り出し処理
    for i in range(len(self.__horses)):

      # TODO:何を目的としているかコメントに残す
      t2 = re.split(r'</td>',str(history_table[i * 11 + 11]))
      t4 = re.split(r'</td>',str(history_table[i * 11 + 10]))

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
        h1 = History(RaceCourse(place, dis), time[i][j], date, baba, parts, gate, last3F[i][j], jockeys[i][j])
        self.__horses[i].addHistory(h1)
    
    # ここまで来れば正常終了
    return True

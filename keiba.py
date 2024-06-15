from race import Race
from racecoursedictionary import RaceCourseDictionary
import sys
import datetime
import urllib.parse
dic = RaceCourseDictionary("racecoursedictionary.json")

#URLを作成
# url = sys.argv[1]
url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?"
if len(sys.argv) > 3:
  url = url + "k_raceDate=" + urllib.parse.quote(sys.argv[3]) + "&"
else:
  dt_now = datetime.datetime.now()
  url = url + "k_raceDate=" + urllib.parse.quote(dt_now.strftime('%Y/%m/%d')) + "&"

url = url + "k_raceNo=" + sys.argv[2] + "&"
url = url + "k_babaCode=" + dic.inquireBabaCode(sys.argv[1])

# argv[1]:URL
race = Race(url)

if race.analyzeUrl():
  # レースと同じ条件の時計を出力
  thisCodData = race.analyzeThisCondition()
  if len(thisCodData) > 0:
    print(thisCodData)
  else:
    print("このレースの条件のデータが1頭分もありません")

  # レースに近い条件の時計を出力
  nearlyData = race.analyzeNearlyCondition()
  if len(nearlyData) > 0:
    print(nearlyData)
  else:
    print("近い条件のデータがありません")

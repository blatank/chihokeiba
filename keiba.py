from race import Race
from racecoursedictionary import RaceCourseDictionary
import sys
import datetime
import urllib.parse
import argparse

dic = RaceCourseDictionary("racecoursedictionary.json")

dt_now = datetime.datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument("--place", help="競馬場")
parser.add_argument("--no", help="レース番号")
parser.add_argument("--date", help="レース日(yyyy/mm/dd)", default=dt_now.strftime('%Y/%m/%d'))
args = parser.parse_args()

#URLを作成
# url = sys.argv[1]
url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?"
url = url + "k_raceDate=" + urllib.parse.quote(args.date) + "&"
url = url + "k_raceNo=" + args.no + "&"
url = url + "k_babaCode=" + dic.inquireBabaCode(args.place)

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

from race import Race
from racecoursedictionary import RaceCourseDictionary
from url import Url
from analyze import Analyze
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

url = Url.getUrl(args.date, args.no, args.place)
print(Analyze.getResult(url))

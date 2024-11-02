import urllib.parse
from racecoursedictionary import RaceCourseDictionary

class Url:
  @classmethod
  def getUrl(cls, date, no, place):
    dic = RaceCourseDictionary("racecoursedictionary.json")
    #URLを作成
    # url = sys.argv[1]
    url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?"
    url = url + "k_raceDate=" + urllib.parse.quote(date) + "&"
    url = url + "k_raceNo=" + no + "&"
    url = url + "k_babaCode=" + dic.inquireBabaCode(place)
  
    return url

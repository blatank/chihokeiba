from race import Race
import datetime

class Analyze:
  @classmethod
  def getResult(cls, url, period = False, start = datetime.datetime(2000, 1, 1)):
    result = ""
    race = Race(url, period, start)

    if race.analyzeUrl():
      # レースと同じ条件の時計を出力
      thisCodData = race.analyzeThisCondition()
      if len(thisCodData) > 0:
        result += thisCodData
      else:
        result += "このレースの条件のデータが1頭分もありません"
      result += "\n"

      # レースに近い条件の時計を出力
      nearlyData = race.analyzeNearlyCondition()
      if len(nearlyData) > 0:
        result += nearlyData
      else:
        result += "近い条件のデータがありません"
      result += "\n"
      
      timeData = race.analyzeEsitimateTime()
      if len(timeData) > 0:
        result += "補正データ出力\n----------------------------\n"
        result += timeData
      else:
        result += "error"

    return result

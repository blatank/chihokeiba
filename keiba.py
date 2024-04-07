from race import Race  
import sys

# argv[1]:URL
race = Race(sys.argv[1])

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

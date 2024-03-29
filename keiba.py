from race import Race  
import sys

# argv[1]:URL
race = Race(sys.argv[1])

if race.analyzeUrl():
  # レースと同じ条件の時計を出力
  print(race.analyzeThisCondition())

  # レースに近い条件の時計を出力
  print(race.analyzeNearlyCondition())

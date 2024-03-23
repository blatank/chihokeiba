from race import Race  
import sys

# argv[1]:URL
race = Race(sys.argv[1])

if race.analyzeUrl():
  # 検索したい条件を設定
  race.setCourse(race.getRaceCourse())
  race.setDistance(race.getRaceDistance())
  race.setDistance("右1400")

  # 検索条件の結果出力
  race.outputHourseTime()

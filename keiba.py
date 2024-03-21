from race import Race  
import sys

# argv[1]:URL
race = Race(sys.argv[1])
race.analyze()

# 検索したい条件を設定
race.setcourse("高知")
race.setDistance("右1400")
race.setDistance("右1300")
race.setDistance("右1600")

# 検索条件の結果出力
race.outputHourseTime()

from bs4 import BeautifulSoup

import requests
import re
url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f02%2f03&k_raceNo=1&k_babaCode=32"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

names = soup.find_all("a", class_="horseName")
races = soup.find_all("div", class_="raceInfo")
card = soup.find_all("section", class_="cardTable")
tokei = soup.select("tbody > tr")#名前変更予定


bamei = []
keibajou = []
kyori = []
baba = []
time = []

#馬名取り出し処理
for horse in names:
  bamei.append(horse.get_text())#OK
  time.append([])#OK
  keibajou.append([])#OK
  kyori.append([])#OK
  baba.append([])

#走破時計取り出し処理
for i in range(len(names)):
  t2 = re.split(r'</td>',str(tokei[i * 5 + 5]))
  for j in range(5):
    tokei2 = re.findall(r'\d:\d\d\.\d', t2[2+j])
    if len(tokei2) > 0:
      time[i].append(tokei2[0])
    else:
      time[i].append("")

#競馬場取り出し処理
for i in range(len(names)):
  for j in range(5):
    k2 = re.split(r'<br/>', str(races[i * 5 +j]))
    if len(k2) > 1:
      keibajou2 = re.findall(r'\w+　\w+　\w+', k2[1])
      if len(keibajou2) > 0:
        keibajou3 = re.split(r'　', keibajou2[0])
        place = keibajou3[0]
        dis = keibajou3[1]
      else:
        place = ""
        dis = ""
    else:
        place = ""
        dis = ""

    keibajou[i].append(place)
    kyori[i].append(dis)

print(kyori)
  

  # for j in range(5):
  #   tokei2 = re.findall(r'\d:\d\d\.\d', t2[2+j])
  #   if len(tokei2) > 0:
  #     time[i].append(tokei2[0])
  #   else:
  #     time[i].append("")

# a = 0
# for t in tokei:
#   time[int(a / 5)].append(t.replace('　', ''))
#   a = a + 1

# b = 0
# for race in races:
#   # t = race.get_text()
#   r = re.split(r'<br\/*>',str(race))
#   racename = re.split(r'　',r[1])
#   ba = re.split(r'　',r[0]) 
#   if len(racename) > 1:
#     keibajou[int(b / 5)].append(racename[0])
#     kyori[int(b / 5)].append(racename[1])
#     baba[int(b / 5)].append(ba[1])
#   b = b + 1

# print(bamei)
# print(keibajou)
# print(kyori)
# print(baba)
# print(time)
# print(len(races))
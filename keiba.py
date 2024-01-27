from bs4 import BeautifulSoup

import requests
import re
url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate=2024%2f01%2f27&k_raceNo=10&k_babaCode=32"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

names = soup.find_all("a", class_="horseName")
races = soup.find_all("div", class_="raceInfo")
card = soup.find_all("section", class_="cardTable")
tokei = soup.select("tbody > tr")
# races = soup.find_all("div", class_="cardTable raceInfo")

# t1 = re.sub(r'\n','',str(tokei[5]))
t2 = re.split(r'</td>',str(tokei[5]))
tokei2 = re.findall(r'\d:\d\d\.\d', t2[2])
print(tokei2)
#時計の取り出し方法検討中

bamei = []
keibajou = []
kyori = []
baba = []
time = []

for horse in names:
  # print(horse.get_text())
  bamei.append(horse.get_text())
  time.append([])
  keibajou.append([])
  kyori.append([])
  baba.append([])

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
import requests
from bs4 import BeautifulSoup

def get_first_place_time(race_date: str, race_no: int, baba_code: int):
    """
    指定された競馬レースの1着馬のタイムを取得する関数

    :param race_date: レース日付 (例: '2025/04/19')
    :param race_no: レース番号 (例: 3)
    :param baba_code: 競馬場コード (例: 32)
    :return: (馬名, タイム) のタプル、失敗時は None
    """
    base_url = "https://www.keiba.go.jp/KeibaWeb/TodayRaceInfo/RaceMarkTable"
    params = {
        "k_raceDate": race_date,
        "k_raceNo": str(race_no),
        "k_babaCode": str(baba_code)
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    race_results = soup.find_all('tr', class_='raceResult')

    for row in race_results:
        columns = row.find_all('td')
        if len(columns) > 6:
            placement = columns[0].get_text(strip=True)
            horse_name = columns[2].get_text(strip=True)
            time = columns[6].get_text(strip=True)
            if placement == '1':
                return horse_name, time

    return None

# ★ 使用例（2025年4月19日・第3レース・佐賀競馬場（コード: 32））
if __name__ == "__main__":
    result = get_first_place_time("2025/04/19", 3, 32)
    if result:
        horse_name, time = result
        print(f"一着馬: {horse_name}, タイム: {time}")
    else:
        print("タイム情報を取得できませんでした。")

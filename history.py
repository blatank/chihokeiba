import re
import datetime
import logging
from typing import Any


class History:
  """履歴データを保持する小さなレコードクラス。

  既存の外部 API を壊さないようにメソッド名はそのまま維持しています。
  日付・時間パースを堅牢化し、失敗時は警告を出すようにしました。
  """
  def __init__(self, racecourse: Any, time: str, date: str = "", baba: str = "", parts: str = "", gate: str = "", last3F: str = "", jockey: str = ""):
    self.__racecourse = racecourse
    self.__time = time or ""

    # 日付は元コードで 'YY.MM.DD' 形式を想定していたため柔軟に対応
    if date:
      try:
        d = re.split(r'\.', date)
        year = int(d[0])
        if year < 100:
          year = 2000 + year
        self.__date = datetime.datetime(year, int(d[1]), int(d[2]))
      except Exception as e:
        logging.warning("history: failed to parse date '%s': %s", date, e)
        self.__date = datetime.datetime(1999, 1, 1)
    else:
      self.__date = datetime.datetime(1999, 1, 1)

    self.__baba = baba
    self.__parts = parts
    self.__gate = gate
    self.__last3F = last3F
    self.__jockey = jockey
    self.__timeInt = 0

  def getTimeInt(self):
    """内部で保持する時間整数値を返す。

    形式が不正な場合は 0 を返します（ログに警告）。
    単位は既存コードの互換を保ち、m*600 + s*10 の計算結果です。
    """
    if not self.__time:
      return 0

    splited_str = re.split(r':', self.__time)
    try:
      m = int(splited_str[0]) * 600
      s = float(splited_str[1]) * 10
      self.__timeInt = int(m + s)
    except Exception as e:
      logging.warning("history: failed to parse time '%s': %s", self.__time, e)
      self.__timeInt = 0

    return self.__timeInt

  def getTimeStr(self):
    return self.__time

  def getTime(self):
    if self.__time:
      return f"{self.__time} [{self.__last3F}]  ({self.getDateStr()} {self.__baba} {self.__gate}/{self.__parts})"
    else:
      return ""
  
  def getDateStr(self):
    return self.__date.strftime('%Y.%m.%d')

  def getDate(self):
    return self.__date
  
  def getJockey(self):
    return self.__jockey
  
  def hasHistory(self, racecourse: Any) -> bool:
    return self.__racecourse == racecourse
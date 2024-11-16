import json

class RaceCourseDictionary:
  def __init__(self, file):
    with open(file, encoding='utf-8') as f:
      self._data = json.load(f)
  
  # 馬場コードから競馬場名を取得 
  def inquireRaceCourseName(self, babaCode):
    for d in self._data:
      if d["Code"] == babaCode:
        return d["Name"]
    
    return ""
  
  # 競馬場名から馬場コードを取得 
  def inquireBabaCode(self, course):
    for d in self._data:
      if d["Name"] == course:
        return str(d["Code"])
    
    return ""
  
  def getAllRaceCourseName(self):
    names = []
    for d in self._data:
      names.append(d["Name"])

    return names
  
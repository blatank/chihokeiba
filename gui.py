from url import Url
from analyze import Analyze
from tkcalendar import Calendar, DateEntry
from racecoursedictionary import RaceCourseDictionary
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import datetime
import json
import os

class TestTkcalender(tk.Frame):
    def __init__(self,master):
        super().__init__(master)

        if os.path.exists('gui.json'):
            with open('gui.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            dt_now = datetime.datetime.now()
            data = {}
            data["place"] = ""
            data["no"] = ""
            data["year"] = dt_now.year
            data["month"] = dt_now.month
            data["day"] = dt_now.day

        self.pack()
        self.master.title("tkカレンダーテスト")
        self.master.geometry("400x200")

        label = tk.Label(master, text="競馬場")
        label.pack()

        dictionary = RaceCourseDictionary("racecoursedictionary.json")
        self.__place_txt = ttk.Combobox(master, values = dictionary.getAllRaceCourseName())
        self.__place_txt.pack()
        self.__place_txt.set(data["place"])

        label = tk.Label(master, text="レースNo")
        label.pack()

        nos = []
        # レース番号を設定
        for i in range(12):
            nos.append(str(i + 1))
        self.__no_txt = ttk.Combobox(master, values = nos)
        self.__no_txt.pack()
        self.__no_txt.set(data["no"])

        label = tk.Label(master, text="日付")
        label.pack()

        self.data_entry_date = DateEntry()
        self.data_entry_date.pack()
        self.data_entry_date.set_date(datetime.datetime(data["year"], data["month"], data["day"]))
        # self.data_entry_date.place()

        button = tk.Button(master, text="開始", command=self.__do_keiba)
        button.pack()

        # 終了時に呼び出すイベントをバインド
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    # 開始ボタンを押した際の処理
    def __do_keiba(self):
        place = self.__place_txt.get()
        no = self.__no_txt.get()
        dt_now = self.data_entry_date.get_date()
        date = dt_now.strftime('%Y/%m/%d')
        url = Url.getUrl(date, no, place)

        sub_win = tk.Toplevel()
        text = tk.Text(sub_win, height=50)
        text.pack()
        text.insert('1.0', Analyze.getResult(url))
    
    
    def on_close(self):
        data = {}
        data["place"] = self.__place_txt.get()
        data["no"] = self.__no_txt.get()
        dt_now = self.data_entry_date.get_date()
        data["year"] = dt_now.year
        data["month"] = dt_now.month
        data["day"] = dt_now.day

        with open('gui.json', 'w', encoding='utf-8') as f: 
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.master.destroy()


def main():
    root = tk.Tk()
    root = TestTkcalender(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()


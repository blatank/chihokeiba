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
import webbrowser

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
            data["period"] = False
            data["start_year"] = dt_now.year
            data["start_month"] = dt_now.month
            data["start_day"] = dt_now.day

        self.pack()
        self.master.title("地方競馬解析")
        self.master.geometry("400x300")

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

        today = tk.Button(master, text="今日", command=self.__do_today)
        today.pack()

        label = tk.Label(master, text="　")
        label.pack()

        # 絞り込み期間の変更
        self.__chk = tk.BooleanVar()
        self.__chk.set(data["period"])

        chkbox = ttk.Checkbutton(master, variable=self.__chk, text='解析開始日を設定して絞り込む')
        chkbox.pack()

        self.data_entry_start = DateEntry()
        self.data_entry_start.pack()
        self.data_entry_start.set_date(datetime.datetime(data["start_year"], data["start_month"], data["start_day"]))

        label = tk.Label(master, text="　")
        label.pack()

        button = tk.Button(master, text="開始", command=self.__do_keiba)
        button.pack()

        jumpbutton = tk.Button(master, text="地方競馬サイトに飛ぶ", command=self.__jump)
        jumpbutton.pack()

        # 終了時に呼び出すイベントをバインド
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def __make_url(self):
        place = self.__place_txt.get()
        no = self.__no_txt.get()
        dt_now = self.data_entry_date.get_date()
        date = dt_now.strftime('%Y/%m/%d')
        return Url.getUrl(date, no, place)


    # 開始ボタンを押した際の処理
    def __do_keiba(self):
        # place = self.__place_txt.get()
        # no = self.__no_txt.get()
        # dt_now = self.data_entry_date.get_date()
        # date = dt_now.strftime('%Y/%m/%d')
        # url = Url.getUrl(date, no, place)

        sub_win = tk.Toplevel()
        text = tk.Text(sub_win, height=50)
        text.pack()
        dt_start = self.data_entry_start.get_date()
        text.insert('1.0', Analyze.getResult(self.__make_url(), self.__chk.get(),
                                             datetime.datetime(dt_start.year, dt_start.month, dt_start.day)))
        
    def __do_today(self):
        self.data_entry_date.set_date(datetime.datetime.now())

    def __jump(self):
        webbrowser.open(self.__make_url())
    
    def on_close(self):
        data = {}
        data["place"] = self.__place_txt.get()
        data["no"] = self.__no_txt.get()

        dt_now = self.data_entry_date.get_date()
        data["year"] = dt_now.year
        data["month"] = dt_now.month
        data["day"] = dt_now.day

        dt_start = self.data_entry_start.get_date()
        data["start_year"] = dt_start.year
        data["start_month"] = dt_start.month
        data["start_day"] = dt_start.day

        data["period"] = self.__chk.get()

        with open('gui.json', 'w', encoding='utf-8') as f: 
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.master.destroy()


def main():
    root = tk.Tk()
    root = TestTkcalender(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()


from url import Url
from analyze import Analyze
from tkcalendar import Calendar, DateEntry
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import datetime

class TestTkcalender(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.master.title("tkカレンダーテスト")
        # self.master.geometry("800x600")

        label = tk.Label(master, text="競馬場")
        label.pack()

        self.__place_txt = ttk.Combobox(master, values = ("佐賀","高知"))
        self.__place_txt.pack()

        label = tk.Label(master, text="レースNo")
        label.pack()

        nos = []
        for i in range(12):
            nos.append(str(i + 1))
        self.__no_txt = ttk.Combobox(master, values = nos)
        self.__no_txt.pack()

        label = tk.Label(master, text="日付")
        label.pack()

        self.data_entry_date = DateEntry()
        self.data_entry_date.pack()
        # self.data_entry_date.place()

        button = tk.Button(master, text="開始", command=self.__do_keiba)
        button.pack()

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


def main():
    root = tk.Tk()
    root = TestTkcalender(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()


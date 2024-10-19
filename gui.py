import tkinter as tk
import tkinter.ttk as ttk
import subprocess

def do_keiba():
    place = place_txt.get()
    no = no_txt.get()
    str = "python .\\keiba.py --place=" + place + " --no=" + no
    subprocess.Popen(str)

root = tk.Tk()
root.title("サンプルアプリ")

label = tk.Label(root, text="競馬場")
label.pack()

place_txt = ttk.Combobox(root, values = ("佐賀","高知"))
place_txt.pack()

label = tk.Label(root, text="レースNo")
label.pack()

nos = []
for i in range(12):
    nos.append(str(i + 1))
no_txt = ttk.Combobox(root, values = nos)
no_txt.pack()

button = tk.Button(root, text="開始", command=do_keiba)
button.pack()

root.mainloop()
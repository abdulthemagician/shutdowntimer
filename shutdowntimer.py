import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

main = tk.Tk()
main.configure(bg="#a6edff")
main_frame = tk.Frame(main, bg="#a6edff")
main_frame.pack(fill="both", expand=True)

#Window configuration
win_width = 200
win_height = 200

#Screen resolution
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

#Center position of window
x = (screen_width // 2) - (win_width // 2)
y = (screen_height // 2) - (win_height // 2)

#Text Box
hours = tk.StringVar(value=0)
minutes = tk.IntVar(value=0)

hourComboBox = ttk.Combobox(textvariable=hours)
hourComboBox["values"] = [1, 2, 3, 4, 5]
hourComboBox.place(x=10, y=win_height - 120, width=40)

minuteComboBox = ttk.Combobox(textvariable=minutes)
minuteComboBox["values"] = [15, 30, 45]
minuteComboBox.place(x=100, y=win_height - 120, width=40)

#Label
shutdownTimerLabel = tk.Label(main, text="Shutdown Timer", bg="#a6edff", fg="Black", font=10).place(x=40, y=20)
hourLabel = tk.Label(main, text="ชั่วโมง", bg="#a6edff", fg="Black", font=10).place(x=50, y=win_height - 120)
minuteLabel = tk.Label(main, text="นาที", bg="#a6edff", fg="Black",font=10).place(x=140, y=win_height - 120)

#Button
shutdownTimerButton = tk.Button(main, text="ตั้งเวลาปิดเครื่อง",bg="#96ffb6").place(x=10, y=win_height - 60)
abortShutdownButton  = tk.Button(main, text="ยกเลิกปิดเครื่อง", bg="#ff8593").place(x=190, y=win_height - 60, anchor="ne")

main.title("Shutdown Timer")
main.geometry(f"{win_width}x{win_height}+{x}+{y}")
main.mainloop()
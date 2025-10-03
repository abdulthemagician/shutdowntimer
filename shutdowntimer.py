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

def setShutdownTimer(hour: int, minute: int):
    second = (hour * 3600) + (minute * 60)
    if second <= 0:
        confirm = messagebox.askyesno("0 minutes, 0 second", "คุณต้องการปิดเครื่องทันทีหรือไม่ ?")
        if confirm:
            rc = os.system(f"shutdown -s -t 5")
            if rc != 0:
                os.system("shutdown -a")
                os.system(f"shutdown -s -t 5")
            messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"เครื่องกำลังจะปิดในอีก 5 วินาที")
            return
        else:
            return
        
    if second > 0:
        rc = os.system(f"shutdown -s -t {second}")
        if rc != 0:
            answer = messagebox.askyesno("การตั้งเวลาปิดเครื่องทับซ้อน", "ตรวจพบว่ามีการตั้งเวลาปิดเครื่องอยู่แล้ว\nต้องการยกเลิกของเก่าและตั้งค่าใหม่หรือไม่?")
            if not answer:
                return
            else:
                os.system("shutdown -a")
                os.system(f"shutdown -s -t {second}")
                
        if hour <= 0 and minute > 0:
            messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"ตั้งเวลาปิดเครื่องใน {second / 60:.0f} นาทีแล้ว")
        else:
            messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"ตั้งเวลาปิดเครื่องใน {hour} ชั่วโมง {minute} นาทีแล้ว")
        
def abortShutdownTimer():
    os.system("shutdown -a")
    messagebox.showinfo("ยกเลิก", "ยกเลิกการปิดเครื่องเสร็จสิ้น")

def showMessage():
    hour = int(hours.get())
    minute = int(minutes.get())
    print(hour, minute)

#Text Box
hours = tk.StringVar(value=0)
minutes = tk.IntVar(value=0)

hourBox = ttk.Spinbox(textvariable=hours, increment=1, from_=0, to=10)
hourBox.place(x=20, y=win_height - 120, width=40)

minuteBox = ttk.Spinbox(textvariable=minutes, increment=10, from_=1, to=60)
minuteBox.place(x=110, y=win_height - 120, width=40)

#Label
shutdownTimerLabel = tk.Label(main, text="Shutdown Timer", bg="#a6edff", fg="Black", font=10).place(x=40, y=20)
hourLabel = tk.Label(main, text="ชั่วโมง", bg="#a6edff", fg="Black", font=10).place(x=60, y=win_height - 120)
minuteLabel = tk.Label(main, text="นาที", bg="#a6edff", fg="Black",font=10).place(x=150, y=win_height - 120)

#Button
shutdownTimerButton = tk.Button(main, text="ตั้งเวลาปิดเครื่อง",bg="#96ffb6", command=lambda: setShutdownTimer(int(hours.get()), int(minutes.get()))).place(x=10, y=win_height - 60)
abortShutdownButton  = tk.Button(main, text="ยกเลิกปิดเครื่อง", bg="#ff8593", command=abortShutdownTimer).place(x=190, y=win_height - 60, anchor="ne")

main.title("Shutdown Timer")
main.geometry(f"{win_width}x{win_height}+{x}+{y}")
main.mainloop()
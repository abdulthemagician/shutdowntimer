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

def validate_hour(value):
    return value == "" or (value.isdigit() and 0 <= int(value) <= 23)

def validate_minute(value):
    return value == "" or (value.isdigit() and 1 <= int(value) <= 60)

def shutdown(second: int) -> int:
    if second < 0:
        return -1
    return os.system(f"shutdown -s -t {second}")
    
def abortShutdown() -> bool:
    code: int = os.system("shutdown -a")
    if code != 0:
        return False
    return True

def confirmOverideShutdownTimer() -> bool:
    return messagebox.askyesno("การตั้งเวลาปิดเครื่องทับซ้อน", "ตรวจพบว่ามีการตั้งเวลาปิดเครื่องอยู่แล้ว\nต้องการยกเลิกของเก่าและตั้งค่าใหม่หรือไม่?")

def shutdownTimerInfo(hour: int = 0, minute: int = 0, second: int = 0):
    while(minute >= 60):
        hour+=1
        minute-=60
    if second > 0 and hour == 0 and minute == 0:
        messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"ตั้งเวลาปิดเครื่องใน {second :.0f} วินาทีแล้ว")
    elif hour <= 0 and minute > 0:
        messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"ตั้งเวลาปิดเครื่องใน {minute :.0f} นาทีแล้ว")
    else:
        messagebox.showinfo("ตั้งเวลาปิดเครื่อง", f"ตั้งเวลาปิดเครื่องใน {hour} ชั่วโมง {minute} นาทีแล้ว")

def setShutdownTimer(hour: int, minute: int):
    second = (hour * 3600) + (minute * 60)
    if second <= 0:
        confirm: bool = messagebox.askyesno("0 minutes, 0 second", "คุณต้องการปิดเครื่องทันทีหรือไม่ ?\nระบบจะนับเวลาถอยหลัง 10 วินาทีก่อนจะปิดเครื่อง")
        if confirm:
            rc: int = shutdown(10)
            if rc != 0:
                answer = confirmOverideShutdownTimer()
                if not answer:
                    return
                abortShutdown()
                shutdown(10)
            shutdownTimerInfo(second=10)
            return
        
    if second > 0:
        rc: int = shutdown(second)
        if rc != 0:
            answer = confirmOverideShutdownTimer()
            if not answer:
                return
            abortShutdown()
            shutdown(second)
        shutdownTimerInfo(hour, minute, second)
        
def abortShutdownTimer():
    code: bool = abortShutdown()
    if not code:
        messagebox.showwarning("ไม่พบการตั้งเวลาปิดเครื่อง", "ไม่พบการตั้งเวลาปิดเครื่องก่อนหน้า\nไม่สามารถยกเลิกได้")
    else:
        messagebox.showinfo("ยกเลิก", "ยกเลิกการปิดเครื่องเสร็จสิ้น")

#Text Box
hours = tk.StringVar(value=0)
minutes = tk.IntVar(value=0)

vcmd_hour = (main.register(validate_hour), '%P')
vcmd_minute = (main.register(validate_minute), '%P')

hourBox = ttk.Spinbox(main,
                      textvariable=hours,
                      increment=1,
                      from_=0, to=10,
                      validate='key',
                      validatecommand=vcmd_hour
                      )
hourBox.place(x=20, y=win_height - 120, width=40)

minuteBox = ttk.Spinbox(main,
                        textvariable=minutes,
                        increment=5, 
                        from_=0, to=120,
                        validate='key',
                        validatecommand=vcmd_minute
                        )
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
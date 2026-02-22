# Shutdown Timer

โปรแกรมตั้งเวลาปิดเครื่องสำหรับ Windows พร้อมหน้าจอ Dark Theme ทันสมัย สร้างด้วย Python และ Tkinter

---

## คุณสมบัติ

- **ธีมสีเข้ม** — ชุดสี Catppuccin Mocha แบบ Card Layout
- **นาฬิกานับถอยหลังแบบสด** — แสดง `HH : MM : SS` ขนาดใหญ่ อัปเดตแบบเรียลไทม์
- **ปุ่มตั้งเวลาด่วน** — กดครั้งเดียว 15 นาที, 30 นาที, 1 ชม., 2 ชม., 4 ชม.
- **กำหนดเวลาเอง** — ช่องกรอก ชั่วโมง / นาที / วินาที
- **แสดงสถานะ** — บอกว่ามีตัวจับเวลาทำงานอยู่หรือไม่
- **ตรวจจับการตั้งเวลาซ้ำ** — ถามก่อนทับการตั้งเวลาเดิมของ Windows
- **ปุ่มลัด** — `Enter` = ตั้งเวลา, `Escape` = ยกเลิก

---

## โครงสร้างโปรเจกต์

```
shutdowntimer/
├── main.py    # จุดเริ่มต้น — รันไฟล์นี้
├── app.py     # ส่วน GUI — คลาส ShutdownTimerApp
├── core.py    # ส่วนตรรกะ — คำสั่งปิดเครื่องระดับ OS (ไม่พึ่ง GUI)
├── theme.py   # ธีมและสไตล์ทั้งหมด
└── README.md
```

---

## ความต้องการของระบบ

| เครื่องมือ | เวอร์ชันขั้นต่ำ |
|-----------|----------------|
| Python | 3.10 |
| tkinter | มาพร้อม CPython |

> **หมายเหตุ:** `tkinter` มาพร้อมกับตัวติดตั้ง Python บน Windows อยู่แล้ว  
> หากไม่มี (เช่น Linux แบบ minimal) ให้ติดตั้งด้วย  
> `sudo apt install python3-tk` (Debian/Ubuntu) หรือคำสั่งที่เทียบเท่า

ไม่ต้องติดตั้งแพ็กเกจภายนอกเพิ่มเติม

---

## วิธีติดตั้งและรันจาก Source

### 1 · ติดตั้ง Python

ดาวน์โหลดและติดตั้ง Python 3.10 ขึ้นไปจาก [python.org](https://www.python.org/downloads/)

> ตอนติดตั้งให้ **กาเครื่องหมาย ☑ Add Python to PATH** ด้วย

### 2 · ดาวน์โหลดโปรเจกต์

```powershell
git clone https://github.com/thanattsm/shutdowntimer.git
cd shutdowntimer
```

หรือ ดาวน์โหลดเป็น ZIP แล้วแตกไฟล์

### 3 · รันโปรแกรม

```powershell
python main.py
```

เพียงเท่านี้ก็ใช้งานได้ทันที ไม่ต้องติดตั้งอะไรเพิ่ม

---

## สร้างไฟล์ .exe (ไม่ต้องติดตั้ง Python)

หากต้องการแจกจ่ายเป็นไฟล์ `.exe` ให้คนอื่นใช้โดยไม่ต้องติดตั้ง Python:

### 1 · ติดตั้ง PyInstaller

```powershell
pip install pyinstaller
```

### 2 · สร้างไฟล์เดียว (แนะนำ)

```powershell
pyinstaller --onefile --windowed --name "ShutdownTimer" main.py
```

| Flag | ความหมาย |
|------|---------|
| `--onefile` | รวมทุกอย่างเป็นไฟล์ `.exe` เดียว |
| `--windowed` | ไม่แสดงหน้าต่าง Console |
| `--name` | ตั้งชื่อไฟล์ที่ได้ |

ผลลัพธ์: `dist/ShutdownTimer.exe`

### 3 · ใส่ไอคอน (ไม่บังคับ)

```powershell
pyinstaller --onefile --windowed --name "ShutdownTimer" --icon icon.ico main.py
```

### 4 · ลบไฟล์ชั่วคราวจากการ Build

```powershell
Remove-Item -Recurse -Force build, dist, ShutdownTimer.spec
```

---

## สถาปัตยกรรม

| ชั้น | ไฟล์ | หน้าที่ |
|-----|------|--------|
| จุดเริ่มต้น | `main.py` | สร้าง `ShutdownTimerApp` และเริ่ม Event Loop |
| GUI | `app.py` | หน้าต่าง Tkinter, ตรรกะนับถอยหลัง, การโต้ตอบกับผู้ใช้ |
| ตรรกะ | `core.py` | ฟังก์ชันล้วน — `schedule_shutdown()`, `cancel_shutdown()` ฯลฯ คืนค่าเป็น `TimerResult` (ไม่มี messagebox) |
| ธีม | `theme.py` | ชุดสี, ฟอนต์, ฟังก์ชัน `apply_theme()` |

---

## หมายเหตุ

- โปรแกรมเรียกคำสั่ง `shutdown -s -t <วินาที>` และ `shutdown -a` ผ่าน Windows Shell  
  ไม่จำเป็นต้องใช้สิทธิ์ Administrator ยกเว้น UAC จำกัดคำสั่ง `shutdown` บนเครื่องนั้น
- ไม่มีการเขียนข้อมูลลงดิสก์ ไม่มีการเชื่อมต่ออินเทอร์เน็ต

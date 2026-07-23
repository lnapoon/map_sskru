# SSKRU Campus 3D Interactive Map & Django Backend System

ระบบแผนผังนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ พร้อมระบบหลังบ้านผู้ดูแลระบบ (Django Framework + `.env`)

---

## 📁 โครงสร้างไฟล์ในโปรเจกต์ (Clean & Organized Structure)

```
Mark_map/
├── .env                  # ไฟล์ตั้งค่าสภาพแวดล้อม (DEBUG, SECRET_KEY, PORT, ADMIN_USERNAME, ADMIN_PASSWORD)
├── .gitignore            # ไฟล์ละเว้นข้อมูลสำหรับ Git
├── requirements.txt      # รายการแพ็กเกจ Python (django, python-dotenv, pillow)
├── manage.py             # สคริปต์จัดการ Django (พร้อมระบบโหลด .env อัตโนมัติ)
├── db.sqlite3            # ฐานข้อมูล SQLite ของ Django
├── index.html            # หน้าเว็บหลักของระบบ
├── app.js                # โค้ดตรรกะระบบนำทาง + แผนที่ + แผงควบคุมแอดมิน
├── styles.css            # ไฟล์สไตล์ Glassmorphic Design System
├── README.md             # คู่มือการติดตั้งและใช้งานระบบ
├── env/                  # Virtual Environment ของ Python
├── sskru_map/            # โฟลเดอร์ตั้งค่าหลักของ Django Project
├── api/                  # Django REST API App (จัดการข้อมูลอาคาร และ Login แอดมิน)
├── data/
│   └── buildings.json    # ไฟล์ฐานข้อมูลอาคาร (Persistent JSON Store)
└── images/
    ├── Map.png           # ภาพแผนที่ 3D ความละเอียดสูง (3072x2048 Ultra HD)
    └── Map_original.png  # ภาพถ่ายทางอากาศโดรนต้นฉบับ
```

---

## 🚀 คู่มือวิธีการรันเซิร์ฟเวอร์ (Step-by-Step Server Run Guide)

### วิธีที่ 1: รันผ่าน Virtual Environment (`env`) [แนะนำ]

เปิด Terminal ในโฟลเดอร์โปรเจกต์ `Mark_map` แล้วทำตามขั้นตอนต่อไปนี้:

1. **เปิดใช้งาน Virtual Environment**:
   * **macOS / Linux**:
     ```bash
     source env/bin/activate
     ```
   * **Windows (Command Prompt / PowerShell)**:
     ```cmd
     env\Scripts\activate
     ```

2. **รันเซิร์ฟเวอร์ Django**:
   ```bash
   python manage.py runserver 8000
   ```

3. **เปิดใช้งานบนเว็บเบราว์เซอร์**:
   เปิดเว็บเบราว์เซอร์แล้วไปที่: **`http://127.0.0.1:8000`**

---

## 🔑 ข้อมูลเข้าสู่ระบบแอดมิน (Admin Login)

- **Username**: `admin` *(ตั้งค่าในไฟล์ `.env`)*
- **Password**: `admin1234` *(ตั้งค่าในไฟล์ `.env`)*
# map_sskru

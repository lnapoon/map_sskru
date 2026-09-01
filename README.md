# 🗺️ SSKRU Campus Map — ระบบแผนที่ผังเมืองและนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ

ระบบแผนผังนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ (Sisaket Rajabhat University) รองรับทั้งระบบ **Django (Python)** และ **XAMPP (PHP / Apache / MySQL)** พร้อมฐานข้อมูลแบบ Relational Database ครบวงจร

---

## 📁 โครงสร้างโปรเจกต์ (Clean & Organized Project Structure)

```
Mark_map/
├── 📄 index.html                     # หน้าหลักแผนที่แบบ Standalone / Django
├── 📄 index.php                      # หน้าหลักแผนที่ฝั่ง PHP / XAMPP
├── 📄 login.php                      # หน้าระบบเข้าสู่ระบบรวม (PHP)
├── 📄 register_student.php           # หน้ายืนยันตัวตนและลงทะเบียนนักศึกษา (PHP)
├── 📄 register_staff.php             # หน้าสมัครสมาชิกบุคลากร/อาจารย์ (PHP)
├── 📄 reset_password_student.php     # หน้าร้องขอรีเซ็ตรหัสผ่านนักศึกษา (PHP)
├── 📄 reset_password_verify.php      # หน้ายืนยัน OTP/Token รีเซ็ตรหัสนักศึกษา (PHP)
├── 📄 reset_password_staff.php       # หน้าร้องขอรีเซ็ตรหัสผ่านบุคลากร (PHP)
├── 📄 reset_password_staff_verify.php# หน้ายืนยัน OTP รีเซ็ตรหัสบุคลากร (PHP)
├── 📄 api.php                        # REST API รวมฝั่ง PHP / XAMPP
├── 📄 config.php                     # การเชื่อมต่อ MySQL / phpMyAdmin
├── 📄 app.js                         # ตรรกะแผนที่ Leaflet, Dijkstra Navigation & Admin Tools
├── 📄 styles.css                     # Glassmorphic Design System & Signature Theme
├── 📄 sw.js                          # Service Worker (PWA Offline Support)
├── 📄 manifest.json                  # Web App Manifest สำหรับติดตั้งบนมือถือ
├── 📄 .htaccess                      # ความปลอดภัยเว็บเซิร์ฟเวอร์ (Apache / XAMPP)
├── 📄 requirements.txt               # รายการ Dependencies ของ Python Django
│
├── 📂 admin_panel/                   # Django Admin Panel & Authentication App
│   ├── views.py                      # Logic จัดการผู้ใช้, สถิติรายวัน, API
│   ├── models.py                     # SQLite Models (Student, VisitorLog, AdminSession)
│   ├── urls.py                       # Routing ของระบบ Admin
│   └── templates/admin_panel/        # HTML Templates สำหรับระบบสมาชิกและ Dashboard
│
├── 📂 api/                           # Django REST API สำหรับข้อมูลอาคาร
│   ├── views.py                      # API อ่าน/เขียนข้อมูล 40 อาคาร
│   └── urls.py                       # Routing ของ API อาคาร
│
├── 📂 sskru_map/                     # Django Project Core Settings
│   ├── settings.py                   # การตั้งค่าแอปพลิเคชัน
│   └── urls.py                       # Routing หลัก
│
├── 📂 data/                          # แหล่งข้อมูล JSON และ Security Files
│   ├── .htaccess                     # ป้องกันการเข้าถึงไฟล์ข้อมูลตรงๆ
│   ├── buildings.json                # ข้อมูลพิกัดและรายละเอียด 40 อาคาร
│   ├── students_roster.json          # ทะเบียนรายชื่อนักศึกษาสำหรับยืนยันตัวตน
│   ├── user_accounts.json            # บัญชีผู้ใช้งานระบบ (Students & Staff)
│   ├── user_activity_logs.json       # ประวัติการเข้าใช้งานระบบรายวัน
│   └── password_resets.json          # ข้อมูล Token & OTP รีเซ็ตรหัสผ่าน
│
├── 📂 database/                      # สคริปต์จัดการฐานข้อมูล
│   └── migrate_schema.py             # สคริปต์สร้างตาราง Relational 8 Entities ใน phpMyAdmin
│
└── 📂 images/                        # รูปภาพและแผนที่ความละเอียดสูง
    ├── Map.png                       # แผนที่วิทยาเขตความละเอียดสูง (3072x2048)
    └── Map_original.png              # แผนที่ภาพถ่ายทางอากาศต้นฉบับ
```

---

## 🗄️ โครงสร้างฐานข้อมูลใน phpMyAdmin (`sskru_map`)

| # | ตาราง (Entity) | คีย์หลัก (PK) | คีย์นอก (FK) | รายละเอียด |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **`categories`** | `category_key` | - | หมวดหมู่อาคาร (Academic, Office, Facility, Library, Other) |
| 2 | **`faculties`** | `faculty_id` | - | รายชื่อคณะและหน่วยงานในมหาวิทยาลัย |
| 3 | **`buildings`** | `id` | `category_key` ➔ `categories` | พิกัดและข้อมูลของ 40 อาคาร |
| 4 | **`students_roster`** | `student_id` | `faculty_id` ➔ `faculties` | ทะเบียนนักศึกษาสำหรับตรวจสอบสิทธิ์ |
| 5 | **`users`** | `user_id` | `student_id` ➔ `students_roster` | บัญชีผู้ใช้ที่ลงทะเบียน (นักศึกษา, บุคลากร, แอดมิน) |
| 6 | **`user_activity_logs`** | `log_id` | `user_id` ➔ `users` | บันทึกประวัติการเข้าใช้งานและสถิติรายวัน |
| 7 | **`password_resets`** | `reset_id` | `student_id` ➔ `students_roster` | รายการขอ OTP และรีเซ็ตรหัสผ่าน |
| 8 | **`admin_sessions`** | `session_id` | `user_id` ➔ `users` | เซสชันความปลอดภัยของแอดมิน |

---

## 🚀 วิธีการรันระบบ (How to Run)

### วิธีที่ 1: รันผ่าน XAMPP (Apache + MySQL / phpMyAdmin)
1. คัดลอกโปรเจกต์ไปไว้ที่ `/Applications/XAMPP/xamppfiles/htdocs/sskru_map` (หรือ `C:\xampp\htdocs\sskru_map`)
2. สตาร์ต **Apache** และ **MySQL** ใน XAMPP Control Panel
3. รันสคริปต์สร้างฐานข้อมูล:
   ```bash
   python3 database/migrate_schema.py
   ```
4. เปิดเบราว์เซอร์ไปที่: **`http://localhost/sskru_map/`**

### วิธีที่ 2: รันผ่าน Django (Python)
1. เปิด Terminal ในโฟลเดอร์โปรเจกต์
2. ติดตั้ง Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. รันเซิร์ฟเวอร์:
   ```bash
   python manage.py runserver 8000
   ```
4. เปิดเบราว์เซอร์ไปที่: **`http://127.0.0.1:8000/`**

---

## 🔑 ข้อมูลเข้าสู่ระบบ (Credentials)

- **ผู้ดูแลระบบสูงสุด (Super Admin)**:
  - **Username**: `lnwpoon007x`
  - **Password**: `poon300450`
- **นักศึกษาตัวอย่าง (Student)**:
  - **รหัสนักศึกษา**: `6812732120`
  - **รหัสผ่าน**: `0620401150`
- **บุคลากรตัวอย่าง (Staff)**:
  - **Username**: `poon_staff` (หรืออีเมล `mpoontv1234@gmail.com`)
  - **Password**: รหัสผ่านที่ตั้งตอนลงทะเบียน

---

## 🛡️ ความปลอดภัยและความเป็นส่วนตัว (Security & PDPA)
1. **การคุ้มครองข้อมูลส่วนบุคคล (PDPA)**: ขอสิทธิ์ตำแหน่ง GPS แบบ Just-in-Time เฉพาะเมื่อเริ่มใช้งานฟังก์ชันนำทาง
2. **ระบบป้องกัน Brute-Force (Rate Limiting)**: จำกัดการกรอกรหัสผ่านและ OTP ผิดไม่เกิน 5 ครั้ง / 10 นาที
3. **การป้องกันไฟล์ฐานข้อมูล (.htaccess)**: บล็อกการเข้าถึงไฟล์ `.json`, `.sqlite3`, `.log`, `.env` ผ่าน URL โดยตรง 100%
4. **ความปลอดภัยรหัสผ่าน**: เข้ารหัสผ่านแบบ SHA-256 / PBKDF2 พร้อมระบบยืนยันสิทธิ์ก่อนแสดงข้อมูลระบุตัวตน (Privacy Shield)

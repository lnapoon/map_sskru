# 🗺️ SSKRU Campus Map — ระบบแผนที่และนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ

ระบบแผนผังนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ รองรับทั้ง **Django (Python)** และ **XAMPP (PHP / Apache / MySQL)**

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```
Mark_map/
│
├── 📄 index.html                          # หน้าหลักแผนที่ (Django)
├── 📄 index.php                           # หน้าหลักแผนที่ (XAMPP/PHP)
├── 📄 manage.py                           # Django Management Script
├── 📄 requirements.txt                    # Python Dependencies
├── 📄 README.md                           # เอกสารโปรเจกต์
├── 📄 .env                                # ตัวแปรสภาพแวดล้อม (SECRET_KEY, ADMIN, SMTP)
├── 📄 .gitignore                          # ไฟล์ที่ไม่ต้อง Track ใน Git
├── 📄 .htaccess                           # Apache Security Rules
├── 📄 db.sqlite3                          # ฐานข้อมูล SQLite ของ Django
│
├── 📂 assets/                             # ═══ ไฟล์ Static ของระบบ UI ═══
│   ├── 📁 css/
│   │   └── 📄 styles.css                  # Glassmorphic Design System
│   ├── 📁 js/
│   │   ├── 📄 app.js                      # โค้ดแผนที่ Leaflet, Dijkstra, Admin Tools
│   │   └── 📄 sw.js                       # Service Worker (PWA Offline)
│   └── 📄 manifest.json                   # Web App Manifest (PWA)
│
├── 📂 auth/                               # ═══ ระบบสมาชิก & API ฝั่ง PHP ═══
│   ├── 📄 api.php                         # REST API รวม (CRUD, Login, Register, OTP)
│   ├── 📄 config.php                      # การเชื่อมต่อ MySQL / phpMyAdmin
│   ├── 📄 login.php                       # หน้าเข้าสู่ระบบรวม (นักศึกษา + บุคลากร)
│   ├── 📄 register_student.php            # ลงทะเบียนนักศึกษา
│   ├── 📄 register_staff.php              # ลงทะเบียนบุคลากร/อาจารย์
│   ├── 📄 reset_password_student.php      # ร้องขอรีเซ็ตรหัสนักศึกษา
│   ├── 📄 reset_password_verify.php       # ยืนยัน OTP รีเซ็ตรหัสนักศึกษา
│   ├── 📄 reset_password_staff.php        # ร้องขอรีเซ็ตรหัสบุคลากร
│   └── 📄 reset_password_staff_verify.php # ยืนยัน OTP รีเซ็ตรหัสบุคลากร
│
├── 📂 data/                               # ═══ แหล่งข้อมูล JSON (Master DB) ═══
│   ├── 📄 .htaccess                       # ป้องกันเข้าถึงไฟล์โดยตรง
│   ├── 📄 buildings.json                  # ข้อมูล 40 อาคาร (พิกัด + รายละเอียด)
│   ├── 📄 students_roster.json            # ทะเบียนรายชื่อนักศึกษา
│   ├── 📄 user_accounts.json              # บัญชีผู้ใช้งาน (Students & Staff)
│   ├── 📄 user_activity_logs.json         # ประวัติการเข้าใช้งานรายวัน
│   ├── 📄 password_resets.json            # Token & OTP รีเซ็ตรหัสผ่าน
│   └── 📄 pdpa_policy.json                # นโยบายความเป็นส่วนตัว (PDPA)
│
├── 📂 database/                           # ═══ สคริปต์จัดการฐานข้อมูล ═══
│   └── 📄 migrate_schema.py              # สร้าง 8 ตาราง Relational ใน phpMyAdmin
│
├── 📂 images/                             # ═══ รูปภาพแผนที่ ═══
│   ├── 🖼️ Map.png                         # แผนที่ 3D ความละเอียดสูง (3072×2048)
│   └── 🖼️ Map_original.png               # ภาพถ่ายทางอากาศต้นฉบับ
│
├── 📂 deploy/                             # ═══ ไฟล์สำหรับ Deploy ═══
│   ├── 📄 build_vercel.sh                 # Build Script สำหรับ Vercel
│   └── 📄 vercel.json                     # Vercel Configuration
│
├── 📂 admin_panel/                        # ═══ Django Admin Backend ═══
│   ├── 📄 views.py                        # Logic: ผู้ใช้, สถิติ, API, Rate Limiting
│   ├── 📄 models.py                       # SQLite Models
│   ├── 📄 urls.py                         # Admin Routing
│   └── 📂 templates/admin_panel/          # HTML Templates
│
├── 📂 api/                                # ═══ Django REST API ═══
│   ├── 📄 views.py                        # API อ่าน/เขียนข้อมูลอาคาร
│   └── 📄 urls.py                         # API Routing
│
└── 📂 sskru_map/                          # ═══ Django Core Settings ═══
    ├── 📄 settings.py                     # การตั้งค่าแอป
    └── 📄 urls.py                         # Master URL Routing
```

---

## 🚀 วิธีการรัน

### XAMPP (PHP + MySQL)
```bash
# 1. คัดลอกโปรเจกต์ไปที่ htdocs
# 2. สตาร์ต Apache + MySQL ใน XAMPP
# 3. สร้างฐานข้อมูล
python3 database/migrate_schema.py
# 4. เปิด http://localhost/sskru_map/
```

### Django (Python)
```bash
pip install -r requirements.txt
python manage.py runserver 8000
# เปิด http://127.0.0.1:8000/
```

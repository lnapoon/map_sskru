import json
import pymysql
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_migration():
    print("🚀 Starting MySQL / phpMyAdmin Full Schema Migration...")
    
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        charset='utf8mb4',
        autocommit=True
    )
    
    with conn.cursor() as c:
        c.execute("CREATE DATABASE IF NOT EXISTS `sskru_map` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        c.execute("USE `sskru_map`;")
        c.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Drop old tables
        tables = [
            'admin_sessions', 'password_resets', 'user_activity_logs', 
            'users', 'students_roster', 'buildings', 'categories', 'faculties'
        ]
        for t in tables:
            c.execute(f"DROP TABLE IF EXISTS `{t}`;")
            
        print("✅ Cleaned old tables")

        # 1. Entity: categories
        c.execute("""
        CREATE TABLE `categories` (
            `category_key` VARCHAR(50) NOT NULL,
            `category_name_th` VARCHAR(100) NOT NULL,
            `category_name_en` VARCHAR(100) NOT NULL,
            `color_hex` VARCHAR(20) NOT NULL,
            `icon_class` VARCHAR(50) DEFAULT 'fa-building',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`category_key`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        categories_data = [
            ('academic', 'อาคารเรียน / คณะ', 'Academic Buildings', '#1a4fa0', 'fa-graduation-cap'),
            ('office', 'อาคารสำนักงาน / หน่วยงาน', 'Offices & Administration', '#e67e22', 'fa-briefcase'),
            ('facility', 'สิ่งอำนวยความสะดวก', 'Facilities & Services', '#2ecc71', 'fa-store'),
            ('library', 'หอสมุดและแหล่งเรียนรู้', 'Library & Learning Center', '#9b59b6', 'fa-book'),
            ('other', 'สถานที่อื่นๆ / ลานกิจกรรม', 'Other Landmarks', '#7f8c8d', 'fa-map-pin')
        ]
        c.executemany("""
        INSERT INTO `categories` (`category_key`, `category_name_th`, `category_name_en`, `color_hex`, `icon_class`)
        VALUES (%s, %s, %s, %s, %s);
        """, categories_data)
        print("✅ Entity 1: categories created & seeded")

        # 2. Entity: faculties
        c.execute("""
        CREATE TABLE `faculties` (
            `faculty_id` INT AUTO_INCREMENT,
            `faculty_name` VARCHAR(150) NOT NULL UNIQUE,
            `faculty_code` VARCHAR(50) DEFAULT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`faculty_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        faculties_data = [
            ('มหาวิทยาลัยราชภัฏศรีสะเกษ', 'SSKRU'),
            ('คณะครุศาสตร์', 'EDU'),
            ('คณะมนุษยศาสตร์และสังคมศาสตร์', 'HUSOC'),
            ('คณะศิลปศาสตร์และวิทยาศาสตร์', 'FLAS'),
            ('คณะวิทยาการจัดการ', 'FMS'),
            ('คณะพยาบาลศาสตร์', 'NURSE'),
            ('สำนักงานอธิการบดี', 'OP'),
            ('สำนักวิทยบริการและเทคโนโลยีสารสนเทศ', 'ARIT')
        ]
        c.executemany("""
        INSERT INTO `faculties` (`faculty_name`, `faculty_code`)
        VALUES (%s, %s);
        """, faculties_data)
        print("✅ Entity 2: faculties created & seeded")

        # 3. Entity: buildings (PK: id, FK: category_key -> categories.category_key)
        c.execute("""
        CREATE TABLE `buildings` (
            `id` INT NOT NULL,
            `code` VARCHAR(20) DEFAULT NULL,
            `name` VARCHAR(255) NOT NULL,
            `name_en` VARCHAR(255) DEFAULT NULL,
            `category_key` VARCHAR(50) DEFAULT 'other',
            `coords_y` INT NOT NULL DEFAULT 0,
            `coords_x` INT NOT NULL DEFAULT 0,
            `real_lat` DOUBLE DEFAULT 0.0,
            `real_lng` DOUBLE DEFAULT 0.0,
            `description` TEXT DEFAULT NULL,
            `phone` VARCHAR(100) DEFAULT NULL,
            `hours` VARCHAR(255) DEFAULT NULL,
            `floors_count` INT DEFAULT 1,
            `json_data` LONGTEXT DEFAULT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            KEY `idx_buildings_cat` (`category_key`),
            CONSTRAINT `fk_buildings_category` FOREIGN KEY (`category_key`) 
                REFERENCES `categories` (`category_key`) ON UPDATE CASCADE ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        buildings_file = BASE_DIR / 'data' / 'buildings.json'
        buildings = json.load(open(buildings_file, encoding='utf-8'))
        for b in buildings:
            b_id = b.get('id')
            b_code = str(b.get('code', b_id))
            b_name = b.get('name', '')
            b_name_en = b.get('nameEn', '')
            b_cat = b.get('category', 'other')
            if b_cat not in ['academic', 'office', 'facility', 'library', 'other']:
                b_cat = 'other'
            cy = b.get('coords', [0, 0])[0] if len(b.get('coords', [])) > 0 else 0
            cx = b.get('coords', [0, 0])[1] if len(b.get('coords', [])) > 1 else 0
            lat = b.get('realCoords', [0.0, 0.0])[0] if len(b.get('realCoords', [])) > 0 else 0.0
            lng = b.get('realCoords', [0.0, 0.0])[1] if len(b.get('realCoords', [])) > 1 else 0.0
            desc = b.get('description', '')
            phone = b.get('phone', '')
            hours = b.get('hours', 'จันทร์ - ศุกร์: 08:30 - 16:30 น.')
            floors = b.get('floorsCount', len(b.get('floors', [])) or 1)
            json_str = json.dumps(b, ensure_ascii=False)

            c.execute("""
            INSERT INTO `buildings` (`id`, `code`, `name`, `name_en`, `category_key`, `coords_y`, `coords_x`, `real_lat`, `real_lng`, `description`, `phone`, `hours`, `floors_count`, `json_data`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (b_id, b_code, b_name, b_name_en, b_cat, cy, cx, lat, lng, desc, phone, hours, floors, json_str))
        print(f"✅ Entity 3: buildings created & seeded ({len(buildings)} buildings)")

        # 4. Entity: students_roster (PK: student_id, FK: faculty_id -> faculties.faculty_id)
        c.execute("""
        CREATE TABLE `students_roster` (
            `student_id` VARCHAR(20) NOT NULL,
            `citizen_id` VARCHAR(20) DEFAULT NULL,
            `name` VARCHAR(150) NOT NULL,
            `name_en` VARCHAR(150) DEFAULT NULL,
            `faculty_id` INT DEFAULT 1,
            `major` VARCHAR(150) DEFAULT 'นักศึกษา',
            `status` ENUM('studying', 'graduated', 'resigned') DEFAULT 'studying',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`student_id`),
            KEY `idx_roster_faculty` (`faculty_id`),
            CONSTRAINT `fk_students_faculty` FOREIGN KEY (`faculty_id`) 
                REFERENCES `faculties` (`faculty_id`) ON UPDATE CASCADE ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        roster_file = BASE_DIR / 'data' / 'students_roster.json'
        roster = json.load(open(roster_file, encoding='utf-8'))
        for s in roster:
            sid = s.get('student_id')
            cid = s.get('citizen_id')
            sname = s.get('name')
            sname_en = s.get('name_en', '')
            sfac = s.get('faculty', 'มหาวิทยาลัยราชภัฏศรีสะเกษ')
            smaj = s.get('major', 'เทคโนโลยีดิจิทัล')
            c.execute("SELECT faculty_id FROM faculties WHERE faculty_name = %s LIMIT 1;", (sfac,))
            fac_row = c.fetchone()
            fac_id = fac_row[0] if fac_row else 1
            c.execute("""
            INSERT INTO `students_roster` (`student_id`, `citizen_id`, `name`, `name_en`, `faculty_id`, `major`)
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (sid, cid, sname, sname_en, fac_id, smaj))
        print(f"✅ Entity 4: students_roster created & seeded ({len(roster)} students)")

        # 5. Entity: users / accounts (PK: user_id, FK: student_id -> students_roster.student_id)
        c.execute("""
        CREATE TABLE `users` (
            `user_id` INT AUTO_INCREMENT,
            `username` VARCHAR(100) NOT NULL UNIQUE,
            `email` VARCHAR(150) UNIQUE DEFAULT NULL,
            `password_hash` VARCHAR(255) NOT NULL,
            `role` ENUM('admin', 'staff', 'student') NOT NULL DEFAULT 'student',
            `student_id` VARCHAR(20) DEFAULT NULL,
            `display_name` VARCHAR(150) DEFAULT NULL,
            `bio` TEXT DEFAULT NULL,
            `is_active` BOOLEAN DEFAULT TRUE,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`user_id`),
            KEY `idx_users_student` (`student_id`),
            CONSTRAINT `fk_users_student_id` FOREIGN KEY (`student_id`) 
                REFERENCES `students_roster` (`student_id`) ON UPDATE CASCADE ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Admin user
        c.execute("""
        INSERT INTO `users` (`username`, `email`, `password_hash`, `role`, `display_name`, `bio`)
        VALUES ('lnwpoon007x', 'mpoontv1234@gmail.com', '7b4e857416997d917f9fb57cf41865913e618e768e1ab30be70b13d2f9547d6e', 'admin', 'ผู้ดูแลระบบ (Admin)', 'Super Administrator of SSKRU Campus Map');
        """)

        acc_file = BASE_DIR / 'data' / 'user_accounts.json'
        accs = json.load(open(acc_file, encoding='utf-8'))
        for st in accs.get('students', []):
            sid = st.get('student_id')
            sname = st.get('name')
            phash = st.get('password_hash')
            email = f"stu{sid}@sskru.ac.th"
            c.execute("""
            INSERT INTO `users` (`username`, `email`, `password_hash`, `role`, `student_id`, `display_name`)
            VALUES (%s, %s, %s, 'student', %s, %s)
            ON DUPLICATE KEY UPDATE `display_name` = VALUES(`display_name`);
            """, (sid, email, phash, sid, sname))

        for sf in accs.get('staff', []):
            suser = sf.get('username')
            semail = sf.get('email')
            phash = sf.get('password_hash')
            c.execute("""
            INSERT INTO `users` (`username`, `email`, `password_hash`, `role`, `display_name`)
            VALUES (%s, %s, %s, 'staff', %s)
            ON DUPLICATE KEY UPDATE `email` = VALUES(`email`);
            """, (suser, semail, phash, suser))
        print("✅ Entity 5: users / accounts created & seeded")

        # 6. Entity: user_activity_logs (PK: log_id, FK: user_id -> users.user_id)
        c.execute("""
        CREATE TABLE `user_activity_logs` (
            `log_id` BIGINT AUTO_INCREMENT,
            `user_id` INT DEFAULT NULL,
            `identifier` VARCHAR(100) NOT NULL,
            `name` VARCHAR(150) NOT NULL,
            `role` VARCHAR(50) NOT NULL,
            `role_th` VARCHAR(100) DEFAULT NULL,
            `email` VARCHAR(150) DEFAULT NULL,
            `ip_address` VARCHAR(50) DEFAULT '127.0.0.1',
            `device` VARCHAR(50) DEFAULT 'Desktop',
            `os_name` VARCHAR(50) DEFAULT 'macOS',
            `browser` VARCHAR(50) DEFAULT 'Safari',
            `action` VARCHAR(100) DEFAULT 'เข้าสู่ระบบ (Login)',
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`log_id`),
            KEY `idx_logs_user` (`user_id`),
            CONSTRAINT `fk_logs_user_id` FOREIGN KEY (`user_id`) 
                REFERENCES `users` (`user_id`) ON UPDATE CASCADE ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        logs_file = BASE_DIR / 'data' / 'user_activity_logs.json'
        if logs_file.exists():
            logs = json.load(open(logs_file, encoding='utf-8'))
            for log in logs:
                uid_str = log.get('user_id', '')
                c.execute("SELECT user_id FROM users WHERE username = %s LIMIT 1;", (uid_str,))
                urow = c.fetchone()
                uid = urow[0] if urow else None
                
                name = log.get('name', '')
                role = log.get('role', '')
                role_th = log.get('role_th', '')
                email = log.get('email', '')
                ip = log.get('ip', '127.0.0.1')
                dev = log.get('device', 'Desktop')
                os_n = log.get('os', 'macOS')
                brw = log.get('browser', 'Safari')
                ts = log.get('timestamp', datetime.now().isoformat())
                try:
                    dt = datetime.fromisoformat(ts)
                except Exception:
                    dt = datetime.now()

                c.execute("""
                INSERT INTO `user_activity_logs` (`user_id`, `identifier`, `name`, `role`, `role_th`, `email`, `ip_address`, `device`, `os_name`, `browser`, `created_at`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (uid, uid_str, name, role, role_th, email, ip, dev, os_n, brw, dt))
            print(f"✅ Entity 6: user_activity_logs created & seeded ({len(logs)} logs)")

        # 7. Entity: password_resets (PK: reset_id)
        c.execute("""
        CREATE TABLE `password_resets` (
            `reset_id` BIGINT AUTO_INCREMENT,
            `student_id` VARCHAR(20) DEFAULT NULL,
            `username` VARCHAR(100) DEFAULT NULL,
            `email` VARCHAR(150) NOT NULL,
            `token` VARCHAR(64) NOT NULL UNIQUE,
            `otp` VARCHAR(10) NOT NULL,
            `expires_at` DATETIME NOT NULL,
            `is_used` BOOLEAN DEFAULT FALSE,
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`reset_id`),
            KEY `idx_reset_token` (`token`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        resets_file = BASE_DIR / 'data' / 'password_resets.json'
        if resets_file.exists():
            resets = json.load(open(resets_file, encoding='utf-8'))
            for r in resets:
                sid = r.get('student_id')
                uname = r.get('username')
                em = r.get('email', '')
                tok = r.get('token', '')
                otp = r.get('otp', '')
                try:
                    exp = datetime.fromisoformat(r.get('expires_at'))
                except Exception:
                    exp = datetime.now()
                try:
                    cat = datetime.fromisoformat(r.get('created_at'))
                except Exception:
                    cat = datetime.now()
                used = r.get('used', False)

                c.execute("""
                INSERT INTO `password_resets` (`student_id`, `username`, `email`, `token`, `otp`, `expires_at`, `is_used`, `created_at`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (sid, uname, em, tok, otp, exp, used, cat))
            print(f"✅ Entity 7: password_resets created & seeded ({len(resets)} resets)")

        # 8. Entity: admin_sessions (PK: session_id, FK: user_id -> users.user_id)
        c.execute("""
        CREATE TABLE `admin_sessions` (
            `session_id` BIGINT AUTO_INCREMENT,
            `token` VARCHAR(128) NOT NULL UNIQUE,
            `user_id` INT DEFAULT NULL,
            `is_active` BOOLEAN DEFAULT TRUE,
            `expires_at` DATETIME NOT NULL,
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`session_id`),
            KEY `idx_session_token` (`token`),
            CONSTRAINT `fk_sessions_user_id` FOREIGN KEY (`user_id`) 
                REFERENCES `users` (`user_id`) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        print("✅ Entity 8: admin_sessions created")

        c.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("\n🎉 ALL 8 ENTITIES WITH PROPER PK, FK, ATTRIBUTES AND DATA SUCCESSFULLY DEPLOYED TO PHPMYADMIN / MYSQL!")

    conn.close()

if __name__ == '__main__':
    run_migration()

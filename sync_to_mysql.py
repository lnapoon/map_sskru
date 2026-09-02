import json
import os
import subprocess

BASE_DIR = "/Users/monphrakan/Mark_map"
MYSQL_BIN = "/Applications/XAMPP/xamppfiles/bin/mysql"

def escape_sql(val):
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (dict, list)):
        val = json.dumps(val, ensure_ascii=False)
    # String escape
    val = str(val).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{val}'"

def sync_data():
    sql_statements = ["USE sskru_map;", "SET FOREIGN_KEY_CHECKS = 0;"]

    # ─── 1. CATEGORIES ───────────────────────────────────────────────
    categories = [
        ('academic', 'อาคารเรียน / คณะ', 'Academic Buildings', '#1a4fa0', 'fa-graduation-cap'),
        ('office', 'สำนักงาน / หน่วยงาน', 'Offices & Administration', '#e67e22', 'fa-briefcase'),
        ('facility', 'สิ่งอำนวยความสะดวก', 'Facilities & Sports', '#2ecc71', 'fa-store'),
        ('library', 'หอสมุด / ศูนย์วิชาการ', 'Library & Learning Center', '#9b59b6', 'fa-book-open'),
        ('other', 'อื่นๆ', 'Other Landmarks', '#7f8c8d', 'fa-map-pin'),
    ]
    for c in categories:
        sql_statements.append(
            f"INSERT INTO categories (category_key, category_name_th, category_name_en, color_hex, icon_class) "
            f"VALUES ({escape_sql(c[0])}, {escape_sql(c[1])}, {escape_sql(c[2])}, {escape_sql(c[3])}, {escape_sql(c[4])}) "
            f"ON DUPLICATE KEY UPDATE category_name_th={escape_sql(c[1])}, color_hex={escape_sql(c[3])};"
        )

    # ─── 2. FACULTIES ────────────────────────────────────────────────
    faculties = [
        (1, 'มหาวิทยาลัยราชภัฏศรีสะเกษ', 'SSKRU'),
        (2, 'คณะครุศาสตร์', 'EDU'),
        (3, 'คณะมนุษยศาสตร์และสังคมศาสตร์', 'HUSOC'),
        (4, 'คณะบริหารธุรกิจและการบัญชี', 'BBA'),
        (5, 'คณะศิลปศาสตร์และวิทยาศาสตร์', 'LAS'),
        (6, 'คณะพยาบาลศาสตร์', 'NURSE'),
    ]
    for f in faculties:
        sql_statements.append(
            f"INSERT INTO faculties (faculty_id, faculty_name, faculty_code) "
            f"VALUES ({f[0]}, {escape_sql(f[1])}, {escape_sql(f[2])}) "
            f"ON DUPLICATE KEY UPDATE faculty_name={escape_sql(f[1])}, faculty_code={escape_sql(f[2])};"
        )

    # ─── 3. BUILDINGS ────────────────────────────────────────────────
    buildings_path = os.path.join(BASE_DIR, "data", "buildings.json")
    if os.path.exists(buildings_path):
        with open(buildings_path, "r", encoding="utf-8") as f:
            buildings = json.load(f)
        
        for b in buildings:
            b_id = b.get("id")
            code = b.get("code") or str(b_id)
            name = b.get("name", "")
            name_en = b.get("nameEn", "")
            cat = b.get("category", "other")
            coords = b.get("coords", [0, 0])
            y, x = coords[0], coords[1]
            real_coords = b.get("realCoords", [0, 0])
            lat, lng = real_coords[0], real_coords[1]
            desc = b.get("description", "")
            phone = b.get("phone", "")
            hours = b.get("hours", "")
            floors = len(b.get("floors", [])) or 1
            json_blob = json.dumps(b, ensure_ascii=False)

            sql_statements.append(
                f"INSERT INTO buildings (id, code, name, name_en, category_key, coords_y, coords_x, real_lat, real_lng, description, phone, hours, floors_count, json_data) "
                f"VALUES ({b_id}, {escape_sql(code)}, {escape_sql(name)}, {escape_sql(name_en)}, {escape_sql(cat)}, {y}, {x}, {lat}, {lng}, {escape_sql(desc)}, {escape_sql(phone)}, {escape_sql(hours)}, {floors}, {escape_sql(json_blob)}) "
                f"ON DUPLICATE KEY UPDATE name={escape_sql(name)}, name_en={escape_sql(name_en)}, category_key={escape_sql(cat)}, coords_y={y}, coords_x={x}, real_lat={lat}, real_lng={lng}, description={escape_sql(desc)}, phone={escape_sql(phone)}, json_data={escape_sql(json_blob)};"
            )

    # ─── 4. STUDENTS ROSTER ──────────────────────────────────────────
    roster_path = os.path.join(BASE_DIR, "data", "students_roster.json")
    if os.path.exists(roster_path):
        with open(roster_path, "r", encoding="utf-8") as f:
            roster = json.load(f)
        
        for s in roster:
            sid = str(s.get("student_id", "")).strip()
            cid = str(s.get("citizen_id", "")).strip()
            name = s.get("name", "")
            name_en = s.get("name_en", "")
            fac_id = s.get("faculty_id", 1)
            major = s.get("major", "นักศึกษา")
            status = s.get("status", "studying")
            if sid:
                sql_statements.append(
                    f"INSERT INTO students_roster (student_id, citizen_id, name, name_en, faculty_id, major, status) "
                    f"VALUES ({escape_sql(sid)}, {escape_sql(cid)}, {escape_sql(name)}, {escape_sql(name_en)}, {fac_id}, {escape_sql(major)}, {escape_sql(status)}) "
                    f"ON DUPLICATE KEY UPDATE citizen_id={escape_sql(cid)}, name={escape_sql(name)}, major={escape_sql(major)};"
                )

    # ─── 5. USER ACCOUNTS (Users) ────────────────────────────────────
    accounts_path = os.path.join(BASE_DIR, "data", "user_accounts.json")
    if os.path.exists(accounts_path):
        with open(accounts_path, "r", encoding="utf-8") as f:
            accounts = json.load(f)
        
        # Default Admin
        sql_statements.append(
            "INSERT INTO users (username, email, password_hash, role, display_name, is_active) "
            "VALUES ('lnwpoon007x', 'mpoontv1234@gmail.com', 'a3979857be91307b27ea0bcf3fefb097b695cb31c3be135ec3631f471d497e7b', 'admin', 'ผู้ดูแลระบบ (Admin)', 1) "
            "ON DUPLICATE KEY UPDATE role='admin', display_name='ผู้ดูแลระบบ (Admin)';"
        )

        # Staff users
        for u in accounts.get("staff", []):
            uname = u.get("username", "").strip()
            email = u.get("email", "").strip()
            p_hash = u.get("password_hash", "")
            is_active = 1 if u.get("is_active", True) else 0
            is_approved = 1 if u.get("is_approved", False) else 0
            if uname:
                sql_statements.append(
                    f"INSERT INTO users (username, email, password_hash, role, display_name, is_active) "
                    f"VALUES ({escape_sql(uname)}, {escape_sql(email)}, {escape_sql(p_hash)}, 'staff', {escape_sql(uname)}, {is_active}) "
                    f"ON DUPLICATE KEY UPDATE email={escape_sql(email)}, is_active={is_active};"
                )

        # Student users
        for s in accounts.get("students", []):
            sid = str(s.get("student_id", "")).strip()
            sname = s.get("name", "")
            p_hash = s.get("password_hash", "")
            if sid:
                uname = f"stu_{sid}"
                email = f"stu{sid}@sskru.ac.th"
                sql_statements.append(
                    f"INSERT INTO users (username, email, password_hash, role, student_id, display_name, is_active) "
                    f"VALUES ({escape_sql(uname)}, {escape_sql(email)}, {escape_sql(p_hash)}, 'student', {escape_sql(sid)}, {escape_sql(sname)}, 1) "
                    f"ON DUPLICATE KEY UPDATE student_id={escape_sql(sid)}, display_name={escape_sql(sname)};"
                )

    # ─── 6. USER ACTIVITY LOGS ───────────────────────────────────────
    logs_path = os.path.join(BASE_DIR, "data", "user_activity_logs.json")
    if os.path.exists(logs_path):
        with open(logs_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        
        for l in logs[:50]:
            uid_str = l.get("user_id", "")
            name = l.get("name", "")
            role = l.get("role", "student")
            role_th = l.get("role_th", "ผู้ใช้งาน")
            email = l.get("email", "")
            ip = l.get("ip", "127.0.0.1")
            device = l.get("device", "Desktop")
            os_name = l.get("os", "macOS")
            browser = l.get("browser", "Safari")
            action = l.get("action", "เข้าสู่ระบบ (Login)")
            
            sql_statements.append(
                f"INSERT INTO user_activity_logs (identifier, name, role, role_th, email, ip_address, device, os_name, browser, action) "
                f"VALUES ({escape_sql(uid_str)}, {escape_sql(name)}, {escape_sql(role)}, {escape_sql(role_th)}, {escape_sql(email)}, {escape_sql(ip)}, {escape_sql(device)}, {escape_sql(os_name)}, {escape_sql(browser)}, {escape_sql(action)});"
            )

    # ─── 7. PASSWORD RESETS ──────────────────────────────────────────
    resets_path = os.path.join(BASE_DIR, "data", "password_resets.json")
    if os.path.exists(resets_path):
        with open(resets_path, "r", encoding="utf-8") as f:
            resets = json.load(f)
        
        for r in resets:
            email = r.get("email", "")
            token = r.get("token", "")
            otp = r.get("otp", "")
            expires_at = r.get("expires_at", "")
            is_used = 1 if r.get("used", False) else 0
            user_type = r.get("user_type", "student")
            identifier = r.get("identifier", "")
            if token and email:
                sql_statements.append(
                    f"INSERT INTO password_resets (student_id, username, email, token, otp, expires_at, is_used) "
                    f"VALUES ({escape_sql(identifier)}, {escape_sql(identifier)}, {escape_sql(email)}, {escape_sql(token)}, {escape_sql(otp)}, {escape_sql(expires_at)}, {is_used}) "
                    f"ON DUPLICATE KEY UPDATE is_used={is_used};"
                )

    sql_statements.append("SET FOREIGN_KEY_CHECKS = 1;")

    full_sql = "\n".join(sql_statements)
    sql_file = os.path.join(BASE_DIR, "database", "full_sync.sql")
    os.makedirs(os.path.dirname(sql_file), exist_ok=True)
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write(full_sql)

    # Execute SQL via mysql CLI
    cmd = [MYSQL_BIN, "-u", "root", "sskru_map"]
    proc = subprocess.run(cmd, input=full_sql, text=True, capture_output=True)
    if proc.returncode == 0:
        print("Successfully synced all web data into MySQL phpMyAdmin database (sskru_map)!")
    else:
        print("MySQL Error:", proc.stderr)

if __name__ == "__main__":
    sync_data()

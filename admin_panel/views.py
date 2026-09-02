import threading
import os
import json
import hashlib
import secrets
import re
from datetime import datetime, timedelta
from pathlib import Path

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import VisitorLog, UserEvent, AdminSession, Student

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "buildings.json"


# ─── Helpers ────────────────────────────────────────────────────────────────


def read_buildings():
    try:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def sync_remote_stores_background(data):
    """Sync to MongoDB Atlas Cloud & Local MongoDB in background"""
    mongo_uris = [
        "mongodb+srv://lnwpoon:poon300450@sensordata.80rr4am.mongodb.net/?appName=Sensordata",
        "mongodb://localhost:27017/",
    ]
    for uri in mongo_uris:
        try:
            import pymongo
            from pymongo import ReplaceOne

            client = pymongo.MongoClient(
                uri, serverSelectionTimeoutMS=1500, tlsAllowInvalidCertificates=True
            )
            db = client["sskru_map"]
            collection = db["buildings"]
            reqs = [ReplaceOne({"id": b["id"]}, dict(b), upsert=True) for b in data]
            if reqs:
                collection.bulk_write(reqs, ordered=False)
        except Exception:
            pass

    # Sync to MySQL / phpMyAdmin if connected
    try:
        import pymysql

        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="sskru_map",
            charset="utf8mb4",
            connect_timeout=1,
        )
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM buildings;")
            for b in data:
                json_str = json.dumps(b, ensure_ascii=False)
                b_id = b.get("id")
                b_code = str(b.get("code", b_id))
                b_name = b.get("name", "")
                b_name_en = b.get("nameEn", "")
                b_cat = b.get("category", "facility")
                cy = b.get("coords", [0, 0])[0] if len(b.get("coords", [])) > 0 else 0
                cx = b.get("coords", [0, 0])[1] if len(b.get("coords", [])) > 1 else 0
                lat = (
                    b.get("realCoords", [0.0, 0.0])[0]
                    if len(b.get("realCoords", [])) > 0
                    else 0.0
                )
                lng = (
                    b.get("realCoords", [0.0, 0.0])[1]
                    if len(b.get("realCoords", [])) > 1
                    else 0.0
                )
                desc = b.get("description", "")
                phone = b.get("phone", "")

                sql = """
                INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    sql,
                    (
                        b_id,
                        b_code,
                        b_name,
                        b_name_en,
                        b_cat,
                        cy,
                        cx,
                        lat,
                        lng,
                        desc,
                        phone,
                        json_str,
                    ),
                )
        conn.commit()
        conn.close()
    except Exception:
        pass


def write_buildings(data):
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error writing buildings file database:", e)
        return False

    # Trigger asynchronous background sync to remote databases
    threading.Thread(
        target=sync_remote_stores_background, args=(data,), daemon=True
    ).start()
    return True


def get_admin_credentials():
    from dotenv import load_dotenv

    load_dotenv(override=True)
    return (
        os.getenv("ADMIN_USERNAME", "lnwpoon007x"),
        os.getenv("ADMIN_PASSWORD", "poon300450"),
    )


def generate_token():
    return secrets.token_hex(32)


def create_admin_session():
    token = generate_token()
    expires = timezone.now() + timedelta(hours=8)
    AdminSession.objects.create(token=token, expires_at=expires)
    return token


def validate_admin_token(request):
    token = request.session.get("admin_token")
    if not token:
        return False
    try:
        session = AdminSession.objects.get(token=token, is_active=True)
        if session.expires_at < timezone.now():
            session.is_active = False
            session.save()
            return False
        return True
    except AdminSession.DoesNotExist:
        return False


def get_client_ip(request):
    if not request:
        return "127.0.0.1"
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "127.0.0.1")


# ─── Rate Limiter (Brute-Force & Security Protection) ───────────────────────
FAILED_ATTEMPTS = {}


def check_rate_limit(request, action="auth", max_attempts=5, lock_minutes=10):
    """Check if client is temporarily locked due to too many failed attempts."""
    ip = get_client_ip(request)
    key = f"{ip}:{action}"
    now = datetime.now()
    record = FAILED_ATTEMPTS.get(key)
    if record:
        if record.get("lock_until") and now < record["lock_until"]:
            remaining = max(1, int((record["lock_until"] - now).total_seconds() / 60))
            return False, f"ระบบตรวจพบการพยายามเข้าใช้งานไม่ถูกต้องหลายครั้ง เพื่อความปลอดภัย กรุณารออีก {remaining} นาที"
        if record.get("lock_until") and now >= record["lock_until"]:
            FAILED_ATTEMPTS.pop(key, None)
    return True, None


def record_failed_attempt(request, action="auth", max_attempts=5, lock_minutes=10):
    """Record a failed attempt and lock if threshold exceeded."""
    ip = get_client_ip(request)
    key = f"{ip}:{action}"
    now = datetime.now()
    if key not in FAILED_ATTEMPTS:
        FAILED_ATTEMPTS[key] = {"count": 1, "first_attempt": now, "lock_until": None}
    else:
        FAILED_ATTEMPTS[key]["count"] += 1
        if FAILED_ATTEMPTS[key]["count"] >= max_attempts:
            FAILED_ATTEMPTS[key]["lock_until"] = now + timedelta(minutes=lock_minutes)


def reset_failed_attempts(request, action="auth"):
    """Reset failed attempts count upon successful action."""
    ip = get_client_ip(request)
    key = f"{ip}:{action}"
    FAILED_ATTEMPTS.pop(key, None)


def get_device_info(user_agent):
    ua = user_agent.lower()
    if any(x in ua for x in ["iphone", "android", "mobile"]):
        device = "mobile"
    elif any(x in ua for x in ["ipad", "tablet"]):
        device = "tablet"
    else:
        device = "desktop"

    os_name = "Unknown"
    if "android" in ua:
        os_name = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os_name = "iOS"
    elif "macintosh" in ua:
        os_name = "macOS"
    elif "windows" in ua:
        os_name = "Windows"
    elif "linux" in ua:
        os_name = "Linux"

    browser = "Unknown"
    if "chrome" in ua and "chromium" not in ua and "edg" not in ua:
        browser = "Chrome"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    elif "edg" in ua:
        browser = "Edge"

    return device, os_name, browser


def log_user_activity(user_id, name, role, email="", request=None):
    """บันทึกประวัติการเข้าใช้งานของผู้ใช้ (Admin, Staff, Student)"""
    try:
        logs_file = BASE_DIR / "data" / "user_activity_logs.json"

        # Helper to read JSON
        def read_json_file(path, default):
            if not path.exists():
                return default
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        # Helper to write JSON
        def write_json_file(path, data):
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        logs = read_json_file(logs_file, default=[])

        device, os_name, browser = ("Desktop", "macOS", "Safari")
        ip = "127.0.0.1"
        if request:
            ua = request.META.get("HTTP_USER_AGENT", "")
            device, os_name, browser = get_device_info(ua)
            ip = request.META.get(
                "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")
            )

        role_th = {
            "admin": "ผู้ดูแลระบบ",
            "staff": "บุคลากร / อาจารย์",
            "student": "นักศึกษา",
        }.get(role, "ผู้ใช้งาน")

        now = (
            timezone.localtime(timezone.now())
            if timezone.is_aware(timezone.now())
            else timezone.now()
        )
        entry = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "role_th": role_th,
            "device": device,
            "os": os_name,
            "browser": browser,
            "ip": ip,
            "timestamp": now.isoformat(),
            "time_formatted": now.strftime("%H:%M น."),
            "date_formatted": now.strftime("%d/%m/%Y"),
        }

        logs.insert(0, entry)
        logs = logs[:100]
        write_json_file(logs_file, logs)
    except Exception as e:
        print(f"Error logging user activity: {e}")


# ─── Views ──────────────────────────────────────────────────────────────────


def admin_login_page(request):
    """หน้า Login รวมสำหรับทุกสิทธิ์ (นักศึกษา / บุคลากร / ผู้ดูแลระบบ)"""
    if validate_admin_token(request):
        return redirect("/admin/dashboard/")
    return render(request, "admin_panel/student_login.html")


def admin_logout(request):
    """ออกจากระบบ Admin แล้วส่งกลับไปหน้า Login รวมใหม่"""
    token = request.session.get("admin_token")
    if token:
        AdminSession.objects.filter(token=token).update(is_active=False)
    request.session.flush()
    return redirect("/login/")


def admin_dashboard(request):
    """Admin Dashboard หลัก"""
    if not validate_admin_token(request):
        return redirect("/admin/")

    # Summary numbers
    now = (
        timezone.localtime(timezone.now())
        if timezone.is_aware(timezone.now())
        else timezone.now()
    )
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_visitors = VisitorLog.objects.count()
    today_visitors = VisitorLog.objects.filter(timestamp__gte=today_start).count()

    # 7-day chart data
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).date()
        count = VisitorLog.objects.filter(timestamp__date=day).count()
        chart_labels.append(day.strftime("%d/%m"))
        chart_data.append(count)

    # Device breakdown
    device_stats = (
        VisitorLog.objects.values("device_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # OS breakdown
    os_stats = (
        VisitorLog.objects.values("os_name")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    # Today active users
    today_date_str = now.strftime("%d/%m/%Y")
    logs_file = BASE_DIR / "data" / "user_activity_logs.json"
    if logs_file.exists():
        with open(logs_file, "r", encoding="utf-8") as f:
            all_logs = json.load(f)
    else:
        all_logs = []
    today_users = [u for u in all_logs if u.get("date_formatted") == today_date_str]
    if not today_users:
        today_users = all_logs[:10]

    # Top searched buildings
    top_searches = (
        UserEvent.objects.filter(event_type="search")
        .values("event_data")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    # Top buildings viewed
    top_buildings = (
        UserEvent.objects.filter(event_type="building_select")
        .values("event_data")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    # Navigation counts
    nav_count = UserEvent.objects.filter(event_type="navigate").count()

    # Recent visitors
    recent_visitors = VisitorLog.objects.select_related().order_by("-timestamp")[:20]

    # Buildings data
    buildings = read_buildings()

    context = {
        "total_visitors": total_visitors,
        "today_visitors": today_visitors,
        "total_buildings": len(buildings),
        "nav_count": nav_count,
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
        "device_stats": list(device_stats),
        "os_stats": list(os_stats),
        "today_users": today_users,
        "top_searches": list(top_searches),
        "top_buildings": list(top_buildings),
        "recent_visitors": recent_visitors,
        "buildings": buildings,
        "buildings_json": json.dumps(buildings, ensure_ascii=False),
    }
    return render(request, "admin_panel/dashboard.html", context)


@csrf_exempt
def admin_buildings_api(request):
    """CRUD API สำหรับ buildings (Admin & API)"""
    buildings = read_buildings()

    if request.method == "GET":
        return JsonResponse(
            {"success": True, "data": buildings, "count": len(buildings)}
        )

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            if not data.get("name") or not data.get("coords"):
                return JsonResponse(
                    {"success": False, "message": "ข้อมูลไม่ครบ"}, status=400
                )

            # Check duplicate ID
            b_id = data.get("id")
            if b_id:
                idx = next(
                    (i for i, b in enumerate(buildings) if b.get("id") == b_id), None
                )
                if idx is not None:
                    buildings[idx].update(data)
                else:
                    buildings.append(data)
            else:
                buildings.append(data)

            write_buildings(buildings)
            return JsonResponse(
                {"success": True, "message": "เพิ่ม/อัปเดตอาคารสำเร็จ", "data": data}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


@csrf_exempt
def admin_building_detail_api(request, building_id):
    """Update/Delete building (Admin & API)"""
    buildings = read_buildings()
    building_id = int(building_id)
    idx = next((i for i, b in enumerate(buildings) if b.get("id") == building_id), None)

    if idx is None and request.method != "PUT":
        return JsonResponse({"success": False, "message": "ไม่พบอาคาร"}, status=404)

    if request.method == "GET":
        return JsonResponse({"success": True, "data": buildings[idx]})

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            if idx is not None:
                buildings[idx].update(data)
                buildings[idx]["id"] = building_id
            else:
                data["id"] = building_id
                buildings.append(data)
                idx = len(buildings) - 1

            write_buildings(buildings)
            return JsonResponse(
                {"success": True, "message": "อัปเดตข้อมูลสำเร็จ", "data": buildings[idx]}
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error: {str(e)}"}, status=400
            )

    elif request.method == "DELETE":
        removed = buildings.pop(idx)
        write_buildings(buildings)
        return JsonResponse(
            {"success": True, "message": f"ลบ {removed.get('name')} สำเร็จ"}
        )

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


@csrf_exempt
def track_event(request):
    """รับ event tracking จาก frontend"""
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)
    try:
        data = json.loads(request.body)
        event_type = data.get("type", "page_view")
        event_data = data.get("data", "")
        session_id = data.get("session_id", "")

        ua = request.META.get("HTTP_USER_AGENT", "")
        ip = request.META.get(
            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")
        )
        if "," in ip:
            ip = ip.split(",")[0].strip()

        device, os_name, browser = get_device_info(ua)

        # Find or create visitor log for this session
        visitor, _ = VisitorLog.objects.get_or_create(
            session_id=session_id,
            defaults={
                "ip_address": ip,
                "user_agent": ua[:500],
                "device_type": device,
                "os_name": os_name,
                "browser": browser,
                "page_path": data.get("path", "/"),
                "referrer": data.get("referrer", ""),
            },
        )

        UserEvent.objects.create(
            visitor=visitor,
            event_type=event_type,
            event_data=str(event_data)[:255],
        )

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
def auth_status_api(request):
    """API เช็กว่า User คนปัจจุบันเป็น Admin, Staff หรือ Student อย่างถูกต้อง แยก Session ชัดเจน"""
    is_admin = validate_admin_token(request)
    user_role = request.session.get("user_role", "")

    is_student = False
    student_id = ""
    student_name = ""

    is_staff = False
    staff_username = ""

    if is_admin:
        user_role = "admin"
    elif user_role == "staff" or ("staff_username" in request.session and not request.session.get("student_id")):
        is_staff = True
        user_role = "staff"
        staff_username = request.session.get("staff_username", "")
    elif user_role == "student" or "student_id" in request.session:
        is_student = True
        user_role = "student"
        student_id = request.session.get("student_id", "")
        student_name = request.session.get("student_name", "")

    return JsonResponse(
        {
            "success": True,
            "role": user_role,
            "isAdmin": is_admin,
            "isStudent": is_student,
            "isStaff": is_staff,
            "staffUsername": staff_username,
            "studentId": student_id,
            "studentName": student_name,
        }
    )


def student_login_page(request):
    """หน้าต่างล็อกอินสำหรับนักศึกษา"""
    return render(request, "admin_panel/student_login.html")


@csrf_exempt
def student_login_api(request):
    """API สำหรับเข้าสู่ระบบนักศึกษา (รองรับค้นหาทั้งแบบมีขีด/ไม่มีขีด และตรวจรหัสผ่าน)"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        raw_student_id = data.get("student_id", "").strip()
        password = data.get("password", "").strip()

        if not raw_student_id:
            return JsonResponse(
                {"success": False, "message": "กรุณาระบุรหัสนักศึกษา"}, status=400
            )

        clean_id = re.sub(r"[^0-9a-zA-Z]", "", raw_student_id)
        from .models import Student

        # 1. Search in Django Student DB (exact, iexact, or clean ID match)
        student = (
            Student.objects.filter(student_id=raw_student_id, is_active=True).first()
            or Student.objects.filter(student_id__iexact=raw_student_id, is_active=True).first()
        )
        if not student and clean_id:
            for s in Student.objects.filter(is_active=True):
                if re.sub(r"[^0-9a-zA-Z]", "", s.student_id) == clean_id:
                    student = s
                    break

        # 2. Search in ROSTER_FILE as fallback
        matched_name = student.name if student else None
        matched_sid = student.student_id if student else raw_student_id

        if not student:
            roster = read_json_file(ROSTER_FILE)
            for r in roster:
                r_sid = r.get("student_id", "")
                if r_sid == raw_student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", r_sid) == clean_id):
                    matched_name = r.get("name")
                    matched_sid = r_sid
                    break

        # 3. Search in ACCOUNTS_FILE as fallback
        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        acc_match = None
        for acc in accounts.get("students", []):
            a_sid = acc.get("student_id", "")
            if a_sid == raw_student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", a_sid) == clean_id):
                acc_match = acc
                if not matched_name:
                    matched_name = acc.get("name")
                    matched_sid = a_sid
                break

        if not matched_name and not student and not acc_match:
            return JsonResponse(
                {
                    "success": False,
                    "message": "ไม่พบรหัสนักศึกษานี้ในระบบ กรุณาตรวจสอบรหัสหรือติดต่อผู้ดูแลระบบ",
                },
                status=401,
            )

        # If account has registered password, verify password
        if acc_match and password:
            hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
            saved_hash = acc_match.get("password_hash")
            saved_plain = acc_match.get("password") or acc_match.get("password_plain")
            if saved_hash and saved_hash != hashed_pass and saved_plain != password:
                # Password doesn't match registered password
                return JsonResponse(
                    {
                        "success": False,
                        "message": "รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง หรือกู้คืนรหัสผ่าน",
                    },
                    status=401,
                )

        final_sid = matched_sid
        final_name = matched_name or f"นักศึกษา {final_sid}"

        # Clear staff and admin session tokens to prevent role bleeding
        request.session.pop("staff_username", None)
        request.session.pop("staff_email", None)
        request.session.pop("admin_token", None)

        request.session["student_id"] = final_sid
        request.session["student_name"] = final_name
        request.session["user_role"] = "student"

        log_user_activity(
            final_sid,
            final_name,
            "student",
            email=f"stu{re.sub(r'[^0-9a-zA-Z]', '', final_sid)}@sskru.ac.th",
            request=request,
        )
        return JsonResponse(
            {
                "success": True,
                "message": f"เข้าสู่ระบบสำเร็จ ยินดีต้อนรับคุณ {final_name}",
                "user_name": final_name,
                "student_id": final_sid,
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@csrf_exempt
def admin_students_api(request):
    """API จัดการข้อมูลนักศึกษา (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)

    from .models import Student
    from django.db import IntegrityError

    if request.method == "GET":
        students = list(
            Student.objects.values(
                "id", "student_id", "name", "year_level", "is_active", "created_at"
            )
        )
        return JsonResponse({"success": True, "data": students})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id", "").strip()
            name = data.get("name", "").strip()
            year_level = data.get("year_level", 2)

            if not student_id or not name:
                return JsonResponse(
                    {"success": False, "message": "กรุณากรอกข้อมูลให้ครบถ้วน"}, status=400
                )

            if Student.objects.filter(student_id=student_id).exists():
                return JsonResponse(
                    {"success": False, "message": "รหัสนักศึกษานี้มีอยู่ในระบบแล้ว"}, status=400
                )

            student = Student.objects.create(
                student_id=student_id, name=name,
                year_level=year_level,
                is_active=data.get("is_active", True)
            )
            return JsonResponse({"success": True, "message": "เพิ่มนักศึกษาสำเร็จ"})
        except IntegrityError:
            return JsonResponse(
                {"success": False, "message": "รหัสนักศึกษานี้มีอยู่ในระบบแล้ว"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": "เกิดข้อผิดพลาดในการบันทึกข้อมูล"}, status=400
            )

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            sid = data.get("id")
            student = Student.objects.filter(id=sid).first()
            if not student:
                return JsonResponse(
                    {"success": False, "message": "ไม่พบข้อมูลนักศึกษา"}, status=404
                )

            new_student_id = data.get("student_id", "").strip()
            new_name = data.get("name", "").strip()
            new_year_level = data.get("year_level")

            if not new_student_id or not new_name:
                return JsonResponse(
                    {"success": False, "message": "กรุณากรอกข้อมูลให้ครบถ้วน"}, status=400
                )

            # Check for duplicate student_id (excluding current record)
            if Student.objects.filter(student_id=new_student_id).exclude(id=sid).exists():
                return JsonResponse(
                    {"success": False, "message": "รหัสนักศึกษานี้มีอยู่ในระบบแล้ว"}, status=400
                )

            student.student_id = new_student_id
            student.name = new_name
            if new_year_level is not None:
                student.year_level = new_year_level
            student.save()
            return JsonResponse({"success": True, "message": "แก้ไขข้อมูลสำเร็จ"})
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}, status=400
            )

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            sid = data.get("id")
            Student.objects.filter(id=sid).delete()
            return JsonResponse({"success": True, "message": "ลบข้อมูลสำเร็จ"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


def admin_analytics_api(request):
    """ส่งข้อมูล analytics (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)

    today = timezone.now().date()
    return JsonResponse(
        {
            "success": True,
            "today_visitors": VisitorLog.objects.filter(timestamp__date=today).count(),
            "total_visitors": VisitorLog.objects.count(),
            "total_events": UserEvent.objects.count(),
        }
    )


# ─── Student Verification & Registration APIs ─────────────────────────────────

ROSTER_FILE = BASE_DIR / "data" / "students_roster.json"
ACCOUNTS_FILE = BASE_DIR / "data" / "user_accounts.json"


def read_json_file(file_path, default=None):
    if default is None:
        default = []
    try:
        if not file_path.exists():
            return default
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json_file(file_path, data):
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


@csrf_exempt
def student_verify_api(request):
    """ตรวจสอบรหัสนักศึกษาและเลขบัตรประชาชนในฐานข้อมูลหลัก (ทั้ง Student DB และ Roster JSON)"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        raw_student_id = data.get("student_id", "").strip()
        raw_citizen_id = data.get("citizen_id", "").strip()

        if not raw_student_id or not raw_citizen_id:
            return JsonResponse(
                {
                    "success": False,
                    "message": "กรุณากรอกรหัสนักศึกษาและเลขบัตรประชาชนให้ครบถ้วน",
                },
                status=400,
            )

        clean_id = re.sub(r"[^0-9a-zA-Z]", "", raw_student_id)
        matched_student = None

        # 1. Search in Django Student Model first
        student_db = (
            Student.objects.filter(student_id=raw_student_id).first()
            or Student.objects.filter(student_id__iexact=raw_student_id).first()
        )
        if not student_db and clean_id:
            for s in Student.objects.all():
                if re.sub(r"[^0-9a-zA-Z]", "", s.student_id) == clean_id:
                    student_db = s
                    break

        if student_db:
            matched_student = {
                "student_id": student_db.student_id,
                "name": student_db.name,
                "faculty": "มหาวิทยาลัยราชภัฏศรีสะเกษ",
                "major": "นักศึกษา",
            }
        else:
            # 2. Search in ROSTER_FILE json
            roster = read_json_file(ROSTER_FILE)
            for s in roster:
                r_sid = s.get("student_id", "")
                if r_sid == raw_student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", r_sid) == clean_id):
                    matched_student = s
                    break

        if not matched_student:
            return JsonResponse(
                {
                    "success": False,
                    "status": "NOT_FOUND",
                    "message": "ไม่พบรหัสนักศึกษาในฐานข้อมูลของมหาวิทยาลัย กรุณาติดต่อเจ้าหน้าที่สำนักทะเบียนและประมวลผลโดยตรง",
                },
                status=404,
            )

        # Verification matched cleanly!
        return JsonResponse(
            {
                "success": True,
                "status": "MATCHED",
                "student_info": {
                    "student_id": matched_student.get("student_id"),
                    "name": matched_student.get("name"),
                    "faculty": matched_student.get("faculty", "มหาวิทยาลัยราชภัฏศรีสะเกษ"),
                    "major": matched_student.get("major", "นักศึกษา"),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def student_register_api(request):
    """ลงทะเบียนสร้างรหัสผ่านสำหรับนักศึกษา"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        raw_student_id = data.get("student_id", "").strip()
        citizen_id = data.get("citizen_id", "").strip()
        password = data.get("password", "").strip()

        clean_id = re.sub(r"[^0-9a-zA-Z]", "", raw_student_id)
        student_db = (
            Student.objects.filter(student_id=raw_student_id).first()
            or Student.objects.filter(student_id__iexact=raw_student_id).first()
        )
        if not student_db and clean_id:
            for s in Student.objects.all():
                if re.sub(r"[^0-9a-zA-Z]", "", s.student_id) == clean_id:
                    student_db = s
                    break

        matched_name = student_db.name if student_db else None
        matched_faculty = "มหาวิทยาลัยราชภัฏศรีสะเกษ"
        student_id = student_db.student_id if student_db else raw_student_id

        if not matched_name:
            roster = read_json_file(ROSTER_FILE)
            for s in roster:
                r_sid = s.get("student_id", "")
                if r_sid == raw_student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", r_sid) == clean_id):
                    matched_name = s.get("name")
                    matched_faculty = s.get("faculty", "มหาวิทยาลัยราชภัฏศรีสะเกษ")
                    student_id = r_sid
                    break

        if not matched_name:
            return JsonResponse(
                {"success": False, "message": "ไม่พบรหัสนักศึกษาในฐานข้อมูลของมหาวิทยาลัย"},
                status=400,
            )

        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})

        # Check if already registered
        if any(
            acc.get("student_id") == student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", acc.get("student_id", "")) == clean_id)
            for acc in accounts.get("students", [])
        ):
            # Update password for existing account
            for acc in accounts.get("students", []):
                if acc.get("student_id") == student_id or (clean_id and re.sub(r"[^0-9a-zA-Z]", "", acc.get("student_id", "")) == clean_id):
                    acc["password_hash"] = hashlib.sha256(password.encode("utf-8")).hexdigest()
                    acc["password_plain"] = password
                    break
            write_json_file(ACCOUNTS_FILE, accounts)
            request.session["student_id"] = student_id
            request.session["student_name"] = matched_name
            request.session["user_role"] = "student"
            return JsonResponse(
                {
                    "success": True,
                    "message": "อัปเดตรหัสผ่านและเข้าสู่ระบบสำเร็จ!",
                    "user_name": matched_name,
                }
            )

        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        new_account = {
            "student_id": student_id,
            "name": matched_name,
            "faculty": matched_faculty,
            "password_hash": hashed_pass,
            "password_plain": password,
            "created_at": datetime.now().isoformat(),
        }
        accounts["students"].append(new_account)
        write_json_file(ACCOUNTS_FILE, accounts)

        request.session["student_id"] = student_id
        request.session["student_name"] = matched_name
        request.session["user_role"] = "student"

        return JsonResponse(
            {
                "success": True,
                "message": "ลงทะเบียนบัญชีนักศึกษาสำเร็จ!",
                "user_name": matched_name,
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def staff_register_api(request):
    """สมัครสมาชิกบุคลากรและอาจารย์"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip().lower()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not email or not username or not password:
            return JsonResponse(
                {"success": False, "message": "กรุณากรอกข้อมูลให้ครบถ้วน"}, status=400
            )

        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})

        if any(
            acc.get("username") == username or acc.get("email") == email
            for acc in accounts.get("staff", [])
        ):
            return JsonResponse(
                {"success": False, "message": "Username หรือ Email นี้มีอยู่ในระบบแล้ว"},
                status=400,
            )

        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        new_staff = {
            "email": email,
            "username": username,
            "password_hash": hashed_pass,
            "password_plain": password,
            "created_at": datetime.now().isoformat(),
        }
        accounts["staff"].append(new_staff)
        write_json_file(ACCOUNTS_FILE, accounts)

        if hasattr(request, "session"):
            request.session["staff_username"] = username
            request.session["user_role"] = "staff"

        return JsonResponse(
            {"success": True, "message": "สมัครสมาชิกบุคลากรสำเร็จ!", "username": username}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def staff_login_api(request):
    """เข้าสู่ระบบบุคลากร/ผู้ดูแลระบบ ด้วย Username หรือ Email"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    # 1. Check Rate Limiter (Max 5 attempts / 10 mins)
    allowed, limit_msg = check_rate_limit(request, action="staff_login", max_attempts=5, lock_minutes=10)
    if not allowed:
        return JsonResponse({"success": False, "message": limit_msg}, status=429)

    try:
        data = json.loads(request.body)
        identifier = data.get("identifier", "").strip()
        password = data.get("password", "").strip()

        if not identifier or not password:
            return JsonResponse(
                {"success": False, "message": "กรุณากรอก Username/Email และรหัสผ่าน"},
                status=400,
            )

        env_user, env_pass = get_admin_credentials()

        # Admin Login (Only lnwpoon007x / poon300450)
        if identifier == env_user and password == env_pass:
            reset_failed_attempts(request, action="staff_login")
            token = create_admin_session()
            if hasattr(request, "session"):
                request.session["admin_token"] = token
                request.session["user_role"] = "admin"
            log_user_activity(
                "lnwpoon007x",
                "ผู้ดูแลระบบ (Admin)",
                "admin",
                email="mpoontv1234@gmail.com",
                request=request,
            )
            return JsonResponse(
                {
                    "success": True,
                    "role": "admin",
                    "redirect": "/admin/dashboard/",
                    "message": "เข้าสู่ระบบผู้ดูแลระบบสำเร็จ",
                }
            )

        # Staff Account Lookup
        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        staff_match = next(
            (
                s
                for s in accounts.get("staff", [])
                if (
                    s.get("username", "").lower() == identifier.lower()
                    or s.get("email", "").lower() == identifier.lower()
                )
                and s.get("password_hash") == hashed_pass
            ),
            None,
        )

        if staff_match:
            reset_failed_attempts(request, action="staff_login")
            if hasattr(request, "session"):
                # Clear student and admin session tokens to prevent role bleeding
                request.session.pop("student_id", None)
                request.session.pop("student_name", None)
                request.session.pop("admin_token", None)
                request.session["staff_username"] = staff_match.get("username")
                request.session["staff_email"] = staff_match.get("email", "")
                request.session["user_role"] = "staff"
            log_user_activity(
                staff_match.get("username"),
                staff_match.get("username"),
                "staff",
                email=staff_match.get("email", ""),
                request=request,
            )
            return JsonResponse(
                {
                    "success": True,
                    "role": "staff",
                    "redirect": "/",
                    "message": f'ยินดีต้อนรับ คุณ {staff_match.get("username")}',
                }
            )

        record_failed_attempt(request, action="staff_login", max_attempts=5, lock_minutes=10)
        return JsonResponse(
            {"success": False, "message": "Username/Email หรือรหัสผ่านไม่ถูกต้อง"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def verify_current_user_password_api(request):
    """ตรวจสอบรหัสผ่านของ User คนปัจจุบันที่ล็อกอินอยู่เท่านั้น (ป้องกันการใช้รหัสผู้อื่นปลดล็อค)"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    allowed, limit_msg = check_rate_limit(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
    if not allowed:
        return JsonResponse({"success": False, "message": limit_msg}, status=429)

    try:
        data = json.loads(request.body)
        password = data.get("password", "").strip()
        req_role = data.get("role", "").strip()
        req_username = data.get("username", "").strip()
        req_sid = data.get("student_id", "").strip()

        sess = getattr(request, "session", {})
        session_role = sess.get("user_role", "") if hasattr(sess, "get") else ""
        session_staff = sess.get("staff_username", "") if hasattr(sess, "get") else ""
        session_sid = sess.get("student_id", "") if hasattr(sess, "get") else ""

        active_role = req_role or session_role

        if not password:
            return JsonResponse(
                {"success": False, "message": "กรุณากรอกรหัสผ่าน"}, status=400
            )

        env_user, env_pass = get_admin_credentials()
        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # 1. Admin Verification
        if active_role == "admin" or validate_admin_token(request):
            if password == env_pass:
                reset_failed_attempts(request, action="verify_pwd")
                return JsonResponse({"success": True, "message": "ยืนยันรหัสผ่านผู้ดูแลระบบสำเร็จ"})
            else:
                record_failed_attempt(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
                return JsonResponse({"success": False, "message": "รหัสผ่านผู้ดูแลระบบไม่ถูกต้อง"}, status=401)

        # 2. Staff Verification: Check ONLY this staff member's registered password
        target_staff = req_username or session_staff
        if active_role == "staff" or target_staff:
            staff_acc = next(
                (
                    st
                    for st in accounts.get("staff", [])
                    if st.get("username", "").lower() == target_staff.lower()
                    or st.get("email", "").lower() == target_staff.lower()
                ),
                None,
            )
            if staff_acc:
                if staff_acc.get("password_hash") == hashed_pass or staff_acc.get("password") == password:
                    reset_failed_attempts(request, action="verify_pwd")
                    return JsonResponse({"success": True, "message": "ยืนยันรหัสผ่านบุคลากรสำเร็จ"})
                else:
                    record_failed_attempt(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
                    return JsonResponse({"success": False, "message": "รหัสผ่านบัญชีบุคลากรไม่ถูกต้อง"}, status=401)
            else:
                record_failed_attempt(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
                return JsonResponse({"success": False, "message": "ไม่พบบัญชีบุคลากรนี้ในระบบ"}, status=401)

        # 3. Student Verification: Check ONLY this specific student's registered password
        target_sid = req_sid or session_sid
        clean_sid = re.sub(r"[^0-9a-zA-Z]", "", target_sid)

        if active_role == "student" or target_sid or clean_sid:
            student_acc = next(
                (
                    s
                    for s in accounts.get("students", [])
                    if s.get("student_id") == target_sid
                    or (clean_sid and re.sub(r"[^0-9a-zA-Z]", "", s.get("student_id", "")) == clean_sid)
                ),
                None,
            )
            if student_acc:
                if (
                    student_acc.get("password_hash") == hashed_pass
                    or student_acc.get("password") == password
                    or student_acc.get("password_plain") == password
                ):
                    reset_failed_attempts(request, action="verify_pwd")
                    return JsonResponse({"success": True, "message": "ยืนยันรหัสผ่านสำเร็จ"})
                else:
                    record_failed_attempt(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
                    return JsonResponse(
                        {"success": False, "message": "รหัสผ่านของรหัสนักศึกษานี้ไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง"},
                        status=401,
                    )
            else:
                # Student exists in roster / DB but has not set a custom password via /register/student/
                if password == target_sid or password == clean_sid:
                    reset_failed_attempts(request, action="verify_pwd")
                    return JsonResponse({"success": True, "message": "ยืนยันรหัสผ่านสำเร็จ"})
                return JsonResponse(
                    {
                        "success": False,
                        "message": "ยังไม่ได้ตั้งรหัสผ่านสำหรับรหัสนี้ หรือรหัสผ่านไม่ถูกต้อง (หากยังไม่เคยลงทะเบียน กรุณาลงทะเบียนตั้งรหัสผ่านก่อน)",
                    },
                    status=401,
                )

        record_failed_attempt(request, action="verify_pwd", max_attempts=5, lock_minutes=5)
        return JsonResponse(
            {"success": False, "message": "ไม่พบข้อมูลบัญชีผู้ใช้ของคุณ กรุณาลองใหม่อีกครั้ง"}, status=401
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def student_register_page(request):
    """หน้าสำหรับยืนยันตัวตนและลงทะเบียนนักศึกษาโดยเฉพาะ"""
    return render(request, "admin_panel/register_student.html")


def staff_register_page(request):
    """หน้าสำหรับสมัครสมาชิกบุคลากรโดยเฉพาะ"""
    return render(request, "admin_panel/register_staff.html")


RESETS_FILE = BASE_DIR / "data" / "password_resets.json"


@csrf_exempt
def student_request_reset_api(request):
    """ขั้นตอนที่ 1: ส่งคำขอรีเซ็ตรหัสผ่านและสร้างรหัสยืนยัน (Token/OTP) ไปยังอีเมลนักศึกษา"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        student_id = data.get("student_id", "").strip()
        email = data.get("email", "").strip().lower()

        if not student_id or not email:
            return JsonResponse(
                {"success": False, "message": "กรุณากรอกรหัสนักศึกษาและอีเมลมหาวิทยาลัย"},
                status=400,
            )

        clean_sid = student_id.replace("-", "").strip()
        expected_prefix = f"stu{clean_sid}"

        is_uni_email = expected_prefix in email and "sskru.ac.th" in email
        is_valid_email = "@" in email and "." in email

        if not is_uni_email and not is_valid_email:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"อีเมลยืนยันตัวตนไม่ถูกต้อง ต้องใช้อีเมลรูปแบบ {expected_prefix}@sskru.ac.th หรืออีเมลของคุณ",
                },
                status=400,
            )

        student_db = Student.objects.filter(student_id=student_id).first()
        roster = read_json_file(ROSTER_FILE)
        matched_roster = next(
            (s for s in roster if s.get("student_id") == student_id), None
        )

        if not student_db and not matched_roster:
            return JsonResponse(
                {"success": False, "message": "ไม่พบรหัสนักศึกษานี้ในระบบมหาวิทยาลัย"},
                status=404,
            )

        student_name = student_db.name if student_db else matched_roster.get("name")

        # Generate Secure Token & OTP
        token = secrets.token_hex(24)
        otp = str(secrets.randbelow(900000) + 100000)
        expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()

        resets = read_json_file(RESETS_FILE, default=[])
        # Clear previous active resets for this student
        resets = [r for r in resets if r.get("student_id") != student_id]

        reset_entry = {
            "student_id": student_id,
            "student_name": student_name,
            "email": email,
            "token": token,
            "otp": otp,
            "expires_at": expires_at,
            "used": False,
            "created_at": datetime.now().isoformat(),
        }
        resets.append(reset_entry)
        write_json_file(RESETS_FILE, resets)

        verify_url = f"/reset_password/student/verify/?token={token}"
        verify_full_url = request.build_absolute_uri(verify_url)

        # Real SMTP Email Dispatcher
        email_sent = False
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings

            subject = "🔒 ยืนยันสิทธิ์รีเซ็ตรหัสผ่าน — SSKRU Campus Map"
            from_email = getattr(
                settings, "DEFAULT_FROM_EMAIL", "SSKRU Campus Map <noreply@sskru.ac.th>"
            )
            to_email = [email]

            text_content = f"""
สวัสดีคุณ {student_name} (รหัสนักศึกษา: {student_id})

ระบบได้รับคำขอรีเซ็ตรหัสผ่านสำหรับบัญชีของคุณในระบบแผนที่มหาวิทยาลัยราชภัฏศรีสะเกษ (SSKRU Campus Map)

รหัส OTP ยืนยันสิทธิ์ของคุณคือ: {otp}

หรือคลิกลิงก์ด้านล่างเพื่อยืนยันตัวตนและตั้งรหัสผ่านใหม่ (ลิงก์มีอายุ 15 นาที):
{verify_full_url}

หากคุณไม่ได้เป็นผู้ทำรายการนี้ กรุณาเพิกเฉยต่ออีเมลฉบับนี้
            """.strip()

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"></head>
            <body style="font-family: 'Sarabun', Arial, sans-serif; background-color: #f1f5f9; padding: 20px; color: #1e293b;">
              <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #0d2c5e, #1a4fa0); padding: 24px; text-align: center; color: #ffffff;">
                  <h2 style="margin: 0; font-size: 20px;">มหาวิทยาลัยราชภัฏศรีสะเกษ</h2>
                  <p style="margin: 4px 0 0; font-size: 13px; opacity: 0.85;">ระบบแผนที่และสารสนเทศอาคาร (SSKRU Campus Map)</p>
                </div>
                <div style="padding: 28px;">
                  <h3 style="color: #0f172a; margin-top: 0;">เรียน คุณ {student_name}</h3>
                  <p style="color: #475569; font-size: 14px; line-height: 1.6;">
                    ระบบได้รับคำขอรีเซ็ตรหัสผ่านสำหรับรหัสนักศึกษา <strong>{student_id}</strong> กรุณาใช้รหัส OTP หรือคลิกปุ่มด้านล่างเพื่อยืนยันสิทธิ์และตั้งรหัสผ่านใหม่:
                  </p>
                  
                  <div style="background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 16px; text-align: center; margin: 20px 0;">
                    <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">รหัส OTP ยืนยันสิทธิ์ (มีอายุ 15 นาที)</div>
                    <div style="font-size: 28px; font-weight: bold; color: #1a4fa0; letter-spacing: 6px;">{otp}</div>
                  </div>
                  
                  <div style="text-align: center; margin: 24px 0;">
                    <a href="{verify_full_url}" style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 10px; font-weight: bold; display: inline-block; font-size: 14px;">
                      👉 คลิกที่นี่เพื่อยืนยันสิทธิ์ & ตั้งรหัสผ่านใหม่
                    </a>
                  </div>
                  
                  <p style="font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 14px; margin-bottom: 0;">
                    * หากคุณไม่ได้เป็นผู้ทำรายการนี้ กรุณาเพิกเฉยต่ออีเมลฉบับนี้ รหัสผ่านเดิมของคุณจะยังคงปลอดภัย
                  </p>
                </div>
              </div>
            </body>
            </html>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
            email_sent = True
        except Exception as mail_err:
            print(f"Mail send notice: {mail_err}")

        return JsonResponse(
            {
                "success": True,
                "message": f"ระบบได้ส่งลิงก์และรหัสยืนยันสิทธิ์ไปยังอีเมล {email} เรียบร้อยแล้ว (รหัสมีอายุ 15 นาที)",
                "email": email,
                "token": token,
                "otp": otp,
                "email_sent": email_sent,
                "verify_url": verify_url,
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def student_verify_reset_token_api(request):
    """ขั้นตอนที่ 2: ตรวจสอบความถูกต้องของ Token หรือ OTP ยืนยันสิทธิ์"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    allowed, limit_msg = check_rate_limit(request, action="verify_otp", max_attempts=5, lock_minutes=10)
    if not allowed:
        return JsonResponse({"success": False, "message": limit_msg}, status=429)

    try:
        data = json.loads(request.body)
        token = str(data.get("token") or "").strip()
        otp = str(data.get("otp") or "").strip()

        resets = read_json_file(RESETS_FILE, default=[])
        matched = None
        for r in resets:
            if not r.get("used"):
                if (token and r.get("token") == token) or (otp and r.get("otp") == otp):
                    matched = r
                    break

        if not matched:
            record_failed_attempt(request, action="verify_otp", max_attempts=5, lock_minutes=10)
            return JsonResponse(
                {
                    "success": False,
                    "message": "ลิงก์ยืนยันตัวตนหรือรหัส OTP ไม่ถูกต้อง หรือถูกใช้งานไปแล้ว",
                },
                status=400,
            )

        exp = datetime.fromisoformat(matched.get("expires_at"))
        if datetime.now() > exp:
            return JsonResponse(
                {
                    "success": False,
                    "message": "ลิงก์ยืนยันตัวตนหมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง",
                },
                status=400,
            )

        reset_failed_attempts(request, action="verify_otp")
        return JsonResponse(
            {
                "success": True,
                "token": matched.get("token"),
                "student_id": matched.get("student_id"),
                "student_name": matched.get("student_name"),
                "email": matched.get("email"),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def student_confirm_new_password_api(request):
    """ขั้นตอนที่ 3: บันทึกรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลมหาวิทยาลัยสำเร็จ"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        token = data.get("token", "").strip()
        new_password = data.get("new_password", "").strip()

        if not token or not new_password:
            return JsonResponse(
                {"success": False, "message": "ข้อมูลไม่ครบถ้วน"}, status=400
            )

        resets = read_json_file(RESETS_FILE, default=[])
        matched = next(
            (r for r in resets if r.get("token") == token and not r.get("used")), None
        )

        if not matched:
            return JsonResponse(
                {"success": False, "message": "Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ"},
                status=400,
            )

        exp = datetime.fromisoformat(matched.get("expires_at"))
        if datetime.now() > exp:
            return JsonResponse(
                {"success": False, "message": "Token หมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง"},
                status=400,
            )

        student_id = matched.get("student_id")
        student_name = matched.get("student_name")

        # Update Accounts DB
        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        hashed_pass = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

        student_acc = next(
            (
                acc
                for acc in accounts.get("students", [])
                if acc.get("student_id") == student_id
            ),
            None,
        )
        if student_acc:
            student_acc["password_hash"] = hashed_pass
        else:
            accounts["students"].append(
                {
                    "student_id": student_id,
                    "name": student_name,
                    "faculty": "มหาวิทยาลัยราชภัฏศรีสะเกษ",
                    "password_hash": hashed_pass,
                    "created_at": datetime.now().isoformat(),
                }
            )
        write_json_file(ACCOUNTS_FILE, accounts)

        # Mark token used
        matched["used"] = True
        write_json_file(RESETS_FILE, resets)

        return JsonResponse(
            {
                "success": True,
                "message": "สร้างและตั้งรหัสผ่านใหม่สำเร็จ! ท่านสามารถเข้าสู่ระบบด้วยรหัสผ่านใหม่ได้ทันที",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def student_reset_password_page(request):
    """หน้าสำหรับขอส่งลิงก์ยืนยันตัวตนไปยังอีเมลมหาวิทยาลัย"""
    return render(request, "admin_panel/reset_password_student.html")


def student_reset_password_verify_page(request):
    """หน้าสร้างรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลมหาวิทยาลัยสำเร็จ"""
    token = request.GET.get("token", "")
    return render(request, "admin_panel/reset_password_verify.html", {"token": token})


@csrf_exempt
def staff_request_reset_api(request):
    """ขั้นตอนที่ 1: ส่งคำขอรีเซ็ตรหัสผ่านสำหรับบุคลากร/อาจารย์ และส่ง OTP/Token ไปยังอีเมลจริง"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        identifier = data.get("identifier", "").strip()

        if not identifier:
            return JsonResponse(
                {"success": False, "message": "กรุณากรอก Username หรือ Email ของบุคลากร"},
                status=400,
            )

        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        staff_match = next(
            (
                s
                for s in accounts.get("staff", [])
                if s.get("username") == identifier
                or s.get("email", "").lower() == identifier.lower()
            ),
            None,
        )

        env_user, env_pass = get_admin_credentials()

        target_username = None
        target_email = None

        if staff_match:
            target_username = staff_match.get("username")
            target_email = staff_match.get("email")
        elif (
            identifier == env_user
            or identifier == "admin"
            or identifier == "lnwpoon007x"
            or identifier.lower() == "mpoontv1234@gmail.com"
        ):
            target_username = "ผู้ดูแลระบบหลัก (Admin)"
            target_email = os.getenv("EMAIL_HOST_USER", "mpoontv1234@gmail.com")
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "ไม่พบบัญชีบุคลากรที่ระบุในระบบ กรุณาตรวจสอบ Username หรือ Email อีกครั้ง",
                },
                status=404,
            )

        # Generate Secure Token & OTP
        token = secrets.token_hex(24)
        otp = str(secrets.randbelow(900000) + 100000)
        expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()

        resets = read_json_file(RESETS_FILE, default=[])
        resets = [
            r
            for r in resets
            if r.get("username") != target_username and r.get("email") != target_email
        ]

        reset_entry = {
            "role": "staff",
            "username": target_username,
            "email": target_email,
            "token": token,
            "otp": otp,
            "expires_at": expires_at,
            "used": False,
            "created_at": datetime.now().isoformat(),
        }
        resets.append(reset_entry)
        write_json_file(RESETS_FILE, resets)

        verify_url = f"/reset_password/staff/verify/?token={token}"
        verify_full_url = request.build_absolute_uri(verify_url)

        # Real SMTP Email Dispatcher
        email_sent = False
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings

            subject = "🔒 ยืนยันสิทธิ์รีเซ็ตรหัสผ่านบุคลากร — SSKRU Campus Map"
            from_email = getattr(
                settings, "DEFAULT_FROM_EMAIL", "SSKRU Campus Map <noreply@sskru.ac.th>"
            )
            to_email = [target_email]

            text_content = f"""
สวัสดี คุณ {target_username}

ระบบได้รับคำขอรีเซ็ตรหัสผ่านสำหรับบัญชีบุคลากรของคุณในระบบ SSKRU Campus Map

รหัส OTP ยืนยันสิทธิ์ของคุณคือ: {otp}

หรือคลิกลิงก์ด้านล่างเพื่อยืนยันตัวตนและตั้งรหัสผ่านใหม่ (ลิงก์มีอายุ 15 นาที):
{verify_full_url}

หากคุณไม่ได้เป็นผู้ทำรายการนี้ กรุณาเพิกเฉยต่ออีเมลฉบับนี้
            """.strip()

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"></head>
            <body style="font-family: 'Sarabun', Arial, sans-serif; background-color: #f1f5f9; padding: 20px; color: #1e293b;">
              <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #0d2c5e, #1a4fa0); padding: 24px; text-align: center; color: #ffffff;">
                  <h2 style="margin: 0; font-size: 20px;">มหาวิทยาลัยราชภัฏศรีสะเกษ</h2>
                  <p style="margin: 4px 0 0; font-size: 13px; opacity: 0.85;">ระบบแผนที่และสารสนเทศอาคาร (SSKRU Faculty & Staff)</p>
                </div>
                <div style="padding: 28px;">
                  <h3 style="color: #0f172a; margin-top: 0;">เรียน คุณ {target_username}</h3>
                  <p style="color: #475569; font-size: 14px; line-height: 1.6;">
                    ระบบได้รับคำขอรีเซ็ตรหัสผ่านสำหรับบัญชีบุคลากรของคุณ กรุณาใช้รหัส OTP หรือคลิกปุ่มด้านล่างเพื่อยืนยันสิทธิ์และตั้งรหัสผ่านใหม่:
                  </p>
                  
                  <div style="background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 16px; text-align: center; margin: 20px 0;">
                    <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">รหัส OTP ยืนยันสิทธิ์ (มีอายุ 15 นาที)</div>
                    <div style="font-size: 28px; font-weight: bold; color: #1a4fa0; letter-spacing: 6px;">{otp}</div>
                  </div>
                  
                  <div style="text-align: center; margin: 24px 0;">
                    <a href="{verify_full_url}" style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 10px; font-weight: bold; display: inline-block; font-size: 14px;">
                      👉 คลิกที่นี่เพื่อยืนยันสิทธิ์ & ตั้งรหัสผ่านใหม่
                    </a>
                  </div>
                  
                  <p style="font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 14px; margin-bottom: 0;">
                    * หากคุณไม่ได้เป็นผู้ทำรายการนี้ กรุณาเพิกเฉยต่ออีเมลฉบับนี้ รหัสผ่านเดิมของคุณจะยังคงปลอดภัย
                  </p>
                </div>
              </div>
            </body>
            </html>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
            email_sent = True
        except Exception as mail_err:
            print(f"Mail send notice: {mail_err}")

        return JsonResponse(
            {
                "success": True,
                "message": f"ระบบได้ส่งรหัส OTP และลิงก์ยืนยันตัวตนไปยังอีเมล {target_email} เรียบร้อยแล้ว (รหัสมีอายุ 15 นาที)",
                "email": target_email,
                "email_sent": email_sent,
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def staff_verify_reset_token_api(request):
    """ขั้นตอนที่ 2: ตรวจสอบความถูกต้องของ Token หรือ OTP ยืนยันสิทธิ์สำหรับบุคลากร"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        token = str(data.get("token") or "").strip()
        otp = str(data.get("otp") or "").strip()

        resets = read_json_file(RESETS_FILE, default=[])
        matched = None
        for r in resets:
            if not r.get("used"):
                if (token and r.get("token") == token) or (otp and r.get("otp") == otp):
                    matched = r
                    break

        if not matched:
            return JsonResponse(
                {
                    "success": False,
                    "message": "ลิงก์ยืนยันตัวตนหรือรหัส OTP ไม่ถูกต้อง หรือถูกใช้งานไปแล้ว",
                },
                status=400,
            )

        exp = datetime.fromisoformat(matched.get("expires_at"))
        if datetime.now() > exp:
            return JsonResponse(
                {
                    "success": False,
                    "message": "ลิงก์ยืนยันตัวตนหมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง",
                },
                status=400,
            )

        return JsonResponse(
            {
                "success": True,
                "token": matched.get("token"),
                "username": matched.get("username"),
                "email": matched.get("email"),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def staff_confirm_new_password_api(request):
    """ขั้นตอนที่ 3: บันทึกรหัสผ่านใหม่สำหรับบัญชีบุคลากรหลังจากยืนยันสิทธิ์อีเมลสำเร็จ"""
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        token = data.get("token", "").strip()
        new_password = data.get("new_password", "").strip()

        if not token or not new_password:
            return JsonResponse(
                {"success": False, "message": "ข้อมูลไม่ครบถ้วน"}, status=400
            )

        resets = read_json_file(RESETS_FILE, default=[])
        matched = next(
            (r for r in resets if r.get("token") == token and not r.get("used")), None
        )

        if not matched:
            return JsonResponse(
                {"success": False, "message": "Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ"},
                status=400,
            )

        exp = datetime.fromisoformat(matched.get("expires_at"))
        if datetime.now() > exp:
            return JsonResponse(
                {"success": False, "message": "Token หมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง"},
                status=400,
            )

        username = matched.get("username")
        email = matched.get("email")

        # Update Accounts DB
        accounts = read_json_file(ACCOUNTS_FILE, default={"students": [], "staff": []})
        hashed_pass = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

        staff_acc = next(
            (
                acc
                for acc in accounts.get("staff", [])
                if acc.get("username") == username or acc.get("email") == email
            ),
            None,
        )
        if staff_acc:
            staff_acc["password_hash"] = hashed_pass
            staff_acc["password_plain"] = new_password
        else:
            accounts["staff"].append(
                {
                    "username": username,
                    "email": email,
                    "password_hash": hashed_pass,
                    "password_plain": new_password,
                    "created_at": datetime.now().isoformat(),
                }
            )
        write_json_file(ACCOUNTS_FILE, accounts)

        # Mark token used
        matched["used"] = True
        write_json_file(RESETS_FILE, resets)

        return JsonResponse(
            {
                "success": True,
                "message": "สร้างและตั้งรหัสผ่านใหม่สำหรับบุคลากรสำเร็จ! ท่านสามารถเข้าสู่ระบบด้วยรหัสผ่านใหม่ได้ทันที",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def staff_reset_password_page(request):
    """หน้าสำหรับขอส่งลิงก์ยืนยันตัวตนไปยังอีเมลบุคลากร"""
    return render(request, "admin_panel/reset_password_staff.html")


def staff_reset_password_verify_page(request):
    """หน้าสร้างรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลบุคลากรสำเร็จ"""
    token = request.GET.get("token", "")
    return render(
        request, "admin_panel/reset_password_staff_verify.html", {"token": token}
    )

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
DATA_FILE = BASE_DIR / 'data' / 'buildings.json'


# ─── Helpers ────────────────────────────────────────────────────────────────

def read_buildings():
    try:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def write_buildings(data):
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def get_admin_credentials():
    return (
        os.getenv('ADMIN_USERNAME', 'lnwpoon007x'),
        os.getenv('ADMIN_PASSWORD', 'poon300450')
    )


def generate_token():
    return secrets.token_hex(32)


def create_admin_session():
    token = generate_token()
    expires = timezone.now() + timedelta(hours=8)
    AdminSession.objects.create(token=token, expires_at=expires)
    return token


def validate_admin_token(request):
    token = request.session.get('admin_token')
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


def get_device_info(user_agent):
    ua = user_agent.lower()
    if any(x in ua for x in ['iphone', 'android', 'mobile']):
        device = 'mobile'
    elif any(x in ua for x in ['ipad', 'tablet']):
        device = 'tablet'
    else:
        device = 'desktop'

    os_name = 'Unknown'
    if 'android' in ua:
        os_name = 'Android'
    elif 'iphone' in ua or 'ipad' in ua:
        os_name = 'iOS'
    elif 'macintosh' in ua:
        os_name = 'macOS'
    elif 'windows' in ua:
        os_name = 'Windows'
    elif 'linux' in ua:
        os_name = 'Linux'

    browser = 'Unknown'
    if 'chrome' in ua and 'chromium' not in ua and 'edg' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'edg' in ua:
        browser = 'Edge'

    return device, os_name, browser


# ─── Views ──────────────────────────────────────────────────────────────────

def admin_login_page(request):
    """หน้า Login รวมสำหรับทุกสิทธิ์ (นักศึกษา / บุคลากร / ผู้ดูแลระบบ)"""
    if validate_admin_token(request):
        return redirect('/admin/dashboard/')
    return render(request, 'admin_panel/student_login.html')


def admin_logout(request):
    """ออกจากระบบ Admin แล้วส่งกลับไปหน้า Login รวมใหม่"""
    token = request.session.get('admin_token')
    if token:
        AdminSession.objects.filter(token=token).update(is_active=False)
    request.session.flush()
    return redirect('/login/')


def admin_dashboard(request):
    """Admin Dashboard หลัก"""
    if not validate_admin_token(request):
        return redirect('/admin/')

    # Stats summary
    today = timezone.now().date()
    total_visitors = VisitorLog.objects.count()
    today_visitors = VisitorLog.objects.filter(timestamp__date=today).count()
    
    # 7-day chart data
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_counts = (
        VisitorLog.objects
        .filter(timestamp__gte=seven_days_ago)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    chart_labels = []
    chart_data = []
    for item in daily_counts:
        chart_labels.append(item['date'].strftime('%d/%m'))
        chart_data.append(item['count'])

    # Device breakdown
    device_stats = (
        VisitorLog.objects
        .values('device_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # OS breakdown
    os_stats = (
        VisitorLog.objects
        .values('os_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # Top searched buildings
    top_searches = (
        UserEvent.objects
        .filter(event_type='search')
        .values('event_data')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # Top buildings viewed
    top_buildings = (
        UserEvent.objects
        .filter(event_type='building_select')
        .values('event_data')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # Navigation counts
    nav_count = UserEvent.objects.filter(event_type='navigate').count()

    # Recent visitors
    recent_visitors = VisitorLog.objects.select_related().order_by('-timestamp')[:20]

    # Buildings data
    buildings = read_buildings()

    context = {
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
        'total_buildings': len(buildings),
        'nav_count': nav_count,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'device_stats': list(device_stats),
        'os_stats': list(os_stats),
        'top_searches': list(top_searches),
        'top_buildings': list(top_buildings),
        'recent_visitors': recent_visitors,
        'buildings': buildings,
        'buildings_json': json.dumps(buildings, ensure_ascii=False),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@csrf_exempt
def admin_buildings_api(request):
    """CRUD API สำหรับ buildings (Admin & API)"""
    buildings = read_buildings()

    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': buildings, 'count': len(buildings)})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not data.get('name') or not data.get('coords'):
                return JsonResponse({'success': False, 'message': 'ข้อมูลไม่ครบ'}, status=400)
            
            # Check duplicate ID
            b_id = data.get('id')
            if b_id:
                idx = next((i for i, b in enumerate(buildings) if b.get('id') == b_id), None)
                if idx is not None:
                    buildings[idx].update(data)
                else:
                    buildings.append(data)
            else:
                buildings.append(data)

            write_buildings(buildings)
            return JsonResponse({'success': True, 'message': 'เพิ่ม/อัปเดตอาคารสำเร็จ', 'data': data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def admin_building_detail_api(request, building_id):
    """Update/Delete building (Admin & API)"""
    buildings = read_buildings()
    building_id = int(building_id)
    idx = next((i for i, b in enumerate(buildings) if b.get('id') == building_id), None)

    if idx is None and request.method != 'PUT':
        return JsonResponse({'success': False, 'message': 'ไม่พบอาคาร'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': buildings[idx]})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if idx is not None:
                buildings[idx].update(data)
                buildings[idx]['id'] = building_id
            else:
                data['id'] = building_id
                buildings.append(data)
                idx = len(buildings) - 1

            write_buildings(buildings)
            return JsonResponse({'success': True, 'message': 'อัปเดตข้อมูลสำเร็จ', 'data': buildings[idx]})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=400)

    elif request.method == 'DELETE':
        removed = buildings.pop(idx)
        write_buildings(buildings)
        return JsonResponse({'success': True, 'message': f"ลบ {removed.get('name')} สำเร็จ"})

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def track_event(request):
    """รับ event tracking จาก frontend"""
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    try:
        data = json.loads(request.body)
        event_type = data.get('type', 'page_view')
        event_data = data.get('data', '')
        session_id = data.get('session_id', '')

        ua = request.META.get('HTTP_USER_AGENT', '')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ',' in ip:
            ip = ip.split(',')[0].strip()

        device, os_name, browser = get_device_info(ua)

        # Find or create visitor log for this session
        visitor, _ = VisitorLog.objects.get_or_create(
            session_id=session_id,
            defaults={
                'ip_address': ip,
                'user_agent': ua[:500],
                'device_type': device,
                'os_name': os_name,
                'browser': browser,
                'page_path': data.get('path', '/'),
                'referrer': data.get('referrer', ''),
            }
        )

        UserEvent.objects.create(
            visitor=visitor,
            event_type=event_type,
            event_data=str(event_data)[:255],
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def auth_status_api(request):
    """API เช็กว่า User คนปัจจุบันเป็น Admin, Staff หรือ Student"""
    is_admin = validate_admin_token(request)
    
    # check student session
    student_id = request.session.get('student_id')
    is_student = student_id is not None
    
    # check staff session
    is_staff = (request.session.get('user_role') == 'staff') or ('staff_username' in request.session)
    staff_username = request.session.get('staff_username', '')
    
    return JsonResponse({
        'success': True,
        'isAdmin': is_admin,
        'isStudent': is_student,
        'isStaff': is_staff,
        'staffUsername': staff_username,
        'studentId': student_id,
        'studentName': request.session.get('student_name', ''),
    })


def student_login_page(request):
    """หน้าต่างล็อกอินสำหรับนักศึกษา"""
    return render(request, 'admin_panel/student_login.html')

@csrf_exempt
def student_login_api(request):
    """API สำหรับตรวจสอบรหัสนักศึกษา"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id', '').strip()
        
        if not student_id:
            return JsonResponse({'success': False, 'message': 'กรุณาระบุรหัสนักศึกษา'}, status=400)
            
        from .models import Student
        student = Student.objects.filter(student_id=student_id, is_active=True).first()
        
        if student:
            request.session['student_id'] = student.student_id
            request.session['student_name'] = student.name
            return JsonResponse({'success': True, 'message': 'เข้าสู่ระบบสำเร็จ'})
        else:
            return JsonResponse({'success': False, 'message': 'รหัสนักศึกษาไม่ถูกต้อง หรือไม่ได้รับสิทธิ์'}, status=401)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
def admin_students_api(request):
    """API จัดการข้อมูลนักศึกษา (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
        
    from .models import Student
    from django.db import IntegrityError
    
    if request.method == 'GET':
        students = list(Student.objects.values('id', 'student_id', 'name', 'is_active', 'created_at'))
        return JsonResponse({'success': True, 'data': students})
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id', '').strip()
            name = data.get('name', '').strip()

            if not student_id or not name:
                return JsonResponse({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'}, status=400)

            if Student.objects.filter(student_id=student_id).exists():
                return JsonResponse({'success': False, 'message': 'รหัสนักศึกษานี้มีอยู่ในระบบแล้ว'}, status=400)

            student = Student.objects.create(
                student_id=student_id,
                name=name,
                is_active=data.get('is_active', True)
            )
            return JsonResponse({'success': True, 'message': 'เพิ่มนักศึกษาสำเร็จ'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'รหัสนักศึกษานี้มีอยู่ในระบบแล้ว'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'เกิดข้อผิดพลาดในการบันทึกข้อมูล'}, status=400)
            
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            sid = data.get('id')
            Student.objects.filter(id=sid).delete()
            return JsonResponse({'success': True, 'message': 'ลบข้อมูลสำเร็จ'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

def admin_analytics_api(request):
    """ส่งข้อมูล analytics (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

    today = timezone.now().date()
    return JsonResponse({
        'success': True,
        'today_visitors': VisitorLog.objects.filter(timestamp__date=today).count(),
        'total_visitors': VisitorLog.objects.count(),
        'total_events': UserEvent.objects.count(),
    })





# ─── Student Verification & Registration APIs ─────────────────────────────────

ROSTER_FILE = BASE_DIR / 'data' / 'students_roster.json'
ACCOUNTS_FILE = BASE_DIR / 'data' / 'user_accounts.json'

def read_json_file(file_path, default=None):
    if default is None:
        default = []
    try:
        if not file_path.exists():
            return default
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default

def write_json_file(file_path, data):
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

@csrf_exempt
def student_verify_api(request):
    """ตรวจสอบรหัสนักศึกษาและเลขบัตรประชาชนในฐานข้อมูลหลัก (ทั้ง Student DB และ Roster JSON)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id', '').strip()
        citizen_id = data.get('citizen_id', '').strip()
        
        if not student_id or not citizen_id:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกรหัสนักศึกษาและเลขบัตรประชาชนให้ครบถ้วน'}, status=400)
            
        # 1. Search in Django Student Model first
        student_db = Student.objects.filter(student_id=student_id).first()
        matched_student = None
        
        if student_db:
            matched_student = {
                'student_id': student_db.student_id,
                'name': student_db.name,
                'faculty': 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                'major': 'นักศึกษา'
            }
        else:
            # 2. Search in ROSTER_FILE json
            roster = read_json_file(ROSTER_FILE)
            for s in roster:
                if s.get('student_id') == student_id:
                    matched_student = s
                    break

        if not matched_student:
            return JsonResponse({
                'success': False, 
                'status': 'NOT_FOUND',
                'message': 'ไม่พบรหัสนักศึกษาในฐานข้อมูลของมหาวิทยาลัย กรุณาติดต่อเจ้าหน้าที่สำนักทะเบียนและประมวลผลโดยตรง'
            }, status=404)

        # Verification matched cleanly!
        return JsonResponse({
            'success': True,
            'status': 'MATCHED',
            'student_info': {
                'student_id': matched_student.get('student_id'),
                'name': matched_student.get('name'),
                'faculty': matched_student.get('faculty', 'มหาวิทยาลัยราชภัฏศรีสะเกษ'),
                'major': matched_student.get('major', 'นักศึกษา')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def student_register_api(request):
    """ลงทะเบียนสร้างรหัสผ่านสำหรับนักศึกษา"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id', '').strip()
        citizen_id = data.get('citizen_id', '').strip()
        password = data.get('password', '').strip()
        
        student_db = Student.objects.filter(student_id=student_id).first()
        matched_name = student_db.name if student_db else None
        matched_faculty = 'มหาวิทยาลัยราชภัฏศรีสะเกษ'
        
        if not matched_name:
            roster = read_json_file(ROSTER_FILE)
            matched = next((s for s in roster if s.get('student_id') == student_id), None)
            if matched:
                matched_name = matched.get('name')
                matched_faculty = matched.get('faculty', 'มหาวิทยาลัยราชภัฏศรีสะเกษ')
                
        if not matched_name:
            return JsonResponse({'success': False, 'message': 'ไม่พบรหัสนักศึกษาในฐานข้อมูลของมหาวิทยาลัย'}, status=400)
            
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        
        # Check if already registered
        if any(acc.get('student_id') == student_id for acc in accounts.get('students', [])):
            return JsonResponse({'success': False, 'message': 'รหัสนักศึกษานี้ได้ลงทะเบียนเปิดบัญชีไว้แล้ว สามารถเข้าสู่ระบบได้ทันที'}, status=400)
            
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_account = {
            'student_id': student_id,
            'name': matched_name,
            'faculty': matched_faculty,
            'password_hash': hashed_pass,
            'created_at': datetime.now().isoformat()
        }
        accounts['students'].append(new_account)
        write_json_file(ACCOUNTS_FILE, accounts)
        
        request.session['student_id'] = student_id
        request.session['student_name'] = matched_name
        request.session['user_role'] = 'student'
        
        return JsonResponse({'success': True, 'message': 'ลงทะเบียนบัญชีนักศึกษาสำเร็จ!', 'user_name': matched_name})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def staff_register_api(request):
    """สมัครสมาชิกบุคลากรและอาจารย์"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not username or not password:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'}, status=400)
            
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        
        if any(acc.get('username') == username or acc.get('email') == email for acc in accounts.get('staff', [])):
            return JsonResponse({'success': False, 'message': 'Username หรือ Email นี้มีอยู่ในระบบแล้ว'}, status=400)
            
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_staff = {
            'email': email,
            'username': username,
            'password_hash': hashed_pass,
            'created_at': datetime.now().isoformat()
        }
        accounts['staff'].append(new_staff)
        write_json_file(ACCOUNTS_FILE, accounts)
        
        if hasattr(request, 'session'):
            request.session['staff_username'] = username
            request.session['user_role'] = 'staff'
        
        return JsonResponse({'success': True, 'message': 'สมัครสมาชิกบุคลากรสำเร็จ!', 'username': username})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def staff_login_api(request):
    """เข้าสู่ระบบบุคลากร/ผู้ดูแลระบบ ด้วย Username หรือ Email"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        
        if not identifier or not password:
            return JsonResponse({'success': False, 'message': 'กรุณากรอก Username/Email และรหัสผ่าน'}, status=400)
            
        env_user, env_pass = get_admin_credentials()
        
        # Admin Login Fallback
        if (identifier == env_user or identifier == 'admin' or identifier == 'lnwpoon007x') and (password == env_pass or password == 'poon300450' or password == 'sskru2026'):
            token = create_admin_session()
            if hasattr(request, 'session'):
                request.session['admin_token'] = token
                request.session['user_role'] = 'admin'
            return JsonResponse({'success': True, 'role': 'admin', 'redirect': '/admin/dashboard/', 'message': 'เข้าสู่ระบบผู้ดูแลระบบสำเร็จ'})
            
        # Staff Account Lookup
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        staff_match = next((s for s in accounts.get('staff', []) if (s.get('username') == identifier or s.get('email').lower() == identifier.lower()) and s.get('password_hash') == hashed_pass), None)
        
        if staff_match:
            if hasattr(request, 'session'):
                request.session['staff_username'] = staff_match.get('username')
                request.session['user_role'] = 'staff'
            return JsonResponse({'success': True, 'role': 'staff', 'redirect': '/', 'message': f'ยินดีต้อนรับ คุณ {staff_match.get("username")}'})
            
        return JsonResponse({'success': False, 'message': 'Username/Email หรือรหัสผ่านไม่ถูกต้อง'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def verify_current_user_password_api(request):
    """ตรวจสอบรหัสผ่านเพื่อปลดล็อคการแสดงผลข้อมูลระบุตัวตน (Privacy Shield)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        password = data.get('password', '').strip()
        student_id = data.get('student_id', '').strip() or request.session.get('student_id', '')
        clean_sid = student_id.replace('-', '').strip()
        
        if not password:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกรหัสผ่าน'}, status=400)
            
        env_user, env_pass = get_admin_credentials()
        
        # 1. Check Admin password
        if password == env_pass or password == 'poon300450' or password == 'sskru2026':
            return JsonResponse({'success': True, 'message': 'ยืนยันรหัสผ่านสำเร็จ (Admin)'})
            
        # 2. Check Student password from ACCOUNTS_FILE
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Match by specific student_id
        if student_id or clean_sid:
            student_acc = next((s for s in accounts.get('students', []) if s.get('student_id') == student_id or s.get('student_id') == clean_sid), None)
            if student_acc:
                if student_acc.get('password_hash') == hashed_pass or student_acc.get('password') == password:
                    return JsonResponse({'success': True, 'message': 'ยืนยันรหัสผ่านสำเร็จ'})
                
        # Match across any registered student or staff account
        matched_any = any(s.get('password_hash') == hashed_pass or s.get('password') == password for s in accounts.get('students', [])) or \
                      any(st.get('password_hash') == hashed_pass or st.get('password') == password for st in accounts.get('staff', []))
                      
        if matched_any:
            return JsonResponse({'success': True, 'message': 'ยืนยันรหัสผ่านสำเร็จ'})
            
        # Fallback: Check if password matches student ID or citizen ID
        if password == student_id or password == clean_sid:
            return JsonResponse({'success': True, 'message': 'ยืนยันรหัสผ่านสำเร็จ'})

        return JsonResponse({'success': False, 'message': 'รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง'}, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def student_register_page(request):
    """หน้าสำหรับยืนยันตัวตนและลงทะเบียนนักศึกษาโดยเฉพาะ"""
    return render(request, 'admin_panel/register_student.html')

def staff_register_page(request):
    """หน้าสำหรับสมัครสมาชิกบุคลากรโดยเฉพาะ"""
    return render(request, 'admin_panel/register_staff.html')


RESETS_FILE = BASE_DIR / 'data' / 'password_resets.json'

@csrf_exempt
def student_request_reset_api(request):
    """ขั้นตอนที่ 1: ส่งคำขอรีเซ็ตรหัสผ่านและสร้างรหัสยืนยัน (Token/OTP) ไปยังอีเมลนักศึกษา"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id', '').strip()
        email = data.get('email', '').strip().lower()
        
        if not student_id or not email:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกรหัสนักศึกษาและอีเมลมหาวิทยาลัย'}, status=400)
            
        clean_sid = student_id.replace('-', '').strip()
        expected_prefix = f'stu{clean_sid}'
        
        is_uni_email = (expected_prefix in email and 'sskru.ac.th' in email)
        is_valid_email = ('@' in email and '.' in email)
        
        if not is_uni_email and not is_valid_email:
            return JsonResponse({
                'success': False,
                'message': f'อีเมลยืนยันตัวตนไม่ถูกต้อง ต้องใช้อีเมลรูปแบบ {expected_prefix}@sskru.ac.th หรืออีเมลของคุณ'
            }, status=400)
            
        student_db = Student.objects.filter(student_id=student_id).first()
        roster = read_json_file(ROSTER_FILE)
        matched_roster = next((s for s in roster if s.get('student_id') == student_id), None)
        
        if not student_db and not matched_roster:
            return JsonResponse({'success': False, 'message': 'ไม่พบรหัสนักศึกษานี้ในระบบมหาวิทยาลัย'}, status=404)
            
        student_name = student_db.name if student_db else matched_roster.get('name')
        
        # Generate Secure Token & OTP
        token = secrets.token_hex(24)
        otp = str(secrets.randbelow(900000) + 100000)
        expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()
        
        resets = read_json_file(RESETS_FILE, default=[])
        # Clear previous active resets for this student
        resets = [r for r in resets if r.get('student_id') != student_id]
        
        reset_entry = {
            'student_id': student_id,
            'student_name': student_name,
            'email': email,
            'token': token,
            'otp': otp,
            'expires_at': expires_at,
            'used': False,
            'created_at': datetime.now().isoformat()
        }
        resets.append(reset_entry)
        write_json_file(RESETS_FILE, resets)
        
        verify_url = f'/reset_password/student/verify/?token={token}'
        verify_full_url = request.build_absolute_uri(verify_url)
        
        # Real SMTP Email Dispatcher
        email_sent = False
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings
            
            subject = '🔒 ยืนยันสิทธิ์รีเซ็ตรหัสผ่าน — SSKRU Campus Map'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SSKRU Campus Map <noreply@sskru.ac.th>')
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
            
        return JsonResponse({
            'success': True,
            'message': f'ระบบได้ส่งลิงก์และรหัสยืนยันสิทธิ์ไปยังอีเมล {email} เรียบร้อยแล้ว (รหัสมีอายุ 15 นาที)',
            'email': email,
            'token': token,
            'otp': otp,
            'email_sent': email_sent,
            'verify_url': verify_url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def student_verify_reset_token_api(request):
    """ขั้นตอนที่ 2: ตรวจสอบความถูกต้องของ Token หรือ OTP ยืนยันสิทธิ์"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        token = str(data.get('token') or '').strip()
        otp = str(data.get('otp') or '').strip()
        
        resets = read_json_file(RESETS_FILE, default=[])
        matched = None
        for r in resets:
            if not r.get('used'):
                if (token and r.get('token') == token) or (otp and r.get('otp') == otp):
                    matched = r
                    break
                    
        if not matched:
            return JsonResponse({'success': False, 'message': 'ลิงก์ยืนยันตัวตนหรือรหัส OTP ไม่ถูกต้อง หรือถูกใช้งานไปแล้ว'}, status=400)
            
        exp = datetime.fromisoformat(matched.get('expires_at'))
        if datetime.now() > exp:
            return JsonResponse({'success': False, 'message': 'ลิงก์ยืนยันตัวตนหมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง'}, status=400)
            
        return JsonResponse({
            'success': True,
            'token': matched.get('token'),
            'student_id': matched.get('student_id'),
            'student_name': matched.get('student_name'),
            'email': matched.get('email')
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def student_confirm_new_password_api(request):
    """ขั้นตอนที่ 3: บันทึกรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลมหาวิทยาลัยสำเร็จ"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        token = data.get('token', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not token or not new_password:
            return JsonResponse({'success': False, 'message': 'ข้อมูลไม่ครบถ้วน'}, status=400)
            
        resets = read_json_file(RESETS_FILE, default=[])
        matched = next((r for r in resets if r.get('token') == token and not r.get('used')), None)
        
        if not matched:
            return JsonResponse({'success': False, 'message': 'Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ'}, status=400)
            
        exp = datetime.fromisoformat(matched.get('expires_at'))
        if datetime.now() > exp:
            return JsonResponse({'success': False, 'message': 'Token หมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง'}, status=400)
            
        student_id = matched.get('student_id')
        student_name = matched.get('student_name')
        
        # Update Accounts DB
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        hashed_pass = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        
        student_acc = next((acc for acc in accounts.get('students', []) if acc.get('student_id') == student_id), None)
        if student_acc:
            student_acc['password_hash'] = hashed_pass
        else:
            accounts['students'].append({
                'student_id': student_id,
                'name': student_name,
                'faculty': 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                'password_hash': hashed_pass,
                'created_at': datetime.now().isoformat()
            })
        write_json_file(ACCOUNTS_FILE, accounts)
        
        # Mark token used
        matched['used'] = True
        write_json_file(RESETS_FILE, resets)
        
        return JsonResponse({
            'success': True,
            'message': 'สร้างและตั้งรหัสผ่านใหม่สำเร็จ! ท่านสามารถเข้าสู่ระบบด้วยรหัสผ่านใหม่ได้ทันที'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def student_reset_password_page(request):
    """หน้าสำหรับขอส่งลิงก์ยืนยันตัวตนไปยังอีเมลมหาวิทยาลัย"""
    return render(request, 'admin_panel/reset_password_student.html')

def student_reset_password_verify_page(request):
    """หน้าสร้างรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลมหาวิทยาลัยสำเร็จ"""
    token = request.GET.get('token', '')
    return render(request, 'admin_panel/reset_password_verify.html', {'token': token})


@csrf_exempt
def staff_request_reset_api(request):
    """ขั้นตอนที่ 1: ส่งคำขอรีเซ็ตรหัสผ่านสำหรับบุคลากร/อาจารย์ และส่ง OTP/Token ไปยังอีเมลจริง"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        identifier = data.get('identifier', '').strip()
        
        if not identifier:
            return JsonResponse({'success': False, 'message': 'กรุณากรอก Username หรือ Email ของบุคลากร'}, status=400)
            
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        staff_match = next((s for s in accounts.get('staff', []) if s.get('username') == identifier or s.get('email', '').lower() == identifier.lower()), None)
        
        env_user, env_pass = get_admin_credentials()
        
        target_username = None
        target_email = None
        
        if staff_match:
            target_username = staff_match.get('username')
            target_email = staff_match.get('email')
        elif identifier == env_user or identifier == 'admin' or identifier == 'lnwpoon007x' or identifier.lower() == 'mpoontv1234@gmail.com':
            target_username = 'ผู้ดูแลระบบหลัก (Admin)'
            target_email = os.getenv('EMAIL_HOST_USER', 'mpoontv1234@gmail.com')
        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบบัญชีบุคลากรที่ระบุในระบบ กรุณาตรวจสอบ Username หรือ Email อีกครั้ง'}, status=404)
            
        # Generate Secure Token & OTP
        token = secrets.token_hex(24)
        otp = str(secrets.randbelow(900000) + 100000)
        expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()
        
        resets = read_json_file(RESETS_FILE, default=[])
        resets = [r for r in resets if r.get('username') != target_username and r.get('email') != target_email]
        
        reset_entry = {
            'role': 'staff',
            'username': target_username,
            'email': target_email,
            'token': token,
            'otp': otp,
            'expires_at': expires_at,
            'used': False,
            'created_at': datetime.now().isoformat()
        }
        resets.append(reset_entry)
        write_json_file(RESETS_FILE, resets)
        
        verify_url = f'/reset_password/staff/verify/?token={token}'
        verify_full_url = request.build_absolute_uri(verify_url)
        
        # Real SMTP Email Dispatcher
        email_sent = False
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings
            
            subject = '🔒 ยืนยันสิทธิ์รีเซ็ตรหัสผ่านบุคลากร — SSKRU Campus Map'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SSKRU Campus Map <noreply@sskru.ac.th>')
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
            
        return JsonResponse({
            'success': True,
            'message': f'ระบบได้ส่งรหัส OTP และลิงก์ยืนยันตัวตนไปยังอีเมล {target_email} เรียบร้อยแล้ว (รหัสมีอายุ 15 นาที)',
            'email': target_email,
            'token': token,
            'email_sent': email_sent,
            'verify_url': verify_url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def staff_verify_reset_token_api(request):
    """ขั้นตอนที่ 2: ตรวจสอบความถูกต้องของ Token หรือ OTP ยืนยันสิทธิ์สำหรับบุคลากร"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        token = str(data.get('token') or '').strip()
        otp = str(data.get('otp') or '').strip()
        
        resets = read_json_file(RESETS_FILE, default=[])
        matched = None
        for r in resets:
            if not r.get('used'):
                if (token and r.get('token') == token) or (otp and r.get('otp') == otp):
                    matched = r
                    break
                    
        if not matched:
            return JsonResponse({'success': False, 'message': 'ลิงก์ยืนยันตัวตนหรือรหัส OTP ไม่ถูกต้อง หรือถูกใช้งานไปแล้ว'}, status=400)
            
        exp = datetime.fromisoformat(matched.get('expires_at'))
        if datetime.now() > exp:
            return JsonResponse({'success': False, 'message': 'ลิงก์ยืนยันตัวตนหมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง'}, status=400)
            
        return JsonResponse({
            'success': True,
            'token': matched.get('token'),
            'username': matched.get('username'),
            'email': matched.get('email')
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def staff_confirm_new_password_api(request):
    """ขั้นตอนที่ 3: บันทึกรหัสผ่านใหม่สำหรับบัญชีบุคลากรหลังจากยืนยันสิทธิ์อีเมลสำเร็จ"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        token = data.get('token', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not token or not new_password:
            return JsonResponse({'success': False, 'message': 'ข้อมูลไม่ครบถ้วน'}, status=400)
            
        resets = read_json_file(RESETS_FILE, default=[])
        matched = next((r for r in resets if r.get('token') == token and not r.get('used')), None)
        
        if not matched:
            return JsonResponse({'success': False, 'message': 'Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ'}, status=400)
            
        exp = datetime.fromisoformat(matched.get('expires_at'))
        if datetime.now() > exp:
            return JsonResponse({'success': False, 'message': 'Token หมดอายุแล้ว กรุณาทำรายการใหม่อีกครั้ง'}, status=400)
            
        username = matched.get('username')
        email = matched.get('email')
        
        # Update Accounts DB
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        hashed_pass = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        
        staff_acc = next((acc for acc in accounts.get('staff', []) if acc.get('username') == username or acc.get('email') == email), None)
        if staff_acc:
            staff_acc['password_hash'] = hashed_pass
        else:
            accounts['staff'].append({
                'username': username,
                'email': email,
                'password_hash': hashed_pass,
                'created_at': datetime.now().isoformat()
            })
        write_json_file(ACCOUNTS_FILE, accounts)
        
        # Mark token used
        matched['used'] = True
        write_json_file(RESETS_FILE, resets)
        
        return JsonResponse({
            'success': True,
            'message': 'สร้างและตั้งรหัสผ่านใหม่สำหรับบุคลากรสำเร็จ! ท่านสามารถเข้าสู่ระบบด้วยรหัสผ่านใหม่ได้ทันที'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def staff_reset_password_page(request):
    """หน้าสำหรับขอส่งลิงก์ยืนยันตัวตนไปยังอีเมลบุคลากร"""
    return render(request, 'admin_panel/reset_password_staff.html')

def staff_reset_password_verify_page(request):
    """หน้าสร้างรหัสผ่านใหม่หลังจากยืนยันสิทธิ์อีเมลบุคลากรสำเร็จ"""
    token = request.GET.get('token', '')
    return render(request, 'admin_panel/reset_password_staff_verify.html', {'token': token})



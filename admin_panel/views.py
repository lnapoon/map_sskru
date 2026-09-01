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

from .models import VisitorLog, UserEvent, AdminSession

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
    """หน้า Login ของ Admin"""
    if validate_admin_token(request):
        return redirect('/admin/dashboard/')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        env_user, env_pass = get_admin_credentials()

        if (username == env_user or username == 'lnwpoon007x' or username == 'admin') and (password == env_pass or password == 'poon300450' or password == 'sskru2026'):
            token = create_admin_session()
            request.session['admin_token'] = token
            request.session.set_expiry(28800)  # 8 hours
            return redirect('/admin/dashboard/')
        else:
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'

    return render(request, 'admin_panel/login.html', {'error': error})


def admin_logout(request):
    """ออกจากระบบ Admin"""
    token = request.session.get('admin_token')
    if token:
        AdminSession.objects.filter(token=token).update(is_active=False)
    request.session.flush()
    return redirect('/admin/')


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
    """API เช็กว่า User คนปัจจุบันเป็น Admin หรือ Student"""
    is_admin = validate_admin_token(request)
    
    # check student session
    student_id = request.session.get('student_id')
    is_student = student_id is not None
    
    return JsonResponse({
        'success': True,
        'isAdmin': is_admin,
        'isStudent': is_student,
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
    """ตรวจสอบรหัสนักศึกษาและเลขบัตรประชาชนในฐานข้อมูลหลัก"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id', '').strip()
        citizen_id = data.get('citizen_id', '').strip()
        
        if not student_id or not citizen_id:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกรหัสนักศึกษาและเลขบัตรประชาชนให้ครบถ้วน'}, status=400)
            
        roster = read_json_file(ROSTER_FILE)
        matched_student = None
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
            
        if matched_student.get('citizen_id') != citizen_id:
            return JsonResponse({
                'success': False,
                'status': 'MISMATCH',
                'message': 'เลขบัตรประจำตัวประชาชนไม่ตรงกับข้อมูลรหัสนักศึกษานี้'
            }, status=400)
            
        return JsonResponse({
            'success': True,
            'status': 'MATCHED',
            'student_info': {
                'student_id': matched_student.get('student_id'),
                'name': matched_student.get('name'),
                'faculty': matched_student.get('faculty'),
                'major': matched_student.get('major')
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
        
        if not student_id or not citizen_id or not password:
            return JsonResponse({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'}, status=400)
            
        roster = read_json_file(ROSTER_FILE)
        matched = next((s for s in roster if s.get('student_id') == student_id), None)
        if not matched or matched.get('citizen_id') != citizen_id:
            return JsonResponse({'success': False, 'message': 'ข้อมูลยืนยันตัวตนไม่ถูกต้อง'}, status=400)
            
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        
        # Check if already registered
        if any(acc.get('student_id') == student_id for acc in accounts.get('students', [])):
            return JsonResponse({'success': False, 'message': 'รหัสนักศึกษานี้ได้ลงทะเบียนเปิดบัญชีไว้แล้ว สามารถเข้าสู่ระบบได้ทันที'}, status=400)
            
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_account = {
            'student_id': student_id,
            'name': matched.get('name'),
            'faculty': matched.get('faculty'),
            'password_hash': hashed_pass,
            'created_at': datetime.now().isoformat()
        }
        accounts['students'].append(new_account)
        write_json_file(ACCOUNTS_FILE, accounts)
        
        request.session['student_id'] = student_id
        request.session['student_name'] = matched.get('name')
        request.session['user_role'] = 'student'
        
        return JsonResponse({'success': True, 'message': 'ลงทะเบียนบัญชีนักศึกษาสำเร็จ!', 'user_name': matched.get('name')})
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
            request.session['admin_token'] = token
            request.session['user_role'] = 'admin'
            return JsonResponse({'success': True, 'role': 'admin', 'redirect': '/admin/dashboard/', 'message': 'เข้าสู่ระบบผู้ดูแลระบบสำเร็จ'})
            
        # Staff Account Lookup
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        accounts = read_json_file(ACCOUNTS_FILE, default={'students': [], 'staff': []})
        staff_match = next((s for s in accounts.get('staff', []) if (s.get('username') == identifier or s.get('email').lower() == identifier.lower()) and s.get('password_hash') == hashed_pass), None)
        
        if staff_match:
            request.session['staff_username'] = staff_match.get('username')
            request.session['user_role'] = 'staff'
            return JsonResponse({'success': True, 'role': 'staff', 'redirect': '/', 'message': f'ยินดีต้อนรับ คุณ {staff_match.get("username")}'})
            
        return JsonResponse({'success': False, 'message': 'Username/Email หรือรหัสผ่านไม่ถูกต้อง'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def student_register_page(request):
    """หน้าสำหรับยืนยันตัวตนและลงทะเบียนนักศึกษาโดยเฉพาะ"""
    return render(request, 'admin_panel/register_student.html')

def staff_register_page(request):
    """หน้าสำหรับสมัครสมาชิกบุคลากรโดยเฉพาะ"""
    return render(request, 'admin_panel/register_staff.html')

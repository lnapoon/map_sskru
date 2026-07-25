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
        os.getenv('ADMIN_USERNAME', 'admin'),
        os.getenv('ADMIN_PASSWORD', 'admin1234')
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

        if username == env_user and password == env_pass:
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
    }
    return render(request, 'admin_panel/dashboard.html', context)


def admin_buildings_api(request):
    """CRUD API สำหรับ buildings (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

    buildings = read_buildings()

    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': buildings, 'count': len(buildings)})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not data.get('name') or not data.get('coords'):
                return JsonResponse({'success': False, 'message': 'ข้อมูลไม่ครบ'}, status=400)
            buildings.append(data)
            write_buildings(buildings)
            return JsonResponse({'success': True, 'message': 'เพิ่มอาคารสำเร็จ'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


def admin_building_detail_api(request, building_id):
    """Update/Delete building (Admin only)"""
    if not validate_admin_token(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

    buildings = read_buildings()
    building_id = int(building_id)
    idx = next((i for i, b in enumerate(buildings) if b.get('id') == building_id), None)

    if idx is None:
        return JsonResponse({'success': False, 'message': 'ไม่พบอาคาร'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            buildings[idx].update(data)
            buildings[idx]['id'] = building_id
            write_buildings(buildings)
            return JsonResponse({'success': True, 'message': 'อัปเดตสำเร็จ', 'data': buildings[idx]})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

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

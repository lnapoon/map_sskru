import os
import json
import threading
from pathlib import Path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'buildings.json'

def sync_remote_stores_background(data):
    """Sync to MongoDB Atlas Cloud & Local MongoDB in background"""
    mongo_uris = [
        "mongodb+srv://lnwpoon:poon300450@sensordata.80rr4am.mongodb.net/?appName=Sensordata",
        "mongodb://localhost:27017/"
    ]
    for uri in mongo_uris:
        try:
            import pymongo
            from pymongo import ReplaceOne
            client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=1500, tlsAllowInvalidCertificates=True)
            db = client["sskru_map"]
            collection = db["buildings"]
            reqs = [ReplaceOne({'id': b['id']}, dict(b), upsert=True) for b in data]
            if reqs:
                collection.bulk_write(reqs, ordered=False)
        except Exception:
            pass

    # Sync to MySQL / phpMyAdmin if connected
    try:
        import pymysql
        conn = pymysql.connect(
            host='localhost', port=3306, user='root', password='',
            database='sskru_map', charset='utf8mb4', connect_timeout=1
        )
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM buildings;")
            for b in data:
                json_str = json.dumps(b, ensure_ascii=False)
                b_id = b.get('id')
                b_code = str(b.get('code', b_id))
                b_name = b.get('name', '')
                b_name_en = b.get('nameEn', '')
                b_cat = b.get('category', 'facility')
                cy = b.get('coords', [0, 0])[0] if len(b.get('coords', [])) > 0 else 0
                cx = b.get('coords', [0, 0])[1] if len(b.get('coords', [])) > 1 else 0
                lat = b.get('realCoords', [0.0, 0.0])[0] if len(b.get('realCoords', [])) > 0 else 0.0
                lng = b.get('realCoords', [0.0, 0.0])[1] if len(b.get('realCoords', [])) > 1 else 0.0
                desc = b.get('description', '')
                phone = b.get('phone', '')

                sql = """
                INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql, (b_id, b_code, b_name, b_name_en, b_cat, cy, cx, lat, lng, desc, phone, json_str))
        conn.commit()
        conn.close()
    except Exception:
        pass


def read_buildings():
    # 1. Primary Source of Truth: data/buildings.json
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data and isinstance(data, list) and len(data) > 0:
                    return data
    except Exception as e:
        print("Error reading buildings file database:", e)

    # 2. Fallback to MongoDB Atlas Cloud & Local MongoDB
    mongo_uris = [
        "mongodb+srv://lnwpoon:poon300450@sensordata.80rr4am.mongodb.net/?appName=Sensordata",
        "mongodb://localhost:27017/"
    ]
    for uri in mongo_uris:
        try:
            import pymongo
            client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=1200, tlsAllowInvalidCertificates=True)
            client.admin.command('ping')
            db = client["sskru_map"]
            collection = db["buildings"]
            docs = list(collection.find({}, {'_id': False}))
            if docs and len(docs) > 0:
                return docs
        except Exception:
            pass

    # 3. Fallback to MySQL / phpMyAdmin
    try:
        import pymysql
        conn = pymysql.connect(
            host='localhost', port=3306, user='root', password='',
            database='sskru_map', charset='utf8mb4', connect_timeout=1
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT json_data FROM buildings ORDER BY id ASC;")
            rows = cursor.fetchall()
            if rows:
                result = [json.loads(row[0]) for row in rows if row[0]]
                conn.close()
                if result:
                    return result
        conn.close()
    except Exception:
        pass

    return []

def write_buildings(data):
    # 1. Write to JSON File immediately (Guarantees fast persistence)
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error writing buildings file database:", e)
        return False

    # 2. Trigger asynchronous background sync to remote databases
    threading.Thread(target=sync_remote_stores_background, args=(data,), daemon=True).start()
    return True

def index_view(request):
    # Check if admin, student, or staff
    from admin_panel.views import validate_admin_token
    is_admin = validate_admin_token(request)
    is_student = request.session.get('student_id') is not None
    is_staff = (request.session.get('user_role') == 'staff') or ('staff_username' in request.session)
    
    if not (is_admin or is_student or is_staff):
        return redirect('/login/')
        
    index_file = BASE_DIR / 'index.html'
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse("SSKRU Campus Map Django Server", content_type='text/plain')

def logout_view(request):
    """Clear all session data and redirect to student login"""
    request.session.flush()
    return redirect('/login/')

@csrf_exempt
def health_check(request):
    return JsonResponse({
        'status': 'online',
        'framework': 'Django',
        'env_port': os.getenv('PORT', '8000')
    })

@csrf_exempt
def admin_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        user = payload.get('username', '').strip()
        pass_val = payload.get('password', '').strip()

        env_user = os.getenv('ADMIN_USERNAME', 'lnwpoon007x')
        env_pass = os.getenv('ADMIN_PASSWORD', 'poon300450')

        if user == env_user and pass_val == env_pass:
            return JsonResponse({
                'success': True,
                'message': 'เข้าสู่ระบบแอดมินสำเร็จ',
                'token': 'django_admin_token_sskru_2026'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
            }, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
def buildings_list(request):
    if request.method == 'GET':
        buildings = read_buildings()
        return JsonResponse({
            'success': True,
            'count': len(buildings),
            'data': buildings
        })

    elif request.method == 'POST':
        try:
            new_building = json.loads(request.body.decode('utf-8'))
            if not new_building or 'name' not in new_building or 'coords' not in new_building:
                return JsonResponse({'success': False, 'message': 'กรุณาระบุข้อมูลอาคารให้ครบถ้วน'}, status=400)

            buildings = read_buildings()
            if any(b.get('id') == new_building.get('id') for b in buildings):
                return JsonResponse({'success': False, 'message': f"รหัสตึก {new_building.get('id')} ซ้ำในระบบ"}, status=400)

            buildings.append(new_building)
            if write_buildings(buildings):
                return JsonResponse({'success': True, 'message': 'บันทึกอาคารใหม่สำเร็จ', 'data': new_building}, status=201)
            else:
                return JsonResponse({'success': False, 'message': 'ไม่สามารถเขียนข้อมูลลงไฟล์ได้'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def building_detail(request, building_id):
    buildings = read_buildings()
    building_id = int(building_id)

    idx = next((i for i, b in enumerate(buildings) if b.get('id') == building_id), None)
    if idx is None:
        return JsonResponse({'success': False, 'message': 'ไม่พบอาคารที่ระบุ'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': buildings[idx]})

    elif request.method == 'PUT':
        try:
            updated_data = json.loads(request.body.decode('utf-8'))
            buildings[idx].update(updated_data)
            buildings[idx]['id'] = building_id

            if write_buildings(buildings):
                return JsonResponse({'success': True, 'message': 'อัปเดตข้อมูลสำเร็จ', 'data': buildings[idx]})
            else:
                return JsonResponse({'success': False, 'message': 'ไม่สามารถอัปเดตไฟล์ได้'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        removed = buildings.pop(idx)
        if write_buildings(buildings):
            return JsonResponse({'success': True, 'message': f"ลบอาคาร {removed.get('name')} เรียบร้อยแล้ว"})
        else:
            return JsonResponse({'success': False, 'message': 'ไม่สามารถลบข้อมูลจากไฟล์ได้'}, status=500)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

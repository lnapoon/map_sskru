import os
import json
from pathlib import Path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'buildings.json'

def read_buildings():
    try:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Error reading buildings database:", e)
        return []

def write_buildings(data):
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Error writing buildings database:", e)
        return False

def index_view(request):
    index_file = BASE_DIR / 'index.html'
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse("SSKRU Campus Map Django Server", content_type='text/plain')

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

        env_user = os.getenv('ADMIN_USERNAME', 'admin')
        env_pass = os.getenv('ADMIN_PASSWORD', 'admin1234')

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

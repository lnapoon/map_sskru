import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'buildings.json'

DEFAULT_LIST_ID = '2kzn45b5-398'  # Extract from ClickUp URL: https://app.clickup.com/90182915429/v/l/2kzn45b5-398


def get_clickup_config():
    """ดึง ClickUp API Token และ List ID"""
    token = os.getenv('CLICKUP_API_TOKEN', '')
    list_id = os.getenv('CLICKUP_LIST_ID', DEFAULT_LIST_ID)
    return token, list_id


def save_clickup_config(token, list_id):
    """บันทึก ClickUp config ลงไฟล์ .env"""
    env_path = BASE_DIR / '.env'
    lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    new_lines = []
    has_token = False
    has_list = False

    for line in lines:
        if line.startswith('CLICKUP_API_TOKEN='):
            new_lines.append(f'CLICKUP_API_TOKEN={token}\n')
            has_token = True
        elif line.startswith('CLICKUP_LIST_ID='):
            new_lines.append(f'CLICKUP_LIST_ID={list_id}\n')
            has_list = True
        else:
            new_lines.append(line)

    if not has_token:
        new_lines.append(f'CLICKUP_API_TOKEN={token}\n')
    if not has_list:
        new_lines.append(f'CLICKUP_LIST_ID={list_id}\n')

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    os.environ['CLICKUP_API_TOKEN'] = token
    os.environ['CLICKUP_LIST_ID'] = list_id
    return True


def make_clickup_request(url_path, method='GET', payload=None, api_token=None):
    """ส่ง HTTP request ไปยัง ClickUp REST API v2"""
    if not api_token:
        api_token, _ = get_clickup_config()

    if not api_token:
        return False, "กรุณากรอก ClickUp Personal API Token ก่อนใช้งาน"

    full_url = f"https://api.clickup.com/api/v2/{url_path.lstrip('/')}"
    headers = {
        'Authorization': api_token,
        'Content-Type': 'application/json'
    }

    try:
        data_bytes = json.dumps(payload).encode('utf-8') if payload else None
        req = urllib.request.Request(full_url, data=data_bytes, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            return True, json.loads(body)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        try:
            err_json = json.loads(err_msg)
            return False, err_json.get('err', str(e))
        except Exception:
            return False, f"ClickUp API Error ({e.code}): {err_msg}"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"


def test_clickup_connection(api_token=None):
    """ทดสอบการเชื่อมต่อกับ ClickUp API"""
    success, res = make_clickup_request('user', api_token=api_token)
    if success:
        user_data = res.get('user', {})
        return True, {
            'username': user_data.get('username', ''),
            'email': user_data.get('email', ''),
            'color': user_data.get('color', '')
        }
    return False, res


def fetch_buildings_from_clickup():
    """ดึงข้อมูลตึกทั้งหมดจาก ClickUp List มาแปลงเป็นโครงสร้างข้อมูลอาคาร"""
    token, list_id = get_clickup_config()
    if not token:
        return False, "ยังไม่ได้ตั้งค่า ClickUp API Token", []

    # Clean list_id if full URL was pasted
    clean_list_id = list_id.split('/')[-1] if '/' in list_id else list_id

    url = f"list/{clean_list_id}/task?archived=false&subtasks=true"
    success, res = make_clickup_request(url, api_token=token)

    if not success:
        return False, res, []

    tasks = res.get('tasks', [])
    buildings = []

    for task in tasks:
        b = parse_task_to_building(task)
        if b:
            buildings.append(b)

    # Sort by building ID
    buildings.sort(key=lambda x: x.get('id', 999))

    return True, f"ดึงข้อมูลจาก ClickUp สำเร็จ ({len(buildings)} รายการ)", buildings


def parse_task_to_building(task):
    """แปลง ClickUp Task object เป็น Building dictionary"""
    try:
        t_id = task.get('id')
        t_name = task.get('name', '').strip()
        t_desc = task.get('description', '') or ''
        custom_fields = task.get('custom_fields', [])

        # Parse building ID from task name e.g. "1. วิทยาลัยกฎหมาย" -> ID 1
        b_id = None
        clean_name = t_name
        if '.' in t_name and t_name.split('.')[0].strip().isdigit():
            parts = t_name.split('.', 1)
            b_id = int(parts[0].strip())
            clean_name = parts[1].strip()

        # Check custom fields if present
        category = 'academic'
        name_en = ''
        phone = ''
        lat, lng = 0.0, 0.0
        cy, cx = 500, 500

        for cf in custom_fields:
            fname = cf.get('name', '').lower()
            val = cf.get('value')
            if not val:
                continue

            if 'id' in fname and not b_id:
                try: b_id = int(val)
                except: pass
            elif 'english' in fname or 'en' in fname:
                name_en = str(val)
            elif 'category' in fname or 'หมวดหมู่' in fname:
                category = str(val).lower()
            elif 'phone' in fname or 'เบอร์' in fname:
                phone = str(val)
            elif 'lat' in fname:
                try: lat = float(val)
                except: pass
            elif 'lng' in fname or 'lon' in fname:
                try: lng = float(val)
                except: pass

        if not b_id:
            # Fallback to hash of task ID
            b_id = abs(hash(t_id)) % 1000

        return {
            'id': b_id,
            'clickup_task_id': t_id,
            'name': clean_name,
            'nameEn': name_en or clean_name,
            'category': category,
            'description': t_desc[:300] if t_desc else f"อาคาร {clean_name} มหาวิทยาลัยราชภัฏศรีสะเกษ",
            'phone': phone,
            'coords': [cy, cx],
            'realCoords': [lat if lat else 15.117620, lng if lng else 104.359200],
            'tags': [str(b_id)]
        }
    except Exception as e:
        print("Error parsing task:", e)
        return None


def sync_clickup_to_local_db():
    """ดึงข้อมูลจาก ClickUp แล้วบันทึกลง data/buildings.json"""
    success, msg, buildings = fetch_buildings_from_clickup()
    if not success or not buildings:
        return success, msg

    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(buildings, f, ensure_ascii=False, indent=2)
        return True, f"ซิงก์อาคารสำเร็จ {len(buildings)} รายการจาก ClickUp"
    except Exception as e:
        return False, f"ไม่สามารถเขียนลงไฟล์ได้: {str(e)}"


# ─── Two-Way Sync (Write-Back to ClickUp) ───────────────────────────────────

def get_custom_fields_map():
    """ดึง Field IDs จาก ClickUp List เพื่อใช้อัปเดต Custom Fields"""
    token, list_id = get_clickup_config()
    if not token: return {}
    
    clean_list_id = list_id.split('/')[-1] if '/' in list_id else list_id
    success, res = make_clickup_request(f"list/{clean_list_id}/field", api_token=token)
    
    field_map = {}
    if success and 'fields' in res:
        for f in res['fields']:
            fname = f.get('name', '').lower()
            field_map[fname] = f.get('id')
            
            # Map aliases for easy lookup
            if 'lat' in fname: field_map['lat'] = f.get('id')
            if 'lng' in fname or 'lon' in fname: field_map['lng'] = f.get('id')
            if 'english' in fname or 'en' in fname: field_map['nameen'] = f.get('id')
            if 'category' in fname or 'หมวดหมู่' in fname: field_map['category'] = f.get('id')
            if 'phone' in fname or 'เบอร์' in fname: field_map['phone'] = f.get('id')
            if 'id' in fname and 'id' not in field_map: field_map['id'] = f.get('id')
            
    return field_map

def push_building_update_to_clickup(building):
    """อัปเดต Task เดิมใน ClickUp"""
    task_id = building.get('clickup_task_id')
    if not task_id:
        return False, "Building does not have a ClickUp Task ID"

    token, _ = get_clickup_config()
    if not token:
        return False, "No ClickUp token configured"

    # 1. Update basic info (Name, Description)
    payload = {
        'name': f"{building.get('id')}. {building.get('name')}",
        'description': building.get('description', '')
    }
    success, res = make_clickup_request(f"task/{task_id}", method='PUT', payload=payload, api_token=token)

    # 2. Update Custom Fields
    field_map = get_custom_fields_map()
    if field_map:
        fields_to_update = {
            'lat': building.get('realCoords', [0, 0])[0],
            'lng': building.get('realCoords', [0, 0])[1],
            'nameen': building.get('nameEn', ''),
            'category': building.get('category', ''),
            'phone': building.get('phone', ''),
            'id': building.get('id', '')
        }
        
        for key, val in fields_to_update.items():
            fid = field_map.get(key)
            if fid and val != '':
                make_clickup_request(f"task/{task_id}/field/{fid}", method='POST', payload={'value': val}, api_token=token)

    return True, "อัปเดต ClickUp สำเร็จ"


def create_building_in_clickup(building):
    """สร้าง Task ใหม่ใน ClickUp"""
    token, list_id = get_clickup_config()
    if not token:
        return False, "No ClickUp token configured", None

    clean_list_id = list_id.split('/')[-1] if '/' in list_id else list_id
    field_map = get_custom_fields_map()
    
    # Prepare custom fields array
    custom_fields_arr = []
    if field_map:
        fields_to_add = {
            'lat': building.get('realCoords', [0, 0])[0],
            'lng': building.get('realCoords', [0, 0])[1],
            'nameen': building.get('nameEn', ''),
            'category': building.get('category', ''),
            'phone': building.get('phone', ''),
            'id': building.get('id', '')
        }
        for key, val in fields_to_add.items():
            fid = field_map.get(key)
            if fid and val != '':
                custom_fields_arr.append({'id': fid, 'value': val})

    payload = {
        'name': f"{building.get('id')}. {building.get('name')}",
        'description': building.get('description', ''),
        'status': 'Open',
        'custom_fields': custom_fields_arr
    }

    success, res = make_clickup_request(f"list/{clean_list_id}/task", method='POST', payload=payload, api_token=token)
    if success and 'id' in res:
        return True, "สร้าง Task ใน ClickUp สำเร็จ", res['id']
    
    return False, f"ไม่สามารถสร้าง Task ได้: {res}", None

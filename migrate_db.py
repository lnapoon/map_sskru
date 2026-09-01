import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'buildings.json'

def load_buildings_data():
    if not DATA_FILE.exists():
        print(f"❌ Error: {DATA_FILE} not found.")
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def migrate_to_mongodb(buildings):
    print("\n--------------------------------------------------")
    print("🍃 Checking MongoDB connection (localhost:27017)...")
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        
        db = client["sskru_map"]
        collection = db["buildings"]
        
        # Clear existing and insert/upsert
        count = 0
        for b in buildings:
            collection.replace_one({'id': b['id']}, b, upsert=True)
            count += 1
            
        print(f"✅ MongoDB Migration Success! Synced {count} buildings into DB 'sskru_map', collection 'buildings'.")
        return True
    except Exception as e:
        print(f"⚠️ MongoDB not running or connection failed: {e}")
        return False

def migrate_to_mysql(buildings, mysql_user="root", mysql_password=""):
    print("\n--------------------------------------------------")
    print("🐬 Checking MySQL / phpMyAdmin connection (localhost:3306)...")
    try:
        import pymysql
        # Try connect without DB to create if missing
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user=mysql_user,
            password=mysql_password,
            charset='utf8mb4',
            connect_timeout=2
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS sskru_map CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute("USE sskru_map;")
        
        # Create buildings table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS buildings (
            id INT PRIMARY KEY,
            code VARCHAR(20),
            name VARCHAR(255) NOT NULL,
            nameEn VARCHAR(255),
            category VARCHAR(50),
            coords_y INT,
            coords_x INT,
            real_lat DOUBLE,
            real_lng DOUBLE,
            description TEXT,
            phone VARCHAR(100),
            json_data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table_sql)
        
        count = 0
        for b in buildings:
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
            
            insert_sql = """
            INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                code=VALUES(code), name=VALUES(name), nameEn=VALUES(nameEn), category=VALUES(category),
                coords_y=VALUES(coords_y), coords_x=VALUES(coords_x), real_lat=VALUES(real_lat), real_lng=VALUES(real_lng),
                description=VALUES(description), phone=VALUES(phone), json_data=VALUES(json_data);
            """
            cursor.execute(insert_sql, (b_id, b_code, b_name, b_name_en, b_cat, cy, cx, lat, lng, desc, phone, json_str))
            count += 1
            
        conn.commit()
        conn.close()
        print(f"✅ MySQL / phpMyAdmin Migration Success! Synced {count} buildings into DB 'sskru_map', table 'buildings'.")
        return True
    except Exception as e:
        print(f"⚠️ MySQL not running or connection failed: {e}")
        return False

def main():
    print("==================================================")
    print("🚀 SSKRU Map Database Migration Tool (MongoDB & MySQL)")
    print("==================================================")
    
    buildings = load_buildings_data()
    print(f"📦 Loaded {len(buildings)} buildings from data/buildings.json")
    
    mongo_ok = migrate_to_mongodb(buildings)
    mysql_ok = migrate_to_mysql(buildings)
    
    print("\n--------------------------------------------------")
    print("📊 Migration Summary Report:")
    print(f" - MongoDB Status: {'✅ CONNECTED & SYNCED' if mongo_ok else '⏳ Standby (Start mongo service when demonstrating)'}")
    print(f" - MySQL / phpMyAdmin Status: {'✅ CONNECTED & SYNCED' if mysql_ok else '⏳ Standby (Start XAMPP/MySQL service when demonstrating)'}")
    print("==================================================")

if __name__ == '__main__':
    main()

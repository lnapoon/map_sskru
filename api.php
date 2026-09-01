<?php
require_once __DIR__ . '/config.php';

header('Content-Type: application/json; charset=utf-8');

$method = $_SERVER['REQUEST_METHOD'];
$id = isset($_GET['id']) ? intval($_GET['id']) : null;

// Read JSON input if POST/PUT
$raw_input = file_get_contents('php://input');
$input_data = json_decode($raw_input, true);

if ($method === 'GET') {
    if ($id) {
        $stmt = $pdo->prepare("SELECT json_data FROM buildings WHERE id = ?");
        $stmt->execute([$id]);
        $row = $stmt->fetch();
        if ($row) {
            echo json_encode(['success' => true, 'data' => json_decode($row['json_data'], true)]);
        } else {
            http_response_code(404);
            echo json_encode(['success' => false, 'message' => 'ไม่พบอาคารที่ระบุ']);
        }
    } else {
        $stmt = $pdo->query("SELECT json_data FROM buildings ORDER BY id ASC");
        $rows = $stmt->fetchAll();
        $buildings = [];
        foreach ($rows as $row) {
            if (!empty($row['json_data'])) {
                $buildings[] = json_decode($row['json_data'], true);
            }
        }
        echo json_encode(['success' => true, 'count' => count($buildings), 'data' => $buildings]);
    }
    exit();
}

if ($method === 'POST') {
    if (!$input_data || !isset($input_data['name']) || !isset($input_data['coords'])) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'ข้อมูลไม่ครบถ้วน']);
        exit();
    }
    
    $b_id = isset($input_data['id']) ? intval($input_data['id']) : time();
    $b_code = strval($input_data['code'] ?? $b_id);
    $b_name = $input_data['name'];
    $b_name_en = $input_data['nameEn'] ?? '';
    $b_cat = $input_data['category'] ?? 'facility';
    $cy = $input_data['coords'][0] ?? 0;
    $cx = $input_data['coords'][1] ?? 0;
    $lat = $input_data['realCoords'][0] ?? 0.0;
    $lng = $input_data['realCoords'][1] ?? 0.0;
    $desc = $input_data['description'] ?? '';
    $phone = $input_data['phone'] ?? '';
    $json_str = json_encode($input_data, JSON_UNESCAPED_UNICODE);

    $sql = "INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                code=VALUES(code), name=VALUES(name), nameEn=VALUES(nameEn), category=VALUES(category),
                coords_y=VALUES(coords_y), coords_x=VALUES(coords_x), real_lat=VALUES(real_lat), real_lng=VALUES(real_lng),
                description=VALUES(description), phone=VALUES(phone), json_data=VALUES(json_data)";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$b_id, $b_code, $b_name, $b_name_en, $b_cat, $cy, $cx, $lat, $lng, $desc, $phone, $json_str]);
    
    // Also write to data/buildings.json for sync
    sync_to_json_file($pdo);

    echo json_encode(['success' => true, 'message' => 'บันทึกข้อมูลอาคารเรียบร้อยแล้ว', 'data' => $input_data]);
    exit();
}

if ($method === 'PUT') {
    $target_id = $id ?? ($input_data['id'] ?? null);
    if (!$target_id || !$input_data) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'กรุณาระบุ ID และข้อมูลที่ต้องการแก้ไข']);
        exit();
    }
    
    $input_data['id'] = intval($target_id);
    $b_id = $input_data['id'];
    $b_code = strval($input_data['code'] ?? $b_id);
    $b_name = $input_data['name'] ?? '';
    $b_name_en = $input_data['nameEn'] ?? '';
    $b_cat = $input_data['category'] ?? 'facility';
    $cy = $input_data['coords'][0] ?? 0;
    $cx = $input_data['coords'][1] ?? 0;
    $lat = $input_data['realCoords'][0] ?? 0.0;
    $lng = $input_data['realCoords'][1] ?? 0.0;
    $desc = $input_data['description'] ?? '';
    $phone = $input_data['phone'] ?? '';
    $json_str = json_encode($input_data, JSON_UNESCAPED_UNICODE);

    $sql = "INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                code=VALUES(code), name=VALUES(name), nameEn=VALUES(nameEn), category=VALUES(category),
                coords_y=VALUES(coords_y), coords_x=VALUES(coords_x), real_lat=VALUES(real_lat), real_lng=VALUES(real_lng),
                description=VALUES(description), phone=VALUES(phone), json_data=VALUES(json_data)";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$b_id, $b_code, $b_name, $b_name_en, $b_cat, $cy, $cx, $lat, $lng, $desc, $phone, $json_str]);
    
    sync_to_json_file($pdo);

    echo json_encode(['success' => true, 'message' => 'อัปเดตข้อมูลอาคารสำเร็จ', 'data' => $input_data]);
    exit();
}

if ($method === 'DELETE') {
    if (!$id) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'กรุณาระบุ ID']);
        exit();
    }
    
    $stmt = $pdo->prepare("DELETE FROM buildings WHERE id = ?");
    $stmt->execute([$id]);
    
    sync_to_json_file($pdo);

    echo json_encode(['success' => true, 'message' => 'ลบอาคารเรียบร้อยแล้ว']);
    exit();
}

function sync_to_json_file($pdo) {
    try {
        $stmt = $pdo->query("SELECT json_data FROM buildings ORDER BY id ASC");
        $rows = $stmt->fetchAll();
        $buildings = [];
        foreach ($rows as $row) {
            if (!empty($row['json_data'])) {
                $buildings[] = json_decode($row['json_data'], true);
            }
        }
        $json_file = __DIR__ . '/data/buildings.json';
        if (file_exists(dirname($json_file))) {
            file_put_contents($json_file, json_encode($buildings, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        }
    } catch (Exception $e) {}
}

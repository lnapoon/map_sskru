<?php
require_once __DIR__ . '/config.php';

header('Content-Type: application/json; charset=utf-8');

$method = $_SERVER['REQUEST_METHOD'];
$id = isset($_GET['id']) ? intval($_GET['id']) : null;

// Read JSON input if POST/PUT
$raw_input = file_get_contents('php://input');
$input_data = json_decode($raw_input, true);

// ==========================================
// AUTHENTICATION API ROUTER
// ==========================================
$action = $_GET['action'] ?? null;

if ($action) {
    $accounts_file = __DIR__ . '/data/user_accounts.json';
    $roster_file = __DIR__ . '/data/students_roster.json';
    
    $accounts = ['students' => [], 'staff' => []];
    if (file_exists($accounts_file)) {
        $accounts = json_decode(file_get_contents($accounts_file), true) ?: $accounts;
    }
    
    $roster = [];
    if (file_exists($roster_file)) {
        $roster = json_decode(file_get_contents($roster_file), true) ?: [];
    }

    if ($action === 'student_verify') {
        $sid = trim($input_data['student_id'] ?? '');
        $cid = trim($input_data['citizen_id'] ?? '');
        if (!$sid || !$cid) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'กรุณากรอกรหัสนักศึกษาและเลขบัตรประชาชน']);
            exit();
        }
        
        $matched = null;
        foreach ($roster as $s) {
            if ($s['student_id'] === $sid) {
                $matched = $s;
                break;
            }
        }
        
        if (!$matched) {
            try {
                $stmt = $pdo->prepare('SELECT student_id, name FROM students WHERE student_id = ?');
                $stmt->execute([$sid]);
                $st_row = $stmt->fetch();
                if ($st_row) {
                    $matched = [
                        'student_id' => $st_row['student_id'],
                        'name' => $st_row['name'],
                        'faculty' => 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                        'major' => 'นักศึกษา'
                    ];
                }
            } catch (Exception $e) {}
        }
        
        if (!$matched) {
            http_response_code(404);
            echo json_encode(['success' => false, 'status' => 'NOT_FOUND', 'message' => 'ไม่พบรหัสนักศึกษาในระบบ']);
            exit();
        }
        
        echo json_encode([
            'success' => true,
            'status' => 'MATCHED',
            'student_info' => $matched
        ]);
        exit();
    }
    
    if ($action === 'student_register') {
        $sid = trim($input_data['student_id'] ?? '');
        $pass = trim($input_data['password'] ?? '');
        if (!$sid || !$pass) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'กรุณากรอกข้อมูลให้ครบถ้วน']);
            exit();
        }
        
        $matched_name = 'นักศึกษา ' . $sid;
        foreach ($roster as $s) {
            if ($s['student_id'] === $sid) {
                $matched_name = $s['name'];
                break;
            }
        }
        
        $hashed = hash('sha256', $pass);
        $found = false;
        foreach ($accounts['students'] as &$acc) {
            if ($acc['student_id'] === $sid) {
                $acc['password_hash'] = $hashed;
                $found = true;
                break;
            }
        }
        if (!$found) {
            $accounts['students'][] = [
                'student_id' => $sid,
                'name' => $matched_name,
                'faculty' => 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                'password_hash' => $hashed,
                'created_at' => date('c')
            ];
        }
        file_put_contents($accounts_file, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'message' => 'ลงทะเบียนสำเร็จ!', 'user_name' => $matched_name]);
        exit();
    }
    
    if ($action === 'student_reset_password') {
        $sid = trim($input_data['student_id'] ?? '');
        $email = strtolower(trim($input_data['email'] ?? ''));
        $new_pass = trim($input_data['new_password'] ?? '');
        
        $clean_sid = str_replace('-', '', $sid);
        $expected = 'stu' . $clean_sid;
        
        if (strpos($email, $expected) === false || strpos($email, 'sskru.ac.th') === false) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'อีเมลไม่ถูกต้อง ต้องเป็นรูปแบบ ' . $expected . '@sskru.ac.th']);
            exit();
        }
        
        $hashed = hash('sha256', $new_pass);
        $found = false;
        foreach ($accounts['students'] as &$acc) {
            if ($acc['student_id'] === $sid) {
                $acc['password_hash'] = $hashed;
                $found = true;
                break;
            }
        }
        if (!$found) {
            $accounts['students'][] = [
                'student_id' => $sid,
                'name' => 'นักศึกษา ' . $sid,
                'faculty' => 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                'password_hash' => $hashed,
                'created_at' => date('c')
            ];
        }
        file_put_contents($accounts_file, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'message' => 'รีเซ็ตรหัสผ่านสำเร็จ']);
        exit();
    }
    
    if ($action === 'staff_register') {
        $email = trim($input_data['email'] ?? '');
        $user = trim($input_data['username'] ?? '');
        $pass = trim($input_data['password'] ?? '');
        
        if (!$email || !$user || !$pass) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'กรุณากรอกข้อมูลให้ครบถ้วน']);
            exit();
        }
        
        $hashed = hash('sha256', $pass);
        $accounts['staff'][] = [
            'username' => $user,
            'email' => $email,
            'password_hash' => $hashed,
            'created_at' => date('c')
        ];
        file_put_contents($accounts_file, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo json_encode(['success' => true, 'username' => $user, 'message' => 'สมัครสมาชิกบุคลากรสำเร็จ']);
        exit();
    }

    if ($action === 'staff_login') {
        $ident = trim($input_data['identifier'] ?? '');
        $pass = trim($input_data['password'] ?? '');
        
        if (($ident === 'lnwpoon007x' || $ident === 'admin') && ($pass === 'poon300450' || $pass === 'sskru2026')) {
            echo json_encode(['success' => true, 'role' => 'admin', 'redirect' => 'admin_dashboard.php', 'message' => 'เข้าสู่ระบบผู้ดูแลระบบสำเร็จ']);
            exit();
        }
        
        $hashed = hash('sha256', $pass);
        foreach ($accounts['staff'] as $st) {
            if (($st['username'] === $ident || $st['email'] === $ident) && $st['password_hash'] === $hashed) {
                echo json_encode(['success' => true, 'role' => 'staff', 'redirect' => 'index.php', 'user_name' => $st['username']]);
                exit();
            }
        }
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง']);
        exit();
    }

    if ($action === 'student_login') {
        $sid = trim($input_data['student_id'] ?? '');
        $pass = trim($input_data['password'] ?? '');
        $hashed = hash('sha256', $pass);
        
        foreach ($accounts['students'] as $st) {
            if ($st['student_id'] === $sid && $st['password_hash'] === $hashed) {
                echo json_encode(['success' => true, 'role' => 'student', 'redirect' => 'index.php', 'user_name' => $st['name']]);
                exit();
            }
        }
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'รหัสนักศึกษาหรือรหัสผ่านไม่ถูกต้อง หรือยังไม่ได้ลงทะเบียน']);
        exit();
    }
}

// ==========================================
// BUILDINGS API
// ==========================================
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

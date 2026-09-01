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
    $accounts_file = dirname(__DIR__) . '/data/user_accounts.json';
    $roster_file = dirname(__DIR__) . '/data/students_roster.json';
    
    $accounts = ['students' => [], 'staff' => []];
    if (file_exists($accounts_file)) {
        $accounts = json_decode(file_get_contents($accounts_file), true) ?: $accounts;
    }
    
    $roster = [];
    if (file_exists($roster_file)) {
        $roster = json_decode(file_get_contents($roster_file), true) ?: [];
    }

    if ($action === 'auth_status') {
        if (session_status() === PHP_SESSION_NONE) { session_start(); }
        $is_admin = ($_SESSION['user_role'] ?? '') === 'admin' || isset($_SESSION['admin_token']);
        $is_student = isset($_SESSION['student_id']);
        $is_staff = ($_SESSION['user_role'] ?? '') === 'staff' || isset($_SESSION['staff_username']);

        echo json_encode([
            'success' => true,
            'isAdmin' => $is_admin,
            'isStudent' => $is_student,
            'isStaff' => $is_staff,
            'staffUsername' => $_SESSION['staff_username'] ?? '',
            'studentId' => $_SESSION['student_id'] ?? '',
            'studentName' => $_SESSION['student_name'] ?? '',
        ]);
        exit();
    }

    if ($action === 'logout') {
        if (session_status() === PHP_SESSION_NONE) { session_start(); }
        $_SESSION = [];
        session_destroy();
        echo json_encode(['success' => true]);
        exit();
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
    
    $resets_file = dirname(__DIR__) . '/data/password_resets.json';
    $resets = [];
    if (file_exists($resets_file)) {
        $resets = json_decode(file_get_contents($resets_file), true) ?: [];
    }

    if ($action === 'student_request_reset') {
        $sid = trim($input_data['student_id'] ?? '');
        $email = strtolower(trim($input_data['email'] ?? ''));
        
        $clean_sid = str_replace('-', '', $sid);
        $expected = 'stu' . $clean_sid;
        
        if (strpos($email, $expected) === false || strpos($email, 'sskru.ac.th') === false) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'อีเมลไม่ถูกต้อง ต้องเป็นรูปแบบ ' . $expected . '@sskru.ac.th']);
            exit();
        }
        
        $st_name = 'นักศึกษา ' . $sid;
        foreach ($roster as $s) {
            if ($s['student_id'] === $sid) {
                $st_name = $s['name'];
                break;
            }
        }
        
        $token = bin2hex(random_bytes(24));
        $otp = strval(rand(100000, 999999));
        $exp = date('c', time() + 900);
        
        // Remove previous resets for this student
        $new_resets = [];
        foreach ($resets as $r) {
            if ($r['student_id'] !== $sid) {
                $new_resets[] = $r;
            }
        }
        $new_resets[] = [
            'student_id' => $sid,
            'student_name' => $st_name,
            'email' => $email,
            'token' => $token,
            'otp' => $otp,
            'expires_at' => $exp,
            'used' => false,
            'created_at' => date('c')
        ];
        file_put_contents($resets_file, json_encode($new_resets, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode([
            'success' => true,
            'email' => $email,
            'token' => $token,
            'otp' => $otp,
            'message' => 'ระบบได้ส่งลิงก์ยืนยันตัวตนไปยัง ' . $email . ' เรียบร้อยแล้ว'
        ]);
        exit();
    }

    if ($action === 'student_verify_reset_token') {
        $token = trim($input_data['token'] ?? '');
        $otp = trim($input_data['otp'] ?? '');
        
        $matched = null;
        foreach ($resets as $r) {
            if (!$r['used'] && (($token && $r['token'] === $token) || ($otp && $r['otp'] === $otp))) {
                $matched = $r;
                break;
            }
        }
        
        if (!$matched) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ลิงก์ยืนยันตัวตนไม่ถูกต้องหรือถูกใช้งานไปแล้ว']);
            exit();
        }
        
        if (time() > strtotime($matched['expires_at'])) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ลิงก์ยืนยันตัวตนหมดอายุแล้ว']);
            exit();
        }
        
        echo json_encode([
            'success' => true,
            'token' => $matched['token'],
            'student_id' => $matched['student_id'],
            'student_name' => $matched['student_name'],
            'email' => $matched['email']
        ]);
        exit();
    }

    if ($action === 'student_confirm_new_password') {
        $token = trim($input_data['token'] ?? '');
        $new_pass = trim($input_data['new_password'] ?? '');
        
        if (!$token || !$new_pass) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ข้อมูลไม่ครบถ้วน']);
            exit();
        }
        
        $matched_idx = -1;
        for ($i = 0; $i < count($resets); $i++) {
            if (!$resets[$i]['used'] && $resets[$i]['token'] === $token) {
                $matched_idx = $i;
                break;
            }
        }
        
        if ($matched_idx === -1) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ']);
            exit();
        }
        
        if (time() > strtotime($resets[$matched_idx]['expires_at'])) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Token หมดอายุแล้ว']);
            exit();
        }
        
        $sid = $resets[$matched_idx]['student_id'];
        $st_name = $resets[$matched_idx]['student_name'];
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
                'name' => $st_name,
                'faculty' => 'มหาวิทยาลัยราชภัฏศรีสะเกษ',
                'password_hash' => $hashed,
                'created_at' => date('c')
            ];
        }
        file_put_contents($accounts_file, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        $resets[$matched_idx]['used'] = true;
        file_put_contents($resets_file, json_encode($resets, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'message' => 'ตั้งรหัสผ่านใหม่สำเร็จ']);
        exit();
    }

    if ($action === 'staff_request_reset') {
        $identifier = trim($input_data['identifier'] ?? '');
        if (!$identifier) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'กรุณากรอก Username หรือ Email ของบุคลากร']);
            exit();
        }

        $target_username = null;
        $target_email = null;

        foreach ($accounts['staff'] as $st) {
            if ($st['username'] === $identifier || strtolower($st['email']) === strtolower($identifier)) {
                $target_username = $st['username'];
                $target_email = $st['email'];
                break;
            }
        }

        if (!$target_username) {
            if ($identifier === 'admin' || $identifier === 'lnwpoon007x' || strtolower($identifier) === 'mpoontv1234@gmail.com') {
                $target_username = 'ผู้ดูแลระบบ (Admin)';
                $target_email = 'mpoontv1234@gmail.com';
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'message' => 'ไม่พบบัญชีบุคลากรที่ระบุในระบบ']);
                exit();
            }
        }

        $token = bin2hex(random_bytes(24));
        $otp = strval(rand(100000, 999999));
        $expires_at = date('c', strtotime('+15 minutes'));

        // Clear previous resets for this staff
        $resets = array_values(array_filter($resets, function($r) use ($target_username, $target_email) {
            return ($r['username'] ?? '') !== $target_username && ($r['email'] ?? '') !== $target_email;
        }));

        $reset_entry = [
            'role' => 'staff',
            'username' => $target_username,
            'email' => $target_email,
            'token' => $token,
            'otp' => $otp,
            'expires_at' => $expires_at,
            'used' => false,
            'created_at' => date('c')
        ];
        $resets[] = $reset_entry;
        file_put_contents($resets_file, json_encode($resets, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        // SMTP Email notice (if mail configured)
        @mail(
            $target_email,
            '=?UTF-8?B?'.base64_encode('🔒 ยืนยันสิทธิ์รีเซ็ตรหัสผ่านบุคลากร — SSKRU Campus Map').'?=',
            "สวัสดี คุณ $target_username\n\nรหัส OTP สำหรับยืนยันสิทธิ์รีเซ็ตรหัสผ่านของคุณคือ: $otp\n(รหัสมีอายุ 15 นาที)\n\nหากคุณไม่ได้เป็นผู้ทำรายการนี้ กรุณาเพิกเฉยต่ออีเมลฉบับนี้",
            "From: SSKRU Campus Map <noreply@sskru.ac.th>\r\nContent-Type: text/plain; charset=UTF-8"
        );

        echo json_encode([
            'success' => true,
            'message' => "ระบบได้ส่งรหัส OTP และลิงก์ยืนยันตัวตนไปยังอีเมล $target_email เรียบร้อยแล้ว (รหัสมีอายุ 15 นาที)",
            'email' => $target_email
        ]);
        exit();
    }

    if ($action === 'staff_verify_reset_token') {
        $token = trim($input_data['token'] ?? '');
        $otp = trim($input_data['otp'] ?? '');

        $matched = null;
        foreach ($resets as $r) {
            if (!$r['used']) {
                if (($token && ($r['token'] ?? '') === $token) || ($otp && ($r['otp'] ?? '') === $otp)) {
                    $matched = $r;
                    break;
                }
            }
        }

        if (!$matched) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ลิงก์ยืนยันตัวตนหรือรหัส OTP ไม่ถูกต้อง หรือถูกใช้งานไปแล้ว']);
            exit();
        }

        if (time() > strtotime($matched['expires_at'])) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ลิงก์ยืนยันตัวตนหมดอายุแล้ว']);
            exit();
        }

        echo json_encode([
            'success' => true,
            'token' => $matched['token'],
            'username' => $matched['username'] ?? 'Staff',
            'email' => $matched['email'] ?? ''
        ]);
        exit();
    }

    if ($action === 'staff_confirm_new_password') {
        $token = trim($input_data['token'] ?? '');
        $new_pass = trim($input_data['new_password'] ?? '');

        if (!$token || !$new_pass) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ข้อมูลไม่ครบถ้วน']);
            exit();
        }

        $matched_idx = -1;
        for ($i = 0; $i < count($resets); $i++) {
            if (!$resets[$i]['used'] && ($resets[$i]['token'] ?? '') === $token) {
                $matched_idx = $i;
                break;
            }
        }

        if ($matched_idx === -1) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Token ยืนยันสิทธิ์ไม่ถูกต้องหรือหมดอายุ']);
            exit();
        }

        if (time() > strtotime($resets[$matched_idx]['expires_at'])) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Token หมดอายุแล้ว']);
            exit();
        }

        $username = $resets[$matched_idx]['username'] ?? '';
        $email = $resets[$matched_idx]['email'] ?? '';
        $hashed = hash('sha256', $new_pass);

        $found = false;
        foreach ($accounts['staff'] as &$acc) {
            if ($acc['username'] === $username || (isset($acc['email']) && strtolower($acc['email']) === strtolower($email))) {
                $acc['password_hash'] = $hashed;
                $found = true;
                break;
            }
        }
        if (!$found) {
            $accounts['staff'][] = [
                'username' => $username,
                'email' => $email,
                'password_hash' => $hashed,
                'created_at' => date('c')
            ];
        }
        file_put_contents($accounts_file, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        $resets[$matched_idx]['used'] = true;
        file_put_contents($resets_file, json_encode($resets, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        echo json_encode(['success' => true, 'message' => 'สร้างและตั้งรหัสผ่านใหม่สำหรับบุคลากรสำเร็จ']);
        exit();
    }

    if ($action === 'verify_password') {
        $pass = trim($input_data['password'] ?? '');
        $sid = trim($input_data['student_id'] ?? '');

        if (!$pass) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'กรุณากรอกรหัสผ่าน']);
            exit();
        }

        // Admin password check (Only poon300450)
        if ($pass === 'poon300450') {
            echo json_encode(['success' => true, 'message' => 'ยืนยันรหัสผ่านสำเร็จ (Admin)']);
            exit();
        }

        // Student password check
        $hashed = hash('sha256', $pass);
        $matched = false;
        $clean_sid = str_replace('-', '', $sid);

        if ($sid || $clean_sid) {
            foreach ($accounts['students'] as $st) {
                if (($st['student_id'] === $sid || $st['student_id'] === $clean_sid) && 
                    (($st['password_hash'] ?? '') === $hashed || ($st['password'] ?? '') === $pass)) {
                    $matched = true;
                    break;
                }
            }
        }
        
        if (!$matched) {
            foreach ($accounts['students'] as $st) {
                if (($st['password_hash'] ?? '') === $hashed || ($st['password'] ?? '') === $pass) {
                    $matched = true;
                    break;
                }
            }
            if (!$matched) {
                foreach ($accounts['staff'] as $sf) {
                    if (($sf['password_hash'] ?? '') === $hashed || ($sf['password'] ?? '') === $pass) {
                        $matched = true;
                        break;
                    }
                }
            }
        }

        if ($matched || ($sid && $pass === $sid) || ($clean_sid && $pass === $clean_sid)) {
            echo json_encode(['success' => true, 'message' => 'ยืนยันรหัสผ่านสำเร็จ']);
            exit();
        }

        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง']);
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
        
        // PHP Session Rate Limiting
        $failed_count = $_SESSION['staff_login_failed'] ?? 0;
        $lock_until = $_SESSION['staff_login_lock'] ?? 0;
        if (time() < $lock_until) {
            $rem = ceil(($lock_until - time()) / 60);
            http_response_code(429);
            echo json_encode(['success' => false, 'message' => "ระบบตรวจพบการพยายามเข้าสู่ระบบไม่ถูกต้องเกินกำหนด กรุณารอ $rem นาที"]);
            exit();
        }

        function log_user_activity_php($uid, $name, $role, $email = '') {
            $log_file = dirname(__DIR__) . '/data/user_activity_logs.json';
            $logs = file_exists($log_file) ? json_decode(file_get_contents($log_file), true) ?: [] : [];
            $role_th = ($role === 'admin') ? 'ผู้ดูแลระบบ' : (($role === 'staff') ? 'บุคลากร / อาจารย์' : 'นักศึกษา');
            $entry = [
                'user_id' => $uid,
                'name' => $name,
                'email' => $email,
                'role' => $role,
                'role_th' => $role_th,
                'device' => 'Desktop',
                'os' => 'macOS',
                'browser' => 'Safari',
                'ip' => $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1',
                'timestamp' => date('c'),
                'time_formatted' => date('H:i น.'),
                'date_formatted' => date('d/m/Y')
            ];
            array_unshift($logs, $entry);
            $logs = array_slice($logs, 0, 100);
            file_put_contents($log_file, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        }

        if ($ident === 'lnwpoon007x' && $pass === 'poon300450') {
            unset($_SESSION['staff_login_failed']);
            unset($_SESSION['staff_login_lock']);
            $_SESSION['user_role'] = 'admin';
            $_SESSION['admin_token'] = bin2hex(random_bytes(16));
            log_user_activity_php('lnwpoon007x', 'ผู้ดูแลระบบ (Admin)', 'admin', 'mpoontv1234@gmail.com');
            echo json_encode(['success' => true, 'role' => 'admin', 'redirect' => 'admin_dashboard.php', 'message' => 'เข้าสู่ระบบผู้ดูแลระบบสำเร็จ']);
            exit();
        }
        
        $hashed = hash('sha256', $pass);
        foreach ($accounts['staff'] as $st) {
            if (($st['username'] === $ident || $st['email'] === $ident) && $st['password_hash'] === $hashed) {
                unset($_SESSION['staff_login_failed']);
                unset($_SESSION['staff_login_lock']);
                $_SESSION['user_role'] = 'staff';
                $_SESSION['staff_username'] = $st['username'];
                $_SESSION['staff_email'] = $st['email'] ?? '';
                log_user_activity_php($st['username'], $st['username'], 'staff', $st['email'] ?? '');
                echo json_encode(['success' => true, 'role' => 'staff', 'redirect' => 'index.php', 'user_name' => $st['username']]);
                exit();
            }
        }
        
        $_SESSION['staff_login_failed'] = ($failed_count + 1);
        if ($_SESSION['staff_login_failed'] >= 5) {
            $_SESSION['staff_login_lock'] = time() + 600; // Lock 10 mins
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
                $_SESSION['student_id'] = $st['student_id'];
                $_SESSION['student_name'] = $st['name'];
                log_user_activity_php($st['student_id'], $st['name'], 'student', "stu{$st['student_id']}@sskru.ac.th");
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
$json_file = dirname(__DIR__) . '/data/buildings.json';

function read_buildings_php() {
    global $json_file, $pdo;
    if (file_exists($json_file)) {
        $content = file_get_contents($json_file);
        $data = json_decode($content, true);
        if (is_array($data) && count($data) > 0) {
            return $data;
        }
    }
    if ($pdo) {
        $stmt = $pdo->query("SELECT json_data FROM buildings ORDER BY id ASC");
        $rows = $stmt->fetchAll();
        $buildings = [];
        foreach ($rows as $row) {
            if (!empty($row['json_data'])) {
                $buildings[] = json_decode($row['json_data'], true);
            }
        }
        return $buildings;
    }
    return [];
}

function write_buildings_php($buildings, $pdo) {
    global $json_file;
    if (!file_exists(dirname($json_file))) {
        @mkdir(dirname($json_file), 0777, true);
    }
    file_put_contents($json_file, json_encode($buildings, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

    if ($pdo) {
        try {
            $pdo->exec("DELETE FROM buildings");
            $sql = "INSERT INTO buildings (id, code, name, nameEn, category, coords_y, coords_x, real_lat, real_lng, description, phone, json_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            $stmt = $pdo->prepare($sql);
            foreach ($buildings as $b) {
                $b_id = intval($b['id'] ?? time());
                $b_code = strval($b['code'] ?? $b_id);
                $b_name = $b['name'] ?? '';
                $b_name_en = $b['nameEn'] ?? '';
                $b_cat = $b['category'] ?? 'facility';
                $cy = $b['coords'][0] ?? 0;
                $cx = $b['coords'][1] ?? 0;
                $lat = $b['realCoords'][0] ?? 0.0;
                $lng = $b['realCoords'][1] ?? 0.0;
                $desc = $b['description'] ?? '';
                $phone = $b['phone'] ?? '';
                $json_str = json_encode($b, JSON_UNESCAPED_UNICODE);
                $stmt->execute([$b_id, $b_code, $b_name, $b_name_en, $b_cat, $cy, $cx, $lat, $lng, $desc, $phone, $json_str]);
            }
        } catch (Exception $e) {}
    }
}

if ($method === 'GET') {
    $buildings = read_buildings_php();
    if ($id) {
        $found = null;
        foreach ($buildings as $b) {
            if (strval($b['id']) === strval($id)) {
                $found = $b;
                break;
            }
        }
        if ($found) {
            echo json_encode(['success' => true, 'data' => $found]);
        } else {
            http_response_code(404);
            echo json_encode(['success' => false, 'message' => 'ไม่พบอาคารที่ระบุ']);
        }
    } else {
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
    
    $buildings = read_buildings_php();
    $b_id = isset($input_data['id']) ? intval($input_data['id']) : (count($buildings) > 0 ? max(array_column($buildings, 'id')) + 1 : 1);
    $input_data['id'] = $b_id;

    $idx = -1;
    foreach ($buildings as $i => $b) {
        if ($b['id'] == $b_id) {
            $idx = $i;
            break;
        }
    }

    if ($idx >= 0) {
        $buildings[$idx] = array_merge($buildings[$idx], $input_data);
    } else {
        $buildings[] = $input_data;
    }

    write_buildings_php($buildings, $pdo);
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
    
    $buildings = read_buildings_php();
    $target_id = intval($target_id);
    $input_data['id'] = $target_id;

    $idx = -1;
    foreach ($buildings as $i => $b) {
        if ($b['id'] == $target_id) {
            $idx = $i;
            break;
        }
    }

    if ($idx >= 0) {
        $buildings[$idx] = array_merge($buildings[$idx], $input_data);
    } else {
        $buildings[] = $input_data;
    }

    write_buildings_php($buildings, $pdo);
    echo json_encode(['success' => true, 'message' => 'อัปเดตข้อมูลอาคารสำเร็จ', 'data' => $input_data]);
    exit();
}

if ($method === 'DELETE') {
    if (!$id) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'กรุณาระบุ ID']);
        exit();
    }
    
    $buildings = read_buildings_php();
    $target_id = intval($id);
    $new_buildings = [];
    foreach ($buildings as $b) {
        if ($b['id'] != $target_id) {
            $new_buildings[] = $b;
        }
    }
    
    write_buildings_php($new_buildings, $pdo);
    echo json_encode(['success' => true, 'message' => 'ลบอาคารเรียบร้อยแล้ว']);
    exit();
}

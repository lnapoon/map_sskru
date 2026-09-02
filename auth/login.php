<?php
// SSKRU Native PHP Multi-Role Authentication Portal
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>เข้าสู่ระบบ — SSKRU Campus Map</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --primary: #1a4fa0;
      --primary-dark: #0d2c5e;
      --primary-light: #2563eb;
      --accent: #f59e0b;
      --danger: #ef4444;
      --success: #10b981;
      --surface: #ffffff;
      --text: #1e293b;
      --text-secondary: #64748b;
    }

    body {
      font-family: 'Sarabun', 'Outfit', sans-serif;
      background: linear-gradient(135deg, #0d2c5e 0%, #1a4fa0 40%, #2563eb 70%, #1e40af 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      position: relative;
      overflow: hidden;
    }

    body::before, body::after {
      content: '';
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.25;
      animation: float 8s ease-in-out infinite alternate;
    }
    body::before {
      width: 500px; height: 500px;
      background: #f59e0b;
      top: -150px; right: -100px;
    }
    body::after {
      width: 400px; height: 400px;
      background: #10b981;
      bottom: -100px; left: -80px;
      animation-delay: 4s;
    }
    @keyframes float {
      0% { transform: translate(0, 0) scale(1); }
      100% { transform: translate(40px, -30px) scale(1.1); }
    }

    .particles {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      overflow: hidden;
      z-index: 0;
    }
    .particle {
      position: absolute;
      width: 6px; height: 6px;
      background: rgba(255,255,255,0.15);
      border-radius: 50%;
      animation: rise 12s linear infinite;
    }
    .particle:nth-child(2) { left: 15%; width: 4px; height: 4px; animation-delay: 2s; animation-duration: 14s; }
    .particle:nth-child(3) { left: 35%; width: 8px; height: 8px; animation-delay: 4s; animation-duration: 10s; }
    .particle:nth-child(4) { left: 55%; width: 3px; height: 3px; animation-delay: 1s; animation-duration: 16s; }
    .particle:nth-child(5) { left: 75%; width: 5px; height: 5px; animation-delay: 6s; animation-duration: 11s; }

    @keyframes rise {
      0% { bottom: -10%; opacity: 0; }
      10% { opacity: 1; }
      90% { opacity: 0.5; }
      100% { bottom: 110%; opacity: 0; }
    }

    .login-card {
      position: relative;
      z-index: 1;
      background: rgba(255,255,255,0.96);
      backdrop-filter: blur(20px);
      border-radius: 24px;
      box-shadow: 0 25px 80px rgba(0,0,0,0.3);
      width: 100%;
      max-width: 480px;
      overflow: hidden;
      animation: cardIn 0.6s cubic-bezier(0.23, 1, 0.32, 1);
    }
    @keyframes cardIn {
      0% { opacity: 0; transform: translateY(30px) scale(0.95); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    .card-header {
      background: linear-gradient(135deg, var(--primary-dark), var(--primary-light));
      padding: 32px 28px 24px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .card-header::after {
      content: '';
      position: absolute;
      bottom: -20px; left: -10%; right: -10%;
      height: 40px;
      background: rgba(255,255,255,0.96);
      border-radius: 50% 50% 0 0;
    }

    .university-badge {
      width: 68px; height: 68px;
      background: rgba(255,255,255,0.15);
      border: 2px solid rgba(255,255,255,0.3);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 12px;
      font-size: 30px;
      color: white;
      animation: pulse 3s ease-in-out infinite;
    }
    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.3); }
      50% { box-shadow: 0 0 0 12px rgba(255,255,255,0); }
    }

    .card-header h1 {
      color: white;
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 2px;
    }
    .card-header p {
      color: rgba(255,255,255,0.85);
      font-size: 12.5px;
      font-weight: 400;
    }

    .role-switcher {
      display: flex;
      background: #f1f5f9;
      margin: 20px 24px 0 24px;
      padding: 4px;
      border-radius: 14px;
      border: 1px solid #e2e8f0;
    }
    .role-btn {
      flex: 1;
      padding: 11px 12px;
      border: none;
      background: transparent;
      color: var(--text-secondary);
      font-family: inherit;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.25s ease;
    }
    .role-btn.active {
      background: var(--primary);
      color: white;
      box-shadow: 0 4px 12px rgba(26, 79, 160, 0.3);
    }

    .card-body {
      padding: 24px 28px 28px;
    }

    .panel-content {
      display: none;
    }
    .panel-content.active {
      display: block;
      animation: fadeIn 0.3s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .form-group {
      margin-bottom: 18px;
    }
    .form-label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 6px;
    }
    .input-wrapper {
      position: relative;
      display: flex;
      align-items: center;
    }
    .input-icon {
      position: absolute;
      left: 14px;
      color: var(--text-secondary);
      font-size: 15px;
      transition: color 0.2s;
    }
    .form-input {
      width: 100%;
      padding: 12px 14px 12px 42px;
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      color: var(--text);
      font-size: 13.5px;
      font-family: inherit;
      outline: none;
      transition: all 0.2s ease;
    }
    .form-input:focus {
      border-color: var(--primary-light);
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
    }
    .form-input:focus + .input-icon, .form-input:focus ~ .input-icon {
      color: var(--primary-light);
    }
    .btn-toggle-pw {
      position: absolute;
      right: 12px;
      background: none;
      border: none;
      color: var(--text-secondary);
      font-size: 15px;
      cursor: pointer;
      padding: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.2s;
      z-index: 5;
    }
    .btn-toggle-pw:hover {
      color: var(--primary-light);
    }

    .btn-primary {
      width: 100%;
      padding: 13px;
      background: linear-gradient(135deg, var(--primary), var(--primary-light));
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 14.5px;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(26, 79, 160, 0.3);
      transition: all 0.25s ease;
      margin-top: 10px;
    }
    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(26, 79, 160, 0.4);
    }

    .sub-link-container {
      text-align: center;
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid #f1f5f9;
    }
    .sub-link {
      color: var(--primary-light);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: color 0.2s;
    }
    .sub-link:hover {
      color: var(--primary-dark);
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <div class="particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
  </div>

  <div class="login-card">
    <div class="card-header">
      <div class="university-badge">
        <i class="fa-solid fa-graduation-cap"></i>
      </div>
      <h1>มหาวิทยาลัยราชภัฏศรีสะเกษ</h1>
      <p>SSKRU 3D Campus Map & Authentication Portal</p>
    </div>

    <!-- Main Role Switcher Tabs -->
    <div class="role-switcher">
      <button class="role-btn active" id="tab-student" onclick="switchRole('student')">
        <i class="fa-solid fa-user-graduate"></i> สำหรับนักศึกษา
      </button>
      <button class="role-btn" id="tab-staff" onclick="switchRole('staff')">
        <i class="fa-solid fa-user-tie"></i> สำหรับบุคลากร
      </button>
    </div>

    <div class="card-body">
      <!-- 1. STUDENT LOGIN PANEL -->
      <div class="panel-content active" id="panel-student">
        <form id="form-student-login" onsubmit="handleStudentLogin(event)">
          <div class="form-group">
            <label class="form-label">รหัสนักศึกษา (Student ID)</label>
            <div class="input-wrapper">
              <i class="fa-solid fa-graduation-cap input-icon"></i>
              <input type="text" id="login-student-id" class="form-input" placeholder="กรอกรหัสนักศึกษา" required />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">รหัสผ่าน (Password)</label>
            <div class="input-wrapper">
              <i class="fa-solid fa-lock input-icon"></i>
              <input type="password" id="login-student-pass" class="form-input" style="padding-right: 42px;" placeholder="กรอกรหัสผ่าน" required />
              <button type="button" class="btn-toggle-pw" onclick="togglePasswordVisibility('login-student-pass', this)" title="แสดง/ซ่อนรหัสผ่าน">
                <i class="fa-solid fa-eye"></i>
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary">
            <i class="fa-solid fa-right-to-bracket"></i> เข้าสู่ระบบนักศึกษา
          </button>
        </form>

        <div class="sub-link-container" style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; gap: 8px; font-size: 13px;">
          <a href="/register/student/" class="sub-link" id="link-reg-student" style="font-weight: 600; color: #2563eb;">
            <i class="fa-solid fa-user-plus"></i> ลงทะเบียนครั้งแรก
          </a>
          <a href="/reset_password/student/" class="sub-link" id="link-reset-student" style="color: #64748b;">
            <i class="fa-solid fa-key"></i> ลืมรหัสผ่าน?
          </a>
        </div>
      </div>

      <!-- 2. STAFF LOGIN PANEL -->
      <div class="panel-content" id="panel-staff">
        <form id="form-staff-login" onsubmit="handleStaffLogin(event)">
          <div class="form-group">
            <label class="form-label">Username หรือ Email</label>
            <div class="input-wrapper">
              <i class="fa-solid fa-at input-icon"></i>
              <input type="text" id="staff-identifier" class="form-input" placeholder="กรอก Username หรือ Email บุคลากร" required />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">รหัสผ่าน (Password)</label>
            <div class="input-wrapper">
              <i class="fa-solid fa-lock input-icon"></i>
              <input type="password" id="staff-password" class="form-input" style="padding-right: 42px;" placeholder="กรอกรหัสผ่าน" required />
              <button type="button" class="btn-toggle-pw" onclick="togglePasswordVisibility('staff-password', this)" title="แสดง/ซ่อนรหัสผ่าน">
                <i class="fa-solid fa-eye"></i>
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary">
            <i class="fa-solid fa-right-to-bracket"></i> เข้าสู่ระบบบุคลากร
          </button>
        </form>

        <div class="sub-link-container" style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; gap: 8px; font-size: 13px;">
          <a href="register_staff.php" class="sub-link" id="link-reg-staff" style="font-weight: 600; color: #2563eb;">
            <i class="fa-solid fa-user-plus"></i> สมัครสมาชิกบุคลากร
          </a>
          <a href="reset_password_staff.php" class="sub-link" id="link-reset-staff" style="color: #64748b;">
            <i class="fa-solid fa-key"></i> ลืมรหัสผ่าน?
          </a>
        </div>
      </div>
    </div>
  </div>

  <script>
    if (window.location.pathname.endsWith('.php')) {
      document.getElementById('link-reg-student').href = 'register_student.php';
      document.getElementById('link-reg-staff').href = 'register_staff.php';
      if (document.getElementById('link-reset-student')) {
        document.getElementById('link-reset-student').href = 'reset_password_student.php';
      }
      if (document.getElementById('link-reset-staff')) {
        document.getElementById('link-reset-staff').href = 'reset_password_staff.php';
      }
    }

    function switchRole(role) {
      document.querySelectorAll('.role-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.panel-content').forEach(panel => panel.classList.remove('active'));
      
      document.getElementById('tab-' + role).classList.add('active');
      document.getElementById('panel-' + role).classList.add('active');
    }

    async function handleStudentLogin(e) {
      e.preventDefault();
      const sid = document.getElementById('login-student-id').value.trim();
      const pass = document.getElementById('login-student-pass').value.trim();
      const isPhp = window.location.pathname.endsWith('.php');
      const apiEndpoint = isPhp ? 'api.php?action=student_login' : '/admin/api/auth/student_login/';
      try {
        const res = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: sid, password: pass })
        });
        const data = await res.json();
        if (data.success) {
          window.location.href = isPhp ? 'index.php' : '/';
        } else {
          alert(data.message || 'รหัสนักศึกษาหรือรหัสผ่านไม่ถูกต้อง');
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาดในการเข้าสู่ระบบ');
      }
    }

    async function handleStaffLogin(e) {
      e.preventDefault();
      const identifier = document.getElementById('staff-identifier').value.trim();
      const pass = document.getElementById('staff-password').value.trim();
      const isPhp = window.location.pathname.endsWith('.php');
      const apiEndpoint = isPhp ? 'api.php?action=staff_login' : '/admin/api/auth/staff_login/';
      try {
        const res = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: identifier, password: pass })
        });
        const data = await res.json();
        if (data.success) {
          if (isPhp) {
            window.location.href = data.role === 'admin' ? 'index.php?admin=1' : 'index.php';
          } else {
            window.location.href = data.role === 'admin' ? '/admin/dashboard/' : '/';
          }
        } else {
          alert(data.message || 'Username/Email หรือรหัสผ่านไม่ถูกต้อง');
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาดในการเข้าสู่ระบบ');
      }
    }

    function togglePasswordVisibility(inputId, btn) {
      const input = document.getElementById(inputId);
      if (!input) return;
      const icon = btn.querySelector('i');
      if (input.type === 'password') {
        input.type = 'text';
        if (icon) {
          icon.classList.remove('fa-eye');
          icon.classList.add('fa-eye-slash');
        }
      } else {
        input.type = 'password';
        if (icon) {
          icon.classList.remove('fa-eye-slash');
          icon.classList.add('fa-eye');
        }
      }
    }
  </script>
</body>
</html>

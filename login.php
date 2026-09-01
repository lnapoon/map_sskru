<?php
// SSKRU Native PHP Multi-Role Authentication Portal
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>เข้าสู่ระบบ — SSKRU 3D Campus Map System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --primary: #0284c7;
      --primary-dark: #0f172a;
      --primary-accent: #2563eb;
      --accent: #f59e0b;
      --danger: #ef4444;
      --success: #10b981;
      --surface: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.85);
      --border: rgba(56, 189, 248, 0.25);
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }

    body {
      font-family: 'Sarabun', 'Outfit', sans-serif;
      background: radial-gradient(circle at top left, #0f172a, #0b1329);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      color: var(--text);
      position: relative;
      overflow-x: hidden;
    }

    /* Ambient background blur blobs */
    .bg-blob {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      z-index: 0;
      opacity: 0.45;
      pointer-events: none;
    }
    .blob-1 { top: -100px; left: -100px; width: 350px; height: 350px; background: #0284c7; }
    .blob-2 { bottom: -100px; right: -100px; width: 400px; height: 400px; background: #2563eb; }

    .portal-container {
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 900px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1.5px solid var(--border);
      border-radius: 28px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 30px rgba(14, 165, 233, 0.2);
      overflow: hidden;
    }

    /* Portal Header */
    .portal-header {
      text-align: center;
      padding: 30px 24px 20px 24px;
      background: rgba(30, 41, 59, 0.5);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .portal-logo {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      border-radius: 18px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: #fff;
      box-shadow: 0 8px 24px rgba(2, 132, 199, 0.4);
      margin-bottom: 12px;
    }
    .portal-title {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      letter-spacing: -0.3px;
    }
    .portal-subtitle {
      font-size: 13px;
      color: #38bdf8;
      margin-top: 4px;
      font-weight: 500;
    }

    /* Main Dual Role Tabs */
    .role-switcher {
      display: flex;
      background: rgba(15, 23, 42, 0.8);
      padding: 6px;
      border-bottom: 1px solid var(--border);
    }
    .role-btn {
      flex: 1;
      padding: 14px 18px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 14.5px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .role-btn.active {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #ffffff;
      box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35);
    }

    /* Panels Content */
    .panel-content {
      padding: 32px 36px;
      display: none;
    }
    .panel-content.active {
      display: block;
      animation: fadeIn 0.35s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Sub Tabs inside panel */
    .sub-tabs {
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 12px;
    }
    .sub-tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      padding: 8px 16px;
      border-radius: 10px;
      transition: all 0.2s;
    }
    .sub-tab-btn.active {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
    }

    /* Form Fields */
    .form-group {
      margin-bottom: 20px;
    }
    .form-label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 8px;
    }
    .input-wrapper {
      position: relative;
      display: flex;
      align-items: center;
    }
    .input-icon {
      position: absolute;
      left: 16px;
      color: #38bdf8;
      font-size: 16px;
      pointer-events: none;
    }
    .form-input {
      width: 100%;
      padding: 13px 16px 13px 46px;
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 14px;
      color: #ffffff;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: all 0.25s ease;
    }
    .form-input:focus {
      border-color: #38bdf8;
      background: rgba(30, 41, 59, 1);
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.3);
    }
    .form-input::placeholder {
      color: #64748b;
    }

    /* Primary Submit Button */
    .btn-submit {
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
      border: none;
      border-radius: 14px;
      font-size: 15px;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
      transition: all 0.25s ease;
      margin-top: 10px;
    }
    .btn-submit:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(16, 185, 129, 0.5);
    }

    /* Verification Result Card */
    .verify-result-card {
      margin-top: 20px;
      padding: 18px;
      border-radius: 16px;
      background: rgba(30, 41, 59, 0.9);
      border: 1.5px solid rgba(56, 189, 248, 0.4);
      display: none;
    }
    .verify-result-card.active {
      display: block;
      animation: fadeIn 0.3s ease-out;
    }
    .verify-result-card.error {
      border-color: rgba(239, 68, 68, 0.5);
      background: rgba(239, 68, 68, 0.1);
    }
    .result-info {
      font-size: 13px;
      line-height: 1.6;
      color: #cbd5e1;
    }
    .result-info strong {
      color: #ffffff;
    }

    /* Contact Support Link Button */
    .btn-contact-support {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 12px;
      padding: 10px 18px;
      background: #ef4444;
      color: white;
      border-radius: 12px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
    }

    /* Social Login Area */
    .social-login-divider {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 24px 0 18px 0;
      color: var(--text-muted);
      font-size: 12px;
    }
    .social-login-divider::before, .social-login-divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: rgba(255, 255, 255, 0.1);
    }
    .social-buttons {
      display: flex;
      gap: 10px;
      justify-content: center;
    }
    .btn-social {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: rgba(30, 41, 59, 0.6);
      color: #cbd5e1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      cursor: not-allowed;
      opacity: 0.6;
      position: relative;
    }

    /* Guest Footer */
    .guest-footer {
      text-align: center;
      padding: 18px 24px;
      background: rgba(15, 23, 42, 0.95);
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .btn-guest {
      color: #38bdf8;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .btn-guest:hover {
      color: #ffffff;
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <div class="bg-blob blob-1"></div>
  <div class="bg-blob blob-2"></div>

  <div class="portal-container">
    <!-- Portal Header -->
    <div class="portal-header">
      <div class="portal-logo">
        <i class="fa-solid fa-map-location-dot"></i>
      </div>
      <h1 class="portal-title">มหาวิทยาลัยราชภัฏศรีสะเกษ</h1>
      <p class="portal-subtitle">SSKRU 3D Campus Map & Authentication Portal</p>
    </div>

    <!-- Dual Role Switcher -->
    <div class="role-switcher">
      <button class="role-btn active" id="tab-student" onclick="switchRole('student')">
        <i class="fa-solid fa-graduation-cap"></i> สำหรับนักศึกษา (Student)
      </button>
      <button class="role-btn" id="tab-staff" onclick="switchRole('staff')">
        <i class="fa-solid fa-user-shield"></i> สำหรับบุคลากร & Admin
      </button>
    </div>

    <!-- 1. STUDENT PANEL -->
    <div class="panel-content active" id="panel-student">
      <div class="sub-tabs">
        <button class="sub-tab-btn active" id="subtab-student-verify" onclick="switchStudentSubTab('verify')">
          <i class="fa-solid fa-id-card"></i> ยืนยันตัวตน & ลงทะเบียน
        </button>
        <button class="sub-tab-btn" id="subtab-student-login" onclick="switchStudentSubTab('login')">
          <i class="fa-solid fa-key"></i> เข้าสู่ระบบนักศึกษา
        </button>
      </div>

      <!-- Student Verify & Register Form -->
      <form id="form-student-verify" onsubmit="handleStudentVerify(event)">
        <div class="form-group">
          <label class="form-label"><i class="fa-solid fa-hashtag"></i> รหัสนักศึกษา (Student ID)</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-user-graduate input-icon"></i>
            <input type="text" id="verify-student-id" class="form-input" placeholder="เช่น 6512345678-9" required />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label"><i class="fa-solid fa-id-badge"></i> เลขบัตรประจำตัวประชาชน (13 หลัก)</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-address-card input-icon"></i>
            <input type="text" id="verify-citizen-id" class="form-input" placeholder="เช่น 1330100XXXXXX" maxlength="13" required />
          </div>
        </div>
        <button type="submit" class="btn-submit">
          <i class="fa-solid fa-magnifying-glass"></i> ตรวจสอบข้อมูลสิทธิ์นักศึกษา
        </button>
      </form>

      <!-- Student Verification Result Box -->
      <div class="verify-result-card" id="student-verify-result"></div>

      <!-- Student Existing Login Form -->
      <form id="form-student-login" style="display: none;" onsubmit="handleStudentLogin(event)">
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
            <input type="password" id="login-student-pass" class="form-input" placeholder="กรอกรหัสผ่าน" required />
          </div>
        </div>
        <button type="submit" class="btn-submit">
          <i class="fa-solid fa-right-to-bracket"></i> เข้าสู่ระบบนักศึกษา
        </button>
      </form>
    </div>

    <!-- 2. STAFF & ADMIN PANEL -->
    <div class="panel-content" id="panel-staff">
      <div class="sub-tabs">
        <button class="sub-tab-btn active" id="subtab-staff-login" onclick="switchStaffSubTab('login')">
          <i class="fa-solid fa-user-lock"></i> เข้าสู่ระบบบุคลากร & Admin
        </button>
        <button class="sub-tab-btn" id="subtab-staff-reg" onclick="switchStaffSubTab('reg')">
          <i class="fa-solid fa-user-plus"></i> สมัครสมาชิกบุคลากรใหม่
        </button>
      </div>

      <!-- Staff/Admin Login Form -->
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
            <input type="password" id="staff-password" class="form-input" placeholder="กรอกรหัสผ่าน" required />
          </div>
        </div>
        <button type="submit" class="btn-submit">
          <i class="fa-solid fa-right-to-bracket"></i> เข้าสู่ระบบบุคลากร & Admin
        </button>

        <!-- Future Social Login Options -->
        <div class="social-login-divider">หรือเข้าสู่ระบบด้วยบริการภายนอก (เร็วๆ นี้)</div>
        <div class="social-buttons">
          <div class="btn-social" title="Google Login (เร็วๆ นี้)"><i class="fa-brands fa-google"></i></div>
          <div class="btn-social" title="Facebook Login (เร็วๆ นี้)"><i class="fa-brands fa-facebook"></i></div>
          <div class="btn-social" title="LINE Login (เร็วๆ นี้)"><i class="fa-brands fa-line"></i></div>
          <div class="btn-social" title="GitHub Login (เร็วๆ นี้)"><i class="fa-brands fa-github"></i></div>
        </div>
      </form>

      <!-- Staff Registration Form -->
      <form id="form-staff-reg" style="display: none;" onsubmit="handleStaffRegister(event)">
        <div class="form-group">
          <label class="form-label">อีเมลองค์กร / มหาวิทยาลัย (Email)</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-envelope input-icon"></i>
            <input type="email" id="reg-staff-email" class="form-input" placeholder="name@sskru.ac.th" required />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">ชื่อผู้ใช้งาน (Username)</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-user input-icon"></i>
            <input type="text" id="reg-staff-username" class="form-input" placeholder="กำหนด Username" required />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">รหัสผ่าน (Password)</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-key input-icon"></i>
            <input type="password" id="reg-staff-pass" class="form-input" placeholder="กำหนดรหัสผ่าน" required />
          </div>
        </div>
        <button type="submit" class="btn-submit" style="background: linear-gradient(135deg, #0284c7, #2563eb);">
          <i class="fa-solid fa-user-check"></i> สมัครสมาชิกบุคลากร
        </button>
      </form>
    </div>

    <!-- Guest Visitor Footer Access -->
    <div class="guest-footer">
      <a href="/" class="btn-guest">
        <i class="fa-solid fa-compass"></i> เข้าใช้งานแบบผู้เข้าชมทั่วไป (Guest Visitor Access)
      </a>
    </div>
  </div>

  <script>
    function switchRole(role) {
      document.querySelectorAll('.role-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.panel-content').forEach(panel => panel.classList.remove('active'));
      
      document.getElementById('tab-' + role).classList.add('active');
      document.getElementById('panel-' + role).classList.add('active');
    }

    function switchStudentSubTab(tab) {
      document.getElementById('subtab-student-verify').classList.toggle('active', tab === 'verify');
      document.getElementById('subtab-student-login').classList.toggle('active', tab === 'login');
      document.getElementById('form-student-verify').style.display = tab === 'verify' ? 'block' : 'none';
      document.getElementById('form-student-login').style.display = tab === 'login' ? 'block' : 'none';
      document.getElementById('student-verify-result').style.display = 'none';
    }

    function switchStaffSubTab(tab) {
      document.getElementById('subtab-staff-login').classList.toggle('active', tab === 'login');
      document.getElementById('subtab-staff-reg').classList.toggle('active', tab === 'reg');
      document.getElementById('form-staff-login').style.display = tab === 'login' ? 'block' : 'none';
      document.getElementById('form-staff-reg').style.display = tab === 'reg' ? 'block' : 'none';
    }

    async function handleStudentVerify(e) {
      e.preventDefault();
      const studentId = document.getElementById('verify-student-id').value.trim();
      const citizenId = document.getElementById('verify-citizen-id').value.trim();
      const resCard = document.getElementById('student-verify-result');

      resCard.className = 'verify-result-card active';
      resCard.innerHTML = '<div class="result-info"><i class="fa-solid fa-spinner fa-spin"></i> กำลังตรวจสอบข้อมูลรหัสนักศึกษา...</div>';

      try {
        const res = await fetch('/admin/api/auth/student_verify/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: studentId, citizen_id: citizenId })
        });
        const data = await res.json();

        if (data.success && data.status === 'MATCHED') {
          const info = data.student_info;
          resCard.className = 'verify-result-card active';
          resCard.innerHTML = `
            <div class="result-info">
              <p style="color:#10b981; font-weight:700; font-size:14px; margin-bottom:8px;"><i class="fa-solid fa-circle-check"></i> ตรวจสอบข้อมูลสิทธิ์สำเร็จ!</p>
              <p><strong>ชื่อ-นามสกุล:</strong> ${info.name}</p>
              <p><strong>รหัสนักศึกษา:</strong> ${info.student_id}</p>
              <p><strong>สังกัด:</strong> ${info.faculty} (${info.major})</p>
              <div style="margin-top:14px; border-top:1px solid rgba(255,255,255,0.1); padding-top:12px;">
                <label class="form-label">กำหนดรหัสผ่านใหม่สำหรับบัญชีนักศึกษา:</label>
                <input type="password" id="reg-student-password" class="form-input" placeholder="สร้างรหัสผ่าน" required style="margin-bottom:10px;" />
                <button type="button" onclick="completeStudentRegister('${info.student_id}', '${citizenId}')" class="btn-submit">
                  <i class="fa-solid fa-user-plus"></i> สร้างบัญชีและเข้าสู่ระบบ
                </button>
              </div>
            </div>
          `;
        } else {
          resCard.className = 'verify-result-card active error';
          resCard.innerHTML = `
            <div class="result-info" style="color:#f87171;">
              <p style="font-weight:700; font-size:14px; margin-bottom:6px;"><i class="fa-solid fa-triangle-exclamation"></i> ไม่พบข้อมูลในระบบ</p>
              <p>${data.message || 'ไม่พบรหัสนักศึกษาในระบบ'}</p>
              <a href="https://reg.sskru.ac.th" target="_blank" class="btn-contact-support">
                <i class="fa-solid fa-headset"></i> ติดต่อเจ้าหน้าที่สำนักทะเบียนและประมวลผล SSKRU
              </a>
            </div>
          `;
        }
      } catch (err) {
        resCard.className = 'verify-result-card active error';
        resCard.innerHTML = '<div class="result-info" style="color:#f87171;"><i class="fa-solid fa-circle-xmark"></i> เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์</div>';
      }
    }

    async function completeStudentRegister(studentId, citizenId) {
      const password = document.getElementById('reg-student-password').value.trim();
      if (!password) {
        alert('กรุณากรอกรหัสผ่านที่ต้องการสร้าง');
        return;
      }
      try {
        const res = await fetch('/admin/api/auth/student_register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: studentId, citizen_id: citizenId, password: password })
        });
        const data = await res.json();
        if (data.success) {
          alert('ลงทะเบียนสำเร็จ! เข้าสู่ระบบในนาม ' + data.user_name);
          window.location.href = '/';
        } else {
          alert(data.message || 'ลงทะเบียนไม่สำเร็จ');
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาดในการลงทะเบียน');
      }
    }

    async function handleStudentLogin(e) {
      e.preventDefault();
      const sid = document.getElementById('login-student-id').value.trim();
      const pass = document.getElementById('login-student-pass').value.trim();
      try {
        const res = await fetch('/admin/api/auth/student_login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ student_id: sid, password: pass })
        });
        const data = await res.json();
        if (data.success) {
          window.location.href = '/';
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
      try {
        const res = await fetch('/admin/api/auth/staff_login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: identifier, password: pass })
        });
        const data = await res.json();
        if (data.success) {
          window.location.href = data.redirect || '/';
        } else {
          alert(data.message || 'Username/Email หรือรหัสผ่านไม่ถูกต้อง');
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาดในการเข้าสู่ระบบ');
      }
    }

    async function handleStaffRegister(e) {
      e.preventDefault();
      const email = document.getElementById('reg-staff-email').value.trim();
      const username = document.getElementById('reg-staff-username').value.trim();
      const pass = document.getElementById('reg-staff-pass').value.trim();
      try {
        const res = await fetch('/admin/api/auth/staff_register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, username: username, password: pass })
        });
        const data = await res.json();
        if (data.success) {
          alert('สมัครสมาชิกบุคลากรสำเร็จ! ยินดีต้อนรับ คุณ ' + data.username);
          window.location.href = '/';
        } else {
          alert(data.message || 'สมัครสมาชิกไม่สำเร็จ');
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาดในการสมัครสมาชิก');
      }
    }
  </script>
</body>
</html>

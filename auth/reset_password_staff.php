<?php
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>รีเซ็ตรหัสผ่านบุคลากร — SSKRU Campus Map</title>
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
    @keyframes rise {
      0% { bottom: -10%; opacity: 0; }
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
    }

    .card-body {
      padding: 28px;
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
    }

    .card-footer {
      padding: 16px 28px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      text-align: center;
    }
    .back-link {
      color: var(--primary-light);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
    }
    .back-link:hover {
      text-decoration: underline;
    }

    .success-result-box {
      display: none;
      background: #f0fdf4;
      border: 1.5px solid #bbf7d0;
      border-radius: 14px;
      padding: 20px;
      margin-top: 20px;
      text-align: center;
      animation: fadeIn 0.4s ease;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .success-icon {
      font-size: 36px;
      color: var(--success);
      margin-bottom: 8px;
    }
    .success-title {
      font-size: 16px;
      font-weight: 700;
      color: #166534;
      margin-bottom: 6px;
    }
    .success-desc {
      font-size: 13px;
      color: #15803d;
      line-height: 1.5;
    }
  </style>
</head>
<body>

  <div class="particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
  </div>

  <div class="login-card">
    <div class="card-header">
      <div class="university-badge">
        <i class="fa-solid fa-key"></i>
      </div>
      <h1>รีเซ็ตรหัสผ่านบุคลากร</h1>
      <p>มหาวิทยาลัยราชภัฏศรีสะเกษ (SSKRU Faculty & Staff)</p>
    </div>

    <div class="card-body">
      <div class="intro-text" style="font-size: 13px; color: #64748b; margin-bottom: 18px; line-height: 1.5;">
        กรุณากรอก <strong>Username</strong> หรือ <strong>Email</strong> ที่ท่านลงทะเบียนไว้ ระบบจะส่งลิงก์และรหัสยืนยันตัวตน (OTP) ไปยังอีเมลของท่าน
      </div>

      <form id="form-staff-request-reset" onsubmit="handleRequestReset(event)">
        <div class="form-group">
          <label class="form-label">Username หรือ Email ของบุคลากร</label>
          <div class="input-wrapper">
            <i class="fa-solid fa-at input-icon"></i>
            <input type="text" id="staff-identifier-input" class="form-input" placeholder="กรอก Username หรือ Email" required />
          </div>
        </div>

        <button type="submit" class="btn-primary" id="btn-submit-request">
          <i class="fa-solid fa-paper-plane"></i> ส่งรหัสยืนยันสิทธิ์ไปยังอีเมล
        </button>
      </form>

      <!-- Clean Success Box (Shows Email Sent Only - Strictly via Email) -->
      <div class="success-result-box" id="success-box">
        <div class="success-icon"><i class="fa-solid fa-envelope-circle-check"></i></div>
        <div class="success-title">ส่งอีเมลยืนยันสิทธิ์สำเร็จ!</div>
        <div class="success-desc">
          ระบบได้ส่งรหัส OTP และลิงก์สำหรับตั้งรหัสผ่านใหม่ไปยัง<br>
          <strong id="res-email" style="color:#0f172a; font-size:14px; background:#e2e8f0; padding:2px 8px; border-radius:6px; display:inline-block; margin-top:6px;"></strong>
        </div>
        <div style="background:#ffffff; border:1px solid #bbf7d0; border-radius:12px; padding:12px; font-size:12.5px; color:#64748b; line-height:1.5; margin-top:14px; text-align:left;">
          <i class="fa-solid fa-circle-info" style="color:#2563eb;"></i> กรุณาเปิดกล่องจดหมายอีเมล (Inbox / Spam) ของท่าน และคลิกลิงก์ยืนยันที่ได้รับในอีเมลเพื่อดำเนินการตั้งรหัสผ่านใหม่ (ลิงก์มีอายุ 15 นาที)
        </div>
      </div>
    </div>

    <div class="card-footer">
      <a href="/login/" class="back-link" id="link-back-login">
        <i class="fa-solid fa-arrow-left"></i> ย้อนกลับไปหน้าเข้าสู่ระบบ
      </a>
    </div>
  </div>

  <script>
    if (window.location.pathname.endsWith('.php')) {
      document.getElementById('link-back-login').href = 'login.php';
    }

    async function handleRequestReset(e) {
      e.preventDefault();
      const identifier = document.getElementById('staff-identifier-input').value.trim();
      const btn = document.getElementById('btn-submit-request');

      if (!identifier) {
        alert('กรุณากรอก Username หรือ Email');
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังส่งคำขอ...';

      const isPhp = window.location.pathname.endsWith('.php');
      const endpoint = isPhp ? 'api.php?action=staff_request_reset' : '/admin/api/auth/staff_request_reset/';

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: identifier })
        });
        const data = await res.json();

        if (data.success) {
          document.getElementById('form-staff-request-reset').style.display = 'none';
          document.getElementById('res-email').textContent = data.email;
          document.getElementById('success-box').style.display = 'block';
        } else {
          alert(data.message || 'ไม่สามารถส่งรหัสยืนยันได้ กรุณาลองใหม่อีกครั้ง');
          btn.disabled = false;
          btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> ส่งรหัสยืนยันสิทธิ์ไปยังอีเมล';
        }
      } catch (err) {
        alert('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์');
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> ส่งรหัสยืนยันสิทธิ์ไปยังอีเมล';
      }
    }
  </script>
</body>
</html>

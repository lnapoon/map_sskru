<?php
// SSKRU 3D Map Application (Native PHP & MySQL Integration)
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <!-- ============================================================
       Cross-Platform Viewport & PWA Meta Tags
       ============================================================ -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>SSKRU Campus Map - แผนที่นำทาง มรภ.ศรีสะเกษ</title>

  <!-- SEO -->
  <meta name="description" content="ระบบแผนผังนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ ค้นหาตึก นำทางเดินเท้า และระบุตำแหน่ง GPS บนแผนที่วิทยาเขตได้จริง">
  <meta name="keywords" content="แผนที่ มรภ.ศก, มหาวิทยาลัยราชภัฏศรีสะเกษ, นำทางอาคาร, SSKRU Map, Sisaket Rajabhat University">
  <meta name="author" content="Sisaket Rajabhat University">

  <!-- PWA / Android Chrome -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="theme-color" content="#1a4fa0" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0d2c5e" media="(prefers-color-scheme: dark)">
  <link rel="manifest" href="manifest.json">

  <!-- PWA / iOS Safari -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="SSKRU Map">
  <link rel="apple-touch-icon" href="images/icon-192.png">

  <!-- Open Graph -->
  <meta property="og:title" content="SSKRU Campus Map - แผนที่นำทาง มรภ.ศรีสะเกษ">
  <meta property="og:description" content="ค้นหาตึก นำทางเดินเท้า GPS Tracking บนแผนผัง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ">
  <meta property="og:type" content="website">
  <meta property="og:image" content="images/Map.png?v=4.1">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <!-- FontAwesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />

  <!-- Main Dynamic Stylesheet -->
  <link rel="stylesheet" href="styles.css?v=14.0" />
</head>
<body>

  <div class="app-container" id="app-container">

    <!-- ==========================================
         SIDE DRAWER OVERLAY BACKDROP
         ========================================== -->
    <div class="drawer-backdrop" id="drawer-backdrop"></div>

    <!-- ==========================================
         SIDE DRAWER MENU (Left Slide-in)
         ========================================== -->
    <aside class="side-drawer" id="side-drawer" aria-label="เมนูหลัก" role="complementary">
      <!-- Profile Header -->
      <div class="drawer-profile">
        <div class="drawer-close-btn" id="btn-drawer-close" aria-label="ปิดเมนู">
          <i class="fa-solid fa-xmark"></i>
        </div>
        <div class="drawer-avatar" id="drawer-avatar-icon">
          <i class="fa-solid fa-graduation-cap"></i>
        </div>
        <div class="drawer-user-info">
          <div class="drawer-username" id="drawer-username">SSKRU Campus Map</div>
          <div class="drawer-subtitle" id="drawer-subtitle">มหาวิทยาลัยราชภัฏศรีสะเกษ</div>
        </div>
      </div>

      <!-- Nav Items -->
      <nav class="drawer-nav" role="navigation" aria-label="เมนูนำทาง">
        <!-- Admin Dashboard Button -->
        <a href="/admin/dashboard/" class="drawer-nav-item" id="btn-drawer-admin-dashboard" style="display: none; text-decoration: none; background: rgba(37,99,235,0.08); border-radius: 10px; margin: 4px 10px; width: calc(100% - 20px);">
          <div class="drawer-nav-icon" style="background: #2563eb; color: white;"><i class="fa-solid fa-gauge-high"></i></div>
          <span style="font-weight: 700; color: #1d4ed8;">กลับหน้า Admin Dashboard</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow" style="color: #2563eb;"></i>
        </a>

        <div class="drawer-divider" id="drawer-admin-divider" style="display: none;"></div>

        <!-- User Profile Button -->
        <button class="drawer-nav-item" id="btn-drawer-profile">
          <div class="drawer-nav-icon purple"><i class="fa-solid fa-user-circle"></i></div>
          <span>โปรไฟล์ของฉัน</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow"></i>
        </button>

        <div class="drawer-divider"></div>

        <button class="drawer-nav-item" id="btn-drawer-info">
          <div class="drawer-nav-icon orange"><i class="fa-solid fa-circle-info"></i></div>
          <span>ข้อมูลติดต่อมหาวิทยาลัย</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow"></i>
        </button>

        <div class="drawer-divider"></div>

        <button class="drawer-nav-item" id="btn-drawer-share">
          <div class="drawer-nav-icon teal"><i class="fa-solid fa-share-nodes"></i></div>
          <span>แชร์แผนที่นี้</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow"></i>
        </button>

        <div class="drawer-divider"></div>

        <button class="drawer-nav-item" id="btn-drawer-pdpa">
          <div class="drawer-nav-icon green" style="background: rgba(16,185,129,0.15); color: #10b981;"><i class="fa-solid fa-shield-halved"></i></div>
          <span>สิทธิ์พิกัด GPS & PDPA</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow"></i>
        </button>

        <div class="drawer-divider"></div>

        <!-- Logout Button -->
        <button class="drawer-nav-item drawer-nav-logout" id="btn-drawer-logout">
          <div class="drawer-nav-icon danger"><i class="fa-solid fa-right-from-bracket"></i></div>
          <span>ออกจากระบบ</span>
          <i class="fa-solid fa-chevron-right drawer-nav-arrow"></i>
        </button>

        <div class="drawer-divider"></div>

        <div class="drawer-version-badge">
          <i class="fa-solid fa-map-location-dot"></i>
          SSKRU Campus Map v3.0
        </div>
      </nav>
    </aside>

    <!-- ==========================================
         USER PROFILE PANEL (Slide-in from right)
         ========================================== -->
    <div class="profile-panel-backdrop" id="profile-panel-backdrop"></div>
    <aside class="profile-panel" id="profile-panel" aria-label="โปรไฟล์ผู้ใช้">
      <div class="profile-panel-header">
        <button class="profile-panel-close" id="btn-profile-close"><i class="fa-solid fa-xmark"></i></button>
        <h3>โปรไฟล์ผู้ใช้</h3>
      </div>
      <div class="profile-panel-body">
        <!-- Avatar Section (Clean without edit button) -->
        <div class="profile-avatar-section">
          <div class="profile-avatar-large" id="profile-avatar-large">
            <i class="fa-solid fa-user-graduate"></i>
          </div>
          <div class="profile-name" id="profile-name">ผู้ใช้งาน</div>
          <div class="profile-role-badge" id="profile-role-badge">นักศึกษา</div>
        </div>

        <!-- Editable Bio Section -->
        <div class="profile-editable-section">
          <div class="profile-section-title">
            <i class="fa-solid fa-pen-to-square"></i> ข้อมูลส่วนตัวที่แก้ไขได้
          </div>
          <div class="profile-form-group">
            <label class="profile-form-label">คำแนะนำตัว / Bio <span class="char-count" id="bio-char-count">0/120</span></label>
            <textarea id="profile-bio-input" class="profile-bio-textarea" maxlength="120" placeholder="เขียนข้อความแนะนำตัวสั้นๆ หรือคติประจำใจ..."></textarea>
          </div>
          <div class="profile-form-group">
            <label class="profile-form-label">ชื่อเล่น (Nickname)</label>
            <input type="text" id="profile-nickname-input" class="profile-text-input" placeholder="เช่น พูน" maxlength="30" />
          </div>
          <button type="button" class="profile-save-btn" id="btn-save-profile">
            <i class="fa-solid fa-floppy-disk"></i> บันทึกข้อมูลโปรไฟล์
          </button>
        </div>

        <!-- Locked Identity Cards Section with Privacy Shield -->
        <div class="profile-info-cards">
          <div class="profile-section-title locked-title" style="display: flex; justify-content: space-between; align-items: center;">
            <span><i class="fa-solid fa-shield-halved"></i> ข้อมูลระบุตัวตน</span>
            <button type="button" class="btn-toggle-privacy" id="btn-toggle-privacy" title="ปลดล็อคเพื่อดูข้อมูล">
              <i class="fa-solid fa-eye" id="privacy-icon"></i> <span id="privacy-toggle-label">แสดงข้อมูล</span>
            </button>
          </div>

          <div class="profile-info-card locked">
            <div class="profile-info-icon"><i class="fa-solid fa-user-check"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">ชื่อ-นามสกุลจริง (ล็อค)</div>
              <div class="profile-info-value privacy-masked" id="profile-fullname-locked">••••••••••••</div>
            </div>
            <span class="locked-badge"><i class="fa-solid fa-lock"></i></span>
          </div>

          <div class="profile-info-card locked">
            <div class="profile-info-icon"><i class="fa-solid fa-id-card"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">รหัสนักศึกษา (ล็อค)</div>
              <div class="profile-info-value privacy-masked" id="profile-student-id">••••••••••</div>
            </div>
            <span class="locked-badge"><i class="fa-solid fa-lock"></i></span>
          </div>

          <div class="profile-info-card locked">
            <div class="profile-info-icon"><i class="fa-solid fa-envelope"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">อีเมลมหาวิทยาลัย (ล็อค)</div>
              <div class="profile-info-value privacy-masked" id="profile-email-locked">••••••••••••••••••••</div>
            </div>
            <span class="locked-badge"><i class="fa-solid fa-lock"></i></span>
          </div>

          <div class="profile-info-card locked">
            <div class="profile-info-icon"><i class="fa-solid fa-university"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">สังกัดสถาบัน (ล็อค)</div>
              <div class="profile-info-value">มหาวิทยาลัยราชภัฏศรีสะเกษ</div>
            </div>
            <span class="locked-badge"><i class="fa-solid fa-lock"></i></span>
          </div>

          <div class="profile-info-card">
            <div class="profile-info-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">สิทธิ์การใช้งาน</div>
              <div class="profile-info-value" id="profile-access-level">ดูแผนที่และค้นหาอาคาร</div>
            </div>
          </div>

          <div class="profile-info-card">
            <div class="profile-info-icon"><i class="fa-solid fa-clock"></i></div>
            <div class="profile-info-detail">
              <div class="profile-info-label">เข้าใช้งานล่าสุด</div>
              <div class="profile-info-value" id="profile-last-access">—</div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="profile-actions">
          <button class="profile-action-btn logout" id="btn-profile-logout">
            <i class="fa-solid fa-right-from-bracket"></i> ออกจากระบบ
          </button>
        </div>
      </div>
    </aside>

    <!-- ==========================================
         TOP NAVBAR (Compact Mobile-First Header)
         ========================================== -->
    <header class="top-navbar" role="banner">
      <!-- Hamburger Menu Button -->
      <button class="nav-hamburger" id="btn-hamburger" aria-label="เปิดเมนู">
        <i class="fa-solid fa-bars"></i>
      </button>

      <!-- Brand Logo (Center on mobile, Left on desktop) -->
      <div class="nav-brand" id="btn-logo-reset" role="button" tabindex="0" aria-label="กลับสู่หน้าแรก">
        <div class="brand-logo">
          <i class="fa-solid fa-graduation-cap"></i>
        </div>
        <div class="brand-text">
          <h1>SSKRU CAMPUS</h1>
          <p>Sisaket Rajabhat University</p>
        </div>
      </div>

      <!-- Integrated Search Box (Desktop) -->
      <div class="nav-search-wrapper" id="nav-search-desktop">
        <div class="nav-search-bar">
          <i class="fa-solid fa-magnifying-glass search-bar-icon"></i>
          <input
            type="search"
            id="search-input"
            placeholder="ค้นหาตึก, คณะ หรืออักษรย่อ..."
            autocomplete="off"
            aria-label="ค้นหาสถานที่ภายในมหาวิทยาลัย"
          />
          <button id="btn-search-clear" class="search-clear-btn" aria-label="ล้างการค้นหา">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div class="autocomplete-dropdown" id="search-suggestions" role="listbox" aria-label="ผลการค้นหา"></div>
      </div>

      <!-- Desktop Action Buttons -->
      <div class="nav-actions" id="nav-desktop-actions">
        <button class="nav-btn secondary" id="btn-univ-info-trigger" aria-label="ข้อมูลมหาวิทยาลัย">
          <i class="fa-solid fa-circle-info"></i> ข้อมูลติดต่อ
        </button>
        <button class="nav-icon-btn theme-toggle-btn" id="btn-theme-toggle" aria-label="สลับโทนสี" title="สลับโทนสี (สว่าง/มืด)">
          <i class="fa-solid fa-moon"></i>
        </button>
      </div>

      <!-- Mobile Actions -->
      <div class="nav-mobile-actions">
        <button class="nav-icon-btn theme-toggle-btn" id="btn-theme-toggle-mobile" aria-label="สลับโทนสี" title="สลับโทนสี (สว่าง/มืด)">
          <i class="fa-solid fa-moon"></i>
        </button>
        <button class="nav-icon-btn" id="btn-mobile-search" aria-label="ค้นหา">
          <i class="fa-solid fa-magnifying-glass"></i>
        </button>
      </div>
    </header>



    <!-- Mobile Search Bar (Expands on tap) -->
    <div class="mobile-search-panel" id="mobile-search-panel">
      <div class="mobile-search-inner">
        <button class="mobile-search-back" id="btn-mobile-search-close">
          <i class="fa-solid fa-arrow-left"></i>
        </button>
        <div class="nav-search-bar mobile-full">
          <i class="fa-solid fa-magnifying-glass search-bar-icon"></i>
          <input
            type="search"
            id="search-input-mobile"
            placeholder="ค้นหาตึก, คณะ หรืออักษรย่อ..."
            autocomplete="off"
            aria-label="ค้นหาสถานที่"
          />
          <button id="btn-search-clear-mobile" class="search-clear-btn">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
      <div class="autocomplete-dropdown" id="search-suggestions-mobile" role="listbox"></div>
    </div>

    <!-- ==========================================
         ACTIVE NAVIGATION HUD OVERLAY (Google Maps Style)
         ========================================== -->
    <div class="nav-hud-overlay" id="nav-hud-overlay" style="display: none;">
      <div class="nav-hud-top-card">
        <div class="nav-hud-turn-icon" id="hud-turn-icon">
          <i class="fa-solid fa-arrow-up"></i>
        </div>
        <div class="nav-hud-turn-info">
          <div class="nav-hud-next-step" id="hud-next-step">ตรงไปตามถนนภายในวิทยาเขต</div>
          <div class="nav-hud-dest-name" id="hud-dest-name">กำลังมุ่งหน้าสู่จุดหมาย</div>
        </div>
      </div>
      <div class="nav-hud-bottom-bar">
        <div class="nav-hud-stats">
          <span class="nav-hud-time" id="hud-time-val">--</span>
          <span class="nav-hud-dist" id="hud-dist-val">--</span>
        </div>
        <button class="nav-hud-stop-btn" id="btn-hud-stop" aria-label="ยกเลิกนำทาง">
          <i class="fa-solid fa-xmark"></i> ยกเลิก
        </button>
      </div>
    </div>

    <!-- ==========================================
         MAP VIEWPORT
         ========================================== -->
    <main class="map-viewport" id="map-viewport" aria-label="แผนผังแบบโต้ตอบ">
      <div id="map"></div>
    </main>

    <!-- ==========================================
         FLOATING MAP CONTROLS
         ========================================== -->
    <div class="map-control-overlay">
      <button class="map-control-btn" id="btn-map-zoom-in" aria-label="ซูมเข้า" title="ซูมเข้า"><i class="fa-solid fa-plus"></i></button>
      <button class="map-control-btn" id="btn-map-zoom-out" aria-label="ซูมออก" title="ซูมออก"><i class="fa-solid fa-minus"></i></button>
      <div class="map-control-divider"></div>
      <button class="map-control-btn gps-btn" id="btn-map-my-location" aria-label="ตำแหน่งปัจจุบัน" title="ระบุตำแหน่งของฉัน">
        <i class="fa-solid fa-location-crosshairs"></i>
      </button>
      <button class="map-control-btn" id="btn-map-reset" aria-label="กลับสู่กึ่งกลาง" title="มุมมองปกติ">
        <i class="fa-solid fa-compress"></i>
      </button>
    </div>

    <!-- ==========================================
         BOTTOM CAROUSEL PANEL
         ========================================== -->
    <div class="carousel-container" id="carousel-panel" aria-label="รายการอาคาร">
      <div class="carousel-header">
        <div class="carousel-title-row">
          <h3><i class="fa-regular fa-compass"></i> สำรวจสถานที่</h3>
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="carousel-counter" id="carousel-item-counter">21 ตึกอาคาร</span>
            <button class="btn-tour-3d" id="btn-tour-3d" title="นำทางทัวร์ชมวิทยาเขต 3D แบบอัตโนมัติ">
              <i class="fa-solid fa-video"></i> ทัวร์ 3D
            </button>
            <button class="carousel-toggle-btn" id="btn-toggle-carousel" title="ย่อ/ขยายแท็บ" aria-label="ย่อหรือขยายแท็บ">
              <i class="fa-solid fa-chevron-down"></i>
            </button>
          </div>
        </div>
        <nav class="category-tabs" id="category-filter" aria-label="กรองประเภท">
          <button class="category-tab active" data-category="all">ทั้งหมด</button>
          <button class="category-tab" data-category="academic">คณะ/เรียน</button>
          <button class="category-tab" data-category="office">สำนักงาน</button>
          <button class="category-tab" data-category="facility">บริการ</button>
          <button class="category-tab" data-category="library">วิทยบริการ</button>
          <button class="category-tab" data-category="other">อื่นๆ</button>
        </nav>
      </div>
      <div class="building-carousel" id="building-carousel-wrapper" role="list">
        <div class="loading-placeholder-carousel">
          <i class="fa-solid fa-circle-notch fa-spin"></i> กำลังโหลดข้อมูล...
        </div>
      </div>
    </div>

    <!-- Navigation panel removed - replaced with location display -->

    <!-- ==========================================
         BUILDING INFO PANEL / BOTTOM SHEET
         ========================================== -->
    <section class="info-panel" id="building-info-panel" aria-label="รายละเอียดอาคาร">
      <div class="info-panel-drag-handle" id="panel-drag-handle"></div>

      <!-- Visual Banner -->
      <div class="info-panel-header">
        <button class="info-panel-close" id="btn-panel-close" aria-label="ปิด">
          <i class="fa-solid fa-xmark"></i>
        </button>
        <div id="panel-image-container" style="height: 100%; width: 100%;"></div>
      </div>

      <!-- Info Body with Tabs -->
      <div class="info-panel-tabs-bar">
        <button class="info-tab-btn active" data-tab="info">ข้อมูล</button>
        <button class="info-tab-btn" data-tab="hours">เวลา</button>
        <button class="info-tab-btn" data-tab="contact">ติดต่อ</button>
      </div>

      <div class="info-panel-body">
        <!-- Tab: Info -->
        <div class="info-tab-pane active" id="tab-info">
          <div class="building-header-info">
            <h2 class="building-title-th" id="panel-title-th">อาคารเรียน</h2>
            <div class="building-title-en" id="panel-title-en">Building</div>
            <div class="building-badge-row">
              <span class="building-cat-badge" id="panel-badge-category">หมวดหมู่</span>
              <span class="building-status-badge" id="panel-badge-status">
                <span class="status-dot-pulse"></span>
                <span id="panel-status-text">ปิดบริการ</span>
              </span>
            </div>
          </div>
          <p class="building-description" id="panel-description">คำอธิบายตึก...</p>
          <div class="meta-detail-item">
            <div class="meta-icon"><i class="fa-solid fa-location-dot"></i></div>
            <div class="meta-content">
              <div class="meta-label">พิกัด GPS</div>
              <div class="meta-val" id="panel-meta-coords">-</div>
            </div>
          </div>
        </div>

        <!-- Tab: Hours -->
        <div class="info-tab-pane" id="tab-hours">
          <div class="meta-detail-item">
            <div class="meta-icon"><i class="fa-regular fa-clock"></i></div>
            <div class="meta-content">
              <div class="meta-label">เวลาเปิด-ปิดทำการ</div>
              <div class="meta-val" id="panel-meta-hours">-</div>
            </div>
          </div>
          <div class="hours-week-grid" id="hours-week-grid">
            <div class="hours-day-row"><span class="hours-day-name">จันทร์ - ศุกร์</span><span class="hours-day-time">08:30 – 16:30</span></div>
            <div class="hours-day-row closed"><span class="hours-day-name">เสาร์ - อาทิตย์</span><span class="hours-day-time">ปิดทำการ</span></div>
          </div>
        </div>

        <!-- Tab: Contact -->
        <div class="info-tab-pane" id="tab-contact">
          <div class="meta-detail-item" id="panel-meta-phone-row">
            <div class="meta-icon"><i class="fa-solid fa-phone"></i></div>
            <div class="meta-content">
              <div class="meta-label">เบอร์ติดต่อภายใน</div>
              <div class="meta-val" id="panel-meta-phone">-</div>
            </div>
          </div>
          <div class="meta-detail-item">
            <div class="meta-icon"><i class="fa-solid fa-building"></i></div>
            <div class="meta-content">
              <div class="meta-label">มหาวิทยาลัย</div>
              <div class="meta-val">มหาวิทยาลัยราชภัฏศรีสะเกษ</div>
            </div>
          </div>
          <div class="meta-detail-item">
            <div class="meta-icon"><i class="fa-solid fa-globe"></i></div>
            <div class="meta-content">
              <div class="meta-label">เว็บไซต์</div>
              <div class="meta-val"><a href="https://www.sskru.ac.th" target="_blank" rel="noopener">www.sskru.ac.th</a></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons — Google Maps Style (4 buttons) -->
      <div class="info-panel-actions">
        <button class="action-btn-card" id="btn-action-gmaps" aria-label="เปิดใน Google Maps">
          <div class="action-btn-icon navigate"><i class="fa-solid fa-map-location-dot"></i></div>
          <span>ดูใน Maps</span>
        </button>
        <button class="action-btn-card" id="btn-action-save" aria-label="บันทึกสถานที่">
          <div class="action-btn-icon save"><i class="fa-regular fa-bookmark"></i></div>
          <span>บันทึก</span>
        </button>
        <button class="action-btn-card" id="btn-action-share" aria-label="แชร์ตำแหน่ง">
          <div class="action-btn-icon share"><i class="fa-regular fa-share-from-square"></i></div>
          <span>แชร์</span>
        </button>
        <button class="action-btn-card" id="btn-action-call" aria-label="โทรติดต่อ">
          <div class="action-btn-icon call"><i class="fa-solid fa-phone"></i></div>
          <span>โทร</span>
        </button>
      </div>
    </section>

  </div><!-- /.app-container -->

  <!-- ==========================================
       MODALS & OVERLAYS
       ========================================== -->
  <!-- General Modal -->
  <div class="modal-overlay" id="custom-modal-overlay">
    <div class="modal-content-card">
      <div class="modal-body">
        <div class="modal-icon warning" id="modal-status-icon">
          <i class="fa-solid fa-triangle-exclamation"></i>
        </div>
        <h3 class="modal-title" id="modal-title-text">ข้อความ</h3>
        <p class="modal-desc" id="modal-desc-text">รายละเอียด...</p>
        <div class="modal-actions">
          <button class="modal-btn btn-primary" id="btn-modal-ok">ตกลง</button>
        </div>
      </div>
    </div>
  </div>



  <!-- Building Form Modal -->
  <div class="modal-overlay" id="building-form-overlay">
    <div class="modal-content-card" style="max-width: 480px;">
      <div class="modal-body" style="padding: 24px; text-align: left;">
        <h3 class="modal-title" id="building-form-title" style="margin-bottom:15px; color:var(--primary-color); border-bottom:1px solid var(--border-color); padding-bottom:8px;"><i class="fa-solid fa-edit"></i> จัดการข้อมูลตึก</h3>
        <form id="building-editor-form" style="display: flex; flex-direction: column; gap: 12px;">
          <input type="hidden" id="edit-building-id">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="nav-input-box">
              <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">รหัสตึก</label>
              <input type="text" id="edit-building-num" required class="form-input">
            </div>
            <div class="nav-input-box">
              <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">หมวดหมู่</label>
              <div class="nav-select-wrapper">
                <select id="edit-building-category" class="nav-select" style="height:38px; border-radius:6px; width: 100%;">
                  <option value="academic">เรียน/คณะ</option>
                  <option value="office">สำนักงาน</option>
                  <option value="facility">บริการ</option>
                  <option value="library">ไอที/สมุด</option>
                  <option value="other">อื่นๆ</option>
                </select>
              </div>
            </div>
          </div>
          <div class="nav-input-box">
            <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">ชื่อตึก (ภาษาไทย)</label>
            <input type="text" id="edit-building-name" required class="form-input">
          </div>
          <div class="nav-input-box">
            <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">ชื่อตึก (English)</label>
            <input type="text" id="edit-building-name-en" required class="form-input">
          </div>
          <div class="nav-input-box">
            <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">คำอธิบาย</label>
            <textarea id="edit-building-desc" class="form-input" style="height:70px; resize:none;"></textarea>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="nav-input-box">
              <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">เบอร์โทรศัพท์</label>
              <input type="text" id="edit-building-phone" class="form-input">
            </div>
            <div class="nav-input-box">
              <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">พิกัดพิกเซล [Y, X]</label>
              <input type="text" id="edit-building-coords" required readonly class="form-input" style="background:#f1f5f9;">
            </div>
          </div>
          <div class="nav-input-box">
            <label style="font-size:10px; font-weight:bold; color:var(--text-secondary);">พิกัด GPS จริง [Lat, Lng]</label>
            <input type="text" id="edit-building-real-coords" required placeholder="15.117620, 104.359200" class="form-input">
          </div>
          <div style="margin-top: 15px; display: flex; gap: 10px;">
            <button type="button" class="modal-btn" id="btn-building-delete" style="background:#ef4444; color:white; border:none; display:none; border-radius:8px; font-weight:bold; cursor:pointer; padding: 8px 16px;">ลบตึกนี้</button>
            <div style="display: flex; gap: 10px; margin-left: auto;">
              <button type="button" class="modal-btn btn-secondary" id="btn-building-form-cancel">ยกเลิก</button>
              <button type="submit" class="modal-btn btn-primary" id="btn-building-form-submit" style="background:var(--primary-color); color:white;">บันทึก</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Admin Dashboard Modal -->
  <div class="modal-overlay" id="admin-dashboard-overlay">
    <div class="modal-content-card admin-dashboard-card">
      <div class="modal-body" style="padding: 24px; text-align: left;">
        <div class="admin-dashboard-header">
          <div>
            <h3 class="modal-title" style="color:var(--primary-color); display: flex; align-items: center; gap: 8px;">
              <i class="fa-solid fa-server"></i> Backend Admin Dashboard
            </h3>
            <p style="font-size:12px; color:var(--text-secondary); margin-top:4px;">
              จัดการข้อมูลอาคารและพิกัดใน <code>data/buildings.json</code>
            </p>
          </div>
          <button class="modal-btn btn-secondary" id="btn-dash-close" style="padding: 6px 14px;"><i class="fa-solid fa-xmark"></i> ปิด</button>
        </div>
        <div class="dash-stats-grid">
          <div class="dash-stat-card"><span class="dash-stat-val" id="dash-total-buildings">0</span><span class="dash-stat-lbl">อาคารทั้งหมด</span></div>
          <div class="dash-stat-card academic"><span class="dash-stat-val" id="dash-academic-count">0</span><span class="dash-stat-lbl">คณะ/เรียน</span></div>
          <div class="dash-stat-card office"><span class="dash-stat-val" id="dash-office-count">0</span><span class="dash-stat-lbl">สำนักงาน</span></div>
          <div class="dash-stat-card facility"><span class="dash-stat-val" id="dash-facility-count">0</span><span class="dash-stat-lbl">บริการ</span></div>
          <div class="dash-stat-card library"><span class="dash-stat-val" id="dash-library-count">0</span><span class="dash-stat-lbl">ไอที/สมุด</span></div>
        </div>
        <div class="dash-toolbar">
          <div class="dash-search-box">
            <i class="fa-solid fa-magnifying-glass"></i>
            <input type="text" id="dash-search-input" placeholder="ค้นหาตามชื่อ, รหัส หรือหมวดหมู่...">
          </div>
          <div class="dash-toolbar-actions">
            <button class="admin-btn highlight" id="btn-dash-add"><i class="fa-solid fa-plus"></i> เพิ่มอาคาร</button>
            <button class="admin-btn" id="btn-dash-export"><i class="fa-solid fa-download"></i> สำรอง JSON</button>
          </div>
        </div>
        <div class="dash-table-wrapper">
          <table class="dash-table">
            <thead>
              <tr>
                <th style="width:50px;">รหัส</th>
                <th>ชื่ออาคาร (ไทย)</th>
                <th>ชื่ออาคาร (EN)</th>
                <th>หมวดหมู่</th>
                <th>พิกัด Pixel</th>
                <th>พิกัด GPS</th>
                <th>เบอร์โทร</th>
                <th style="text-align:center; width:110px;">จัดการ</th>
              </tr>
            </thead>
            <tbody id="dash-table-body"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Export Modal -->
  <div class="modal-overlay" id="export-modal-overlay">
    <div class="modal-content-card" style="max-width: 600px;">
      <div class="modal-body" style="padding: 24px; text-align: left;">
        <h3 class="modal-title" style="color:var(--primary-color);"><i class="fa-solid fa-code"></i> Export Config</h3>
        <p style="font-size:12px; color:var(--text-secondary); margin-bottom: 12px;">คัดลอกโค้ดด้านล่างแทนตัวแปร <code>BUILDINGS</code> ใน <code>app.js</code></p>
        <textarea id="export-textarea" readonly class="form-input" style="height:240px; font-family:monospace; font-size:11px; resize:none; background:#0f172a; color:#38bdf8; border:none; width:100%;"></textarea>
        <div style="margin-top:15px; display:flex; gap:10px; justify-content:flex-end;">
          <button class="modal-btn btn-secondary" id="btn-export-copy">คัดลอกโค้ด</button>
          <button class="modal-btn btn-primary" id="btn-export-close" style="background:var(--primary-color); color:white;">ปิด</button>
        </div>
      </div>
    </div>
  </div>

  <!-- PDPA Thai Digital Law Consent Modal -->
  <div class="pdpa-overlay" id="pdpa-modal-overlay">
    <div class="pdpa-card">
      <div class="pdpa-header">
        <div class="pdpa-icon-badge">
          <i class="fa-solid fa-shield-halved"></i>
        </div>
        <div>
          <h3 class="pdpa-title">ข้อตกลงคุ้มครองข้อมูลส่วนบุคคล (PDPA)</h3>
          <p class="pdpa-subtitle">ปฏิบัติตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 และกฎหมายดิจิทัลของไทย</p>
        </div>
      </div>
      <div class="pdpa-body">
        <p class="pdpa-intro">ระบบแผนที่ผังเมือง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ ขออนุญาตประมวลผลข้อมูลการใช้งานเพื่อให้บริการนำทางและอำนวยความสะดวกในการเข้าถึงสถานที่ ดังนี้:</p>
        <div class="pdpa-purpose-list">
          <div class="pdpa-purpose-item">
            <i class="fa-solid fa-location-crosshairs pdpa-item-icon"></i>
            <div>
              <strong>พิกัดตำแหน่งปัจจุบัน (GPS Location)</strong>
              <p>ใช้สำหรับคำนวณระยะทางและนำทางจากตำแหน่งของคุณไปยัง 40 อาคารในมหาวิทยาลัย</p>
            </div>
          </div>
          <div class="pdpa-purpose-item">
            <i class="fa-solid fa-cookie-bite pdpa-item-icon"></i>
            <div>
              <strong>ตัวเลือกและความจำระบบ (LocalStorage & Preferences)</strong>
              <p>ใช้สำหรับบันทึกธีมการแสดงผล (Dark/Light Mode) และอาคารที่คุณค้นหาบ่อย</p>
            </div>
          </div>
        </div>
      </div>
      <div class="pdpa-footer" style="display: flex; gap: 10px; width: 100%;">
        <button class="pdpa-btn pdpa-btn-accept" id="btn-pdpa-accept" style="flex: 1;">
          <i class="fa-solid fa-circle-check"></i> ยินยอมและเข้าสู่ระบบแผนที่
        </button>
        <button class="pdpa-btn" id="btn-pdpa-decline" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3);">
          <i class="fa-solid fa-circle-xmark"></i> ปฏิเสธ
        </button>
      </div>
    </div>
  </div>

  <!-- Password Prompt Modal for Privacy Shield -->
  <div class="privacy-modal-backdrop" id="privacy-modal-backdrop" style="display:none;">
    <div class="privacy-modal-card">
      <div class="privacy-modal-header">
        <div class="privacy-modal-icon"><i class="fa-solid fa-shield-halved"></i></div>
        <h4>ยืนยันรหัสผ่านเพื่อดูข้อมูล</h4>
        <button type="button" class="privacy-modal-close" id="btn-close-privacy-modal"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <div class="privacy-modal-body">
        <p style="font-size:12.5px; color:#64748b; margin-bottom:12px; line-height:1.5;">
          เพื่อความปลอดภัยของข้อมูลส่วนบุคคล กรุณากรอกรหัสผ่านบัญชีของคุณเพื่อปลดล็อคการแสดงผล
        </p>
        <div class="form-group" style="margin-bottom:12px;">
          <div class="input-wrapper" style="position:relative;">
            <i class="fa-solid fa-key" style="position:absolute; left:12px; top:12px; color:#94a3b8; font-size:14px;"></i>
            <input type="password" id="privacy-password-input" class="form-input" style="width:100%; padding:10px 14px 10px 38px; border-radius:10px; border:1.5px solid #cbd5e1; font-size:13px;" placeholder="กรอกรหัสผ่านของคุณ" />
          </div>
          <div id="privacy-error-msg" style="color:#ef4444; font-size:12px; margin-top:6px; display:none;"></div>
        </div>
        <button type="button" class="btn-primary" id="btn-submit-privacy-password" style="width:100%; padding:10px; border-radius:10px; font-weight:600; font-size:13.5px; background:linear-gradient(135deg, #1a4fa0, #2563eb);">
          <i class="fa-solid fa-unlock"></i> ยืนยันรหัสผ่านเพื่อแสดงข้อมูล
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast-container" id="toast-bar">
    <i class="fa-solid fa-circle-check" style="color: var(--color-open);"></i>
    <span id="toast-message">สำเร็จ</span>
  </div>

  <!-- ==========================================
       SCRIPTS
       ========================================== -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script src="app.js?v=17.0"></script>

</body>
</html>

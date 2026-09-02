/**
 * SSKRU Campus Map - Unified Custom Modal & Dialog Engine
 * Replaces native browser alert() and confirm() with modern frosted glass UI
 */

(function() {
  // 1. Inject Stylesheet if not present
  if (!document.getElementById('sskru-dialog-injected-styles')) {
    const style = document.createElement('style');
    style.id = 'sskru-dialog-injected-styles';
    style.textContent = `
      .sskru-dialog-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.68);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
      }
      .sskru-dialog-backdrop.open {
        opacity: 1;
        pointer-events: auto;
      }
      .sskru-dialog-modal {
        background: #ffffff;
        border-radius: 24px;
        width: 100%;
        max-width: 410px;
        box-shadow: 0 25px 60px -12px rgba(13, 44, 94, 0.35), 0 0 0 1px rgba(226, 232, 240, 0.9);
        overflow: hidden;
        text-align: center;
        padding: 32px 26px 24px;
        transform: scale(0.92) translateY(12px);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
      }
      .sskru-dialog-backdrop.open .sskru-dialog-modal {
        transform: scale(1) translateY(0);
      }
      .sskru-dialog-icon-wrapper {
        width: 68px;
        height: 68px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 18px;
        font-size: 32px;
        transition: all 0.3s ease;
      }
      .sskru-dialog-icon-wrapper.success {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #16a34a;
        border: 2px solid #86efac;
        box-shadow: 0 8px 24px rgba(22, 163, 74, 0.22);
      }
      .sskru-dialog-icon-wrapper.error, .sskru-dialog-icon-wrapper.danger {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #dc2626;
        border: 2px solid #fca5a5;
        box-shadow: 0 8px 24px rgba(220, 38, 38, 0.22);
      }
      .sskru-dialog-icon-wrapper.warning {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #d97706;
        border: 2px solid #fcd34d;
        box-shadow: 0 8px 24px rgba(217, 119, 6, 0.22);
      }
      .sskru-dialog-icon-wrapper.info, .sskru-dialog-icon-wrapper.primary {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        color: #2563eb;
        border: 2px solid #bfdbfe;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.22);
      }
      .sskru-dialog-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 10px;
        line-height: 1.4;
      }
      .sskru-dialog-message {
        font-size: 14.5px;
        color: #475569;
        line-height: 1.6;
        margin: 0 0 24px;
        word-break: break-word;
      }
      .sskru-dialog-actions {
        display: flex;
        gap: 12px;
      }
      .sskru-dialog-btn {
        flex: 1;
        padding: 13px 20px;
        border-radius: 14px;
        font-size: 14.5px;
        font-weight: 600;
        cursor: pointer;
        border: none;
        font-family: inherit;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.2s ease;
      }
      .sskru-dialog-btn-cancel {
        background: #f1f5f9;
        color: #475569;
        border: 1.5px solid #cbd5e1;
      }
      .sskru-dialog-btn-cancel:hover {
        background: #e2e8f0;
        color: #1e293b;
      }
      .sskru-dialog-btn-confirm {
        background: linear-gradient(135deg, #1a4fa0, #2563eb);
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
      }
      .sskru-dialog-btn-confirm:hover {
        background: linear-gradient(135deg, #0d2c5e, #1d4ed8);
        transform: translateY(-1.5px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
      }
      .sskru-dialog-btn-confirm.success {
        background: linear-gradient(135deg, #16a34a, #059669) !important;
        box-shadow: 0 4px 16px rgba(22, 163, 74, 0.35) !important;
      }
      .sskru-dialog-btn-confirm.success:hover {
        background: linear-gradient(135deg, #15803d, #047857) !important;
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.5) !important;
      }
      .sskru-dialog-btn-confirm.danger, .sskru-dialog-btn-confirm.error {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.35) !important;
      }
      .sskru-dialog-btn-confirm.danger:hover, .sskru-dialog-btn-confirm.error:hover {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.5) !important;
      }
    `;
    document.head.appendChild(style);
  }

  // 2. Custom Alert Implementation
  window.showSskruAlert = function({
    title = "แจ้งเตือน",
    message = "",
    type = "info", // success, error, warning, info
    buttonText = "ตกลง"
  } = {}) {
    return new Promise((resolve) => {
      let backdrop = document.getElementById('sskru-custom-alert-backdrop');
      if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.id = 'sskru-custom-alert-backdrop';
        backdrop.className = 'sskru-dialog-backdrop';
        backdrop.innerHTML = `
          <div class="sskru-dialog-modal">
            <div class="sskru-dialog-icon-wrapper" id="sskru-alert-icon-wrap">
              <i id="sskru-alert-icon" class="fa-solid fa-circle-info"></i>
            </div>
            <h3 class="sskru-dialog-title" id="sskru-alert-title"></h3>
            <p class="sskru-dialog-message" id="sskru-alert-message"></p>
            <div class="sskru-dialog-actions">
              <button type="button" class="sskru-dialog-btn sskru-dialog-btn-confirm" id="sskru-alert-btn-ok" style="width:100%;">ตกลง</button>
            </div>
          </div>
        `;
        document.body.appendChild(backdrop);
      }

      const iconWrap = backdrop.querySelector('#sskru-alert-icon-wrap');
      const iconEl = backdrop.querySelector('#sskru-alert-icon');
      const titleEl = backdrop.querySelector('#sskru-alert-title');
      const msgEl = backdrop.querySelector('#sskru-alert-message');
      const okBtn = backdrop.querySelector('#sskru-alert-btn-ok');

      let iconClass = 'fa-circle-info';
      if (type === 'success') iconClass = 'fa-circle-check';
      else if (type === 'error' || type === 'danger') iconClass = 'fa-circle-xmark';
      else if (type === 'warning') iconClass = 'fa-triangle-exclamation';

      iconWrap.className = `sskru-dialog-icon-wrapper ${type}`;
      iconEl.className = `fa-solid ${iconClass}`;
      titleEl.textContent = title;
      msgEl.textContent = message;
      okBtn.textContent = buttonText;
      okBtn.className = `sskru-dialog-btn sskru-dialog-btn-confirm ${type}`;

      backdrop.style.display = 'flex';
      requestAnimationFrame(() => backdrop.classList.add('open'));

      const closeAlert = () => {
        backdrop.classList.remove('open');
        setTimeout(() => {
          backdrop.style.display = 'none';
          resolve(true);
        }, 250);
      };

      okBtn.onclick = closeAlert;
      backdrop.onclick = (e) => {
        if (e.target === backdrop) closeAlert();
      };
    });
  };

  // 3. Custom Confirm Implementation
  window.showSskruConfirm = function({
    title = "ยืนยันการทำรายการ",
    message = "ต้องการดำเนินการต่อใช่หรือไม่?",
    icon = "fa-circle-question",
    type = "primary", // primary, danger, warning, success
    confirmText = "ตกลง",
    cancelText = "ยกเลิก"
  } = {}) {
    return new Promise((resolve) => {
      let backdrop = document.getElementById('sskru-custom-dialog-backdrop');
      if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.id = 'sskru-custom-dialog-backdrop';
        backdrop.className = 'sskru-dialog-backdrop';
        backdrop.innerHTML = `
          <div class="sskru-dialog-modal">
            <div class="sskru-dialog-icon-wrapper" id="sskru-dialog-icon-wrap">
              <i id="sskru-dialog-icon" class="fa-solid fa-circle-question"></i>
            </div>
            <h3 class="sskru-dialog-title" id="sskru-dialog-title"></h3>
            <p class="sskru-dialog-message" id="sskru-dialog-message"></p>
            <div class="sskru-dialog-actions" id="sskru-dialog-actions">
              <button type="button" class="sskru-dialog-btn sskru-dialog-btn-cancel" id="sskru-dialog-btn-cancel">ยกเลิก</button>
              <button type="button" class="sskru-dialog-btn sskru-dialog-btn-confirm" id="sskru-dialog-btn-confirm">ตกลง</button>
            </div>
          </div>
        `;
        document.body.appendChild(backdrop);
      }

      const iconWrap = backdrop.querySelector('#sskru-dialog-icon-wrap');
      const iconEl = backdrop.querySelector('#sskru-dialog-icon');
      const titleEl = backdrop.querySelector('#sskru-dialog-title');
      const msgEl = backdrop.querySelector('#sskru-dialog-message');
      const cancelBtn = backdrop.querySelector('#sskru-dialog-btn-cancel');
      const confirmBtn = backdrop.querySelector('#sskru-dialog-btn-confirm');

      iconWrap.className = `sskru-dialog-icon-wrapper ${type}`;
      iconEl.className = `fa-solid ${icon}`;
      titleEl.textContent = title;
      msgEl.textContent = message;
      cancelBtn.textContent = cancelText;
      confirmBtn.textContent = confirmText;

      if (type === 'danger' || type === 'error') {
        confirmBtn.className = 'sskru-dialog-btn sskru-dialog-btn-confirm danger';
      } else if (type === 'success') {
        confirmBtn.className = 'sskru-dialog-btn sskru-dialog-btn-confirm success';
      } else {
        confirmBtn.className = 'sskru-dialog-btn sskru-dialog-btn-confirm';
      }

      backdrop.style.display = 'flex';
      requestAnimationFrame(() => backdrop.classList.add('open'));

      const closeDialog = (result) => {
        backdrop.classList.remove('open');
        setTimeout(() => {
          backdrop.style.display = 'none';
          resolve(result);
        }, 250);
      };

      cancelBtn.onclick = () => closeDialog(false);
      confirmBtn.onclick = () => closeDialog(true);
      backdrop.onclick = (e) => {
        if (e.target === backdrop) closeDialog(false);
      };
    });
  };

  // 4. Fallback override for any direct alert() call
  window.alert = function(message) {
    let type = 'info';
    let title = 'แจ้งเตือน';
    if (typeof message === 'string') {
      if (message.includes('สำเร็จ') || message.includes('🎉')) {
        type = 'success';
        title = 'ทำรายการสำเร็จ';
      } else if (message.includes('ไม่สำเร็จ') || message.includes('ผิดพลาด') || message.includes('ไม่ถูกต้อง') || message.includes('หมดอายุ')) {
        type = 'error';
        title = 'แจ้งเตือนข้อผิดพลาด';
      } else if (message.includes('กรุณา') || message.includes('ตรวจสอบ') || message.includes('ซ้ำ')) {
        type = 'warning';
        title = 'โปรดตรวจสอบข้อมูล';
      }
    }
    return window.showSskruAlert({ title, message: String(message), type });
  };
})();

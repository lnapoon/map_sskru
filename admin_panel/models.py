from django.db import models

class VisitorLog(models.Model):
    """บันทึกผู้เข้าชมเว็บไซต์"""
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, default='unknown')  # mobile, desktop, tablet
    os_name = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    page_path = models.CharField(max_length=255, default='/')
    referrer = models.URLField(max_length=500, blank=True, null=True)
    session_id = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'ผู้เข้าชม'
        verbose_name_plural = 'ผู้เข้าชมทั้งหมด'

    def __str__(self):
        return f"{self.ip_address} - {self.device_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class UserEvent(models.Model):
    """บันทึก event การใช้งาน (ค้นหา, นำทาง ฯลฯ)"""
    EVENT_TYPES = [
        ('page_view', 'เปิดหน้าแผนที่'),
        ('building_select', 'เลือกอาคาร'),
        ('search', 'ค้นหาอาคาร'),
        ('navigate', 'กดนำทาง'),
        ('gps_track', 'ขอตำแหน่ง GPS'),
        ('share', 'แชร์อาคาร'),
    ]
    visitor = models.ForeignKey(VisitorLog, on_delete=models.SET_NULL, null=True, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    event_data = models.CharField(max_length=255, blank=True)  # e.g. building name, search query
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event_type}: {self.event_data}"


class AdminSession(models.Model):
    """จัดการ session ของ admin"""
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.token[:16]}... (active={self.is_active})"


class Student(models.Model):
    """ข้อมูลนักศึกษาสำหรับเข้าสู่ระบบแผนที่"""
    student_id = models.CharField(max_length=20, unique=True, verbose_name="รหัสนักศึกษา")
    name = models.CharField(max_length=255, verbose_name="ชื่อ-นามสกุล")
    year_level = models.PositiveIntegerField(default=2, verbose_name="ชั้นปี")
    is_active = models.BooleanField(default=True, verbose_name="สถานะใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'นักศึกษา'
        verbose_name_plural = 'นักศึกษาทั้งหมด'

    def __str__(self):
        return f"{self.student_id} - {self.name}"

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
    password_hash = models.CharField(max_length=128, blank=True, null=True, verbose_name="รหัสผ่าน (Hash)")
    password_plain = models.CharField(max_length=128, blank=True, null=True, verbose_name="รหัสผ่าน (Plain)")
    is_active = models.BooleanField(default=True, verbose_name="สถานะใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'นักศึกษา'
        verbose_name_plural = 'นักศึกษาทั้งหมด'

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class StaffUser(models.Model):
    """ข้อมูลบุคลากรและอาจารย์"""
    username = models.CharField(max_length=100, unique=True, verbose_name="ชื่อผู้ใช้")
    email = models.EmailField(unique=True, verbose_name="อีเมล")
    password_hash = models.CharField(max_length=128, verbose_name="รหัสผ่าน (Hash)")
    password_plain = models.CharField(max_length=128, blank=True, null=True, verbose_name="รหัสผ่าน (Plain)")
    is_active = models.BooleanField(default=True, verbose_name="สถานะใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'บุคลากร'
        verbose_name_plural = 'บุคลากรทั้งหมด'

    def __str__(self):
        return f"{self.username} ({self.email})"


class PasswordResetToken(models.Model):
    """บันทึก Token และ OTP สำหรับรีเซ็ตรหัสผ่าน"""
    user_type = models.CharField(max_length=20, default='student')  # student / staff
    identifier = models.CharField(max_length=100)  # student_id or username
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    otp = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reset {self.user_type}:{self.identifier} ({'used' if self.used else 'active'})"


class Building(models.Model):
    """ข้อมูลอาคารและสถานที่บนแผนที่มหาวิทยาลัย"""
    building_id = models.IntegerField(unique=True, verbose_name="รหัสอาคาร")
    name = models.CharField(max_length=255, verbose_name="ชื่ออาคาร (ไทย)")
    name_en = models.CharField(max_length=255, blank=True, verbose_name="ชื่ออาคาร (อังกฤษ)")
    category = models.CharField(max_length=50, default="academic", verbose_name="หมวดหมู่")
    code = models.CharField(max_length=50, blank=True, verbose_name="รหัสย่อ")
    coord_x = models.FloatField(default=0, verbose_name="พิกัดแผนที่ X")
    coord_y = models.FloatField(default=0, verbose_name="พิกัดแผนที่ Y")
    lat = models.FloatField(null=True, blank=True, verbose_name="Latitude GPS")
    lng = models.FloatField(null=True, blank=True, verbose_name="Longitude GPS")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    phone = models.CharField(max_length=100, blank=True, verbose_name="เบอร์โทร")
    tags = models.JSONField(default=list, blank=True, verbose_name="แท็กค้นหา")
    image = models.CharField(max_length=500, blank=True, null=True, verbose_name="รูปภาพอาคาร")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['building_id']
        verbose_name = 'อาคาร'
        verbose_name_plural = 'อาคารทั้งหมด'

    def __str__(self):
        return f"[{self.building_id}] {self.name}"


class UserActivityLog(models.Model):
    """บันทึกประวัติการเข้าใช้งานและกิจกรรมของผู้ใช้ (Students, Staff, Admin)"""
    user_id = models.CharField(max_length=100, verbose_name="รหัสผู้ใช้")
    user_name = models.CharField(max_length=255, verbose_name="ชื่อผู้ใช้")
    role = models.CharField(max_length=50, verbose_name="บทบาท")
    email = models.CharField(max_length=255, blank=True, verbose_name="อีเมล")
    ip_address = models.CharField(max_length=100, blank=True, verbose_name="IP Address")
    device = models.CharField(max_length=255, blank=True, verbose_name="อุปกรณ์")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="วันเวลา")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'ประวัติกิจกรรมผู้ใช้'
        verbose_name_plural = 'ประวัติกิจกรรมผู้ใช้ทั้งหมด'

    def __str__(self):
        return f"{self.user_name} ({self.role}) - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"



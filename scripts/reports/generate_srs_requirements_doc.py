#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate the Software Requirements Specification (SRS) Document
for SSKRU Campus Map & Smart Navigation System.
Output: docs/SSKRU_Campus_Map_Requirements.docx
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def set_font_run(run, font_name="Angsana New", size_pt=16, bold=False, italic=False, color_rgb=None):
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)
    
    if size_pt:
        run.font.size = Pt(size_pt)
    if bold:
        run.font.bold = True
    if italic:
        run.font.italic = True
    if color_rgb:
        run.font.color.rgb = color_rgb

def add_p(doc, text="", font_name="Angsana New", size_pt=16, bold=False, italic=False, align=None, 
          space_before=0, space_after=2, indent=False, color_rgb=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    if space_before:
        p.paragraph_format.space_before = Pt(space_before)
    if space_after:
        p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        set_font_run(run, font_name, size_pt, bold, italic, color_rgb)
    return p

def add_heading_1(doc, text):
    p = add_p(doc, text, font_name="Angsana New", size_pt=20, bold=True, space_before=14, space_after=6,
              color_rgb=RGBColor(13, 44, 94)) # Primary Dark Blue
    return p

def add_heading_2(doc, text):
    p = add_p(doc, text, font_name="Angsana New", size_pt=18, bold=True, space_before=10, space_after=4,
              color_rgb=RGBColor(26, 79, 160)) # Primary Blue
    return p

def add_heading_3(doc, text):
    p = add_p(doc, text, font_name="Angsana New", size_pt=16, bold=True, space_before=6, space_after=2,
              color_rgb=RGBColor(30, 41, 59))
    return p

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_styled_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], "1A4FA0") # Deep Blue Header
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            set_font_run(run, font_name="Angsana New", size_pt=15, bold=True, color_rgb=RGBColor(255, 255, 255))
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            if bg_color != "FFFFFF":
                set_cell_background(row_cells[col_idx], bg_color)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            # Align center for short IDs, left for descriptions
            if col_idx == 0 or (len(str(cell_value)) <= 10 and "\n" not in str(cell_value)):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                set_font_run(run, font_name="Angsana New", size_pt=15, bold=(col_idx == 0))
            row_cells[col_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Set Widths
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    # Space after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)
    return table

def build_srs_document():
    doc = Document()

    # Standard A4 Margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # ═════════════════════════════════════════════════════════════════════════
    # 1. หน้าปก (COVER PAGE)
    # ═════════════════════════════════════════════════════════════════════════
    logo_path = os.path.join(BASE_DIR, "images", "image1.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(14)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.25))

    add_p(doc, "เอกสารข้อกำหนดความต้องการของระบบ", font_name="Angsana New", size_pt=26, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "(Software Requirements Specification: SRS)", font_name="Angsana New", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "เรื่อง ระบบแผนผังดิจิทัลและระบบนำทางอัจฉริยะ มหาวิทยาลัยราชภัฏศรีสะเกษ", font_name="Angsana New", size_pt=24, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "(SSKRU Campus Map & Smart Navigation System)", font_name="Angsana New", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=28)

    add_p(doc, "จัดทำโดย", font_name="Angsana New", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "นายมนต์พระกาฬ ทิมเกิด  รหัสนักศึกษา 6712732120", font_name="Angsana New", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

    add_p(doc, "เสนอ", font_name="Angsana New", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "ผู้ช่วยศาสตราจารย์ ดร.กนิษฐา อินธิชิต", font_name="Angsana New", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=32)

    add_p(doc, "รายงานนี้เป็นส่วนหนึ่งของรายวิชาระบบฐานข้อมูล ( 4123202 )", font_name="Angsana New", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "ภาคเรียนที่ 2 ปีการศึกษา 2568", font_name="Angsana New", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "สาขาวิทยาการคอมพิวเตอร์ คณะศิลปศาสตร์และวิทยาศาสตร์", font_name="Angsana New", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "มหาวิทยาลัยราชภัฏศรีสะเกษ", font_name="Angsana New", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 2. สารบัญ (TABLE OF CONTENTS)
    # ═════════════════════════════════════════════════════════════════════════
    add_p(doc, "สารบัญ (Table of Contents)", font_name="Angsana New", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

    toc_items = [
        ("บทที่ 1: บทนำและภาพรวมของระบบ (Introduction & Overview)", "1"),
        ("     1.1 ความเป็นมาและความสำคัญ", "1"),
        ("     1.2 วัตถุประสงค์ของระบบ", "1"),
        ("     1.3 ขอบเขตของระบบ (System Scope)", "2"),
        ("     1.4 บทบาทและกลุ่มผู้ใช้งาน (User Roles & Personas)", "2"),
        ("บทที่ 2: ข้อกำหนดความต้องการเชิงฟังก์ชัน (Functional Requirements - FR)", "4"),
        ("     2.1 หมวดการแสดงผลแผนที่และควบคุมมุมมอง (Map Visualization)", "4"),
        ("     2.2 หมวดการสืบค้นและคัดกรองสถานที่ (Search & Filtering)", "5"),
        ("     2.3 หมวดระบุพิกัดและการนำทาง (GPS Tracking & Routing)", "6"),
        ("     2.4 หมวดการยืนยันตัวตนและการจัดการสิทธิ์ (Authentication & Roles)", "7"),
        ("     2.5 หมวดโปรไฟล์และการคุ้มครองข้อมูลส่วนบุคคล (Profile & PDPA)", "9"),
        ("     2.6 หมวดจัดการข้อมูลสำหรับผู้ดูแลระบบ (Admin CMS & Drag-Drop)", "10"),
        ("     2.7 หมวดการแสดงผลและประสบการณ์ผู้ใช้ (UI/UX & PWA)", "12"),
        ("บทที่ 3: ข้อกำหนดความต้องการเชิงคุณภาพ (Non-Functional Requirements - NFR)", "13"),
        ("     3.1 ด้านประสิทธิภาพและความรวดเร็ว (Performance Requirements)", "13"),
        ("     3.2 ด้านความมั่นคงปลอดภัย (Security Requirements)", "14"),
        ("     3.3 ด้านความน่าเชื่อถือและความพร้อมใช้งาน (Reliability & Availability)", "15"),
        ("     3.4 ด้านการใช้งานและการเข้าถึง (Usability & Accessibility)", "15"),
        ("     3.5 ด้านความเข้ากันได้และการติดตั้ง (Compatibility & PWA)", "16"),
        ("บทที่ 4: สถาปัตยกรรมและโครงสร้างข้อมูล (Architecture & Data Dictionary)", "17"),
        ("     4.1 สถาปัตยกรรมระบบ Dual-Stack (PHP & Django)", "17"),
        ("     4.2 แผนภาพความสัมพันธ์ของข้อมูล (E-R Diagram)", "18"),
        ("     4.3 พจนานุกรมข้อมูล (Data Dictionary 8 ตาราง)", "19"),
        ("บทที่ 5: กรณีการใช้งานและการดำเนินงานของผู้ใช้ (Use Case Specifications)", "23"),
        ("     5.1 กรณีการใช้งานของผู้เยี่ยมชมทั่วไป (Guest User Journey)", "23"),
        ("     5.2 กรณีการใช้งานของนักศึกษา (Student User Journey)", "24"),
        ("     5.3 กรณีการใช้งานของบุคลากร (Staff User Journey)", "25"),
        ("     5.4 กรณีการใช้งานของผู้ดูแลระบบ (Admin User Journey)", "26"),
        ("บทที่ 6: เกณฑ์การยอมรับและการส่งมอบงาน (Acceptance Criteria & Traceability)", "27")
    ]

    for title, page_num in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.15
        p_toc.paragraph_format.space_after = Pt(2)
        r_title = p_toc.add_run(title)
        set_font_run(r_title, font_name="Angsana New", size_pt=16, bold=title.startswith("บทที่"))

        total_width = 80
        title_len = len(title)
        dots_count = max(4, total_width - title_len - len(page_num) * 2)
        r_dots = p_toc.add_run(" " + "." * dots_count + " ")
        set_font_run(r_dots, font_name="Angsana New", size_pt=14, bold=False, color_rgb=RGBColor(160, 174, 192))

        r_page = p_toc.add_run(page_num)
        set_font_run(r_page, font_name="Angsana New", size_pt=16, bold=True)

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 1: บทนำและภาพรวมของระบบ
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 1: บทนำและภาพรวมของระบบ (Introduction & System Overview)")

    add_heading_2(doc, "1.1 ความเป็นมาและความสำคัญ (Background & Rationale)")
    add_p(doc, "มหาวิทยาลัยราชภัฏศรีสะเกษ (SSKRU) เป็นสถาบันอุดมศึกษาที่มีพื้นที่วิทยาเขตกว้างขวาง ประกอบด้วยอาคารเรียน คณะ หน่วยงานบริหารจัดการ ศูนย์บริการนักศึกษา หอพัก และสิ่งอำนวยความสะดวกจำนวนมาก ซึ่งในแต่ละวันมีผู้ใช้งานพื้นที่หลากหลายกลุ่ม ทั้งนักศึกษาปัจจุบัน นักศึกษาใหม่ คณาจารย์ บุคลากร รวมไปถึงบุคคลภายนอก เช่น ผู้ปกครอง คณะกรรมการ ผู้มาติดต่อราชการ และแขกผู้มีเกียรติที่เดินทางมาเยี่ยมชมมหาวิทยาลัย", indent=True)
    add_p(doc, "ปัญหาสำคัญที่พบในอดีตคือ การค้นหาตำแหน่งอาคารเรียนและห้องปฏิบัติการเป็นไปด้วยความยากลำบาก เนื่องจากป้ายบอกทางมีจำกัดและแผนที่แบบป้ายไวนิลหรือเอกสารสิ่งพิมพ์ไม่สามารถตอบสนองการระบุตำแหน่งแบบเรียลไทม์ได้ การพัฒนาระบบแผนผังดิจิทัลและระบบนำทางอัจฉริยะ (SSKRU Campus Map & Smart Navigation System) จึงถูกริเริ่มขึ้นเพื่อยกระดับมหาวิทยาลัยสู่ Smart Campus อย่างเป็นรูปธรรม", indent=True)

    add_heading_2(doc, "1.2 วัตถุประสงค์ของระบบ (System Objectives)")
    add_p(doc, "1. เพื่อพัฒนาระบบแผนผังวิทยาเขตแบบ 3D Interactive Map ที่มีความละเอียดสูง สวยงาม และใช้งานง่ายบนทุกอุปกรณ์", indent=True)
    add_p(doc, "2. เพื่อจัดให้มีระบบระบุพิกัดตำแหน่งจริงผ่านดาวเทียม GPS สด และเชื่อมต่อระบบนำทางเดินเท้าและยานพาหนะผ่าน Google Maps", indent=True)
    add_p(doc, "3. เพื่อพัฒนาระบบบริหารจัดการสิทธิ์ผู้ใช้งานแบบหลายระดับ (Multi-Role Authentication) รองรับบุคคลทั่วไป, นักศึกษา, บุคลากร และผู้ดูแลระบบ", indent=True)
    add_p(doc, "4. เพื่อจัดให้มีช่องทางการเข้าใช้งานแบบทันทีสำหรับผู้ใหญ่และบุคคลภายนอกที่เข้ามาเยี่ยมชมมหาวิทยาลัย โดยไม่ต้องมีบัญชีนักศึกษาหรือเปิดเผยข้อมูลส่วนบุคคล", indent=True)
    add_p(doc, "5. เพื่อสร้างระบบบริหารจัดการฐานข้อมูลอาคารสำหรับผู้ดูแลระบบ (Admin CMS) ที่รองรับการลากย้ายพิกัดหมุด (Drag & Drop) แบบเรียลไทม์", indent=True)

    add_heading_2(doc, "1.3 ขอบเขตของระบบ (System Scope)")
    add_p(doc, "ระบบครอบคลุมพื้นที่ทั้งหมดของมหาวิทยาลัยราชภัฏศรีสะเกษ รองรับอาคารหลักมากกว่า 40 หลัง พร้อมข้อมูลรายละเอียด ภาพถ่าย เวลาทำการ เบอร์ติดต่อ และเส้นทางคมนาคม โดยระบบถูกออกแบบให้ทำงานได้ทั้งในรูปแบบ Native PHP (MySQL) และ Python Django Framework เชื่อมโยงฐานข้อมูลแบบ Multi-Store Synchronization (SQLite3, MySQL, MongoDB Atlas และ JSON Cache)", indent=True)

    add_heading_2(doc, "1.4 บทบาทและกลุ่มผู้ใช้งาน (User Roles & Personas)")
    add_p(doc, "ระบบจำแนกผู้ใช้งานออกเป็น 4 บทบาทหลักอย่างชัดเจน เพื่อตอบสนองความต้องการและกำหนดขอบเขตความปลอดภัยของข้อมูล:", indent=True)

    roles_headers = ["บทบาท (Role)", "คำอธิบายกลุ่มเป้าหมาย", "สิทธิ์การเข้าถึงและการใช้งาน"]
    roles_data = [
        ["บุคคลทั่วไป / ผู้เยี่ยมชม\n(Guest / Visitor)",
         "ผู้ปกครอง, แขกผู้มีเกียรติ, บุคคลภายนอก และผู้ใหญ่ที่เดินทางมาติดต่อหรือเยี่ยมชมมหาวิทยาลัย",
         "• เข้าใช้งานแผนที่ได้ทันที 1 คลิกจากหน้าล็อกอิน โดยไม่ต้องกรอกรหัสผ่าน\n• ค้นหาอาคาร ดูรายละเอียด และใช้งานระบบนำทาง GPS เต็มรูปแบบ\n• ไม่สามารถเข้าถึงหรือมีข้อมูลนักศึกษา/ข้อมูลส่วนตัวใดๆ ป้องกันข้อมูลรั่วไหล"],
        ["นักศึกษา\n(Student)",
         "นักศึกษาปัจจุบันทุกชั้นปีของมหาวิทยาลัยราชภัฏศรีสะเกษ",
         "• เข้าสู่ระบบผ่านรหัสนักศึกษาและรหัสผ่าน\n• ดูแผนที่ ค้นหาห้องเรียน และใช้งานระบบนำทาง\n• จัดการโปรไฟล์ส่วนตัว คำแนะนำตัว และชื่อเล่น\n• มีระบบ Privacy Masking Shield ซ่อน/ปลดล็อคข้อมูลส่วนตัวด้วยรหัสผ่าน\n• ขอรับรหัส OTP ทางอีเมลมหาวิทยาลัยเพื่อรีเซ็ตรหัสผ่าน"],
        ["อาจารย์และบุคลากร\n(Staff / Faculty)",
         "คณาจารย์ เจ้าหน้าที่ และบุคลากรสังกัดคณะ/สำนักต่างๆ ในมหาวิทยาลัย",
         "• ลงทะเบียนบุคลากรด้วย Username และ Email ทางการ\n• เข้าสู่ระบบหลังได้รับการตรวจสอบและอนุมัติสิทธิ์จากผู้ดูแลระบบ\n• เข้าถึงข้อมูลอาคารและหน่วยงานภายใน พร้อมจัดการโปรไฟล์บุคลากร"],
        ["ผู้ดูแลระบบ\n(System Administrator)",
         "ผู้ดูแลระบบเทคโนโลยีสารสนเทศและแผนที่มหาวิทยาลัย",
         "• เข้าถึงแผงควบคุมหลัก Admin Dashboard\n• เพิ่ม ลบ แก้ไขข้อมูลอาคารและหมวดหมู่ทั้งหมด\n• ลากย้ายตำแหน่งหมุดบนแผนที่ 3D (Interactive Drag & Drop) อัปเดตพิกัดทันที\n• ตรวจสอบและอนุมัติสิทธิ์บุคลากร (Staff Approval)\n• ดูสถิติการใช้งาน Analytics และตรวจสอบ Audit Security Logs"]
    ]
    create_styled_table(doc, roles_headers, roles_data, [1.6, 2.2, 2.7])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 2: ข้อกำหนดความต้องการเชิงฟังก์ชัน (Functional Requirements - FR)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 2: ข้อกำหนดความต้องการเชิงฟังก์ชัน (Functional Requirements - FR)")
    add_p(doc, "ข้อกำหนดความต้องการเชิงฟังก์ชันระบุถึงความสามารถ คุณสมบัติ และพฤติกรรมการทำงานของระบบที่พัฒนาขึ้นทั้งหมด โดยแบ่งออกเป็น 7 หมวดหมู่หลักดังต่อไปนี้:", indent=True)

    # 2.1 Map Visualization
    add_heading_2(doc, "2.1 หมวดการแสดงผลแผนที่และควบคุมมุมมอง (Map Visualization)")
    map_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    map_data = [
        ["FR-MAP-01", "3D Interactive Canvas", "สูง (High)", "แสดงผลแผนผังจำลองวิทยาเขต 3D/2D ความละเอียดสูง รองรับการเรนเดอร์แบบ Ultra-Fast 0ms ด้วยเทคโนโลยี Local Memory Caching"],
        ["FR-MAP-02", "Map Navigation Controls", "สูง (High)", "รองรับการซูมเข้า-ออก (Zoom In/Out), การเลื่อนหน้าจอ (Pan/Drag), และปุ่มรีเซ็ตมุมมองกึ่งกลางแผนที่ (Recenter View)"],
        ["FR-MAP-03", "Custom Tile / Image Overlay", "สูง (High)", "แสดงผลเลเยอร์แผนผังแบบภาพดิจิทัลความคมชัดสูง ปรับระดับความโปร่งใสและแสดงหมุดพิกัดอาคารได้อย่างแม่นยำ"],
        ["FR-MAP-04", "Building Carousel Slider", "ปานกลาง", "แถบแสดงการ์ดรายการอาคารแบบสไลด์แนวนอนด้านล่างหน้าจอ เมื่อแตะที่การ์ด แผนที่จะเลื่อนไปยังหมุดอาคารนั้นโดยอัตโนมัติ"]
    ]
    create_styled_table(doc, map_headers, map_data, [1.2, 1.8, 1.1, 2.4])

    # 2.2 Search & Filtering
    add_heading_2(doc, "2.2 หมวดการสืบค้นและคัดกรองสถานที่ (Search & Filtering System)")
    srch_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    srch_data = [
        ["FR-SRCH-01", "Real-Time Smart Search", "สูง (High)", "ช่องค้นหาที่ประมวลผลทันทีขณะพิมพ์ (Debounced Instant Search) รองรับทั้งชื่อภาษาไทย ภาษาอังกฤษ และรหัสอาคาร"],
        ["FR-SRCH-02", "Category Filter Tabs", "สูง (High)", "ตัวกรองแยกประเภทอาคาร: ทั้งหมด, อาคารเรียน, สำนักงาน, สิ่งอำนวยความสะดวก, หอสมุด และจุดบริการ"],
        ["FR-SRCH-03", "Auto Fly-to Target", "ปานกลาง", "เมื่อเลือกผลลัพธ์การค้นหา กล้องของแผนที่จะเคลื่อนที่ (Smooth Pan & Zoom Animation) ไปยังพิกัดอาคารเป้าหมายทันที"],
        ["FR-SRCH-04", "Building Detail Modal", "สูง (High)", "เปิดแผงข้อมูลรายละเอียดอาคาร แสดงชื่อตึก, รหัส, รูปภาพ, รายละเอียดคณะ/หน่วยงาน, สถานะเปิดทำการ, เบอร์โทร และปุ่มนำทาง"]
    ]
    create_styled_table(doc, srch_headers, srch_data, [1.2, 1.8, 1.1, 2.4])

    # 2.3 GPS & Routing
    add_heading_2(doc, "2.3 หมวดระบุพิกัดและการนำทาง (GPS Tracking & Routing)")
    nav_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    nav_data = [
        ["FR-NAV-01", "Live GPS Geolocation", "สูง (High)", "ดึงพิกัดจริงจากดาวเทียม GPS ของอุปกรณ์ผู้ใช้งาน (WGS84) ผ่านเบราว์เซอร์ พร้อมแสดงเรดาร์ระบุตำแหน่งสีฟ้ากระพริบ"],
        ["FR-NAV-02", "Coordinate Transformation", "สูง (High)", "อัลกอริทึมคณิตศาสตร์แปลงพิกัดละติจูด/ลองจิจูดจริง (GPS) เข้าสู่ระบบพิกัดแกน (X, Y) ของภาพแผนผัง 3D ได้อย่างแม่นยำ"],
        ["FR-NAV-03", "Turn-by-Turn Routing", "สูง (High)", "ปุ่มกดเชื่อมต่อไปยัง Google Maps Application ส่งพิกัดอาคารปลายทางเพื่อนำทางแบบเลี้ยวต่อเลี้ยวได้ทันที"],
        ["FR-NAV-04", "Travel Mode Selector", "ปานกลาง", "รองรับการเลือกรูปแบบการเดินทาง: เดินเท้า (Walking), รถจักรยานยนต์, รถยนต์ พร้อมคำนวณระยะทางโดยประมาณ"]
    ]
    create_styled_table(doc, nav_headers, nav_data, [1.2, 1.8, 1.1, 2.4])

    # 2.4 Authentication & Role Management
    add_heading_2(doc, "2.4 หมวดการยืนยันตัวตนและการจัดการสิทธิ์ (Authentication & Roles)")
    auth_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    auth_data = [
        ["FR-AUTH-01", "Unified Role Login Portal", "สูง (High)", "หน้าต่างเข้าสู่ระบบแบบรวม รองรับการสลับแท็บระหว่าง นักศึกษา, บุคลากร และบุคคลทั่วไป"],
        ["FR-AUTH-02", "Guest Direct Access Mode", "สูง (High)", "ปุ่มทางลัดและแท็บเฉพาะสำหรับบุคคลทั่วไป/ผู้ใหญ่ที่เข้ามาเยี่ยมชม เข้าดูแผนที่ได้ทันที 1 คลิกโดยไม่ต้องล็อกอิน และไม่มีการแสดงข้อมูลนักศึกษา"],
        ["FR-AUTH-03", "Student Authentication", "สูง (High)", "เข้าสู่ระบบนักศึกษาด้วยรหัสนักศึกษาและรหัสผ่าน ตรวจสอบความถูกต้องกับบัญชีที่ลงทะเบียนและฐานข้อมูลทะเบียน Roster"],
        ["FR-AUTH-04", "Student Self-Register", "สูง (High)", "ระบบลงทะเบียนครั้งแรกสำหรับนักศึกษา ตรวจสอบเลขประจำตัวประชาชน 13 หลักตรงกับ Roster ก่อนให้ตั้งรหัสผ่าน"],
        ["FR-AUTH-05", "Staff Self-Register", "สูง (High)", "ระบบสมัครสมาชิกสำหรับบุคลากร กรอก Username, Email มหาวิทยาลัย, เบอร์โทร และตั้งรหัสผ่าน"],
        ["FR-AUTH-06", "Staff Approval Workflow", "สูง (High)", "บัญชีบุคลากรที่สมัครใหม่จะถูกพักสถานะไว้ (Pending) ต้องรอให้ผู้ดูแลระบบ (Admin) กดอนุมัติก่อนจึงจะล็อกอินได้"],
        ["FR-AUTH-07", "OTP Password Reset", "สูง (High)", "ระบบกู้คืนรหัสผ่านความปลอดภัยสูง ส่งรหัส OTP 6 หลักไปยังอีเมลมหาวิทยาลัย มีอายุ 15 นาที พร้อมระบบกันเดารหัสผ่าน"],
        ["FR-AUTH-08", "Anti-Brute Force Lockout", "สูง (High)", "ระบบป้องกันการสุ่มรหัสผ่าน หากกรอกผิดติดต่อกัน 5 ครั้ง ระบบจะระงับการล็อกอินชั่วคราวเป็นเวลา 10 นาที"]
    ]
    create_styled_table(doc, auth_headers, auth_data, [1.2, 1.8, 1.1, 2.4])

    # 2.5 Profile & Privacy Shield
    add_heading_2(doc, "2.5 หมวดโปรไฟล์และการคุ้มครองข้อมูลส่วนบุคคล (Profile & PDPA)")
    prof_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    prof_data = [
        ["FR-PROF-01", "Side Drawer Header Info", "สูง (High)", "แถบเมนูสไลด์ด้านข้าง แสดงชื่อผู้ใช้ สิทธิ์ และไอคอนสถานะ (หากเป็นผู้เยี่ยมชมจะแสดงเป็น 'ผู้เยี่ยมชมมหาวิทยาลัย')"],
        ["FR-PROF-02", "User Profile Slide Panel", "สูง (High)", "แผงแสดงข้อมูลโปรไฟล์ สิทธิประโยชน์ เวลาเข้าใช้งานล่าสุด และปุ่มออกจากระบบ"],
        ["FR-PROF-03", "Privacy Masking Shield", "สูง (High)", "ระบบคุ้มครองข้อมูลตาม พ.ร.บ. PDPA ทำการพรางชื่อจริง รหัสนักศึกษา และอีเมลเป็นเครื่องหมายจุดไข่ปลา (••••••••) โดยอัตโนมัติ"],
        ["FR-PROF-04", "Password Privacy Unlock", "สูง (High)", "ผู้ใช้งานต้องกรอกรหัสผ่านเพื่อปลดล็อคดูข้อมูลส่วนบุคคลจริง และสามารถกดซ่อนข้อมูลกลับได้ตลอดเวลา"],
        ["FR-PROF-05", "Guest Profile Isolation", "สูง (High)", "ในโหมดผู้เยี่ยมชม ระบบจะซ่อนฟอร์มแก้ไข Bio นักศึกษา ซ่อนปุ่มปลดล็อค และแสดงข้อมูลระบุตัวตนเป็นบุคคลทั่วไปอย่างสมบูรณ์"],
        ["FR-PROF-06", "PDPA Consent Banner", "สูง (High)", "กล่องข้อความขอความยินยอมในการเข้าถึงพิกัด GPS และการประมวลผลข้อมูลตามมาตรฐานกฎหมายความปลอดภัย"]
    ]
    create_styled_table(doc, prof_headers, prof_data, [1.2, 1.8, 1.1, 2.4])

    # 2.6 Admin CMS & Drag-Drop
    add_heading_2(doc, "2.6 หมวดจัดการข้อมูลสำหรับผู้ดูแลระบบ (Admin CMS & Drag-Drop)")
    adm_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    adm_data = [
        ["FR-ADM-01", "Admin Management Dashboard", "สูง (High)", "หน้าต่างภาพรวมสถิติจำนวนอาคาร, สถิติการเข้าชม, การค้นหา, กิจกรรมยอดนิยม และรายชื่อบุคลากรที่รอการอนุมัติ"],
        ["FR-ADM-02", "Building CRUD Operations", "สูง (High)", "ความสามารถในการเพิ่มอาคารใหม่, แก้ไขชื่ออาคาร, คำอธิบาย, รูปภาพ, เบอร์โทร และการลบอาคารที่ไม่ใช้งาน"],
        ["FR-ADM-03", "Interactive Drag & Drop Marker", "สูง (High)", "ผู้ดูแลระบบสามารถคลิกและลากหมุดบนแผนที่ 3D เพื่อปรับเปลี่ยนตำแหน่งอาคารได้ทันที โดยระบบจะบันทึกพิกัดใหม่แบบเรียลไทม์"],
        ["FR-ADM-04", "Multi-Store Auto Sync", "สูง (High)", "การแก้ไขข้อมูลอาคารจะถูกซิงค์ไปยัง data/buildings.json, SQLite3, MySQL (phpMyAdmin) และ MongoDB Atlas โดยอัตโนมัติ"],
        ["FR-ADM-05", "User & Staff Management", "สูง (High)", "ระบบค้นหาบัญชีนักศึกษา การจัดการบัญชีบุคลากร การกดอนุมัติ (Approve) หรือระงับสิทธิ์การใช้งาน (Suspend)"],
        ["FR-ADM-06", "Audit & Security Logs", "สูง (High)", "ระบบบันทึกประวัติการเข้าใช้งาน กิจกรรมสำคัญ และการกระทำของผู้ดูแลระบบ เพื่อการตรวจสอบย้อนหลัง (Audit Trail)"]
    ]
    create_styled_table(doc, adm_headers, adm_data, [1.2, 1.8, 1.1, 2.4])

    # 2.7 UI/UX & PWA
    add_heading_2(doc, "2.7 หมวดการแสดงผลและประสบการณ์ผู้ใช้ (UI/UX & PWA)")
    ui_headers = ["รหัส (ID)", "ชื่อฟังก์ชัน", "ความสำคัญ", "รายละเอียดการทำงาน"]
    ui_data = [
        ["FR-UI-01", "Dark / Light Mode Toggle", "ปานกลาง", "ปุ่มสลับธีมสีของส่วนติดต่อผู้ใช้ระหว่างโหมดสว่างและโหมดมืด โดยจดจำการตั้งค่าไว้ใน LocalStorage"],
        ["FR-UI-02", "Responsive Mobile-First", "สูง (High)", "การจัดวางหน้าจอที่ยืดหยุ่น รองรับทั้งสมาร์ตโฟน แท็บเล็ต และคอมพิวเตอร์เดสก์ท็อปอย่างสมบูรณ์แบบ"],
        ["FR-UI-03", "Progressive Web App (PWA)", "ปานกลาง", "รองรับการติดตั้งลงบนหน้าจอหลักของสมาร์ตโฟน (Add to Home Screen) มี Service Worker แคชไฟล์สำหรับโหลดแบบออฟไลน์"]
    ]
    create_styled_table(doc, ui_headers, ui_data, [1.2, 1.8, 1.1, 2.4])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 3: ข้อกำหนดความต้องการเชิงคุณภาพ (NFR)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 3: ข้อกำหนดความต้องการเชิงคุณภาพ (Non-Functional Requirements - NFR)")
    add_p(doc, "ข้อกำหนดความต้องการเชิงคุณภาพกำหนดเกณฑ์มาตรฐานด้านประสิทธิภาพ ความมั่นคงปลอดภัย และคุณภาพโดยรวมของระบบ เพื่อให้มั่นใจว่าระบบสามารถรองรับการใช้งานได้อย่างมีเสถียรภาพ:", indent=True)

    nfr_headers = ["หมวดหมู่ (Category)", "รหัส (ID)", "เกณฑ์มาตรฐานและข้อกำหนดเชิงคุณภาพ"]
    nfr_data = [
        ["1. ประสิทธิภาพ\n(Performance)", "NFR-PERF-01", "เวลาตอบสนองในการโหลดหน้าแรก (Initial Page Load) ต้องไม่เกิน 1.5 วินาที บนเครือข่ายอินเทอร์เน็ตความเร็วปกติ"],
        ["1. ประสิทธิภาพ\n(Performance)", "NFR-PERF-02", "การเรนเดอร์ข้อมูลอาคารจาก Local Cache ต้องใช้เวลา 0 มิลลิวินาที (Instant Render) เพื่อประสบการณ์การใช้งานที่ลื่นไหล"],
        ["1. ประสิทธิภาพ\n(Performance)", "NFR-PERF-03", "การค้นหาข้อมูลอาคารแบบเรียลไทม์ (Search Query) ต้องแสดงผลลัพธ์ภายใน 200 มิลลิวินาที"],
        ["2. ความปลอดภัย\n(Security)", "NFR-SEC-01", "รหัสผ่านของผู้ใช้งานทุกคนต้องถูกเข้ารหัสทางเดียวด้วยอัลกอริทึม SHA-256 หรือ Bcrypt ก่อนจัดเก็บลงฐานข้อมูล"],
        ["2. ความปลอดภัย\n(Security)", "NFR-SEC-02", "ระบบต้องป้องกันการโจมตีแบบ Brute Force Attack โดยมีกลไกล็อกบัญชีชั่วคราวหลังกรอกรหัสผิด 5 ครั้ง"],
        ["2. ความปลอดภัย\n(Security)", "NFR-SEC-03", "ป้องกันช่องโหว่ความปลอดภัยมาตรฐาน OWASP Top 10 เช่น SQL Injection, XSS (Cross-Site Scripting) และ CSRF Token"],
        ["2. ความปลอดภัย\n(Security)", "NFR-SEC-04", "ปฏิบัติตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 (PDPA) มีการพรางข้อมูล (Data Masking) และขอความยินยอมเข้าถึงพิกัด GPS"],
        ["3. ความน่าเชื่อถือ\n(Reliability)", "NFR-REL-01", "ระบบต้องมีความพร้อมใช้งาน (System Availability / Uptime) ไม่น้อยกว่าร้อยละ 99.5"],
        ["3. ความน่าเชื่อถือ\n(Reliability)", "NFR-REL-02", "ระบบฐานข้อมูลมีกลไก Multi-Store Fallback หากฐานข้อมูลหลักมีปัญหา สามารถอ่านข้อมูลสำรองจาก JSON Cache ได้อย่างต่อเนื่อง"],
        ["4. ความเข้ากันได้\n(Compatibility)", "NFR-COMP-01", "รองรับการทำงานบนเว็บเบราว์เซอร์มาตรฐานสากล ได้แก่ Google Chrome, Apple Safari, Microsoft Edge, Mozilla Firefox และ Opera"],
        ["4. ความเข้ากันได้\n(Compatibility)", "NFR-COMP-02", "รองรับการแสดงผล Responsive บนระบบปฏิบัติการ Android, iOS, iPadOS, Windows และ macOS"],
        ["5. การบำรุงรักษา\n(Maintainability)", "NFR-MAINT-01", "โครงสร้างซอร์สโค้ดถูกออกแบบตามหลัก Modular Design แยกส่วน Frontend, Backend API และ Database เพื่อให้ง่ายต่อการปรับปรุงในอนาคต"]
    ]
    create_styled_table(doc, nfr_headers, nfr_data, [1.5, 1.2, 3.8])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 4: สถาปัตยกรรมและโครงสร้างข้อมูล (Architecture & Data Dictionary)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 4: สถาปัตยกรรมและโครงสร้างข้อมูล (Architecture & Data Requirements)")

    add_heading_2(doc, "4.1 สถาปัตยกรรมการทำงานแบบ Dual-Stack Hybrid")
    add_p(doc, "ระบบถูกออกแบบด้วยสถาปัตยกรรมแบบ Dual-Stack เพื่อความยืดหยุ่นในการติดตั้งและใช้งานในสภาพแวดล้อมที่หลากหลาย:", indent=True)
    add_p(doc, "• Stack ที่ 1: Native PHP & MySQL — เหมาะสำหรับการโฮสต์บนเซิร์ฟเวอร์เว็บมาตรฐาน เช่น Apache, Nginx, XAMPP และ phpMyAdmin ประมวลผลรวดเร็วและใช้ทรัพยากรน้อย", indent=True)
    add_p(doc, "• Stack ที่ 2: Python Django Framework — เหมาะสำหรับระบบแบ็กเอนด์ระดับองค์กร รองรับ ORM, Django Admin, REST API และ SQLite3/PostgreSQL", indent=True)
    add_p(doc, "• ส่วนติดต่อผู้ใช้ (Frontend): สร้างขึ้นด้วย Vanilla HTML5, CSS3, JavaScript (ES6+), Leaflet.js และ FontAwesome โดยไม่พึ่งพา Framework หนักๆ ทำให้ดาวน์โหลดหน้าเว็บได้รวดเร็ว", indent=True)

    add_heading_2(doc, "4.2 แผนภาพความสัมพันธ์ของข้อมูล (E-R Diagram)")
    add_p(doc, "ระบบฐานข้อมูลประกอบด้วย 8 เอนทิตีหลักที่มีความสัมพันธ์เชื่อมโยงกันอย่างสมบูรณ์แบบ (Normalized Relational Database Design):", indent=True)

    erd_img = os.path.join(BASE_DIR, "images", "er_diagram_hd.png")
    if os.path.exists(erd_img):
        p_erd = doc.add_paragraph()
        p_erd.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_erd.paragraph_format.space_before = Pt(4)
        p_erd.paragraph_format.space_after = Pt(8)
        run_erd = p_erd.add_run()
        run_erd.add_picture(erd_img, width=Inches(6.4))
        p_erd_caption = doc.add_paragraph()
        p_erd_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_erd_caption.add_run("รูปที่ 4.1 แผนภาพความสัมพันธ์ของข้อมูล (Complete Connected E-R Diagram)")
        set_font_run(r_cap, font_name="Angsana New", size_pt=14, bold=True, italic=True)

    add_heading_2(doc, "4.3 พจนานุกรมข้อมูล (Data Dictionary 8 ตารางหลัก)")
    add_p(doc, "ตารางข้อมูลทั้ง 8 ตารางที่ใช้งานจริงในระบบ มีรายละเอียดโครงสร้างฟิลด์ ชนิดข้อมูล และข้อจำกัด (Constraints) ดังนี้:", indent=True)

    # Table 1: buildings
    add_heading_3(doc, "1) ตาราง buildings (ข้อมูลอาคารและสถานที่)")
    bldg_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    bldg_data = [
        ["id", "INT", "PK, AI", "รหัสประจำตัวอาคาร (Primary Key อัตโนมัติ)"],
        ["code", "VARCHAR(50)", "INDEX", "รหัสอาคารของมหาวิทยาลัย (เช่น B1, B2)"],
        ["name", "VARCHAR(255)", "NOT NULL", "ชื่ออาคารภาษาไทย"],
        ["nameEn", "VARCHAR(255)", "NULL", "ชื่ออาคารภาษาอังกฤษ"],
        ["category", "VARCHAR(50)", "NOT NULL", "หมวดหมู่อาคาร (academic, office, facility ฯลฯ)"],
        ["coords_y", "INT", "NOT NULL", "พิกัดแกน Y บนแผนผังจำลอง 3D"],
        ["coords_x", "INT", "NOT NULL", "พิกัดแกน X บนแผนผังจำลอง 3D"],
        ["real_lat", "DECIMAL(10,7)", "NOT NULL", "พิกัดละติจูดจริงของอาคาร (GPS)"],
        ["real_lng", "DECIMAL(10,7)", "NOT NULL", "พิกัดลองจิจูดจริงของอาคาร (GPS)"],
        ["description", "TEXT", "NULL", "รายละเอียดหน่วยงานและห้องปฏิบัติการภายใน"],
        ["phone", "VARCHAR(50)", "NULL", "เบอร์โทรศัพท์ติดต่อประจำอาคาร"],
        ["json_data", "LONGTEXT", "NULL", "ข้อมูลเสริมและเวลาทำการรูปแบบ JSON"]
    ]
    create_styled_table(doc, bldg_headers, bldg_data, [1.4, 1.4, 1.1, 2.6])

    # Table 2: students
    add_heading_3(doc, "2) ตาราง students (ข้อมูลบัญชีนักศึกษา)")
    stu_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    stu_data = [
        ["student_id", "VARCHAR(20)", "PK", "รหัสนักศึกษา (เช่น 6712732120)"],
        ["name", "VARCHAR(150)", "NOT NULL", "ชื่อ-นามสกุลจริงของนักศึกษา"],
        ["year", "INT", "DEFAULT 1", "ระดับชั้นปีที่กำลังศึกษา"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "รหัสผ่านที่ผ่านการแฮช SHA-256"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่ลงทะเบียนเข้าสู่ระบบ"]
    ]
    create_styled_table(doc, stu_headers, stu_data, [1.4, 1.4, 1.1, 2.6])

    # Table 3: staff_users
    add_heading_3(doc, "3) ตาราง staff_users (ข้อมูลบัญชีอาจารย์และบุคลากร)")
    staff_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    staff_data = [
        ["id", "INT", "PK, AI", "รหัสลำดับบุคลากร"],
        ["username", "VARCHAR(100)", "UNIQUE", "ชื่อผู้ใช้สำหรับเข้าสู่ระบบ"],
        ["email", "VARCHAR(150)", "UNIQUE", "อีเมลทางการของบุคลากร (@sskru.ac.th)"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "รหัสผ่านแฮชความปลอดภัย"],
        ["role", "VARCHAR(20)", "DEFAULT 'staff'", "สิทธิ์การใช้งาน (staff หรือ admin)"],
        ["is_approved", "TINYINT(1)", "DEFAULT 0", "สถานะการอนุมัติสิทธิ์ (0=รออนุมัติ, 1=อนุมัติแล้ว)"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่สมัครสมาชิก"]
    ]
    create_styled_table(doc, staff_headers, staff_data, [1.4, 1.4, 1.1, 2.6])

    # Table 4: visitor_logs
    add_heading_3(doc, "4) ตาราง visitor_logs (สถิติผู้เข้าชมเว็บไซต์)")
    vis_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    vis_data = [
        ["id", "INT", "PK, AI", "รหัสบันทึกผู้เข้าชม"],
        ["visitor_id", "VARCHAR(64)", "INDEX", "รหัสระบุผู้เข้าชม (Session / Hash ID)"],
        ["ip_address", "VARCHAR(45)", "NOT NULL", "หมายเลข IP Address ของผู้ใช้งาน"],
        ["device_type", "VARCHAR(20)", "NULL", "ประเภทอุปกรณ์ (mobile, desktop, tablet)"],
        ["browser", "VARCHAR(50)", "NULL", "เว็บเบราว์เซอร์ที่เปิดใช้งาน"],
        ["os", "VARCHAR(50)", "NULL", "ระบบปฏิบัติการของอุปกรณ์"],
        ["first_seen", "DATETIME", "DEFAULT NOW", "เวลาที่เข้าสู่ระบบครั้งแรก"],
        ["last_seen", "DATETIME", "DEFAULT NOW", "เวลาที่มีการใช้งานล่าสุด"]
    ]
    create_styled_table(doc, vis_headers, vis_data, [1.4, 1.4, 1.1, 2.6])

    # Table 5: user_events
    add_heading_3(doc, "5) ตาราง user_events (บันทึกกิจกรรมการใช้งานบนแผนที่)")
    ev_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    ev_data = [
        ["id", "INT", "PK, AI", "รหัสลำดับกิจกรรม"],
        ["visitor_id", "VARCHAR(64)", "FK, INDEX", "เชื่อมโยงไปยังผู้เข้าชมใน visitor_logs"],
        ["event_type", "VARCHAR(50)", "INDEX", "ประเภทกิจกรรม (search, select_building, navigate)"],
        ["event_data", "VARCHAR(255)", "NULL", "รายละเอียดเพิ่มเติม (เช่น รหัสอาคารที่กดดู)"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่เกิดกิจกรรมขึ้น"]
    ]
    create_styled_table(doc, ev_headers, ev_data, [1.4, 1.4, 1.1, 2.6])

    # Table 6: user_activity_logs
    add_heading_3(doc, "6) ตาราง user_activity_logs (ประวัติความปลอดภัยและการจัดการระบบ)")
    act_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    act_data = [
        ["id", "INT", "PK, AI", "รหัสประวัติการทำรายการ"],
        ["user_id", "VARCHAR(100)", "INDEX", "รหัสผู้ใช้, รหัสนักศึกษา หรือ GUEST"],
        ["user_name", "VARCHAR(150)", "NOT NULL", "ชื่อผู้ใช้ หรือชื่อนักศึกษา"],
        ["role", "VARCHAR(20)", "NOT NULL", "สิทธิ์ผู้ใช้งาน (guest, student, staff, admin)"],
        ["activity_type", "VARCHAR(50)", "NOT NULL", "ประเภทรายการ (login, logout, edit_building ฯลฯ)"],
        ["ip_address", "VARCHAR(45)", "NULL", "หมายเลข IP ของผู้ทำรายการ"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่บันทึกรายการ"]
    ]
    create_styled_table(doc, act_headers, act_data, [1.4, 1.4, 1.1, 2.6])

    # Table 7: password_reset_tokens
    add_heading_3(doc, "7) ตาราง password_reset_tokens (รหัส OTP และโทเค็นรีเซ็ตรหัสผ่าน)")
    otp_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    otp_data = [
        ["id", "INT", "PK, AI", "รหัสรายการรีเซ็ต"],
        ["identifier", "VARCHAR(100)", "INDEX", "รหัสนักศึกษา หรือ Username/Email บุคลากร"],
        ["role", "VARCHAR(20)", "NOT NULL", "ประเภทผู้ขอรีเซ็ต (student หรือ staff)"],
        ["token", "VARCHAR(64)", "UNIQUE", "รหัสลับโทเค็นความปลอดภัย (Secure Hash)"],
        ["otp_code", "VARCHAR(6)", "NOT NULL", "รหัส OTP 6 หลักที่ส่งเข้าอีเมล"],
        ["attempts", "INT", "DEFAULT 0", "จำนวนครั้งที่กรอกรหัส OTP ผิดพลาด"],
        ["expires_at", "DATETIME", "NOT NULL", "เวลาหมดอายุของรหัส OTP (15 นาที)"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่ส่งคำขอ"]
    ]
    create_styled_table(doc, otp_headers, otp_data, [1.4, 1.4, 1.1, 2.6])

    # Table 8: admin_sessions
    add_heading_3(doc, "8) ตาราง admin_sessions (เซสชันความปลอดภัยของผู้ดูแลระบบ)")
    adm_s_headers = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย (Description)"]
    adm_s_data = [
        ["id", "INT", "PK, AI", "รหัสเซสชันแอดมิน"],
        ["admin_username", "VARCHAR(100)", "INDEX", "ชื่อผู้ใช้ของผู้ดูแลระบบ"],
        ["token", "VARCHAR(64)", "UNIQUE", "Session Token รับรองความถูกต้องของผู้ดูแลระบบ"],
        ["ip_address", "VARCHAR(45)", "NOT NULL", "หมายเลข IP Address ของแอดมิน"],
        ["expires_at", "DATETIME", "NOT NULL", "เวลาหมดอายุของเซสชัน"],
        ["created_at", "DATETIME", "DEFAULT NOW", "วันและเวลาที่เข้าสู่ระบบ"]
    ]
    create_styled_table(doc, adm_s_headers, adm_s_data, [1.4, 1.4, 1.1, 2.6])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 5: กรณีการใช้งานและการดำเนินงานของผู้ใช้ (Use Case Specifications)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 5: กรณีการใช้งานและการดำเนินงานของผู้ใช้ (Use Case Specifications)")
    add_p(doc, "บทนี้อธิบายขั้นตอนการทำงานจริง (Step-by-Step User Journey) ของผู้ใช้งานแต่ละกลุ่ม โดยเน้นย้ำฟังก์ชันการเข้าใช้งานของผู้เยี่ยมชมทั่วไปที่เพิ่งพัฒนาล่าสุด:", indent=True)

    # 5.1 Guest User Journey
    add_heading_2(doc, "5.1 กรณีการใช้งาน: บุคคลทั่วไป / ผู้ใหญ่ที่เข้ามาเยี่ยมชม (Guest Visitor Journey)")
    add_p(doc, "ผู้ใช้งานกลุ่มนี้คือผู้ปกครอง แขกผู้มีเกียรติ และผู้มาติดต่อภายนอก โดยมีขั้นตอนการดำเนินงานดังนี้:", indent=True)
    add_p(doc, "1. ผู้ใช้เปิดหน้าเว็บไซต์ระบบแผนที่ หากยังไม่มีการเข้าสู่ระบบ ระบบจะแสดงหน้าต่าง Login Portal", indent=True)
    add_p(doc, "2. ที่หน้า Login Portal ผู้ใช้สามารถกดปุ่ม 'ผู้มาติดต่อ / บุคคลทั่วไป เข้าดูแผนที่ได้เลย' หรือเลือกแท็บ 'บุคคลทั่วไป' แล้วกดปุ่ม 'เข้าสู่แผนที่ทันที (สำหรับบุคคลทั่วไป)'", indent=True)
    add_p(doc, "3. ระบบจะบันทึกสถานะผู้ใช้งานเป็น Guest Mode โดยอัตโนมัติ และนำผู้ใช้เข้าสู่หน้าแผนที่ 3D ทันที โดยไม่ต้องกรอกรหัสผ่านหรือลงทะเบียนใดๆ", indent=True)
    add_p(doc, "4. ผู้ใช้สามารถพิมพ์ชื่ออาคารในช่องค้นหา เลือกหมวดหมู่อาคาร หรือกดเลื่อนแผนที่ดูตึกต่างๆ ได้อย่างอิสระ", indent=True)
    add_p(doc, "5. ผู้ใช้สามารถกดปุ่มเป้าเล็ง GPS เพื่อตรวจจับตำแหน่งปัจจุบันของตนเองบนแผนผังมหาวิทยาลัย และกดปุ่ม 'นำทาง' เพื่อเปิด Google Maps เดินทางไปยังอาคารนั้นได้", indent=True)
    add_p(doc, "6. เมื่อเปิดดูแถบเมนู (Drawer) หรือหน้าโปรไฟล์ ระบบจะแสดงสถานะเป็น 'ผู้เยี่ยมชมมหาวิทยาลัย' ข้อมูลระบุตัวตนแสดงเป็น 'บุคคลทั่วไป / ผู้ใหญ่ที่เข้ามาเยี่ยมชม' รหัสนักศึกษาแสดงเป็น 'ไม่มี' และไม่มีการบันทึกหรือเก็บข้อมูลส่วนบุคคลใดๆ ทั้งสิ้น", indent=True)
    add_p(doc, "7. เมื่อต้องการออกจากการใช้งาน สามารถกดปุ่ม 'กลับไปหน้าเข้าสู่ระบบ' เพื่อกลับสู่หน้าหลักได้อย่างสะดวก", indent=True)

    # 5.2 Student User Journey
    add_heading_2(doc, "5.2 กรณีการใช้งาน: นักศึกษา (Student User Journey)")
    add_p(doc, "1. นักศึกษาเข้าสู่ระบบด้วยรหัสนักศึกษาและรหัสผ่าน (หากเข้าใช้ครั้งแรก สามารถกด 'ลงทะเบียนครั้งแรก' เพื่อยืนยันเลขบัตรประชาชน)", indent=True)
    add_p(doc, "2. เมื่อเข้าสู่ระบบสำเร็จ แผนที่จะแสดงข้อมูลนักศึกษาบนแถบเมนูด้านข้าง", indent=True)
    add_p(doc, "3. นักศึกษาสามารถค้นหาอาคารเรียน ตึกคณะ ห้องสมุด หรือโรงอาหาร พร้อมกดนำทางด้วย GPS ไปยังห้องเรียนได้", indent=True)
    add_p(doc, "4. ในหน้าต่างโปรไฟล์ ข้อมูลชื่อจริง รหัสนักศึกษา และอีเมลจะถูกพรางด้วยม่านกำบังความปลอดภัย (Privacy Shield) หากต้องการดูข้อมูลจริง ต้องกรอกรหัสผ่านเพื่อปลดล็อค", indent=True)
    add_p(doc, "5. นักศึกษาสามารถแก้ไขคำแนะนำตัวสั้นๆ (Bio) และชื่อเล่นของตนเองเพื่อแสดงบนระบบได้", indent=True)
    add_p(doc, "6. กรณีลืมรหัสผ่าน นักศึกษาสามารถกด 'ลืมรหัสผ่าน?' เพื่อรับรหัส OTP 6 หลักทางอีเมลมหาวิทยาลัยและตั้งรหัสผ่านใหม่ได้ทันที", indent=True)

    # 5.3 Staff User Journey
    add_heading_2(doc, "5.3 กรณีการใช้งาน: อาจารย์และบุคลากร (Staff / Faculty Journey)")
    add_p(doc, "1. บุคลากรสมัครสมาชิกผ่านฟอร์ม 'สมัครสมาชิกบุคลากร' โดยระบุ Username, อีเมลทางการ และรหัสผ่าน", indent=True)
    add_p(doc, "2. ระบบจะแจ้งเตือนว่า 'อยู่ระหว่างรอการอนุมัติสิทธิ์จากผู้ดูแลระบบ'", indent=True)
    add_p(doc, "3. เมื่อผู้ดูแลระบบทำการอนุมัติสิทธิ์ บุคลากรจะสามารถล็อกอินเข้าสู่ระบบได้ตามปกติ", indent=True)
    add_p(doc, "4. บุคลากรสามารถค้นหาอาคาร ติดต่อหน่วยงานภายใน และจัดการข้อมูลส่วนตัวในระดับบุคลากรได้", indent=True)

    # 5.4 Admin User Journey
    add_heading_2(doc, "5.4 กรณีการใช้งาน: ผู้ดูแลระบบ (Admin User Journey)")
    add_p(doc, "1. ผู้ดูแลระบบเข้าสู่ระบบด้วยบัญชีแอดมินที่มีสิทธิ์ระดับสูง", indent=True)
    add_p(doc, "2. ระบบจะเปิดแถบเครื่องมือ Admin Panel ด้านล่างหน้าจอแผนที่ พร้อมปุ่มลัดเข้าสู่หน้า 'Admin Dashboard'", indent=True)
    add_p(doc, "3. ผู้ดูแลระบบสามารถคลิกที่หมุดอาคารใดๆ แล้วลากย้ายตำแหน่ง (Drag & Drop) เพื่อปรับพิกัดอาคารใหม่ได้ทันทีบนแผนผัง 3D", indent=True)
    add_p(doc, "4. ผู้ดูแลระบบสามารถกดแก้ไขข้อมูลอาคาร เพิ่มอาคารใหม่ หรือลบอาคารผ่านหน้าต่าง Admin Modal", indent=True)
    add_p(doc, "5. ในหน้า Admin Dashboard ผู้ดูแลระบบสามารถดูสถิติผู้เข้าชมแบบเรียลไทม์ ตรวจสอบประวัติการใช้งาน (Audit Logs) และกดอนุมัติสิทธิ์ให้แก่บุคลากรที่สมัครเข้ามาใหม่ได้", indent=True)

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # บทที่ 6: เกณฑ์การยอมรับและการส่งมอบงาน (Acceptance Criteria & Traceability)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_1(doc, "บทที่ 6: เกณฑ์การยอมรับและการส่งมอบงาน (Acceptance Criteria & Verification)")
    add_p(doc, "ตารางตรวจสอบความสอดคล้องของระบบ (Requirements Traceability Matrix: RTM) เพื่อยืนยันว่าการพัฒนางานทั้งหมดตรงตามข้อกำหนดความต้องการที่ตั้งไว้ครบถ้วนร้อยละ 100:", indent=True)

    rtm_headers = ["รหัสข้อกำหนด", "ชื่อฟังก์ชันการทำงาน", "ผลการทดสอบ", "สถานะการส่งมอบ"]
    rtm_data = [
        ["FR-MAP-01", "ระบบแผนผังจำลองวิทยาเขต 3D Interactive Map", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-MAP-02", "ระบบควบคุมมุมมอง ซูม เลื่อน และกึ่งกลาง", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-SRCH-01", "ระบบค้นหาอาคารอัจฉริยะแบบเรียลไทม์", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-SRCH-02", "ระบบตัวกรองหมวดหมู่อาคาร", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-NAV-01", "ระบบตรวจจับพิกัดดาวเทียมสด GPS บนแผนผัง 3D", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-NAV-03", "ระบบส่งพิกัดนำทางไปยัง Google Maps ภายนอก", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-AUTH-01", "หน้าต่างเข้าสู่ระบบแบบรวม Role-Based Login", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-AUTH-02", "โหมดผู้เยี่ยมชมทั่วไป เข้าดูแผนที่ได้ทันที 1 คลิก ไร้ข้อมูลนักศึกษา", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-AUTH-03", "ระบบเข้าสู่ระบบนักศึกษาและตรวจสอบฐานข้อมูล Roster", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-AUTH-06", "ระบบลงทะเบียนบุคลากรและ Workflow รอแอดมินอนุมัติ", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-AUTH-07", "ระบบกู้คืนรหัสผ่านความปลอดภัยสูงผ่าน OTP ทางอีเมล", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-PROF-03", "ระบบม่านพรางข้อมูลส่วนบุคคลตามมาตรฐาน PDPA", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-ADM-01", "หน้าแผงควบคุมสถิติผู้ดูแลระบบ Admin Dashboard", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-ADM-03", "ระบบลากย้ายพิกัดหมุด Interactive Drag & Drop Marker", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-ADM-04", "ระบบซิงค์ข้อมูลอัตโนมัติ Multi-Store (SQLite, MySQL, Mongo)", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-UI-01", "ระบบสลับธีม Dark Mode / Light Mode", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"],
        ["FR-UI-03", "ระบบ Progressive Web App (PWA) ติดตั้งลงมือถือได้", "ผ่าน (Pass)", "ส่งมอบสมบูรณ์ 100%"]
    ]
    create_styled_table(doc, rtm_headers, rtm_data, [1.4, 2.8, 1.1, 1.2])

    add_heading_2(doc, "สรุปผลการพัฒนาระบบ")
    add_p(doc, "ระบบแผนผังดิจิทัลและระบบนำทางอัจฉริยะ มหาวิทยาลัยราชภัฏศรีสะเกษ (SSKRU Campus Map & Smart Navigation System) ได้รับการพัฒนาและตรวจสอบข้อกำหนดความต้องการครบถ้วนทุกประการ ทั้งในส่วนของการรองรับผู้ใช้งานทุกกลุ่ม โดยเฉพาะอย่างยิ่งกลุ่มผู้ใหญ่และบุคคลภายนอกที่เข้ามาเยี่ยมชมมหาวิทยาลัย ซึ่งสามารถเข้าถึงแผนที่ได้ทันทีโดยสะดวก ปลอดภัย และไม่มีข้อมูลนักศึกษาหลุดรั่วไหล พร้อมทั้งมีระบบบริหารจัดการหลังบ้านสำหรับผู้ดูแลระบบที่มีประสิทธิภาพสูง สามารถนำไปใช้งานจริงเพื่อยกระดับมหาวิทยาลัยราชภัฏศรีสะเกษสู่ Smart Campus ได้อย่างยั่งยืน", indent=True, space_after=18)

    # Save Document
    docs_dir = os.path.join(BASE_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, "SSKRU_Campus_Map_Requirements.docx")
    doc.save(out_path)
    print(f"SUCCESS: Saved SRS Requirements Document to: {out_path}")
    return out_path

if __name__ == "__main__":
    build_srs_document()

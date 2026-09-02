import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.font_manager as fm

def setup_font():
    available = [f.name for f in fm.fontManager.ttflist]
    for font_name in ['Arial Unicode MS', 'Thonburi', 'Ayuthaya', 'Arial']:
        if font_name in available:
            plt.rcParams['font.family'] = font_name
            return font_name
    return 'sans-serif'

def draw_smart_connector(ax, pts, start_label="1", end_label="N", rel_name="", color="#1E40AF", lw=1.6):
    """
    Draw a multi-point orthogonal relationship line with Crow's Foot and relationship verb label
    pts: list of (x, y) tuples
    """
    verts = pts
    codes = [Path.MOVETO] + [Path.LINETO] * (len(pts) - 1)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', edgecolor=color, lw=lw, zorder=2, alpha=0.9)
    ax.add_patch(patch)

    # Start 1 notation
    x1, y1 = pts[0]
    ax.text(x1, y1 + 0.12, start_label, fontsize=9.5, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)

    # End Crow's Foot & N notation
    x_last, y_last = pts[-1]
    x_prev, y_prev = pts[-2]

    # Calculate crow's foot fork direction based on last segment
    dx = x_last - x_prev
    dy = y_last - y_prev

    if abs(dx) > abs(dy):
        if dx > 0: # Entering from left to right edge
            ax.plot([x_last - 0.22, x_last, x_last - 0.22], [y_last + 0.14, y_last, y_last - 0.14], color=color, lw=lw, zorder=3)
            ax.text(x_last - 0.35, y_last + 0.12, end_label, fontsize=9.5, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)
        else: # Entering from right to left edge
            ax.plot([x_last + 0.22, x_last, x_last + 0.22], [y_last + 0.14, y_last, y_last - 0.14], color=color, lw=lw, zorder=3)
            ax.text(x_last + 0.35, y_last + 0.12, end_label, fontsize=9.5, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)
    else:
        if dy > 0: # Entering upwards to bottom edge
            ax.plot([x_last - 0.14, x_last, x_last + 0.14], [y_last - 0.22, y_last, y_last - 0.22], color=color, lw=lw, zorder=3)
            ax.text(x_last + 0.2, y_last - 0.28, end_label, fontsize=9.5, fontweight='bold', color=color, ha='left', va='center', zorder=5)
        else: # Entering downwards to top edge
            ax.plot([x_last - 0.14, x_last, x_last + 0.14], [y_last + 0.22, y_last, y_last + 0.22], color=color, lw=lw, zorder=3)
            ax.text(x_last + 0.2, y_last + 0.28, end_label, fontsize=9.5, fontweight='bold', color=color, ha='left', va='center', zorder=5)

    # Relationship verb in the middle segment
    if rel_name and len(pts) >= 2:
        mid_idx = len(pts) // 2
        mx = (pts[mid_idx-1][0] + pts[mid_idx][0]) / 2
        my = (pts[mid_idx-1][1] + pts[mid_idx][1]) / 2
        
        # Pill background for text
        t_box = patches.FancyBboxPatch((mx - 0.85, my - 0.18), 1.7, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06",
                                       facecolor='#FFFFFF', edgecolor=color, lw=0.8, zorder=4)
        ax.add_patch(t_box)
        ax.text(mx, my, rel_name, fontsize=8.0, fontweight='bold', color=color, ha='center', va='center', zorder=5)

def draw_complete_erd():
    font_name = setup_font()
    print(f"Drawing complete ERD using font: {font_name}")

    fig, ax = plt.subplots(figsize=(26, 16), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    # Main Diagram Title
    ax.text(13, 15.3, "SSKRU Campus Map — Full Relational Database ER-Diagram", 
            fontsize=24, fontweight='bold', color='#0D2C5E', ha='center', va='center')
    ax.text(13, 14.8, "ผังแสดงความสัมพันธ์ของโครงสร้างฐานข้อมูลทุก Entity ครบถ้วน 100% (Entity-Relationship Model)", 
            fontsize=13.5, color='#475569', ha='center', va='center')

    # Legend / Key Guide Box
    leg_x, leg_y, leg_w, leg_h = 0.8, 14.4, 7.8, 1.0
    leg_card = patches.FancyBboxPatch((leg_x, leg_y), leg_w, leg_h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.0, zorder=3)
    ax.add_patch(leg_card)
    ax.text(leg_x + 0.25, leg_y + 0.5, "Database Keys:", fontsize=10, fontweight='bold', color='#1E293B', va='center')
    
    # PK badge
    ax.add_patch(patches.Rectangle((leg_x + 1.6, leg_y + 0.35), 0.45, 0.3, facecolor='#DC2626', edgecolor='none', zorder=4))
    ax.text(leg_x + 1.825, leg_y + 0.5, "PK", fontsize=8.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
    ax.text(leg_x + 2.15, leg_y + 0.5, "= Primary Key", fontsize=9.5, color='#475569', va='center')

    # FK badge
    ax.add_patch(patches.Rectangle((leg_x + 3.6, leg_y + 0.35), 0.45, 0.3, facecolor='#2563EB', edgecolor='none', zorder=4))
    ax.text(leg_x + 3.825, leg_y + 0.5, "FK", fontsize=8.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
    ax.text(leg_x + 4.15, leg_y + 0.5, "= Foreign Key", fontsize=9.5, color='#475569', va='center')

    # UK badge
    ax.add_patch(patches.Rectangle((leg_x + 5.6, leg_y + 0.35), 0.45, 0.3, facecolor='#059669', edgecolor='none', zorder=4))
    ax.text(leg_x + 5.825, leg_y + 0.5, "UK", fontsize=8.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
    ax.text(leg_x + 6.15, leg_y + 0.5, "= Unique Key", fontsize=9.5, color='#475569', va='center')

    # ═════════════════════════════════════════════════════════════════════════
    # ENTITIES LAYOUT (Clean Balanced Matrix)
    # ═════════════════════════════════════════════════════════════════════════
    entities = {
        "STUDENT": {
            "title": "STUDENT (ข้อมูลนักศึกษา)",
            "x": 0.8, "y": 7.8, "w": 4.6, "h": 5.4,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("student_id", "Varchar(20)", "UK"),
                ("name", "Varchar(255)", ""),
                ("year_level", "Integer", ""),
                ("password_hash", "Varchar(128)", ""),
                ("password_plain", "Varchar(128)", ""),
                ("is_active", "Boolean", ""),
                ("created_at", "DateTime", "")
            ]
        },
        "STAFF_USER": {
            "title": "STAFF_USER (บุคลากร/อาจารย์)",
            "x": 0.8, "y": 1.0, "w": 4.6, "h": 5.6,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("username", "Varchar(100)", "UK"),
                ("email", "Varchar(255)", "UK"),
                ("password_hash", "Varchar(128)", ""),
                ("password_plain", "Varchar(128)", ""),
                ("is_active", "Boolean", ""),
                ("is_approved", "Boolean", ""),
                ("created_at", "DateTime", "")
            ]
        },
        "PASSWORD_RESET_TOKEN": {
            "title": "PASSWORD_RESET_TOKEN (กู้คืนรหัส OTP)",
            "x": 6.8, "y": 7.8, "w": 5.0, "h": 5.4,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("user_type", "Varchar(20)", ""),
                ("identifier", "Varchar(100)", "FK"),
                ("email", "Varchar(255)", ""),
                ("token", "Varchar(64)", "UK"),
                ("otp", "Varchar(10)", ""),
                ("expires_at", "DateTime", ""),
                ("used", "Boolean", ""),
                ("created_at", "DateTime", "")
            ]
        },
        "USER_ACTIVITY_LOG": {
            "title": "USER_ACTIVITY_LOG (ประวัติกิจกรรม)",
            "x": 6.8, "y": 1.0, "w": 5.0, "h": 5.6,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("user_id", "Varchar(100)", "FK"),
                ("user_name", "Varchar(255)", ""),
                ("role", "Varchar(50)", ""),
                ("email", "Varchar(255)", ""),
                ("ip_address", "Varchar(100)", ""),
                ("device", "Varchar(255)", ""),
                ("timestamp", "DateTime", "")
            ]
        },
        "BUILDING": {
            "title": "BUILDING (อาคารและสถานที่)",
            "x": 13.4, "y": 6.2, "w": 5.0, "h": 7.0,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("building_id", "Integer", "UK"),
                ("name", "Varchar(255)", ""),
                ("name_en", "Varchar(255)", ""),
                ("category", "Varchar(50)", ""),
                ("code", "Varchar(50)", ""),
                ("coord_x", "Float", ""),
                ("coord_y", "Float", ""),
                ("lat", "Float", ""),
                ("lng", "Float", ""),
                ("description", "Text", ""),
                ("phone", "Varchar(100)", ""),
                ("tags", "JSON", ""),
                ("image", "Varchar(500)", ""),
                ("created_at", "DateTime", ""),
                ("updated_at", "DateTime", "")
            ]
        },
        "ADMIN_SESSION": {
            "title": "ADMIN_SESSION (เซสชันแอดมิน)",
            "x": 13.4, "y": 1.0, "w": 5.0, "h": 4.0,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("token", "Varchar(128)", "UK"),
                ("created_at", "DateTime", ""),
                ("expires_at", "DateTime", ""),
                ("is_active", "Boolean", "")
            ]
        },
        "VISITOR_LOG": {
            "title": "VISITOR_LOG (สถิติผู้เข้าชม)",
            "x": 20.0, "y": 7.8, "w": 5.0, "h": 5.4,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("ip_address", "GenericIP", ""),
                ("user_agent", "Text", ""),
                ("device_type", "Varchar(20)", ""),
                ("os_name", "Varchar(50)", ""),
                ("browser", "Varchar(50)", ""),
                ("page_path", "Varchar(255)", ""),
                ("referrer", "Varchar(500)", ""),
                ("session_id", "Varchar(64)", ""),
                ("timestamp", "DateTime", "")
            ]
        },
        "USER_EVENT": {
            "title": "USER_EVENT (กิจกรรมบนแผนที่)",
            "x": 20.0, "y": 1.0, "w": 5.0, "h": 5.6,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("visitor_id", "Integer", "FK"),
                ("event_type", "Varchar(30)", ""),
                ("event_data", "Varchar(255)", "FK"),
                ("timestamp", "DateTime", "")
            ]
        }
    }

    # Render all entity boxes
    for key_name, e in entities.items():
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        
        # Soft Drop Shadow
        shadow = patches.FancyBboxPatch((x+0.06, y-0.06), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                                        facecolor='#0F172A', alpha=0.07, edgecolor='none', zorder=1)
        ax.add_patch(shadow)

        # Entity Card Frame
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                                      facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.3, zorder=2)
        ax.add_patch(card)

        # Table Header Bar
        hdr_h = 0.65
        hdr = patches.FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, 
                                     boxstyle="round,pad=0.05,rounding_size=0.12",
                                     facecolor='#1A4FA0', edgecolor='#1A4FA0', zorder=3)
        ax.add_patch(hdr)

        # Table Header Text
        ax.text(x + w/2, y + h - hdr_h/2, e["title"],
                fontsize=11.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        # Draw Columns/Attributes
        start_y = y + h - hdr_h - 0.28
        line_step = (h - hdr_h - 0.35) / max(len(e["items"]), 1)

        for i, (col_name, col_type, col_key) in enumerate(e["items"]):
            cy = start_y - (i * line_step)
            
            # Row dividing line
            if i > 0:
                ax.plot([x + 0.1, x + w - 0.1], [cy + (line_step * 0.45), cy + (line_step * 0.45)],
                        color='#F1F5F9', lw=0.8, zorder=3)

            # Key Badges
            if col_key == "PK":
                badge = patches.FancyBboxPatch((x + 0.15, cy - 0.11), 0.42, 0.22, boxstyle="round,pad=0.02,rounding_size=0.05",
                                               facecolor='#DC2626', edgecolor='none', zorder=4)
                ax.add_patch(badge)
                ax.text(x + 0.36, cy, "PK", fontsize=8.0, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
            elif col_key == "FK":
                badge = patches.FancyBboxPatch((x + 0.15, cy - 0.11), 0.42, 0.22, boxstyle="round,pad=0.02,rounding_size=0.05",
                                               facecolor='#2563EB', edgecolor='none', zorder=4)
                ax.add_patch(badge)
                ax.text(x + 0.36, cy, "FK", fontsize=8.0, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
            elif col_key == "UK":
                badge = patches.FancyBboxPatch((x + 0.15, cy - 0.11), 0.42, 0.22, boxstyle="round,pad=0.02,rounding_size=0.05",
                                               facecolor='#059669', edgecolor='none', zorder=4)
                ax.add_patch(badge)
                ax.text(x + 0.36, cy, "UK", fontsize=8.0, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)

            # Column Name
            is_k = col_key in ['PK', 'FK', 'UK']
            name_x = x + 0.68 if col_key else x + 0.22
            ax.text(name_x, cy, col_name, fontsize=9.2, fontweight='bold' if is_k else 'normal',
                    color='#0F172A' if is_k else '#334155', ha='left', va='center', zorder=4)

            # Column Type
            ax.text(x + w - 0.18, cy, col_type, fontsize=8.5, color='#64748B', ha='right', va='center', zorder=4)

    # ═════════════════════════════════════════════════════════════════════════
    # ALL COMPREHENSIVE RELATIONSHIPS (100% Interconnected Architecture)
    # ═════════════════════════════════════════════════════════════════════════

    # 1. STUDENT ───< PASSWORD_RESET_TOKEN  (student_id -> identifier)
    draw_smart_connector(ax, 
                         pts=[(0.8 + 4.6, 7.8 + 4.2), (6.8, 7.8 + 4.2)],
                         start_label="1", end_label="N", rel_name="requests_otp", color="#2563EB")

    # 2. STAFF_USER ───< PASSWORD_RESET_TOKEN (username/email -> identifier)
    draw_smart_connector(ax, 
                         pts=[(0.8 + 4.6, 1.0 + 4.2), (5.9, 1.0 + 4.2), (5.9, 7.8 + 2.0), (6.8, 7.8 + 2.0)],
                         start_label="1", end_label="N", rel_name="requests_otp", color="#4F46E5")

    # 3. STUDENT ───< USER_ACTIVITY_LOG (student_id -> user_id)
    draw_smart_connector(ax, 
                         pts=[(0.8 + 4.6, 7.8 + 1.8), (5.6, 7.8 + 1.8), (5.6, 1.0 + 4.6), (6.8, 1.0 + 4.6)],
                         start_label="1", end_label="N", rel_name="logs_student", color="#0284C7")

    # 4. STAFF_USER ───< USER_ACTIVITY_LOG (username -> user_id)
    draw_smart_connector(ax, 
                         pts=[(0.8 + 4.6, 1.0 + 2.0), (6.8, 1.0 + 2.0)],
                         start_label="1", end_label="N", rel_name="logs_staff", color="#0D9488")

    # 5. STAFF_USER ───< ADMIN_SESSION (username -> admin_token session)
    draw_smart_connector(ax, 
                         pts=[(0.8 + 2.3, 1.0), (0.8 + 2.3, 0.3), (13.4 + 1.5, 0.3), (13.4 + 1.5, 1.0)],
                         start_label="1", end_label="N", rel_name="authenticates_admin", color="#D97706")

    # 6. ADMIN_SESSION ───< USER_ACTIVITY_LOG (admin actions recorded)
    draw_smart_connector(ax, 
                         pts=[(13.4, 1.0 + 2.0), (6.8 + 5.0, 1.0 + 2.0)],
                         start_label="1", end_label="N", rel_name="audits_admin", color="#EA580C")

    # 7. BUILDING ───< USER_EVENT (building_id -> event_data for click/navigate)
    draw_smart_connector(ax, 
                         pts=[(13.4 + 5.0, 6.2 + 3.5), (19.3, 6.2 + 3.5), (19.3, 1.0 + 4.5), (20.0, 1.0 + 4.5)],
                         start_label="1", end_label="N", rel_name="triggers_map_action", color="#059669")

    # 8. VISITOR_LOG ───< USER_EVENT (id -> visitor_id)
    draw_smart_connector(ax, 
                         pts=[(20.0 + 2.5, 7.8), (20.0 + 2.5, 1.0 + 5.6)],
                         start_label="1", end_label="N", rel_name="records_actions", color="#2563EB")

    # 9. BUILDING ───< USER_ACTIVITY_LOG (building modifications by staff/admin)
    draw_smart_connector(ax, 
                         pts=[(13.4, 6.2 + 1.5), (12.2, 6.2 + 1.5), (12.2, 1.0 + 4.0), (6.8 + 5.0, 1.0 + 4.0)],
                         start_label="1", end_label="N", rel_name="updates_building", color="#7C3AED")

    ax.set_xlim(0, 26)
    ax.set_ylim(0, 16)

    plt.tight_layout()
    output_img = "/Users/monphrakan/Mark_map/images/er_diagram_hd.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print(f"Full Connected ER Diagram generated at: {output_img}")

if __name__ == "__main__":
    draw_complete_erd()

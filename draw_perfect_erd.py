import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.font_manager as fm

def setup_font():
    # Find best available font that supports both Thai and English
    available = [f.name for f in fm.fontManager.ttflist]
    for font_name in ['Arial Unicode MS', 'Thonburi', 'Ayuthaya', 'Arial']:
        if font_name in available:
            plt.rcParams['font.family'] = font_name
            return font_name
    return 'sans-serif'

def draw_crows_foot(ax, start_pt, end_pt, start_label="1", end_label="N", color="#1E40AF"):
    """
    Draw an orthogonal connecting line with 1:N crow's foot notation
    start_pt: (x, y)
    end_pt: (x, y)
    """
    x1, y1 = start_pt
    x2, y2 = end_pt
    
    # Orthogonal midpoint
    mid_x = (x1 + x2) / 2
    
    # Path with 90-degree corners
    verts = [
        (x1, y1),
        (mid_x, y1),
        (mid_x, y2),
        (x2, y2)
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', edgecolor=color, lw=1.8, zorder=2)
    ax.add_patch(patch)
    
    # 1 notation at start (hash mark)
    ax.text(x1 + (0.15 if x2 > x1 else -0.15), y1 + 0.12, start_label, 
            fontsize=10, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)
    
    # Crow's foot at end (arrow or 3-fork)
    if x2 > mid_x: # pointing right to left edge of target
        ax.plot([x2 - 0.2, x2, x2 - 0.2], [y2 + 0.15, y2, y2 - 0.15], color=color, lw=1.8, zorder=3)
        ax.text(x2 - 0.3, y2 + 0.12, end_label, fontsize=10, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)
    elif x2 < mid_x: # pointing left to right edge of target
        ax.plot([x2 + 0.2, x2, x2 + 0.2], [y2 + 0.15, y2, y2 - 0.15], color=color, lw=1.8, zorder=3)
        ax.text(x2 + 0.3, y2 + 0.12, end_label, fontsize=10, fontweight='bold', color=color, ha='center', va='bottom', zorder=5)
    elif y2 < y1: # pointing downwards to top edge of target
        ax.plot([x2 - 0.15, x2, x2 + 0.15], [y2 + 0.2, y2, y2 + 0.2], color=color, lw=1.8, zorder=3)
        ax.text(x2 + 0.2, y2 + 0.25, end_label, fontsize=10, fontweight='bold', color=color, ha='left', va='center', zorder=5)
    else: # pointing upwards to bottom edge of target
        ax.plot([x2 - 0.15, x2, x2 + 0.15], [y2 - 0.2, y2, y2 - 0.2], color=color, lw=1.8, zorder=3)
        ax.text(x2 + 0.2, y2 - 0.25, end_label, fontsize=10, fontweight='bold', color=color, ha='left', va='center', zorder=5)

def draw_erd():
    font_name = setup_font()
    print(f"Using font: {font_name}")

    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    # Main Diagram Header
    ax.text(12, 14.3, "SSKRU Campus Map — Relational Database ER-Diagram", 
            fontsize=22, fontweight='bold', color='#0D2C5E', ha='center', va='center')
    ax.text(12, 13.8, "ผังแสดงความสัมพันธ์ของโครงสร้างฐานข้อมูลระบบแผนผังดิจิทัล มหาวิทยาลัยราชภัฏศรีสะเกษ", 
            fontsize=13, color='#64748B', ha='center', va='center')

    # Legend / Key Guide Box
    leg_x, leg_y, leg_w, leg_h = 0.8, 13.5, 6.2, 0.9
    leg_card = patches.FancyBboxPatch((leg_x, leg_y), leg_w, leg_h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.0)
    ax.add_patch(leg_card)
    ax.text(leg_x + 0.2, leg_y + 0.45, "Key Types:", fontsize=9.5, fontweight='bold', color='#334155', va='center')
    
    # PK badge in legend
    ax.add_patch(patches.Rectangle((leg_x + 1.2, leg_y + 0.3), 0.45, 0.3, facecolor='#DC2626', edgecolor='none'))
    ax.text(leg_x + 1.425, leg_y + 0.45, "PK", fontsize=8, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    ax.text(leg_x + 1.75, leg_y + 0.45, "= Primary Key", fontsize=9, color='#475569', va='center')

    # FK badge in legend
    ax.add_patch(patches.Rectangle((leg_x + 2.9, leg_y + 0.3), 0.45, 0.3, facecolor='#2563EB', edgecolor='none'))
    ax.text(leg_x + 3.125, leg_y + 0.45, "FK", fontsize=8, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    ax.text(leg_x + 3.45, leg_y + 0.45, "= Foreign Key", fontsize=9, color='#475569', va='center')

    # UK badge in legend
    ax.add_patch(patches.Rectangle((leg_x + 4.6, leg_y + 0.3), 0.45, 0.3, facecolor='#059669', edgecolor='none'))
    ax.text(leg_x + 4.825, leg_y + 0.45, "UK", fontsize=8, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    ax.text(leg_x + 5.15, leg_y + 0.45, "= Unique Key", fontsize=9, color='#475569', va='center')

    # ═════════════════════════════════════════════════════════════════════════
    # ENTITIES LAYOUT (Clean 4-column balanced architecture)
    # ═════════════════════════════════════════════════════════════════════════
    entities = {
        "STUDENT": {
            "title": "STUDENT (ข้อมูลนักศึกษา)",
            "x": 0.8, "y": 7.4, "w": 4.6, "h": 5.4,
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
            "x": 0.8, "y": 0.8, "w": 4.6, "h": 5.6,
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
            "title": "PASSWORD_RESET_TOKEN (OTP กู้รหัส)",
            "x": 6.6, "y": 7.4, "w": 4.8, "h": 5.4,
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
            "title": "USER_ACTIVITY_LOG (ประวัติล็อกอิน/กิจกรรม)",
            "x": 6.6, "y": 0.8, "w": 4.8, "h": 5.6,
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
            "x": 12.6, "y": 5.6, "w": 4.8, "h": 7.2,
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
            "x": 12.6, "y": 0.8, "w": 4.8, "h": 3.8,
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
            "x": 18.6, "y": 7.4, "w": 4.6, "h": 5.4,
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
            "x": 18.6, "y": 0.8, "w": 4.6, "h": 5.6,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("visitor_id", "Integer", "FK"),
                ("event_type", "Varchar(30)", ""),
                ("event_data", "Varchar(255)", "FK"),
                ("timestamp", "DateTime", "")
            ]
        }
    }

    # Render all entities
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
            
            # Subtle Row dividing line
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
    # RELATIONSHIP CONNECTING LINES (Clean Orthogonal Architecture)
    # ═════════════════════════════════════════════════════════════════════════
    
    # 1. VISITOR_LOG (1) ───< USER_EVENT (N)  [via visitor_id]
    draw_crows_foot(ax, 
                    start_pt=(18.6 + 2.3, 7.4), 
                    end_pt=(18.6 + 2.3, 0.8 + 5.6), 
                    start_label="1", end_label="N (visitor_id)", color="#2563EB")

    # 2. STUDENT (1) ───< PASSWORD_RESET_TOKEN (N) [via identifier]
    draw_crows_foot(ax, 
                    start_pt=(0.8 + 4.6, 7.4 + 4.0), 
                    end_pt=(6.6, 7.4 + 4.0), 
                    start_label="1", end_label="N (identifier)", color="#2563EB")

    # 3. STAFF_USER (1) ───< PASSWORD_RESET_TOKEN (N) [via identifier]
    draw_crows_foot(ax, 
                    start_pt=(0.8 + 4.6, 0.8 + 4.0), 
                    end_pt=(6.6, 7.4 + 2.0), 
                    start_label="1", end_label="N", color="#2563EB")

    # 4. STUDENT (1) ───< USER_ACTIVITY_LOG (N) [via user_id]
    draw_crows_foot(ax, 
                    start_pt=(0.8 + 4.6, 7.4 + 1.5), 
                    end_pt=(6.6, 0.8 + 4.5), 
                    start_label="1", end_label="N (user_id)", color="#2563EB")

    # 5. STAFF_USER (1) ───< USER_ACTIVITY_LOG (N) [via user_id]
    draw_crows_foot(ax, 
                    start_pt=(0.8 + 4.6, 0.8 + 2.0), 
                    end_pt=(6.6, 0.8 + 2.0), 
                    start_label="1", end_label="N (user_id)", color="#2563EB")

    # 6. BUILDING (1) ───< USER_EVENT (N) [via event_data / building_id]
    draw_crows_foot(ax, 
                    start_pt=(12.6 + 4.8, 5.6 + 3.0), 
                    end_pt=(18.6, 0.8 + 3.5), 
                    start_label="1", end_label="N (event_data)", color="#2563EB")

    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)

    plt.tight_layout()
    output_img = "/Users/monphrakan/Mark_map/images/er_diagram_hd.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print(f"High-Precision ER Diagram generated at: {output_img}")

if __name__ == "__main__":
    draw_erd()

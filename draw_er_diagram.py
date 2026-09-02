import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(20, 13), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    # Title
    ax.text(10, 12.4, "SSKRU Campus Map — Entity-Relationship Diagram (ER-Diagram)", 
            fontsize=20, fontweight='bold', color='#0D2C5E', ha='center', va='center', fontfamily='sans-serif')
    ax.text(10, 12.0, "ระบบฐานข้อมูลแผนผังดิจิทัลและระบบนำทางอัจฉริยะ มหาวิทยาลัยราชภัฏศรีสะเกษ", 
            fontsize=13, color='#64748B', ha='center', va='center', fontfamily='sans-serif')

    # Entities definitions: (title, x, y, w, h, items)
    # items: list of (name, type, key_type) -> key_type in ['PK', 'FK', 'UK', '']
    entities = [
        # Col 1 (Left)
        {
            "title": "STUDENT (นักศึกษา)",
            "x": 0.8, "y": 7.2, "w": 4.0, "h": 4.0,
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
        {
            "title": "USER_ACTIVITY_LOG (ประวัติกิจกรรม)",
            "x": 0.8, "y": 2.0, "w": 4.0, "h": 4.4,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("user_id", "Varchar(100)", ""),
                ("user_name", "Varchar(255)", ""),
                ("role", "Varchar(50)", ""),
                ("email", "Varchar(255)", ""),
                ("ip_address", "Varchar(100)", ""),
                ("device", "Varchar(255)", ""),
                ("timestamp", "DateTime", "")
            ]
        },

        # Col 2 (Middle-Left)
        {
            "title": "STAFF_USER (อาจารย์/บุคลากร)",
            "x": 5.6, "y": 7.2, "w": 4.0, "h": 4.2,
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
        {
            "title": "PASSWORD_RESET_TOKEN (OTP)",
            "x": 5.6, "y": 2.0, "w": 4.0, "h": 4.4,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("user_type", "Varchar(20)", ""),
                ("identifier", "Varchar(100)", ""),
                ("email", "Varchar(255)", ""),
                ("token", "Varchar(64)", "UK"),
                ("otp", "Varchar(10)", ""),
                ("expires_at", "DateTime", ""),
                ("used", "Boolean", ""),
                ("created_at", "DateTime", "")
            ]
        },

        # Col 3 (Middle-Right)
        {
            "title": "BUILDING (อาคารและสถานที่)",
            "x": 10.4, "y": 5.2, "w": 4.2, "h": 6.2,
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
        {
            "title": "ADMIN_SESSION (เซสชันแอดมิน)",
            "x": 10.4, "y": 1.2, "w": 4.2, "h": 3.2,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("token", "Varchar(128)", "UK"),
                ("created_at", "DateTime", ""),
                ("expires_at", "DateTime", ""),
                ("is_active", "Boolean", "")
            ]
        },

        # Col 4 (Right)
        {
            "title": "VISITOR_LOG (ผู้เข้าชมเว็บไซต์)",
            "x": 15.2, "y": 6.8, "w": 4.0, "h": 4.6,
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
        {
            "title": "USER_EVENT (กิจกรรมการใช้งาน)",
            "x": 15.2, "y": 1.6, "w": 4.0, "h": 3.8,
            "items": [
                ("id", "Integer (Auto)", "PK"),
                ("visitor_id", "Integer", "FK"),
                ("event_type", "Varchar(30)", ""),
                ("event_data", "Varchar(255)", ""),
                ("timestamp", "DateTime", "")
            ]
        }
    ]

    for e in entities:
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        
        # Shadow box
        shadow = patches.FancyBboxPatch((x+0.05, y-0.05), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor='#0F172A', alpha=0.08, edgecolor='none')
        ax.add_patch(shadow)

        # Card body
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2)
        ax.add_patch(card)

        # Header bar
        header_h = 0.55
        header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, 
                                        boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor='#1A4FA0', edgecolor='#1A4FA0')
        ax.add_patch(header)

        # Header Title
        ax.text(x + w/2, y + h - header_h/2, e["title"],
                fontsize=11, fontweight='bold', color='#FFFFFF', ha='center', va='center', fontfamily='sans-serif')

        # Attributes list
        start_y = y + h - header_h - 0.25
        line_step = (h - header_h - 0.35) / max(len(e["items"]), 1)

        for i, (name, dtype, key) in enumerate(e["items"]):
            curr_y = start_y - (i * line_step)
            
            # Key Tag badge
            if key == "PK":
                badge = patches.Rectangle((x + 0.15, curr_y - 0.08), 0.38, 0.16, facecolor='#DC2626', edgecolor='none')
                ax.add_patch(badge)
                ax.text(x + 0.34, curr_y, "PK", fontsize=7.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')
            elif key == "FK":
                badge = patches.Rectangle((x + 0.15, curr_y - 0.08), 0.38, 0.16, facecolor='#2563EB', edgecolor='none')
                ax.add_patch(badge)
                ax.text(x + 0.34, curr_y, "FK", fontsize=7.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')
            elif key == "UK":
                badge = patches.Rectangle((x + 0.15, curr_y - 0.08), 0.38, 0.16, facecolor='#059669', edgecolor='none')
                ax.add_patch(badge)
                ax.text(x + 0.34, curr_y, "UK", fontsize=7.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

            # Attribute Name
            text_x = x + 0.65 if key else x + 0.25
            is_key = key in ['PK', 'FK', 'UK']
            ax.text(text_x, curr_y, name, fontsize=8.8, fontweight='bold' if is_key else 'normal',
                    color='#0F172A' if is_key else '#334155', ha='left', va='center', fontfamily='sans-serif')

            # Data Type
            ax.text(x + w - 0.2, curr_y, dtype, fontsize=8.0, color='#64748B', ha='right', va='center', fontfamily='sans-serif')

    # Draw Relation Line: VISITOR_LOG (1) -> USER_EVENT (N)
    # Line from bottom of VISITOR_LOG to top of USER_EVENT
    vl_x = 15.2 + 2.0
    vl_y_bot = 6.8
    ue_y_top = 1.6 + 3.8
    
    ax.annotate('', xy=(vl_x, ue_y_top), xytext=(vl_x, vl_y_bot),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#2563EB', lw=2.0))
    
    # Crow's foot / 1:N label
    ax.text(vl_x + 0.15, vl_y_bot - 0.2, "1", fontsize=11, fontweight='bold', color='#2563EB')
    ax.text(vl_x + 0.15, ue_y_top + 0.2, "N (visitor_id)", fontsize=10, fontweight='bold', color='#2563EB')

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13)

    plt.tight_layout()
    output_img = "/Users/monphrakan/Mark_map/images/er_diagram_hd.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print(f"High-res ER Diagram generated at: {output_img}")

if __name__ == "__main__":
    draw_er_diagram()

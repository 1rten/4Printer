import FreeCAD as App
import Part

# ==============================================================================
# FreeCAD Python 脚本：1600x800x580mm 终极工作站 (V27.0 500mm立柱大师版: 台面604mm+双大深抽屉+双大拉盘)
# ==============================================================================
# 核心结构与装配规格：
# 1. 框架整体尺寸：1600 mm (长) × 800 mm (深) × 580 mm (高)，台面标高 604 mm (超舒适低矮工位)
# 2. 完美的上下分层全对称美学架构：
#    - 【第一层：左右并列双大深抽屉】(标高 Z=355..515 mm，外宽各 680 mm，深 550 mm，高 160 mm，净深 140 mm)：
#      • 左抽屉：位于激光机正上方，专储激光雕刻防护镜、对焦耗材、夹具零件
#      • 右抽屉：位于右下托盘正上方，专储 3D 打印铲刀、喷嘴、工具、五金配件
#      • 均为高强度 2020 铝型材内胆 + 5mm 亚克力底板
#    - 【底层：左右双超大抽拉托盘】(标高 Z=53..71 mm，宽各 700 mm，深 700 mm，配 600mm 重载楼梯滑轨)：
#      • 左托盘：承载 xTool M2 (610×569×180mm)，上方留 49mm 顺畅滑行净空，后方留 141mm 排烟通道
#      • 右托盘：超大原材料与重型耗材抽拉仓，可平放整叠 600×600mm 木板/亚克力原料、整箱纸张
# 3. 桌面三机并列旗舰系统 (Z=604 mm, 1600×800×24mm 桦木海洋板)：
#    - 左侧：LightMake L4 工业机 (615×624×677mm)，X=40..655, 顶高 1281 mm (轻松俯视热床)
#    - 中间：佳能 MF113w 激光一体机 (372×320×255mm)，X=727..1099，后靠摆放，顶高 859 mm，坐姿顺手拿取
#    - 右侧：Bambu Lab P1S (389×389×457mm) + 顶置 AMS (368×271×224mm)，X=1171..1560，顶高 1285 mm (胸前舒适区)
#    - 黄金对称间距：L4 与 佳能、佳能 与 P1S 之间间距均为 72.0 mm
#    - 前沿纯净作业带：佳能与 P1S 正前方形成长达 833 mm、深 350~400 mm 的平整电脑与手工操作台
# 4. 全要素物理连接件：红角码(16)、青穿芯(12)、紫锚钉(6)、银白桌面平扣(8)
#    - 终极精简架构：后背中梁与十字全去、顶面加劲梁全去、底面专用托盘梁全去；
#    - 楼梯滑轨直接固定于主 Y 梁内侧 T 槽，全桌 19 根 4040 型材，零冗余零过约束！
# ==============================================================================

doc_name = "Workstation_1600x800x580_DualTrays_DualDrawers"
for old_name in ["Workstation_1600x800x630_DualTrays_DualDrawers", "Workstation_1600x800x550_DualTrays_DualDrawers", doc_name]:
    if old_name in App.listDocuments().keys():
        App.closeDocument(old_name)
doc = App.newDocument(doc_name)

# ----------------- 材质与设备配色库 -----------------
C_ALUM        = (0.22, 0.23, 0.25) # 黑色阳极氧化铝 4040
C_DRAWER_ALUM = (0.50, 0.52, 0.56) # 银灰阳极氧化铝 2020 (抽屉框架)
C_WOOD        = (0.82, 0.65, 0.44) # 桦木海洋板木色
C_BRACKET     = (0.88, 0.15, 0.15) # 🔴 红色：压铸抗震三角角码
C_ACRYLIC     = (0.15, 0.18, 0.22) # 黑透：亚克力抽屉底板 (透光30%)
C_THROUGH     = (0.00, 0.70, 0.90) # 🔵 青色：M12 穿芯拉紧节点域
C_ANCHOR      = (0.70, 0.20, 0.90) # 🟣 紫色：Φ12 内嵌锚式销钉节点域
C_CLIP        = (0.75, 0.75, 0.78) # ⚪ 银白：桌面固定紧固件
C_SLIDE       = (0.80, 0.82, 0.86) # ⚪ 银白高亮：镀锌精钢滑轨

# 设备配色
C_M2          = (0.18, 0.22, 0.24) # xTool M2 深空灰
C_L4          = (0.18, 0.20, 0.24) # LightMake L4 工业黑
C_CANON       = (0.22, 0.24, 0.26) # 佳能 MF113w 商务黑灰
C_P1S         = (0.28, 0.29, 0.31) # Bambu P1S 金属灰
C_AMS         = (0.88, 0.88, 0.90) # Bambu AMS 白透

# ----------------- FreeCAD 工程分组 -----------------
grp_frame     = doc.addObject("App::DocumentObjectGroup", "Frame")
grp_fasteners = doc.addObject("App::DocumentObjectGroup", "Fasteners")
grp_panels    = doc.addObject("App::DocumentObjectGroup", "Panels_Drawers")
grp_equip     = doc.addObject("App::DocumentObjectGroup", "Equipment")

# ----------------- 实体与紧固件生成器 -----------------
def create_cube(dx, dy, dz, x, y, z, name, color, transparency=0, group=None):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = Part.makeBox(dx, dy, dz)
    obj.Placement = App.Placement(App.Vector(x, y, z), App.Rotation(0, 0, 0))
    if hasattr(obj, "ViewObject") and obj.ViewObject:
        obj.ViewObject.ShapeColor = color
        if transparency > 0:
            obj.ViewObject.Transparency = transparency
    if group:
        group.addObject(obj)
    return obj

def create_bracket_yz(x, y_c, z_c, dy_sign, dz_sign, name, group=grp_fasteners):
    """侧面 45° 直角三角形压铸角码 (厚度 28mm, 边长 35x35mm)"""
    p1 = App.Vector(x, y_c, z_c)
    p2 = App.Vector(x, y_c + 35 * dy_sign, z_c)
    p3 = App.Vector(x, y_c, z_c + 35 * dz_sign)
    wire = Part.makePolygon([p1, p2, p3, p1])
    face = Part.Face(wire)
    shape = face.extrude(App.Vector(28, 0, 0))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if hasattr(obj, "ViewObject") and obj.ViewObject:
        obj.ViewObject.ShapeColor = C_BRACKET
    if group: group.addObject(obj)
    return obj

def create_bracket_xz(x_c, y, z_c, dx_sign, dz_sign, name, group=grp_fasteners):
    """后面 45° 直角三角形压铸角码 (厚度 28mm, 边长 35x35mm)"""
    p1 = App.Vector(x_c, y, z_c)
    p2 = App.Vector(x_c + 35 * dx_sign, y, z_c)
    p3 = App.Vector(x_c, y, z_c + 35 * dz_sign)
    wire = Part.makePolygon([p1, p2, p3, p1])
    face = Part.Face(wire)
    shape = face.extrude(App.Vector(0, 28, 0))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if hasattr(obj, "ViewObject") and obj.ViewObject:
        obj.ViewObject.ShapeColor = C_BRACKET
    if group: group.addObject(obj)
    return obj


def create_through_marker(x, y, z, name, group=grp_fasteners):
    """🔵 青色：M12 穿芯拉紧节点 (中心孔直穿拉紧套块，微突 1mm 保持 3D 全局可视)"""
    return create_cube(42, 42, 42, x - 1, y - 1, z - 21, name, C_THROUGH, transparency=30, group=group)

def create_anchor_pin(x, y, z, name, axis='Y', group=grp_fasteners):
    """🟣 紫色：Φ12 隐藏式内嵌锚式销钉套块 (T型槽挂接指示，微突 1mm 保持 3D 全局可视)"""
    if axis == 'Y':
        return create_cube(42, 42, 42, x - 1, y - 21, z - 1, name, C_ANCHOR, transparency=50, group=group)
    else:
        return create_cube(42, 42, 42, x - 21, y - 1, z - 1, name, C_ANCHOR, transparency=50, group=group)



# ==============================================================================
# 1. 铝型材骨架系统 (4040 刚性闭环，长 1600mm，立柱 550mm，总高 630mm)
# ==============================================================================
# 4 根长 1600mm X 向外框横梁 (底面 Z=0, 顶面 Z=540)
for y, z in [(0, 0), (760, 0), (0, 540), (760, 540)]:
    create_cube(1600, 40, 40, 0, y, z, f"Beam_X_{'Top' if z else 'Bot'}_{'Back' if y else 'Front'}", C_ALUM, group=grp_frame)

# 6 根主立柱 (高度 500mm，跨距 Z=40..540，中柱 X=780..820，右柱 X=1560..1600)
for x in [0, 780, 1560]:
    for y in [0, 760]:
        create_cube(40, 40, 500, x, y, 40, f"Col_X{x}_{'Back' if y else 'Front'}", C_ALUM, group=grp_frame)

# Y 向横梁系统 (9 根主梁：顶底 6 根由侧面 12 颗角码锁死零锚钉；中层 3 根抽屉滑轨承重梁由 6 颗内嵌锚钉固定)
# - Bot(Z=0): X=0, 780, 1560 (左右两舱底部主梁，重载楼梯滑轨直接固定于侧面 T 槽，无需任何多余底梁)
# - Mid(Z=340..380): X=0, 780, 1560 (距顶梁 Z=540 正好 160mm 黄金开孔，下留整整 300mm 托盘仓，89mm 宽裕防刮净空)
# - Top(Z=540): X=0, 780, 1560 (顶部主梁，依靠 24mm 桦木实木板自身超强刚度承托 L4 与 P1S)
y_levels = [
    ("Bot", 0,   [0, 780, 1560]),
    ("Mid", 340, [0, 780, 1560]),
    ("Top", 540, [0, 780, 1560]),
]
for tag, z, xs in y_levels:
    for x in xs:
        create_cube(40, 720, 40, x, 40, z, f"Beam_Y_{tag}_X{x}", C_ALUM, group=grp_frame)
        # 顶底 6 根立柱主 Y 梁（X=0, 780, 1560）由 12 颗侧面压铸三角角码负责强力紧固，零冗余锚钉；
        # 仅中层 3 根抽屉梁保留纯内嵌锚钉
        if tag in ["Bot", "Top"]:
            continue
        create_anchor_pin(x, 40,  z, f"Anchor_Y_X{x}_Y40_Z{z}",  'Y', grp_fasteners)
        create_anchor_pin(x, 760, z, f"Anchor_Y_X{x}_Y760_Z{z}", 'Y', grp_fasteners)

# ==============================================================================
# 2. 🔵 青色：M12 穿芯拉紧节点阵列 (12 处高可视节点)
# ==============================================================================
for x in [0, 780, 1560]:
    for y in [0, 760]:
        for z in [40, 540]:
            create_through_marker(x, y, z, f"Through_Z{z}_X{x}", grp_fasteners)

# ==============================================================================
# 3. 🔴 红色：16 个防震三角斜撑压铸角码 (全要素物理连接，零紧固过约束)
# ==============================================================================
# 侧面 12 个三角斜撑角码 (左/中/右立柱与顶底 Y 梁连接处，顶角在 Z=540，底角在 Z=40)
for name, x in [("Left", 6), ("Mid", 786), ("Right", 1566)]:
    for y, yt in [(40, "F"), (725, "B")]:
        for z_tag in ["T", "B"]:
            dy_s = 1 if yt == "F" else -1
            dz_s = -1 if z_tag == "T" else 1
            y_corner = 40 if yt == "F" else 760
            z_corner = 540 if z_tag == "T" else 40
            create_bracket_yz(x, y_corner, z_corner, dy_s, dz_s, f"B_{name}_{yt}{z_tag}", grp_fasteners)

# 后面 4 个三角斜撑角码 (外框 4 外角，专职锁死 X 向高速换向晃动；后中梁与十字角码全精简)
back_brackets_spec = [
    ("B_Back_LT",  40,   766, 540,  1, -1),
    ("B_Back_LB",  40,   766, 40,   1,  1),
    ("B_Back_RT",  1560, 766, 540, -1, -1),
    ("B_Back_RB",  1560, 766, 40,  -1,  1),
]
for name, xc, y, zc, dx_s, dz_s in back_brackets_spec:
    create_bracket_xz(xc, y, zc, dx_s, dz_s, name, grp_fasteners)

# ==============================================================================
# 4. ⚪ 桌面物理固定扣件 (8 处 T 槽台面平扣，Z=574 贴合桌面底)
# ==============================================================================
for x_pos in [100, 500, 1100, 1500]:
    create_cube(30, 20, 6, x_pos, 20,  574, f"Top_Clip_Front_X{x_pos}", C_CLIP, group=grp_fasteners)
    create_cube(30, 20, 6, x_pos, 760, 574, f"Top_Clip_Back_X{x_pos}",  C_CLIP, group=grp_fasteners)

# ==============================================================================
# 5. 板材、底层左右双拉盘 与 第一层左右双大抽屉系统
# ==============================================================================
# 1600mm 桌面海洋板 (Z=580, 厚度 24mm，顶标高 Z=604mm)
create_cube(1600, 800, 24, 0, 0, 580, "Wood_Top_Board", C_WOOD, 20, group=grp_panels)

# ----------------- (1) 底层：左右双超大抽拉托盘 (各 700×700×18mm，600mm 重载楼梯滑轨直接固定于主 Y 轴边框梁侧槽) -----------------
# 左舱激光托盘 (承载 xTool M2，滑轨直接固定于 X=40 与 X=780 边框大梁内侧 T 槽)
create_cube(20, 600, 53, 40,  60, 0, "Slide_LeftTray_L",  C_SLIDE, group=grp_panels)
create_cube(20, 600, 53, 760, 60, 0, "Slide_LeftTray_R",  C_SLIDE, group=grp_panels)
create_cube(700, 700, 18, 60,  50, 53, "Wood_Laser_Tray_Left", C_WOOD, 10, group=grp_panels)

# 右舱物料托盘 (承载 600×600mm 原板大木材/亚克力原料，滑轨直接固定于 X=820 与 X=1560 边框大梁内侧 T 槽)
create_cube(20, 600, 53, 820,  60, 0, "Slide_RightTray_L", C_SLIDE, group=grp_panels)
create_cube(20, 600, 53, 1540, 60, 0, "Slide_RightTray_R", C_SLIDE, group=grp_panels)
create_cube(700, 700, 18, 840, 50, 53, "Wood_Material_Tray_Right", C_WOOD, 10, group=grp_panels)

# ----------------- (2) 第一层：左右并列双超宽 2020 铝型材抽屉系统 (精密紧固挂接，零空悬，零缝隙) -----------------
# 物理装配约束：
# - 舱体净宽 740 mm，双侧 13mm 滑轨，抽屉外宽严格定为 714 mm (左右各贴合 13mm 滑轨，严丝合缝)
# - 抽屉进深 550 mm，外高 160 mm (内净深 140 mm)
# - 滑轨安装于中梁 Z=340..380 侧面 T 槽 (高度 40mm)，抽屉底标高 Z=350 (下凹进入中梁 30mm，下底留 10mm 间隙)
# - 抽屉顶标高 Z=510，距顶梁底 Z=540 留有 30mm 充足防蹭抽拉净空
# - 三节伸缩式静音阻尼滑轨：固定外轨锁固于 4040 梁，中节伸缩轨同步延展，活动内轨紧贴抽屉侧壁并随抽屉抽拉

C_SLIDE_MID = (0.72, 0.75, 0.79)

def build_drawer_and_telescopic_slides(bay_x_start, z_mid, pull_offset, prefix):
    w = 714
    d = 550
    h = 160
    y_base = 50
    y_eff = y_base - pull_offset
    z_drawer = z_mid + 10  # Z = 350
    
    # 1. 2020 铝型材抽屉内胆 (外宽 714, 深 550, 高 160)
    x_draw = bay_x_start + 13  # 53 (左舱) 或 833 (右舱)
    
    # 底框 4 根 2020
    create_cube(w, 20, 20, x_draw, y_eff, z_drawer, f"{prefix}_Bot_Front_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(w, 20, 20, x_draw, y_eff + d - 20, z_drawer, f"{prefix}_Bot_Back_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, d - 40, 20, x_draw, y_eff + 20, z_drawer, f"{prefix}_Bot_Left_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, d - 40, 20, x_draw + w - 20, y_eff + 20, z_drawer, f"{prefix}_Bot_Right_2020", C_DRAWER_ALUM, group=grp_panels)
    
    # 抽屉底板 (5mm 黑色透光亚克力，插装于 2020 槽内)
    create_cube(w - 20, d - 20, 5, x_draw + 10, y_eff + 10, z_drawer + 8, f"{prefix}_Plate_Acrylic", C_ACRYLIC, 30, group=grp_panels)
    
    # 四角立柱 4 根 2020 (立柱长 120 mm，抽屉总高 160 mm)
    post_h = h - 40
    create_cube(20, 20, post_h, x_draw, y_eff, z_drawer + 20, f"{prefix}_Post_FL_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, 20, post_h, x_draw + w - 20, y_eff, z_drawer + 20, f"{prefix}_Post_FR_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, 20, post_h, x_draw, y_eff + d - 20, z_drawer + 20, f"{prefix}_Post_BL_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, 20, post_h, x_draw + w - 20, y_eff + d - 20, z_drawer + 20, f"{prefix}_Post_BR_2020", C_DRAWER_ALUM, group=grp_panels)
    
    # 顶框 4 根 2020
    top_z = z_drawer + h - 20
    create_cube(w, 20, 20, x_draw, y_eff, top_z, f"{prefix}_Top_Front_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(w, 20, 20, x_draw, y_eff + d - 20, top_z, f"{prefix}_Top_Back_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, d - 40, 20, x_draw, y_eff + 20, top_z, f"{prefix}_Top_Left_2020", C_DRAWER_ALUM, group=grp_panels)
    create_cube(20, d - 40, 20, x_draw + w - 20, y_eff + 20, top_z, f"{prefix}_Top_Right_2020", C_DRAWER_ALUM, group=grp_panels)

    # 2. 三节伸缩式静音阻尼滑轨组装 (总厚度 13mm，完美连接梁与抽屉)
    # 左侧滑轨 (X: bay_x_start .. bay_x_start + 13)
    # (a) 固定外轨 (厚6mm, 牢固锁紧于 4040 中梁内侧 T 槽)
    create_cube(6, d, 40, bay_x_start, y_base, z_mid, f"{prefix}_SlideL_Outer", C_SLIDE, group=grp_panels)
    # (b) 中节延伸轨 (厚3mm, 抽拉行程一半)
    create_cube(3, d, 34, bay_x_start + 6, y_base - pull_offset * 0.5, z_mid + 3, f"{prefix}_SlideL_Mid", C_SLIDE_MID, group=grp_panels)
    # (c) 活动内轨 (厚4mm, 紧贴抽屉侧壁，随抽屉完全同步滑出)
    create_cube(4, d, 28, bay_x_start + 9, y_eff, z_mid + 6, f"{prefix}_SlideL_Inner", C_SLIDE, group=grp_panels)

    # 右侧滑轨 (X: bay_x_start + 727 .. bay_x_start + 740)
    # (c) 活动内轨 (厚4mm, 紧贴抽屉右侧壁)
    create_cube(4, d, 28, bay_x_start + 727, y_eff, z_mid + 6, f"{prefix}_SlideR_Inner", C_SLIDE, group=grp_panels)
    # (b) 中节延伸轨 (厚3mm)
    create_cube(3, d, 34, bay_x_start + 731, y_base - pull_offset * 0.5, z_mid + 3, f"{prefix}_SlideR_Mid", C_SLIDE_MID, group=grp_panels)
    # (a) 固定外轨 (厚6mm, 牢固锁紧于 4040 中梁外侧 T 槽)
    create_cube(6, d, 40, bay_x_start + 734, y_base, z_mid, f"{prefix}_SlideR_Outer", C_SLIDE, group=grp_panels)

# 左抽屉：位于激光机正上方，向前抽拉 120mm 展示三节滑轨联动与内部结构
build_drawer_and_telescopic_slides(40, 340, 120, "Drawer_Left_LaserTools")

# 右抽屉：位于右下物料托盘正上方，保持完全闭合收纳状态 (pull=0)
build_drawer_and_telescopic_slides(820, 340, 0, "Drawer_Right_3DTools")

# ==============================================================================
# 6. 设备就位 (下层 M2 + 桌面并列三剑客：L4 + 佳能MF113w + P1S/AMS叠放)
# ==============================================================================
# (1) 左舱托盘：xTool M2 (610 mm 宽 × 569 mm 深 × 180 mm 高)
#     - 居中居前：X=105, Y=90, Z=71 (顶高 Z=251mm，距上方中梁 Z=340mm 留有整整 89mm 宽敞净空)
#     - 托盘后部留出 141mm (Y=659..750) 顺畅排烟与电源线区域
create_cube(610, 569, 180, 105, 90, 71, "Machine_xTool_M2", C_M2, 30, group=grp_equip)

# (2) 桌面左侧: LightMake L4 工业机 (X=40..655，宽 615mm，由 24mm 桦木实木大板超强刚度承托)
#     - 宽 615mm, 深 624mm, 高 677mm, 标高 Z=604mm, 顶高 1281 mm (站立俯视热床零疲劳)
create_cube(615, 624, 677, 40, 100, 604, "Machine_LightMake_L4", C_L4, 20, group=grp_equip)

# (3) 桌面中段: 佳能 MF113w 激光一体机 (372×320×255mm，后靠放置留出前方作业台)
#     - X=727..1099，与 L4 间距恰好 72 mm，顶盖无遮挡，掀盖扫描/复印畅通无阻
#     - 标高 Z=604mm，顶高 859 mm，坐姿伸手即达
create_cube(372, 320, 255, 727, 400, 604, "Machine_Canon_MF113w", C_CANON, 25, group=grp_equip)

# (4) 桌面右侧: Bambu Lab P1S 主机 (389×389×457mm)
#     - X=1171..1560，与 佳能间距恰好 72 mm，右侧边缘余量 40 mm
#     - 标高 Z=604mm，主机顶高 1061 mm
create_cube(389, 389, 457, 1171, 350, 604, "Machine_Bambu_P1S", C_P1S, 30, group=grp_equip)

# (5) 桌面右侧: Bambu AMS 自动供料系统 (顶置叠放于 P1S 上盖)
#     - 标高 Z=1061..1285mm (站姿平视胸口位置，装料换卷极顺手)
create_cube(368, 271, 224, 1181.5, 410, 1061, "Machine_Bambu_AMS", C_AMS, 30, group=grp_equip)

# ==============================================================================
# 7. 刷新视角与装配 BOM 清单生成
# ==============================================================================
App.ActiveDocument.recompute()
try:
    import FreeCADGui as Gui
    if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
except Exception:
    pass

print("\n" + "=" * 62)
print("🛠️  1600x800x580mm 终极工作站 (V27.0 500mm立柱大师版) 构建成功！")
print("=" * 62)
print("📐 关键几何特征:")
print("  • 框架外包围尺寸 : 1600 mm (长) × 800 mm (深) × 580 mm (高)")
print("  • 主立柱下料长度 : 500 mm (共 6 根)")
print("  • 台面顶高       : 604 mm (含 24mm 桦木海洋板，黄金低坐姿工位)")
print("  • 完美全对称架构 : 左右两舱净宽均为 740 mm！")
print("  • 第一层(双深抽屉): 左右各一个 714×550×160mm 2020 铝型材宽体深抽屉 (内净深 140mm，双侧贴合13mm三节阻尼轨)")
print("  • 底层(双大托盘) : 左右各一个 700×700×18mm 超大抽拉托盘 (左M2留89mm宽裕净空，右原板材仓)")
print("  • 桌面三机并列   : L4(宽615) + 佳能MF113w(宽372) + P1S(宽389)")
print("  • 黄金等距间隙   : L4与佳能、佳能与P1S之间间隙均为 72.0 mm（手掌自由伸入）")
print("  • 桌面实操前带   : 佳能与P1S前方形成 833×350~400mm 纯净作业区(笔记本/工具)")
print("  • 顶置AMS人机高度: AMS 顶高 1285 mm，换料平视胸口位置，零疲劳")
print("  • 抽屉中梁开孔   : 中梁位于 Z=340..380mm，顶梁至中梁净空 160mm，下层托盘仓净高 300mm")
print("  • 无级高度可调   : 中层 3 根 Y 梁由 6 颗内嵌锚钉锁于立柱 T 槽，松螺丝即可自由微调！")
print("📦 五金物料装配清单 (BOM Summary):")
print("  • 4040 压铸铝三角抗震角码 (45° 加厚肋) : 16 套 (侧面 12 套 + 后面 4 外角)")
print("  • 4040 隐形内嵌锚式销钉套件 (Φ12销轴) : 6 套 (中层 3 根抽屉滑轨梁两端)")
print("  • M12/M8 垂直中心贯穿拉紧螺栓套件     : 12 支 (含平垫片)")
print("  • 桌面板 T型槽防震固定扣件             : 8 套 (含自攻木螺钉)")
print("  • 600mm 重载三节静音阻尼滑轨           : 4 条 (左右双大托盘各2条，直接安装在边框大梁上)")
print("  • 550mm 三节伸缩静音阻尼滑轨           : 4 条 (左右双大抽屉各2条，三节联动伸缩展示)")
print("  • 4040 国标轻/重型铝型材总切割长度     : 15.88 米 (共 19 根)")
print("  • 2020 铝型材抽屉内胆总切割长度       : 10.75 米 (共 24 根: 714mm×8, 510mm×8, 120mm×8)")
print("=" * 62 + "\n")

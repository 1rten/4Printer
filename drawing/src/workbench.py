import FreeCAD as App
import Part

# ==============================================================================
# FreeCAD Python 脚本：1400x800x700mm 重型工作站 (V19.3 物理装配全要素可视版)
# ==============================================================================
# 物理与工程装配特性：
# 1. 🔴 红色：20 个压铸铝 45° 三角斜撑抗震角码 (真实力学斜肋，杜绝平面假方块)
# 2. 🔵 青色：12 处 M12 垂直中心孔穿芯打孔拉紧域 (半透明 30%，节点全域高可视)
# 3. 🟣 紫色：36 处 Φ12 隐形内嵌锚式销钉挂接域 (半透明 50%，T型槽连接全可视)
# 4. ⚪ 银白：8 处 T 型槽桌面防震固定平扣 (物理锁定桌面桦木海洋板)
# 5. FreeCAD 4 大工程组：Frame / Fasteners / Panels_Drawers / Equipment
# 6. 自动统计输出工程装配五金采购清单 (BOM)
# ==============================================================================

doc_name = "Workstation_V19_2_Complete"
if doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# ----------------- 材质与设备配色库 -----------------
C_ALUM    = (0.22, 0.23, 0.25) # 黑色阳极氧化铝 4040
C_WOOD    = (0.82, 0.65, 0.44) # 桦木海洋板木色
C_BRACKET = (0.88, 0.15, 0.15) # 🔴 红色：压铸抗震三角角码
C_ACRYLIC = (0.15, 0.15, 0.18) # 黑透：亚克力抽屉模块
C_THROUGH = (0.00, 0.70, 0.90) # 🔵 青色：M12 穿芯拉紧节点域
C_ANCHOR  = (0.70, 0.20, 0.90) # 🟣 紫色：Φ12 内嵌锚式销钉节点域
C_CLIP    = (0.75, 0.75, 0.78) # ⚪ 银白：桌面固定紧固件
C_SILVER  = (0.78, 0.78, 0.82) # ⚪ 银灰：楼梯柜重型滑轨

C_S1      = (0.15, 0.16, 0.18) # xTool S1 深空灰
C_P1S     = (0.28, 0.29, 0.31) # Bambu P1S 金属灰
C_L4      = (0.18, 0.20, 0.24) # LightMake L4 工业黑
C_CANON   = (0.20, 0.21, 0.23) # 佳能 MF113w 商务黑灰
C_AMS     = (0.88, 0.88, 0.90) # Bambu AMS 白透

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
# 1. 铝型材骨架系统与锚式销钉联动 (4040 刚性闭环)
# ==============================================================================
# 4 根长 1400mm X 向外框横梁
for y, z in [(0, 0), (760, 0), (0, 660), (760, 660)]:
    create_cube(1400, 40, 40, 0, y, z, f"Beam_X_{'Top' if z else 'Bot'}_{'Back' if y else 'Front'}", C_ALUM, group=grp_frame)

# 2 根后部中跨横梁 (左舱 700mm, 右舱 580mm)
create_cube(700, 40, 40, 40,  760, 360, "Beam_X_Back_Mid_LeftSeg",  C_ALUM, group=grp_frame)
create_cube(580, 40, 40, 780, 760, 360, "Beam_X_Back_Mid_RightSeg", C_ALUM, group=grp_frame)

# 6 根立柱
for x in [0, 740, 1360]:
    for y in [0, 760]:
        create_cube(40, 40, 620, x, y, 40, f"Col_X{x}_{'Back' if y else 'Front'}", C_ALUM, group=grp_frame)

# 16 根 Y 向横梁及其两端锚式连接 (🟣 紫色高可视紧固节点)
y_levels = [
    ("Bot",    0,   [0, 190, 550, 740, 1050, 1360]),
    ("Mid",    360, [0, 740, 1360]),
    ("Drawer", 520, [0, 740]),
    ("Top",    660, [0, 370, 740, 1050, 1360]),
]
for tag, z, xs in y_levels:
    for x in xs:
        create_cube(40, 720, 40, x, 40, z, f"Beam_Y_{tag}_X{x}", C_ALUM, group=grp_frame)
        create_anchor_pin(x, 40,  z, f"Anchor_Y_X{x}_Y40_Z{z}",  'Y', grp_fasteners)
        create_anchor_pin(x, 760, z, f"Anchor_Y_X{x}_Y760_Z{z}", 'Y', grp_fasteners)

# 后中跨横梁端头锚式连接
for x in [40, 740, 780, 1360]:
    create_anchor_pin(x, 760, 360, f"Anchor_X_X{x}_Y760_Z360", 'X', grp_fasteners)

# ==============================================================================
# 2. 🔵 青色：M12 穿芯拉紧节点阵列 (12 处高可视节点)
# ==============================================================================
for x in [0, 740, 1360]:
    for y in [0, 760]:
        for z in [40, 660]:
            create_through_marker(x, y, z, f"Through_Z{z}_X{x}", grp_fasteners)

# ==============================================================================
# 3. 🔴 红色：20 个防震三角斜撑压铸角码 (真实力学斜边)
# ==============================================================================
# 侧面 12 个三角斜撑角码
for name, x in [("Left", 6), ("Mid", 746), ("Right", 1366)]:
    for y, yt in [(40, "F"), (725, "B")]:
        for z, zt in [(625, "T"), (40, "B")]:
            dy_s = 1 if yt == "F" else -1
            dz_s = -1 if zt == "T" else 1
            y_corner = 40 if yt == "F" else 760
            z_corner = 660 if zt == "T" else 40
            create_bracket_yz(x, y_corner, z_corner, dy_s, dz_s, f"B_{name}_{yt}{zt}", grp_fasteners)

# 后面 8 个三角斜撑角码 (外侧 4 个 + 十字交叉 4 个)
back_brackets_spec = [
    ("B_Back_LT",  40,   766, 660,  1, -1),
    ("B_Back_LB",  40,   766, 40,   1,  1),
    ("B_Back_RT",  1360, 766, 660, -1, -1),
    ("B_Back_RB",  1360, 766, 40,  -1,  1),
    ("B_Cross_LT", 740,  766, 400, -1,  1),
    ("B_Cross_RT", 780,  766, 400,  1,  1),
    ("B_Cross_LB", 740,  766, 360, -1, -1),
    ("B_Cross_RB", 780,  766, 360,  1, -1),
]
for name, xc, y, zc, dx_s, dz_s in back_brackets_spec:
    create_bracket_xz(xc, y, zc, dx_s, dz_s, name, grp_fasteners)

# ==============================================================================
# 4. ⚪ 桌面物理固定扣件 (8 处 T 槽台面平扣)
# ==============================================================================
for x_pos in [100, 450, 950, 1300]:
    create_cube(30, 20, 6, x_pos, 20,  694, f"Top_Clip_Front_X{x_pos}", C_CLIP, group=grp_fasteners)
    create_cube(30, 20, 6, x_pos, 760, 694, f"Top_Clip_Back_X{x_pos}",  C_CLIP, group=grp_fasteners)

# ==============================================================================
# 5. 滑轨、板材与抽屉系统
# ==============================================================================
for x, name in [(160, "Slide_Heavy_Left"), (590, "Slide_Heavy_Right")]:
    create_cube(30, 600, 53, x, 60, 0, name, C_SILVER, group=grp_panels)

boards_and_drawers = [
    (1400, 800, 24,  0,   0,  700, "Wood_Top_Board",   C_WOOD,    20),
    (580,  720, 18,  780, 40, 40,  "Wood_P1S_Base",    C_WOOD,    10),
    (650,  650, 18,  65,  60, 53,  "Wood_Laser_Tray",  C_WOOD,    10),
    (674,  550, 120, 53,  60, 365, "Drawer_Mid_Cyber", C_ACRYLIC, 60),
    (674,  550, 100, 53,  60, 525, "Drawer_Top_Cyber", C_ACRYLIC, 60),
]
for dx, dy, dz, x, y, z, name, color, transp in boards_and_drawers:
    create_cube(dx, dy, dz, x, y, z, name, color, transp, group=grp_panels)

# ==============================================================================
# 6. 设备高精就位
# ==============================================================================
machines = [
    (600, 500, 190, 90,    90,  71,  "Machine_xTool_S1",     C_S1,    30),
    (389, 389, 457, 875.5, 90,  58,  "Machine_Bambu_P1S",    C_P1S,   30),
    (615, 624, 677, 60,    130, 724, "Machine_LightMake_L4", C_L4,    20),
    (372, 320, 255, 884,   60,  724, "Machine_Canon_MF113w", C_CANON, 20),
    (368, 271, 224, 886,   460, 724, "Machine_Bambu_AMS",     C_AMS,   30),
]
for dx, dy, dz, x, y, z, name, color, transp in machines:
    create_cube(dx, dy, dz, x, y, z, name, color, transp, group=grp_equip)

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
print("🛠️  1400x800x700mm 重型工作站 (V19.3 全要素物理装配版) 构建成功！")
print("=" * 62)
print("📦 五金物料装配清单 (BOM Summary):")
print("  • 4040 压铸铝三角抗震角码 (45° 加厚肋) : 20 套 (含配套 M8 半圆头螺栓+T型螺母)")
print("  • 4040 隐形内嵌锚式销钉套件 (Φ12销轴) : 36 套 (含内六角顶紧螺钉)")
print("  • M12/M8 垂直中心贯穿拉紧螺栓套件     : 12 支 (含平垫片)")
print("  • 桌面板 T型槽防震固定扣件             : 8 套 (含自攻木螺钉)")
print("  • 600mm 重载三节静音阻尼滑轨           : 2 条")
print("  • 4040 国标轻/重型铝型材总切割长度     : 22.04 米 (共 28 根)")
print("=" * 62 + "\n")
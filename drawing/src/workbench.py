import FreeCAD as App
import Part

# ==============================================================================
# FreeCAD Python 脚本：1400x800x700mm 重型工作站 (V19.2 全要素精简版)
# ==============================================================================
doc_name = "Workstation_V19_2_Complete"
if doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# ----------------- 材质与设备配色库 -----------------
C_ALUM, C_WOOD, C_BRACKET, C_ACRYLIC = (0.22, 0.23, 0.25), (0.82, 0.65, 0.44), (0.88, 0.15, 0.15), (0.15, 0.15, 0.18)
C_THROUGH, C_ANCHOR, C_SILVER        = (0.00, 0.70, 0.90), (0.70, 0.20, 0.90), (0.78, 0.78, 0.82)
C_S1, C_P1S, C_L4, C_CANON, C_AMS    = (0.15, 0.16, 0.18), (0.28, 0.29, 0.31), (0.18, 0.20, 0.24), (0.20, 0.21, 0.23), (0.88, 0.88, 0.90)

# ----------------- 实体生成器 -----------------
def create_cube(dx, dy, dz, x, y, z, name, color, transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = Part.makeBox(dx, dy, dz)
    obj.Placement = App.Placement(App.Vector(x, y, z), App.Rotation(0, 0, 0))
    if hasattr(obj, "ViewObject") and obj.ViewObject:
        obj.ViewObject.ShapeColor = color
        if transparency > 0:
            obj.ViewObject.Transparency = transparency
    return obj

def create_marker(x, y, z, name, color, transp=50):
    return create_cube(42, 42, 42, x, y, z, name, color, transp)

# 1. 铝型材骨架与锚钉 (4040 闭环)
for y, z in [(0, 0), (760, 0), (0, 660), (760, 660)]:
    create_cube(1400, 40, 40, 0, y, z, f"Beam_X_{'Top' if z else 'Bot'}_{'Back' if y else 'Front'}", C_ALUM)

create_cube(700, 40, 40, 40, 760, 360, "Beam_X_Back_Mid_LeftSeg", C_ALUM)
create_cube(580, 40, 40, 780, 760, 360, "Beam_X_Back_Mid_RightSeg", C_ALUM)

for x in [0, 740, 1360]:
    for y in [0, 760]:
        create_cube(40, 40, 620, x, y, 40, f"Col_X{x}_{'Back' if y else 'Front'}", C_ALUM)

# 16 根 Y 向横梁及其两端锚式连接 (🟣 紫色)
y_levels = [
    ("Bot",    0,   [0, 190, 550, 740, 1050, 1360]),
    ("Mid",    360, [0, 740, 1360]),
    ("Drawer", 520, [0, 740]),
    ("Top",    660, [0, 370, 740, 1050, 1360]),
]
for tag, z, xs in y_levels:
    for x in xs:
        create_cube(40, 720, 40, x, 40, z, f"Beam_Y_{tag}_X{x}", C_ALUM)
        create_marker(x - 1, 40 - 21, z - 1, f"Anchor_Y_X{x}_Y40_Z{z}", C_ANCHOR)
        create_marker(x - 1, 760 - 21, z - 1, f"Anchor_Y_X{x}_Y760_Z{z}", C_ANCHOR)

for x in [40, 740, 780, 1360]:
    create_marker(x - 21, 760 - 1, 360 - 1, f"Anchor_X_X{x}_Y760_Z360", C_ANCHOR)

# 2. 🔵 青色穿芯打孔 (12 处)
for x in [0, 740, 1360]:
    for y in [0, 760]:
        for z in [40, 660]:
            create_marker(x - 1, y - 1, z - 21, f"Through_Z{z}_X{x}", C_THROUGH, 30)

# 3. 🔴 红色防震角码 (20 处)
for name, x in [("Left", 6), ("Mid", 746), ("Right", 1366)]:
    for y, yt in [(40, "F"), (725, "B")]:
        for z, zt in [(625, "T"), (40, "B")]:
            create_cube(28, 35, 35, x, y, z, f"B_{name}_{yt}{zt}", C_BRACKET)

for pfx, xs, zs in [("Back", [(40, "L"), (1325, "R")], [(625, "T"), (40, "B")]),
                    ("Cross", [(705, "L"), (780, "R")], [(400, "T"), (325, "B")])]:
    for x, xt in xs:
        for z, zt in zs:
            create_cube(35, 28, 35, x, 766, z, f"B_{pfx}_{xt}{zt}", C_BRACKET)

# 4. ⚪ 滑轨与板材抽屉系统
for x, name in [(160, "Slide_Heavy_Left"), (590, "Slide_Heavy_Right")]:
    create_cube(30, 600, 53, x, 60, 0, name, C_SILVER)

for dx, dy, dz, x, y, z, name, color, transp in [
    (1400, 800, 24,  0,   0,  700, "Wood_Top_Board",   C_WOOD,    20),
    (580,  720, 18,  780, 40, 40,  "Wood_P1S_Base",    C_WOOD,    10),
    (650,  650, 18,  65,  60, 53,  "Wood_Laser_Tray",  C_WOOD,    10),
    (674,  550, 120, 53,  60, 365, "Drawer_Mid_Cyber", C_ACRYLIC, 60),
    (674,  550, 100, 53,  60, 525, "Drawer_Top_Cyber", C_ACRYLIC, 60),
]:
    create_cube(dx, dy, dz, x, y, z, name, color, transp)

# 5. 设备就位 (xTool S1, Bambu P1S, L4, Canon, AMS)
for dx, dy, dz, x, y, z, name, color, transp in [
    (600, 500, 190, 90,    90,  71,  "Machine_xTool_S1",     C_S1,    30),
    (389, 389, 457, 875.5, 90,  58,  "Machine_Bambu_P1S",    C_P1S,   30),
    (615, 624, 677, 60,    130, 724, "Machine_LightMake_L4", C_L4,    20),
    (372, 320, 255, 884,   60,  724, "Machine_Canon_MF113w", C_CANON, 20),
    (368, 271, 224, 886,   460, 724, "Machine_Bambu_AMS",     C_AMS,   30),
]:
    create_cube(dx, dy, dz, x, y, z, name, color, transp)

# 6. 刷新视角
App.ActiveDocument.recompute()
try:
    import FreeCADGui as Gui
    if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
except Exception:
    pass

print("✅ FreeCAD V19.2 同步完成：L4 已更新至 X=60，桌面同轴与底层设备全要素闭环！")
import FreeCAD as App
import Part

# ==============================================================================
# FreeCAD Python 脚本：1400x800x700mm 重型工作站 (V19.0 防撞车打孔分类版)
# 核心升级：严格区分“沉头打孔穿芯(青色)”与“锚式连接(紫色)”，彻底解决三维螺丝干涉
# ==============================================================================

doc_name = "Workstation_V19_Connectors"
if doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# ----------------- 材质配色库 -----------------
C_ALUM    = (0.22, 0.23, 0.25) # 黑色阳极氧化铝
C_WOOD    = (0.82, 0.65, 0.44) # 桦木海洋板木色
C_BRACKET = (0.88, 0.15, 0.15) # 红色：20个隐藏式抗震角码
C_ACRYLIC = (0.15, 0.15, 0.18) # 黑透：亚克力抽屉模块
C_THROUGH = (0.00, 0.70, 0.90) # 🔵 青色：沉头打孔穿芯 (走中心孔)
C_ANCHOR  = (0.70, 0.20, 0.90) # 🟣 紫色：锚式销钉连接 (走表面T槽)

# ----------------- 核心生成器 -----------------
def create_cube(dx, dy, dz, x, y, z, name, color, transparency=0):
    box = Part.makeBox(dx, dy, dz)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = box
    obj.Placement = App.Placement(App.Vector(x, y, z), App.Rotation(0, 0, 0))
    obj.ViewObject.ShapeColor = color
    if transparency > 0: obj.ViewObject.Transparency = transparency
    return obj

# 打孔分类标记器 (精确覆盖交汇端面)
def create_through_marker(x, y, z): # Z轴穿芯
    create_cube(42, 42, 42, x-1, y-1, z-21, f"Through_Z{int(z)}", C_THROUGH, 30)
def create_anchor_y(x, y, z): # Y轴锚式
    create_cube(42, 42, 42, x-1, y-21, z-1, f"Anchor_Y_Y{int(y)}", C_ANCHOR, 50)
def create_anchor_x(x, y, z): # X轴锚式
    create_cube(42, 42, 42, x-21, y-1, z-1, f"Anchor_X_X{int(x)}", C_ANCHOR, 50)

# ==============================================================================
# 1. 铝型材骨架系统
# ==============================================================================
create_cube(1400, 40, 40,  0, 0, 0,        "Beam_X_Bot_Front", C_ALUM)
create_cube(1400, 40, 40,  0, 760, 0,      "Beam_X_Bot_Back",  C_ALUM)
create_cube(1400, 40, 40,  0, 0, 660,      "Beam_X_Top_Front", C_ALUM)
create_cube(1400, 40, 40,  0, 760, 660,    "Beam_X_Top_Back",  C_ALUM)
create_cube(660, 40, 40,   40, 760, 360,   "Beam_X_Back_Mid_LeftSeg",  C_ALUM)
create_cube(620, 40, 40,   740, 760, 360,  "Beam_X_Back_Mid_RightSeg", C_ALUM)

for x in [0, 700, 1360]:
    create_cube(40, 40, 620,  x, 0, 40,    f"Col_X{x}_Front", C_ALUM)
    create_cube(40, 40, 620,  x, 760, 40,  f"Col_X{x}_Back",  C_ALUM)

y_beams_z0 = [0, 150, 550, 700, 1050, 1360] 
y_beams_z660 = [0, 350, 700, 1050, 1360]    
y_beams_z360 = [0, 700, 1360]               
y_beams_z520 = [0, 700]                     

for x in y_beams_z0:   create_cube(40, 720, 40, x, 40, 0,   f"Beam_Y_Bot_X{x}", C_ALUM)
for x in y_beams_z660: create_cube(40, 720, 40, x, 40, 660, f"Beam_Y_Top_X{x}", C_ALUM)
for x in y_beams_z360: create_cube(40, 720, 40, x, 40, 360, f"Beam_Y_Mid_X{x}", C_ALUM)
for x in y_beams_z520: create_cube(40, 720, 40, x, 40, 520, f"Beam_Y_Drawer_X{x}", C_ALUM)

# ==============================================================================
# 2. 🔵 青色：沉头打孔穿芯阵列 (锁死Z轴立柱，共 12 处)
# ==============================================================================
for x in [0, 700, 1360]:
    for y in [0, 760]:
        create_through_marker(x, y, 40)  # 底框向上穿芯
        create_through_marker(x, y, 660) # 顶框向下穿芯

# ==============================================================================
# 3. 🟣 紫色：锚式连接阵列 (锁死所有进深梁与内部腰梁，避让穿芯螺丝)
# ==============================================================================
# Y轴进深梁两端锚式
for x in y_beams_z0:   create_anchor_y(x, 40, 0);   create_anchor_y(x, 760, 0)
for x in y_beams_z660: create_anchor_y(x, 40, 660); create_anchor_y(x, 760, 660)
for x in y_beams_z360: create_anchor_y(x, 40, 360); create_anchor_y(x, 760, 360)
for x in y_beams_z520: create_anchor_y(x, 40, 520); create_anchor_y(x, 760, 520)

# X轴背部腰梁两段锚式
create_anchor_x(40, 760, 360);  create_anchor_x(700, 760, 360)  # 左段
create_anchor_x(740, 760, 360); create_anchor_x(1360, 760, 360) # 右段

# ==============================================================================
# 4. 🔴 红色：20 角码绝对防御阵列 (0干涉沉槽版)
# ==============================================================================
create_cube(35, 28, 35, 40, 766, 625, "B_Back_LT", C_BRACKET)
create_cube(35, 28, 35, 40, 766, 40,  "B_Back_LB", C_BRACKET)
create_cube(35, 28, 35, 1325,766,625, "B_Back_RT", C_BRACKET)
create_cube(35, 28, 35, 1325,766,40,  "B_Back_RB", C_BRACKET)
create_cube(35, 28, 35, 665, 766, 400, "B_Cross_LT", C_BRACKET)
create_cube(35, 28, 35, 740, 766, 400, "B_Cross_RT", C_BRACKET)
create_cube(35, 28, 35, 665, 766, 325, "B_Cross_LB", C_BRACKET)
create_cube(35, 28, 35, 740, 766, 325, "B_Cross_RB", C_BRACKET)
create_cube(28, 35, 35, 1366, 40, 625, "B_Right_FT", C_BRACKET)
create_cube(28, 35, 35, 1366, 40, 40,  "B_Right_FB", C_BRACKET)
create_cube(28, 35, 35, 1366, 725,625, "B_Right_BT", C_BRACKET)
create_cube(28, 35, 35, 1366, 725,40,  "B_Right_BB", C_BRACKET)
create_cube(28, 35, 35, 6, 40, 625, "B_Left_FT", C_BRACKET)
create_cube(28, 35, 35, 6, 40, 40,  "B_Left_FB", C_BRACKET)
create_cube(28, 35, 35, 6, 725,625, "B_Left_BT", C_BRACKET)
create_cube(28, 35, 35, 6, 725,40,  "B_Left_BB", C_BRACKET)
create_cube(28, 35, 35, 706, 40, 625, "B_Mid_FT", C_BRACKET)
create_cube(28, 35, 35, 706, 40, 40,  "B_Mid_FB", C_BRACKET)
create_cube(28, 35, 35, 706, 725,625, "B_Mid_BT", C_BRACKET)
create_cube(28, 35, 35, 706, 725,40,  "B_Mid_BB", C_BRACKET)

# ==============================================================================
# 5. 板材与科幻抽屉
# ==============================================================================
create_cube(1400, 800, 24,  0, 0, 700,     "Wood_Top_Board", C_WOOD, 30)
create_cube(660, 720, 18,   740, 40, 40,   "Wood_P1S_Base",  C_WOOD, 10)
create_cube(650, 550, 18,   45, 60, 58,    "Wood_Laser_Tray",C_WOOD, 10)
create_cube(634, 550, 120,  53, 60, 365,   "Drawer_Mid_Cyber", C_ACRYLIC, 60) 
create_cube(634, 550, 100,  53, 60, 525,   "Drawer_Top_Cyber", C_ACRYLIC, 60) 

# ==============================================================================
# 6. 刷新视角
# ==============================================================================
App.ActiveDocument.recompute()
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxometric()
    Gui.ActiveDocument.ActiveView.fitAll()
except: pass

print("✅ V19.0 已生成：蓝块=沉孔穿芯，紫块=锚式连接，红块=防震角码！")
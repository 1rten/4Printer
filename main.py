import FreeCAD as App
import Part

# ==============================================================================
# FreeCAD Python 脚本：1400x800x700mm 重型工作站 (V19.2 全要素全设备装配版)
# ==============================================================================
# 核心同步更新：
# 1. LightMake L4 定位：X=60mm, Y=130mm (中心完美落在 X=370 加劲梁正上方)
# 2. 桌面同轴体系：佳能 MF113w 与 Bambu AMS 锁定中心线 X=1070mm 前后串联
# 3. 底层重载体系：600mm 楼梯柜滑轨贴外侧并排，S1 与 P1S 真实就位
# 4. 骨架闭环：左舱 700mm / 右舱 580mm，红角码/青穿芯/紫锚式无干涉
# ==============================================================================

doc_name = "Workstation_V19_2_Complete"
if doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# ----------------- 材质配色库 -----------------
C_ALUM    = (0.22, 0.23, 0.25) # 黑色阳极氧化铝 4040
C_WOOD    = (0.82, 0.65, 0.44) # 桦木海洋板木色
C_BRACKET = (0.88, 0.15, 0.15) # 🔴 红色：隐藏式抗震角码
C_ACRYLIC = (0.15, 0.15, 0.18) # 黑透：亚克力抽屉模块
C_THROUGH = (0.00, 0.70, 0.90) # 🔵 青色：沉头打孔穿芯 (走中心孔)
C_ANCHOR  = (0.70, 0.20, 0.90) # 🟣 紫色：锚式销钉连接 (走表面T槽)
C_SILVER  = (0.78, 0.78, 0.82) # ⚪ 银色：楼梯柜重型滑轨

# 设备配色
C_S1      = (0.15, 0.16, 0.18) # S1 深空灰
C_P1S     = (0.28, 0.29, 0.31) # P1S 金属灰
C_L4      = (0.18, 0.20, 0.24) # L4 工业黑
C_CANON   = (0.20, 0.21, 0.23) # 佳能 MF113w 商务黑灰
C_AMS     = (0.88, 0.88, 0.90) # AMS 白透

# ----------------- 核心实体生成器 -----------------
def create_cube(dx, dy, dz, x, y, z, name, color, transparency=0):
    box = Part.makeBox(dx, dy, dz)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = box
    obj.Placement = App.Placement(App.Vector(x, y, z), App.Rotation(0, 0, 0))
    obj.ViewObject.ShapeColor = color
    if transparency > 0: obj.ViewObject.Transparency = transparency
    return obj

def create_through_marker(x, y, z): 
    create_cube(42, 42, 42, x-1, y-1, z-21, f"Through_Z{int(z)}_X{int(x)}", C_THROUGH, 30)

def create_anchor_y(x, y, z): 
    create_cube(42, 42, 42, x-1, y-21, z-1, f"Anchor_Y_X{int(x)}_Y{int(y)}", C_ANCHOR, 50)

def create_anchor_x(x, y, z): 
    create_cube(42, 42, 42, x-21, y-1, z-1, f"Anchor_X_X{int(x)}_Z{int(z)}", C_ANCHOR, 50)

# ==============================================================================
# 1. 铝型材骨架系统 (4040 刚性闭环)
# ==============================================================================
create_cube(1400, 40, 40,  0, 0, 0,        "Beam_X_Bot_Front", C_ALUM)
create_cube(1400, 40, 40,  0, 760, 0,      "Beam_X_Bot_Back",  C_ALUM)
create_cube(1400, 40, 40,  0, 0, 660,      "Beam_X_Top_Front", C_ALUM)
create_cube(1400, 40, 40,  0, 760, 660,    "Beam_X_Top_Back",  C_ALUM)

create_cube(700, 40, 40,   40, 760, 360,   "Beam_X_Back_Mid_LeftSeg",  C_ALUM)
create_cube(580, 40, 40,   780, 760, 360,  "Beam_X_Back_Mid_RightSeg", C_ALUM)

for x in [0, 740, 1360]:
    create_cube(40, 40, 620,  x, 0, 40,    f"Col_X{x}_Front", C_ALUM)
    create_cube(40, 40, 620,  x, 760, 40,  f"Col_X{x}_Back",  C_ALUM)

y_beams_z0   = [0, 190, 550, 740, 1050, 1360] 
y_beams_z660 = [0, 370, 740, 1050, 1360]       
y_beams_z360 = [0, 740, 1360]                  
y_beams_z520 = [0, 740]                        

for x in y_beams_z0:   create_cube(40, 720, 40, x, 40, 0,   f"Beam_Y_Bot_X{x}", C_ALUM)
for x in y_beams_z660: create_cube(40, 720, 40, x, 40, 660, f"Beam_Y_Top_X{x}", C_ALUM)
for x in y_beams_z360: create_cube(40, 720, 40, x, 40, 360, f"Beam_Y_Mid_X{x}", C_ALUM)
for x in y_beams_z520: create_cube(40, 720, 40, x, 40, 520, f"Beam_Y_Drawer_X{x}", C_ALUM)

# ==============================================================================
# 2. 🔵 青色：沉头打孔穿芯阵列 (12 处)
# ==============================================================================
for x in [0, 740, 1360]:
    for y in [0, 760]:
        create_through_marker(x, y, 40)  
        create_through_marker(x, y, 660) 

# ==============================================================================
# 3. 🟣 紫色：锚式连接阵列
# ==============================================================================
for x in y_beams_z0:   create_anchor_y(x, 40, 0);   create_anchor_y(x, 760, 0)
for x in y_beams_z660: create_anchor_y(x, 40, 660); create_anchor_y(x, 760, 660)
for x in y_beams_z360: create_anchor_y(x, 40, 360); create_anchor_y(x, 760, 360)
for x in y_beams_z520: create_anchor_y(x, 40, 520); create_anchor_y(x, 760, 520)

create_anchor_x(40, 760, 360);  create_anchor_x(740, 760, 360)  
create_anchor_x(780, 760, 360); create_anchor_x(1360, 760, 360) 

# ==============================================================================
# 4. 🔴 红色：20 个防震角码阵列
# ==============================================================================
create_cube(35, 28, 35, 40, 766, 625,   "B_Back_LT", C_BRACKET)
create_cube(35, 28, 35, 40, 766, 40,    "B_Back_LB", C_BRACKET)
create_cube(35, 28, 35, 1325, 766, 625, "B_Back_RT", C_BRACKET)
create_cube(35, 28, 35, 1325, 766, 40,  "B_Back_RB", C_BRACKET)

create_cube(35, 28, 35, 705, 766, 400,  "B_Cross_LT", C_BRACKET)
create_cube(35, 28, 35, 780, 766, 400,  "B_Cross_RT", C_BRACKET)
create_cube(35, 28, 35, 705, 766, 325,  "B_Cross_LB", C_BRACKET)
create_cube(35, 28, 35, 780, 766, 325,  "B_Cross_RB", C_BRACKET)

create_cube(28, 35, 35, 1366, 40, 625,  "B_Right_FT", C_BRACKET)
create_cube(28, 35, 35, 1366, 40, 40,   "B_Right_FB", C_BRACKET)
create_cube(28, 35, 35, 1366, 725, 625, "B_Right_BT", C_BRACKET)
create_cube(28, 35, 35, 1366, 725, 40,  "B_Right_BB", C_BRACKET)

create_cube(28, 35, 35, 6, 40, 625,     "B_Left_FT", C_BRACKET)
create_cube(28, 35, 35, 6, 40, 40,      "B_Left_FB", C_BRACKET)
create_cube(28, 35, 35, 6, 725, 625,    "B_Left_BT", C_BRACKET)
create_cube(28, 35, 35, 6, 725, 40,     "B_Left_BB", C_BRACKET)

create_cube(28, 35, 35, 746, 40, 625,   "B_Mid_FT", C_BRACKET)
create_cube(28, 35, 35, 746, 40, 40,    "B_Mid_FB", C_BRACKET)
create_cube(28, 35, 35, 746, 725, 625,  "B_Mid_BT", C_BRACKET)
create_cube(28, 35, 35, 746, 725, 40,   "B_Mid_BB", C_BRACKET)

# ==============================================================================
# 5. ⚪ 底层重型滑轨 (靠外并排安装)
# ==============================================================================
create_cube(30, 600, 53, 160, 60, 0, "Slide_Heavy_Left",  C_SILVER) 
create_cube(30, 600, 53, 590, 60, 0, "Slide_Heavy_Right", C_SILVER) 

# ==============================================================================
# 6. 板材与抽屉系统
# ==============================================================================
create_cube(1400, 800, 24, 0, 0, 700,   "Wood_Top_Board", C_WOOD, 20)
create_cube(580, 720, 18,  780, 40, 40, "Wood_P1S_Base",  C_WOOD, 10)
create_cube(650, 650, 18,  65, 60, 53,  "Wood_Laser_Tray", C_WOOD, 10)
create_cube(674, 550, 120, 53, 60, 365, "Drawer_Mid_Cyber", C_ACRYLIC, 60)
create_cube(674, 550, 100, 53, 60, 525, "Drawer_Top_Cyber", C_ACRYLIC, 60)

# ==============================================================================
# 7. 设备高精建模与就位 (已同步 X=60 与同轴布局)
# ==============================================================================
# (1) 底层 xTool S1
create_cube(600, 500, 190, 90, 90, 71,  "Machine_xTool_S1", C_S1, 30)

# (2) 底层 Bambu Lab P1S
create_cube(389, 389, 457, 875.5, 90, 58, "Machine_Bambu_P1S", C_P1S, 30)

# (3) ★ 桌面 LightMake L4 (已更新为 X=60, Y=130) ★
create_cube(615, 624, 677, 60, 130, 724, "Machine_LightMake_L4", C_L4, 20)

# (4) 桌面 佳能 MF113w (同轴中心 X=1070)
create_cube(372, 320, 255, 884, 60, 724, "Machine_Canon_MF113w", C_CANON, 20)

# (5) 桌面 Bambu AMS (同轴中心 X=1070)
create_cube(368, 271, 224, 886, 460, 724, "Machine_Bambu_AMS", C_AMS, 30)

# ==============================================================================
# 8. 刷新视角
# ==============================================================================
App.ActiveDocument.recompute()
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxometric()
    Gui.ActiveDocument.ActiveView.fitAll()
except: pass

print("✅ FreeCAD V19.2 同步完成：L4 已更新至 X=60，桌面同轴与底层设备全要素闭环！")
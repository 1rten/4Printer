import FreeCAD as App
import Part
from FreeCAD import Base
import math

doc_name = "Detailed_Toddler_Shoe_150mm"
if doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# 核心剖面数据
# (x, y_med_sole, y_lat_sole, y_med_up, y_lat_up, z_sole, z_up, roundness)
key_specs = [
    ( -5.0,   8,   8,   6,   6,  8,  22, 0.60 ),
    (  5.0,  26,  26,  23,  23, 10,  50, 0.70 ),
    ( 20.0,  30,  30,  27,  27, 10,  55, 0.75 ),
    ( 40.0,  29,  31,  26,  28, 10,  55, 0.80 ),
    ( 60.0,  28,  31,  25,  28, 10,  51, 0.82 ),
    ( 80.0,  33,  35,  30,  32, 10,  46, 0.85 ),
    (105.0,  41,  38,  37,  35, 10,  42, 0.88 ),
    (125.0,  38,  36,  34,  32, 10,  37, 0.88 ),
    (140.0,  33,  30,  29,  26, 12,  30, 0.85 ),
    (155.0,  22,  20,  18,  16, 16,  24, 0.75 ),
    (163.0,   8,   8,   5,   5, 18,  19, 0.60 ),
]

def interpolate_specs(specs, steps_per_segment=4):
    dense = []
    for i in range(len(specs)-1):
        s1 = specs[i]
        s2 = specs[i+1]
        for j in range(steps_per_segment):
            t = j / steps_per_segment
            # 线性插值
            interp = tuple(s1[k]*(1-t) + s2[k]*t for k in range(len(s1)))
            dense.append(interp)
    dense.append(specs[-1])
    return dense

dense_specs = interpolate_specs(key_specs, 5) # 生成 50+ 个剖面，实现伪平滑

def make_sole_wire(x, ym, yl, z_s):
    z_bot = z_s * 0.2 if x > 140 else 0.0
    pts = [
        Base.Vector(x, 0, z_bot - 1),
        Base.Vector(x, ym * 0.9, z_bot),
        Base.Vector(x, ym, z_s * 0.5),
        Base.Vector(x, ym * 0.95, z_s),
        Base.Vector(x, 0, z_s + 0.5),
        Base.Vector(x, -yl * 0.95, z_s),
        Base.Vector(x, -yl, z_s * 0.5),
        Base.Vector(x, -yl * 0.9, z_bot),
    ]
    bs = Part.BSplineCurve()
    bs.interpolate(pts, PeriodicFlag=True)
    return Part.Wire(bs.toShape())

def make_upper_wire(x, ym, yl, z_s, z_u, rnd):
    z_mid = z_s + (z_u - z_s) * 0.45
    pts = [
        Base.Vector(x, 0, z_s),
        Base.Vector(x, ym * 0.95, z_s),
        Base.Vector(x, ym, z_mid),
        Base.Vector(x, ym * rnd, z_u - 2),
        Base.Vector(x, 0, z_u),
        Base.Vector(x, -yl * rnd, z_u - 2),
        Base.Vector(x, -yl, z_mid),
        Base.Vector(x, -yl * 0.95, z_s),
    ]
    bs = Part.BSplineCurve()
    bs.interpolate(pts, PeriodicFlag=True)
    return Part.Wire(bs.toShape())

sole_wires = []
upper_wires = []
for spec in dense_specs:
    sole_wires.append(make_sole_wire(spec[0], spec[1], spec[2], spec[5]))
    upper_wires.append(make_upper_wire(spec[0], spec[3], spec[4], spec[5], spec[6], spec[7]))

# 注意：恢复 Ruled=True！通过极高密度的截面来实现视觉上的丝滑，避免 NURBS 曲面失控膨胀
sole_body = Part.makeLoft(sole_wires, True, True)
upper_body = Part.makeLoft(upper_wires, True, True)

# 内腔控制点
key_inner_specs = [
    (  4.0,  22, 22, 11, 60, 0.75 ),
    ( 20.0,  24, 24, 11, 65, 0.75 ),
    ( 40.0,  24, 25, 11, 65, 0.80 ),
    ( 60.0,  23, 25, 11, 60, 0.82 ),
    ( 80.0,  27, 29, 11, 42, 0.85 ),
    (105.0,  34, 32, 11, 38, 0.88 ),
    (125.0,  31, 29, 11, 33, 0.85 ),
    (140.0,  26, 23, 13, 26, 0.80 ),
    (154.0,  12, 10, 15, 19, 0.70 ),
]
dense_inner_specs = interpolate_specs(key_inner_specs, 6)

inner_wires = []
for spec in dense_inner_specs:
    inner_wires.append(make_upper_wire(spec[0], spec[1], spec[2], spec[3], spec[4], spec[5]))
inner_cavity = Part.makeLoft(inner_wires, True, True)

# 领口海绵圈
rim_padding = Part.makeTorus(26, 4.0, Base.Vector(42, 0, 48), Base.Vector(0.2, 0, 1))
try:
    rim_padding = rim_padding.cut(inner_cavity)
except:
    pass

# 防踢鞋头
toe_bumper_cutter = Part.makeBox(40, 100, 40, Base.Vector(135, -50, 0))
toe_bumper_solid = upper_body.common(toe_bumper_cutter)
toe_bumper = toe_bumper_solid 

# 魔术贴绑带
strap_base = Part.makeBox(25, 60, 4, Base.Vector(65, -30, 45))
strap_curved = strap_base 

# 鞋底防滑槽
grooves = []
for x_pos in range(25, 140, 15):
    groove = Part.makeCylinder(2.5, 90, Base.Vector(x_pos, -45, -1), Base.Vector(0, 1, 0))
    grooves.append(groove)
if grooves:
    tool_compound = Part.makeCompound(grooves)
    try:
        sole_body = sole_body.cut(tool_compound)
    except:
        pass

# TPU 透气孔
vent_holes = []
for x_pos in [90, 105, 120, 135]:
    for y_pos in [0, 15, -15, 28, -28]:
        if x_pos == 90 and abs(y_pos) > 20: continue
        if x_pos == 135 and abs(y_pos) > 20: continue
        cyl = Part.makeCylinder(3.5, 60, Base.Vector(x_pos, y_pos, 60), Base.Vector(0, 0, -1))
        vent_holes.append(cyl)
        if abs(y_pos) == 28 and x_pos in [105, 120]:
            y_dir = 1 if y_pos > 0 else -1
            cyl_side = Part.makeCylinder(3.5, 60, Base.Vector(x_pos, 0, 20), Base.Vector(0, y_dir, 0))
            vent_holes.append(cyl_side)

if vent_holes:
    vent_compound = Part.makeCompound(vent_holes)
    try:
        upper_with_holes = upper_body.cut(vent_compound)
    except:
        upper_with_holes = upper_body
    
    try:
        upper_final = upper_with_holes.cut(inner_cavity)
    except:
        upper_final = upper_with_holes
else:
    upper_final = upper_body.cut(inner_cavity)

parts = {
    "Sole_Rubber": (sole_body, (0.9, 0.9, 0.9)),
    "Upper_Fabric": (upper_final, (0.3, 0.6, 0.9)),
    "Collar_Padding": (rim_padding, (0.7, 0.7, 0.75)),
    "Toe_Bumper": (toe_bumper, (0.9, 0.9, 0.9)),
    "Velcro_Strap": (strap_curved, (0.2, 0.5, 0.8))
}

for name, (shape, color) in parts.items():
    if shape.Volume > 0:
        obj = Part.show(shape, name)
        if hasattr(obj, "ViewObject") and obj.ViewObject:
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Deviation = 0.05 
            obj.ViewObject.AngularDeflection = 10.0

doc.recompute()
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxometric()
    Gui.ActiveDocument.ActiveView.fitAll()
except:
    pass

try:
    bbox = Part.makeCompound([sole_body, upper_final]).BoundBox
    print(f"✅ 高精度幼儿学步鞋模型生成完毕！")
    print(f"外包围盒: 长 {bbox.XLength:.1f}mm, 宽 {bbox.YLength:.1f}mm, 高 {bbox.ZLength:.1f}mm")
except:
    pass

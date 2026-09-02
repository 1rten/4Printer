// =============================================================================
// 1400x800x700mm 工业级重型工作站 (V19.4 桌面同轴对齐定型版)
// =============================================================================
// 核心更新说明:
// 1. 桌面右侧同轴布局: 佳能 MF113w 与 Bambu AMS 共享同一中心线 (X = 1070mm)。
//    - 前部: 佳能 MF113w (372x320x255mm, Y=60..380), 方便抽纸、取件与扫描。
//    - 后部: Bambu AMS (368x271x224mm, Y=460..731), 垂直对准底舱 P1S, 料管极短。
// 2. 桌面左侧: LightMake L4 四头 3D 打印机 (615x624x677mm), 正压加劲梁。
// 3. 中岛通道: L4 与右侧设备群之间留出 244mm 纯平操作区 (放键鼠/工具)。
// 4. 底层重载: 600mm 楼梯柜滑轨靠外并排 (Z=0..53), 托盘 Z=53 出舱超前横梁 13mm。
// =============================================================================

$fn = 32;

// ==========================================
// 1. 全局几何与物理参数定义
// ==========================================
frame_w          = 1400;  
frame_d          = 800;   
frame_h          = 700;   
p_size           = 40;    

t_top            = 24;    // 桌面厚 24mm 桦木板
t_p1s_base       = 18;    
t_laser_base     = 18;    
t_drawer_wood    = 15;    

left_bay_w       = 700;   
mid_x            = p_size + left_bay_w;      // 740
right_bay_w      = frame_w - mid_x - p_size; // 580

slide_gap_45     = 13;    
drawer_depth     = 550;   
laser_tray_w     = 650;   
laser_tray_d     = 650;   
slide_heavy_len  = 600;   
slide_heavy_w    = 30;    
slide_heavy_h    = 53;    

beam_left_x      = p_size + 150;             // 190
beam_right_x     = mid_x - 150 - p_size;     // 550
left_mid_beam_x  = p_size + (left_bay_w - p_size) / 2;       // 370
right_mid_beam_x = mid_x + p_size + (right_bay_w - p_size) / 2; // 1050

z_mid_beam       = 360;   
z_top_beam       = 520;   

// 配色库
c_alum    = [0.22, 0.23, 0.25, 1.0]; 
c_bracket = [0.88, 0.15, 0.15, 1.0]; 
c_through = [0.00, 0.70, 0.90, 0.4]; 
c_anchor  = [0.70, 0.20, 0.90, 0.4]; 
c_silver  = [0.78, 0.78, 0.82, 1.0]; 
c_wood    = [0.82, 0.65, 0.44, 0.95];
c_drawer  = [0.15, 0.15, 0.18, 0.8]; 

// 设备配色
c_s1_body = [0.15, 0.16, 0.18, 0.9];
c_s1_lid  = [0.10, 0.45, 0.35, 0.5];
c_p1s     = [0.28, 0.29, 0.31, 0.9];
c_ams     = [0.88, 0.88, 0.90, 0.85];
c_l4_body = [0.18, 0.20, 0.24, 0.95];
c_l4_door = [0.10, 0.60, 0.75, 0.4]; 
c_mf113   = [0.20, 0.21, 0.23, 0.95]; // 佳能深黑灰质感商务机身

// ==========================================
// 2. 连接件打孔标记模块
// ==========================================
module marker_through(x, y, z) {
    color(c_through) translate([x - 1, y - 1, z - 21]) cube([42, 42, 42]);
}

module marker_anchor_y(x, y, z) {
    color(c_anchor) translate([x - 1, y - 21, z - 1]) cube([42, 42, 42]);
}

module marker_anchor_x(x, y, z) {
    color(c_anchor) translate([x - 21, y - 1, z - 1]) cube([42, 42, 42]);
}

// ==========================================
// 3. 铝型材骨架系统
// ==========================================
module aluminum_frame() {
    color(c_alum) {
        translate([0, 0, 0]) cube([frame_w, p_size, p_size]);
        translate([0, frame_d - p_size, 0]) cube([frame_w, p_size, p_size]);
        translate([0, 0, frame_h - p_size]) cube([frame_w, p_size, p_size]);
        translate([0, frame_d - p_size, frame_h - p_size]) cube([frame_w, p_size, p_size]);

        translate([p_size, frame_d - p_size, z_mid_beam]) cube([left_bay_w, p_size, p_size]);
        translate([mid_x + p_size, frame_d - p_size, z_mid_beam]) cube([right_bay_w, p_size, p_size]);

        for (x_pos = [0, mid_x, frame_w - p_size]) {
            for (y_pos = [0, frame_d - p_size]) {
                translate([x_pos, y_pos, p_size]) cube([p_size, p_size, frame_h - 2 * p_size]);
            }
        }

        y_beams_z0   = [0, beam_left_x, beam_right_x, mid_x, right_mid_beam_x, frame_w - p_size];
        y_beams_z660 = [0, left_mid_beam_x, mid_x, right_mid_beam_x, frame_w - p_size];
        y_beams_z360 = [0, mid_x, frame_w - p_size];
        y_beams_z520 = [0, mid_x];

        for (x = y_beams_z0)   translate([x, p_size, 0]) cube([p_size, frame_d - 2 * p_size, p_size]);
        for (x = y_beams_z660) translate([x, p_size, frame_h - p_size]) cube([p_size, frame_d - 2 * p_size, p_size]);
        for (x = y_beams_z360) translate([x, p_size, z_mid_beam]) cube([p_size, frame_d - 2 * p_size, p_size]);
        for (x = y_beams_z520) translate([x, p_size, z_top_beam]) cube([p_size, frame_d - 2 * p_size, p_size]);
    }
}

// ==========================================
// 4. 🔴 红色：20 个防震角码
// ==========================================
module corner_brackets() {
    color(c_bracket) {
        translate([40, 766, 625])   cube([35, 28, 35]);
        translate([40, 766, 40])    cube([35, 28, 35]);
        translate([1325, 766, 625]) cube([35, 28, 35]);
        translate([1325, 766, 40])  cube([35, 28, 35]);

        translate([705, 766, 400])  cube([35, 28, 35]);
        translate([780, 766, 400])  cube([35, 28, 35]);
        translate([705, 766, 325])  cube([35, 28, 35]);
        translate([780, 766, 325])  cube([35, 28, 35]);

        translate([1366, 40, 625])  cube([28, 35, 35]);
        translate([1366, 40, 40])   cube([28, 35, 35]);
        translate([1366, 725, 625]) cube([28, 35, 35]);
        translate([1366, 725, 40])  cube([28, 35, 35]);

        translate([6, 40, 625])     cube([28, 35, 35]);
        translate([6, 40, 40])      cube([28, 35, 35]);
        translate([6, 725, 625])    cube([28, 35, 35]);
        translate([6, 725, 40])     cube([28, 35, 35]);

        translate([746, 40, 625])   cube([28, 35, 35]);
        translate([746, 40, 40])    cube([28, 35, 35]);
        translate([746, 725, 625])  cube([28, 35, 35]);
        translate([746, 725, 40])   cube([28, 35, 35]);
    }
}

// ==========================================
// 5. 连接件标记模块
// ==========================================
module connectors_and_machining() {
    for (x = [0, mid_x, frame_w - p_size]) {
        for (y = [0, frame_d - p_size]) {
            marker_through(x, y, p_size);              
            marker_through(x, y, frame_h - p_size);    
        }
    }

    y_beams_z0   = [0, beam_left_x, beam_right_x, mid_x, right_mid_beam_x, frame_w - p_size];
    y_beams_z660 = [0, left_mid_beam_x, mid_x, right_mid_beam_x, frame_w - p_size];
    y_beams_z360 = [0, mid_x, frame_w - p_size];
    y_beams_z520 = [0, mid_x];

    for (x = y_beams_z0)   { marker_anchor_y(x, p_size, 0);   marker_anchor_y(x, frame_d - p_size, 0); }
    for (x = y_beams_z660) { marker_anchor_y(x, p_size, 660); marker_anchor_y(x, frame_d - p_size, 660); }
    for (x = y_beams_z360) { marker_anchor_y(x, p_size, 360); marker_anchor_y(x, frame_d - p_size, 360); }
    for (x = y_beams_z520) { marker_anchor_y(x, p_size, 520); marker_anchor_y(x, frame_d - p_size, 520); }

    marker_anchor_x(p_size, frame_d - p_size, z_mid_beam);
    marker_anchor_x(mid_x, frame_d - p_size, z_mid_beam);
    marker_anchor_x(mid_x + p_size, frame_d - p_size, z_mid_beam);
    marker_anchor_x(frame_w - p_size, frame_d - p_size, z_mid_beam);
}

// ==========================================
// 6. 板材、抽屉与底层重型滑轨
// ==========================================
module furnishings() {
    // 顶部台面 (1400x800x24)
    color(c_wood) translate([0, 0, frame_h]) cube([frame_w, frame_d, t_top]);

    // P1S 承重底板 (580x720x18)
    color(c_wood) translate([mid_x + p_size, p_size, p_size]) cube([right_bay_w, frame_d - 2 * p_size, t_p1s_base]);

    // 楼梯柜滑轨 (靠外安装并排, Z=0..53)
    color(c_silver) {
        translate([beam_left_x - slide_heavy_w, p_size + 20, 0]) cube([slide_heavy_w, slide_heavy_len, slide_heavy_h]);
        translate([beam_right_x + p_size, p_size + 20, 0])       cube([slide_heavy_w, slide_heavy_len, slide_heavy_h]);
    }

    // 激光拉盘托盘 (650x650x18, 底面 Z=53)
    color(c_wood) translate([p_size + (left_bay_w - laser_tray_w) / 2, p_size + 20, slide_heavy_h])
        cube([laser_tray_w, laser_tray_d, t_laser_base]);

    // 双层大抽屉
    drawer_w = left_bay_w - 2 * slide_gap_45;
    color(c_drawer) translate([p_size + slide_gap_45, p_size + 20, 365])
        cube([drawer_w, drawer_depth, 120]);
    color(c_drawer) translate([p_size + slide_gap_45, p_size + 20, 525])
        cube([drawer_w, drawer_depth, 100]);
}

// ==========================================
// 7. 设备高精建模与就位 (同轴对齐体系)
// ==========================================
module machines_suite() {
    desk_z = frame_h + t_top; // Z = 724mm
    axis_right_x = 1070;      // ★ 右侧共享中心轴线 (X = 1070mm) ★

    // --------------------------------------------------
    // (1) [底层左舱] xTool S1 激光雕刻机
    // --------------------------------------------------
    s1_x = p_size + (left_bay_w - 600) / 2;
    s1_y = p_size + 50;
    s1_z = slide_heavy_h + t_laser_base; // Z = 71mm
    color(c_s1_body) translate([s1_x, s1_y, s1_z]) cube([600, 500, 150]);
    color(c_s1_lid)  translate([s1_x + 30, s1_y + 30, s1_z + 150]) cube([540, 440, 40]);

    // --------------------------------------------------
    // (2) [底层右舱] Bambu Lab P1S 打印机 (轴线 X=1070)
    // --------------------------------------------------
    p1s_x = axis_right_x - 389 / 2; // X = 875.5
    p1s_y = p_size + 50;            // Y = 90
    p1s_z = p_size + t_p1s_base;    // Z = 58mm
    color(c_p1s) translate([p1s_x, p1s_y, p1s_z]) cube([389, 389, 457]);
    color([0.1, 0.1, 0.12, 0.4]) translate([p1s_x + 20, p1s_y - 2, p1s_z + 30]) cube([349, 4, 400]);

    // --------------------------------------------------
    // (3) [桌面左侧] LightMake L4 四头 3D 打印机 (615x624x677mm)
    // --------------------------------------------------
    l4_x = 60; 
    l4_y = 60; 
    color(c_l4_body) translate([l4_x, l4_y, desk_z]) cube([615, 624, 677]);
    color(c_l4_door) translate([l4_x + 30, l4_y - 2, desk_z + 100]) cube([555, 4, 520]);

    // --------------------------------------------------
    // (4) [桌面右前] 佳能 MF113w 多功能一体机 (372x320x255mm)
    // 轴线居中: X_center = 1070mm -> X = 1070 - 372/2 = 884mm
    // --------------------------------------------------
    mf113_w = 372;
    mf113_d = 320;
    mf113_h = 255;
    mf113_x = axis_right_x - mf113_w / 2; // X = 884
    mf113_y = 60;                         // 距桌面前沿 60mm
    
    // MF113w 深灰黑商务主机身
    color(c_mf113) translate([mf113_x, mf113_y, desk_z]) cube([mf113_w, mf113_d, 195]);
    // 顶部平板扫描仪翻盖
    color([0.28, 0.29, 0.31, 0.95]) translate([mf113_x + 10, mf113_y + 10, desk_z + 195]) 
        cube([mf113_w - 20, mf113_d - 20, 60]);
    // 操作面板小显示屏
    color([0.1, 0.7, 0.4, 0.8]) translate([mf113_x + 30, mf113_y + 5, desk_z + 200]) 
        cube([70, 10, 30]);

    // --------------------------------------------------
    // (5) [桌面右后] Bambu AMS 四色供料系统 (368x271x224mm)
    // 轴线居中: X_center = 1070mm -> X = 1070 - 368/2 = 886mm (同轴串联)
    // --------------------------------------------------
    ams_w = 368;
    ams_d = 271;
    ams_h = 224;
    ams_x = axis_right_x - ams_w / 2;    // X = 886
    ams_y = mf113_y + mf113_d + 80;      // Y = 60 + 320 + 80 = 460mm (留出80mm检修翻盖余量)

    color(c_ams) translate([ams_x, ams_y, desk_z]) cube([ams_w, ams_d, ams_h]);
    // AMS 翻盖透明窗
    color([0.9, 0.9, 0.95, 0.4]) translate([ams_x + 10, ams_y + 10, desk_z + 180]) 
        cube([ams_w - 20, ams_d - 20, 44]);
}

// ==========================================
// 8. 最终总装调用
// ==========================================
aluminum_frame();
corner_brackets();
connectors_and_machining();
furnishings();
machines_suite();
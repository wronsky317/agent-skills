"""
coord_utils.py
WGS84 坐标变换工具函数集，移植自 trace_runner/src/base/Geometry.h

用法:
    from coord_utils import wgs84_to_enu, enu_to_body, wgs84_to_local
"""
import math

_PI = 3.141592653589793
_D2R = _PI / 180.0
_WGS84_RE = 6378137.0
_WGS84_F = 1.0 / 298.257223563


def _rm_rn(lat_deg):
    """WGS84 曲率半径 (移植自 Geometry.h::rm_rn)"""
    sinL = math.sin(lat_deg * _D2R)
    Rm = _WGS84_RE * (1 - 2.0 * _WGS84_F + 3 * _WGS84_F * sinL * sinL)
    Rn = (_WGS84_RE * (1 + _WGS84_F * sinL * sinL)) * math.cos(lat_deg * _D2R)
    return Rm, Rn


def wgs84_to_enu(lon, lat, lon0, lat0):
    """WGS84 → 局部 ENU (East-North-Up)
    
    Args:
        lon, lat: 目标点经纬度 (度)
        lon0, lat0: 参考原点经纬度 (度)
    Returns:
        (dE, dN): 东向偏移(m), 北向偏移(m)
    """
    Rm, Rn = _rm_rn(lat0)
    dE = (lon - lon0) * _D2R * Rn
    dN = (lat - lat0) * _D2R * Rm
    return dE, dN


def enu_to_body(dE, dN, heading_deg):
    """ENU → 车体局部坐标
    
    Args:
        dE, dN: ENU 偏移 (m)
        heading_deg: 北偏东方位角 (度)
    Returns:
        (x_lateral, y_forward): x=右侧为正, y=前进方向为正
    """
    h = heading_deg * _D2R
    x_lateral = dE * math.cos(h) - dN * math.sin(h)
    y_forward = dE * math.sin(h) + dN * math.cos(h)
    return x_lateral, y_forward


def wgs84_to_local(lon, lat, lon0, lat0, heading_deg):
    """WGS84 → 车体局部坐标 (一步到位)
    
    Args:
        lon, lat: 目标点经纬度 (度)
        lon0, lat0: 参考原点经纬度 (度)
        heading_deg: 车辆航向角, 北偏东 (度)
    Returns:
        (x_lateral, y_forward): 车体坐标 (m)
    """
    dE, dN = wgs84_to_enu(lon, lat, lon0, lat0)
    return enu_to_body(dE, dN, heading_deg)


# ============================================================
# TileInfo: Morton code (移植自 TileInfo.h)
# ============================================================
def xy_to_tile_xy(lon, lat, zoom):
    """经纬度 → tile 像素坐标"""
    tile_num = 1 << zoom
    x = int((lon + 180.0) / (360.0 / tile_num))
    y = int((lat + 90.0) / (180.0 / tile_num))
    y = tile_num - y - 1
    return x, y


def encode_tile(x, y, zoom):
    """tile 坐标 → Morton code"""
    if y < 0:
        y += 0x7FFFFFFF
    bit = 1
    morton = 0
    for i in range(32):
        morton |= ((x & bit) << i) | ((y & bit) << (i + 1))
        bit <<= 1
    return (morton + (1 << (16 + zoom))) & 0x0FFFFFFFF


def get_tile_ids(lon, lat, zoom=15):
    """获取中心点 3x3 邻域 tile IDs"""
    tx, ty = xy_to_tile_xy(lon, lat, zoom)
    return [encode_tile(tx + i, ty + j, zoom)
            for i in range(-1, 2) for j in range(-1, 2)]


# ============================================================
# Liang-Barsky 裁剪
# ============================================================
def clip_segment(x1, y1, x2, y2, lateral=50, forward=100):
    """Liang-Barsky 线段裁剪到矩形 [-lateral, lateral] x [-forward, forward]
    
    Returns:
        (cx1, cy1, cx2, cy2) 或 None (线段在窗口外)
    """
    dx, dy = x2 - x1, y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 + lateral, lateral - x1, y1 + forward, forward - y1]
    u0, u1 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return None
        else:
            r = qi / pi
            if pi < 0:
                u0 = max(u0, r)
            else:
                u1 = min(u1, r)
            if u0 > u1:
                return None
    return (x1 + u0 * dx, y1 + u0 * dy, x1 + u1 * dx, y1 + u1 * dy)


def clip_polyline(pts, lateral=50, forward=100):
    """将折线裁剪到矩形窗口, 返回 (xs, ys) 用 None 分隔不连续段
    
    Args:
        pts: [(x, y), ...] 局部坐标点序列
        lateral: 左右范围 (m)
        forward: 前后范围 (m)
    Returns:
        (xs, ys): 含 None 分隔符的坐标列表
    """
    xs, ys = [], []
    prev_inside = False
    for i in range(len(pts) - 1):
        clipped = clip_segment(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                               lateral, forward)
        if clipped is None:
            prev_inside = False
            continue
        cx1, cy1, cx2, cy2 = clipped
        if not prev_inside:
            if xs:
                xs.append(None)
                ys.append(None)
            xs.append(cx1)
            ys.append(cy1)
        xs.append(cx2)
        ys.append(cy2)
        prev_inside = (abs(cx2 - pts[i+1][0]) < 1e-9 and
                       abs(cy2 - pts[i+1][1]) < 1e-9)
    return xs, ys

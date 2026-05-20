#!/usr/bin/env python3
"""
scaffold_viser.py
快速生成新的 Streamlit 地图可视化页面骨架

用法:
    python .qoder/skills/map-viser-page/scripts/scaffold_viser.py <page_name> [--with-lnds] [--with-lvis]

示例:
    python .qoder/skills/map-viser-page/scripts/scaffold_viser.py fusion
    → 生成 visers/fusion_viser.py

    python .qoder/skills/map-viser-page/scripts/scaffold_viser.py debug --with-lnds --with-lvis
    → 生成 visers/debug_viser.py (含 LNDS 路网 + LVIS 信号模板)
"""
import argparse
import os
import sys
import textwrap


def generate_header(page_name, title, icon):
    return textwrap.dedent(f'''\
        """
        {page_name}_viser.py
        可视化页面: {title}

        用法: streamlit run visers/{page_name}_viser.py
        """
        import os
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deps"))

        import math
        import numpy as np
        import streamlit as st
        import plotly.graph_objects as go

        try:
            import orjson as json_lib
        except ImportError:
            import json as json_lib

        from mars_utils.redis_db import rdb_class


        # 延迟导入 amap_client
        @st.cache_resource
        def _load_amap_module():
            from mars_utils.new_amap_client import amap_client as _ac, correct_amap_client_height as _ch
            return _ac, _ch


        st.set_page_config(page_title='{title}', page_icon='{icon}', layout='wide')

    ''')


def generate_sidebar():
    return textwrap.dedent('''\
        # ============================================================
        # Sidebar: Redis 连接配置
        # ============================================================
        url_params = st.query_params
        host = st.sidebar.text_input('host', value=url_params.get('host', '11.166.9.42'))
        port = st.sidebar.text_input('port', value=int(url_params.get('port', '6391')))
        db = st.sidebar.text_input('db', value=int(url_params.get('db', '10')))
        case_idx = st.sidebar.number_input('case_idx', value=int(url_params.get('case_idx', '0')))
        password = ''

        page_key = f'{host}_{port}_{db}_{case_idx}'

    ''')


def generate_data_loading():
    return textwrap.dedent('''\
        # ============================================================
        # 加载数据
        # ============================================================
        def load_case(host, port, db, password, case_idx):
            rdb = rdb_class(host=host, port=int(port), pw=password)(db=int(db))
            return rdb.get(f'case_{case_idx}')


        case_data = load_case(host, int(port), int(db), password, case_idx)
        if case_data is None:
            st.error(f'case_{case_idx} not found in {host}:{port} db={db}')
            st.stop()

        info_list = case_data['info_list']
        if info_list and isinstance(info_list[0], str):
            info_list = [json_lib.loads(s) for s in info_list]

        n_points = len(info_list)
        st.sidebar.divider()
        st.sidebar.markdown(f'**共 {n_points} 个时刻**')
        min_sn = st.sidebar.number_input('min_sn', 0, n_points - 1, 0, key=f'{page_key}_min_sn')
        max_sn = st.sidebar.number_input('max_sn', 0, n_points - 1, n_points - 1, key=f'{page_key}_max_sn')
        sel_sn = st.sidebar.number_input('选择时刻 point_k', min_value=0, max_value=n_points - 1,
                                          value=0, key=f'{page_key}_sel_sn')

    ''')


def generate_gps_gt_helpers():
    return textwrap.dedent('''\
        # ============================================================
        # Helper: 提取 GPS / GT 信息
        # ============================================================
        def get_gps(info):
            """从 info 中提取 GPS: (lon, lat, alt, spd, azi) 或 None"""
            gps = info.get('gps')
            if not gps:
                return None
            g = gps[0] if isinstance(gps[0], (list, tuple)) else gps
            if len(g) < 4:
                return None
            return (g[2], g[3],
                    g[4] if len(g) > 4 else 0,
                    g[5] if len(g) > 5 else 0,
                    g[6] if len(g) > 6 else 0)


        def get_gt0(info):
            """从 info 中提取 GT0: (lon, lat, alt, spd, azi) 或 None"""
            gt0 = info.get('gt0')
            if not gt0:
                return None
            g = gt0[0]
            if g is None or len(g) < 10:
                return None
            try:
                azi = float(g[9]) if g[9] is not None else 0
                if azi < 0:
                    azi += 360
                vel = [float(v) if v is not None else 0 for v in g[4:7]]
                spd = float(np.linalg.norm(vel))
            except (TypeError, ValueError):
                return None
            return (g[1], g[2], g[3] if len(g) > 3 else 0, spd, azi)

    ''')


def generate_trajectory_collection():
    return textwrap.dedent('''\
        # ============================================================
        # 收集轨迹
        # ============================================================
        gps_points, gt_points = [], []
        for i, info in enumerate(info_list):
            if not (min_sn <= i <= max_sn):
                continue
            gps = get_gps(info)
            if gps:
                gps_points.append((i, gps[0], gps[1], gps[4]))
            gt = get_gt0(info)
            if gt:
                gt_points.append((i, gt[0], gt[1], gt[4]))

    ''')


def generate_map_panel():
    return textwrap.dedent('''\
        # ============================================================
        # 地图轨迹面板
        # ============================================================
        map_col, local_col = st.columns([0.45, 0.55])

        with map_col:
            st.subheader('地图轨迹')
            filter_cols = st.columns(2)
            show_gps = filter_cols[0].checkbox('GPS', value=True, key=f'{page_key}_show_gps')
            show_gt = filter_cols[1].checkbox('GT0', value=True, key=f'{page_key}_show_gt')

            map_points = []
            style_labels = []
            if show_gps and gps_points:
                for i, lon, lat, azi in gps_points:
                    map_points.append([lon, lat, azi, 1, 0, 0, 0, f"gps:{i}"])
                style_labels.append({"color": 0, "label": "gps"})
            if show_gt and gt_points:
                for i, lon, lat, azi in gt_points:
                    map_points.append([lon, lat, azi, 1, 4, 0, 0, f"gt0:{i}"])
                style_labels.append({"color": 4, "label": "gt0"})

            amap_client, correct_amap_client_height = _load_amap_module()
            component_height = correct_amap_client_height()
            amap_client(
                points=map_points if map_points else None,
                points_style_type_labels=style_labels if map_points else None,
                fit_view=True,
                key=f"amap_{page_key}_{show_gps}_{show_gt}_{len(map_points)}",
            )

    ''')


def generate_local_panel():
    return textwrap.dedent('''\
        # ============================================================
        # 局部坐标面板
        # ============================================================
        with local_col:
            info = info_list[sel_sn]
            gt0_data = get_gt0(info)
            if gt0_data:
                origin_lon, origin_lat, _, _, origin_heading = gt0_data
                st.subheader(f'局部视图 @ point_k={sel_sn}')
            else:
                gps_data = get_gps(info)
                if gps_data:
                    origin_lon, origin_lat, _, _, origin_heading = gps_data
                    st.subheader(f'局部视图 @ point_k={sel_sn} (gps)')
                else:
                    origin_lon, origin_lat, origin_heading = None, None, 0
                    st.subheader(f'局部视图 @ point_k={sel_sn} (无定位)')

            fig = go.Figure()

            # 自车标记
            fig.add_trace(go.Scatter(
                x=[0], y=[0], mode='markers', name='ego',
                marker=dict(color='black', size=14, symbol='triangle-up'),
            ))

            # TODO: 在此添加局部坐标元素渲染

            fig.update_layout(
                xaxis_title='横向/m (→右)',
                yaxis_title='纵向/m (→前)',
                yaxis=dict(scaleanchor='x', scaleratio=1),
                height=800,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

    ''')


def generate_lnds_section():
    return textwrap.dedent('''\
        # ============================================================
        # LNDS 路网相关配置 (Sidebar)
        # ============================================================
        st.sidebar.divider()
        st.sidebar.markdown('**LNDS Redis**')
        lnds_host = st.sidebar.text_input('lnds_host', value='11.166.9.42')
        lnds_port = st.sidebar.text_input('lnds_port', value='6380')
        lnds_db = st.sidebar.text_input('lnds_db', value='0')
        lnds_zoom = st.sidebar.number_input('lnds_zoom', value=15, min_value=10, max_value=18)

        # TODO: 添加 LNDS tile 获取与解析逻辑
        # 参考 visers/lnds_viser.py 中的 fetch_lnds_tiles / _parse_lnds_tile

    ''')


def generate_lvis_section():
    return textwrap.dedent('''\
        # ============================================================
        # LVIS / SRI 信号渲染模板
        # ============================================================
        _SHAPE_NORM = {
            1: 'LineString', 2: 'Polygon', 3: 'Point',
            'Polyline': 'LineString', 'LineString': 'LineString',
            'Polygon': 'Polygon', 'Point': 'Point',
        }
        LVIS_COLORS = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        ]

        # TODO: 添加 LVIS/SRI 元素渲染逻辑
        # 参考 visers/lvis_viser.py 中的 LVIS 道路元素绘制

    ''')


def main():
    parser = argparse.ArgumentParser(description='生成 Streamlit 地图可视化页面骨架')
    parser.add_argument('page_name', help='页面名称 (生成 visers/<name>_viser.py)')
    parser.add_argument('--with-lnds', action='store_true', help='包含 LNDS 路网模板')
    parser.add_argument('--with-lvis', action='store_true', help='包含 LVIS/SRI 信号模板')
    parser.add_argument('--title', default=None, help='页面标题')
    parser.add_argument('--icon', default='🗺️', help='页面图标')
    args = parser.parse_args()

    title = args.title or f'Case {args.page_name.upper()}'
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'visers')
    output_path = os.path.join(output_dir, f'{args.page_name}_viser.py')

    if os.path.exists(output_path):
        print(f'[ERROR] {output_path} already exists. Aborting.')
        sys.exit(1)

    parts = [
        generate_header(args.page_name, title, args.icon),
        generate_sidebar(),
        generate_data_loading(),
        generate_gps_gt_helpers(),
        generate_trajectory_collection(),
        generate_map_panel(),
        generate_local_panel(),
    ]

    if args.with_lnds:
        parts.append(generate_lnds_section())
    if args.with_lvis:
        parts.append(generate_lvis_section())

    content = '\n'.join(parts)

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'[OK] Generated: {output_path}')
    print(f'     Run: streamlit run visers/{args.page_name}_viser.py')


if __name__ == '__main__':
    main()

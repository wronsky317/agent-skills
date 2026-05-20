---
name: map-viser-page
description: 创建地图可视化前端页面（Streamlit + Plotly + 高德地图组件）。当用户提到"写一个可视化页面"、"新建viser"、"地图前端"、"轨迹可视化"、"创建streamlit页面"、"plotly可视化"时触发。
---

# 地图可视化页面创建

## 概述

基于项目现有的 `visers/` 目录规范，快速创建 Streamlit 地图可视化页面。页面通常包含：
- 高德地图轨迹展示（amap_client 自定义组件）
- Plotly 局部坐标图（LVIS/SRI/路网等元素）
- Redis 数据加载 + Sidebar 配置面板
- 时序信号图表（速度、航向角等）


## 前置依赖

使用此 skill 前，确保项目具备以下依赖：

| 依赖 | 路径 | 说明 |
|------|------|------|
| mars_utils | `deps/mars_utils/` | Redis 工具、地图组件封装、坐标变换等 |
| amap_client 组件 | `deps/mars_utils/amap_client/` | 高德地图 Streamlit 自定义组件（预编译 HTML/JS/CSS） |
| new_amap_client | `deps/mars_utils/new_amap_client.pyc` | amap_client 封装层（含 correct_amap_client_height） |
| streamlit | pip | `pip install streamlit` |
| plotly | pip | `pip install plotly` |
| numpy | pip | `pip install numpy` |
| orjson (可选) | pip | `pip install orjson`，缺失时回退到标准 json |
| redis | pip | `pip install redis`（仅 LNDS tile 直连时需要） |

如果项目中没有 `deps/mars_utils/` 目录，可通过安装项目 wheel 包获取：
```bash
pip install deps/dist/my_utils-1.0-py3-none-any.whl
```

## 页面骨架

所有 viser 页面遵循以下结构：

```
visers/<name>_viser.py
```

运行方式：
```bash
streamlit run visers/<name>_viser.py
```

## 必须遵循的模式

### 1. 路径与依赖初始化

```python
import os, sys
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
```

### 2. 延迟加载地图组件（避免启动慢）

```python
@st.cache_resource
def _load_amap_module():
    from mars_utils.new_amap_client import amap_client as _ac, correct_amap_client_height as _ch
    return _ac, _ch
```

### 3. page_config 设置

```python
st.set_page_config(page_title='<标题>', page_icon='🗺️', layout='wide')
```

### 4. Sidebar 配置（Redis 连接）

```python
url_params = st.query_params
host = st.sidebar.text_input('host', value=url_params.get('host', '11.166.9.42'))
port = st.sidebar.text_input('port', value=int(url_params.get('port', '6391')))
db = st.sidebar.text_input('db', value=int(url_params.get('db', '10')))
case_idx = st.sidebar.number_input('case_idx', value=int(url_params.get('case_idx', '0')))
password = ''
page_key = f'{host}_{port}_{db}_{case_idx}'
```

### 5. 数据加载

```python
def load_case(host, port, db, password, case_idx):
    rdb = rdb_class(host=host, port=int(port), pw=password)(db=int(db))
    return rdb.get(f'case_{case_idx}')

case_data = load_case(host, int(port), int(db), password, case_idx)
if case_data is None:
    st.error(f'case_{case_idx} not found')
    st.stop()

info_list = case_data['info_list']
if info_list and isinstance(info_list[0], str):
    info_list = [json_lib.loads(s) for s in info_list]
```

### 6. 地图轨迹展示（amap_client）

点数据格式: `[lon, lat, heading, size, color_id, 0, 0, label_text]`

```python
map_points = []
style_labels = []

# GPS 轨迹
for i, lon, lat, azi in gps_points:
    map_points.append([lon, lat, azi, 1, 0, 0, 0, f"gps:{i}"])
style_labels.append({"color": 0, "label": "gps"})

# GT0 轨迹
for i, lon, lat, azi in gt_points:
    map_points.append([lon, lat, azi, 1, 4, 0, 0, f"gt0:{i}"])
style_labels.append({"color": 4, "label": "gt0"})

amap_client, correct_amap_client_height = _load_amap_module()
component_height = correct_amap_client_height()
amap_client(
    points=map_points if map_points else None,
    points_style_type_labels=style_labels if map_points else None,
    fit_view=True,
    key=f"amap_{page_key}_{len(map_points)}",
)
```

color_id 映射: 0=蓝, 1=绿, 2=橙, 3=紫, 4=红

### 7. 局部坐标图（Plotly）

```python
fig = go.Figure()

# 自车标记
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode='markers', name='ego',
    marker=dict(color='black', size=14, symbol='triangle-up'),
))

# ... 添加其他元素 ...

fig.update_layout(
    xaxis_title='横向/m (→右)',
    yaxis_title='纵向/m (→前)',
    yaxis=dict(scaleanchor='x', scaleratio=1),
    height=800,
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig, use_container_width=True)
```

### 8. 坐标变换工具函数

WGS84 → 车体局部坐标需要复制以下函数（已封装在 scripts/coord_utils.py）：

```python
from coord_utils import wgs84_to_local  # 或直接复制到页面内
```

### 9. 布局模式

典型双栏布局：左地图 + 右局部图

```python
map_col, local_col = st.columns([0.45, 0.55])
with map_col:
    # 地图轨迹
with local_col:
    # 局部坐标 Plotly 图
```

## 脚手架脚本

快速生成新页面骨架：

```bash
python .qoder/skills/map-viser-page/scripts/scaffold_viser.py <page_name> [--with-lnds] [--with-lvis]
```

## 参考文件

- 完整示例: `visers/lnds_viser.py`（含 LNDS 路网 + 局部坐标裁剪）
- 信号可视化: `visers/lvis_viser.py`（含 LVIS/SRI 信号渲染）
- 坐标工具: [scripts/coord_utils.py](scripts/coord_utils.py)

## GPS/GT 数据提取模式

```python
def get_gps(info):
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
    gt0 = info.get('gt0')
    if not gt0:
        return None
    g = gt0[0]
    if g is None or len(g) < 10:
        return None
    azi = float(g[9]) if g[9] is not None else 0
    if azi < 0:
        azi += 360
    vel = [float(v) if v is not None else 0 for v in g[4:7]]
    spd = float(np.linalg.norm(vel))
    return (g[1], g[2], g[3] if len(g) > 3 else 0, spd, azi)
```

## 信号覆盖概览组件

```python
with st.expander('信号覆盖概览', expanded=False):
    sig_names = [('gps', 0), ('gt0', -1), ('lvis', -4), ('sri', -5), ('lan0', -7)]
    fig_sig = go.Figure()
    for name, y_val in sig_names:
        xs = [i for i, info in enumerate(info_list) if name in info and min_sn <= i <= max_sn]
        if xs:
            fig_sig.add_trace(go.Scattergl(
                x=xs, y=[y_val] * len(xs), mode='markers',
                name=name, marker=dict(size=3)))
    fig_sig.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_sig, use_container_width=True)
```

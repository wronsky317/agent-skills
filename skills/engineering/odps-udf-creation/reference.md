# ODPS UDF/UDTF 完整示例

## 示例 1: UDF — 训练数据精简

**文件**: `UDFs/udf_auto_lane_train_data_simplify.py`
**签名**: `array<string> -> array<string>`
**功能**: 接收 info_list（每帧 JSON 字符串数组），精简后返回
**资源**: `numpy.zip,a_utils_v17_zth.zip`

```python
# coding:utf-8
# resources: numpy.zip,a_utils_v17_zth.zip
from odps.udf import annotate
import json
import sys
sys.path.insert(0, 'work/numpy.zip')
import numpy as np

import os
from odps.distcache import get_cache_archive
def include_package_path(res_name):
    archive_files = get_cache_archive(res_name)
    if archive_files is None:
        return
    one_file = os.path.normpath(next(archive_files).name)
    pack_dir = one_file.split(res_name)[0] + res_name + '/files/'
    sys.path.insert(0, pack_dir)
if os.environ.get('USER') == 'admin':
    include_package_path('a_utils_v17_zth.zip')
from cpp_utils import Geometry

def make_simple_fea(point_info):
    ret = {}
    if 'gps' in point_info:
        info = point_info['gps']
        ret['gps'] = [info[2], info[3], info[5], info[6], info[7], info[1]/1000]
    if 'gps_floor' in point_info:
        info = point_info['gps_floor']
        ret['gps_floor'] = [info['x'], info['y'], info['speed'], info['angle']]
    if 'match_info' in point_info:
        ret['match_info'] = point_info['match_info']
    # ... 更多字段处理
    return ret

@annotate(" * ->array<string>")
class udf_auto_lane_train_data_simplify(object):
    """处理 info_list，精简后返回 list of json_string"""
    def evaluate(self, info_list_strs, ver='v11'):
        info_list = [json.loads(s) for s in info_list_strs]
        datas = []
        for point_k in range(len(info_list)):
            data = make_simple_fea(info_list[point_k])
            datas.append(json.dumps(data))
        return datas


if __name__ == "__main__":
    import configparser
    from odps import ODPS

    obj = udf_auto_lane_train_data_simplify()
    config = configparser.ConfigParser()
    config.read('config.cfg')
    o = ODPS(config['odps']['access_id'], config['odps']['access_key'],
             config['odps']['project_name'], endpoint=config['odps']['end_point'])

    sql = "select case_data from autonavi_location_dev.lane_auto_case_data limit 1;"
    result = o.run_sql(sql)
    result.wait_for_success()
    with result.open_reader(tunnel=True) as reader:
        for record in reader:
            val = json.loads(record.case_data)
            info_list_strs = [json.dumps(item) for item in val['info_list']]
            ret = obj.evaluate(info_list_strs)
            print(f"output len: {len(ret)}")
```

---

## 示例 2: UDTF — 轨迹数据切分生成 Case

**文件**: `UDFs/udtf_auto_lane_make_case.py`
**签名**: `bigint,bigint,string,... -> string,bigint,bigint,...,array<string>`
**功能**: 接收原始信号流数据，按时间切分成训练 case，每个 case 输出一行
**资源**: `numpy-1.21.6.zip,udf_env.py,modelLocalization_lane.zip,...`

关键设计模式：
- `process()` 中按 adiu/lifeid 分组，key 变化时先 flush 上一组
- `close()` 中 flush 最后一组
- 使用 `dynamic_import()` 延迟加载重依赖，避免 worker 启动慢

```python
# coding:utf-8
# resources: numpy-1.21.6.zip,udf_env.py,modelLocalization_lane.zip,...
import os, sys, json, gc, time, traceback
from odps.udf import annotate
from odps.udf import BaseUDTF

from udf_env import *
importOdpsFileWithNewName('_py3_sqlite3.3.31', '_sqlite3.so')
sys.path.insert(0, os.path.abspath('./'))
sys.path.insert(0, 'work/numpy-1.21.6.zip')
import numpy as np

dynamiced = False

def dynamic_import(signal):
    global dynamiced
    if dynamiced:
        return
    dynamiced = True
    sys.path.insert(0, 'work/modelLocalization_lane.zip')
    import modelLocalization_lane.timeAlign as align
    # ... 延迟导入其他模块
    globals()["align"] = align


@annotate(" * ->string,bigint,bigint,bigint,bigint,float,float,float,float,string,array<string>")
class udtf_auto_lane_make_case(BaseUDTF):
    def __init__(self):
        self.parser = None
        self.adiu = None
        self._inited = False

    def process(self, case_len, gps_continous_len, signal, adiu, lifeid, sn, ver, sig_type, ltt, bsn, content, div1, biz_dt):
        if not self._inited:
            self._inited = True
            gc.collect()
            dynamic_import(signal=signal)
            self.case_len = int(case_len)
            self._init_parser(signal, adiu, lifeid)

        # key 变化时先处理已有数据
        if adiu != self.adiu or lifeid != self.life_id:
            self._flush()
            self._init_parser(signal, adiu, lifeid)

        self.parser.feed(adiu, lifeid, sn, ltt, bsn, content, sig_type)

    def _init_parser(self, signal, adiu, lifeid):
        self.adiu = adiu
        self.life_id = lifeid
        # ... 初始化 parser

    def close(self):
        self._flush()

    def _flush(self):
        if self.parser is None:
            return
        # 处理逻辑...
        # 切分 case 并输出
        for case in cases:
            self.forward(adiu, 0, life_id, segment_k, part_k, ...)
```

---

## 部署示例

修改 `UDFs/create_func.sh` 中的变量：

```bash
# 部署 UDF
udf_prefix=udf_auto_lane_train_data_simplify
additional_res='numpy.zip,a_utils_v17_zth.zip'

# 部署 UDTF（资源更多）
udf_prefix=udtf_auto_lane_make_case
additional_res='numpy-1.21.6.zip,udf_env.py,_py3_sqlite3.3.31,modelLocalization_lane.zip,...'
```

执行：
```bash
cd UDFs && bash create_func.sh
```

## SQL 调用示例

```sql
-- UDF 调用
SELECT udf_auto_lane_train_data_simplify(info_list, 'v11') as simplified_data
FROM source_table;

-- UDTF 调用（需要 LATERAL VIEW 或直接 SELECT）
SELECT t.*
FROM source_table
LATERAL VIEW udtf_auto_lane_make_case(1000, 200, 'drsi', adiu, lifeid, ...) t
AS match_key, zero_col, life_id, segment_k, part_k, dt, err_std, mean_err, median_err, path_list, case_data;
```

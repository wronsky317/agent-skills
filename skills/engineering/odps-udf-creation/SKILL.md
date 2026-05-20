---
name: odps-udf-creation
description: 创建 MaxCompute/ODPS Python UDF 或 UDTF 函数。包含标准模板、create_func.sh 部署脚本、资源依赖管理。当用户提到"创建udf"、"创建udtf"、"新建udf"、"写一个udf"、"odps函数"时触发。
---

# ODPS UDF/UDTF 创建

## 工作流程

1. 确认函数类型（UDF 或 UDTF）、函数名、输入输出签名
2. 基于模板生成 Python 文件，放在 `UDFs/` 目录
3. 生成/更新 `UDFs/create_func.sh` 部署脚本
4. 提示用户执行部署

## UDF vs UDTF

| 类型 | 基类 | 入口方法 | 输出方式 | 典型场景 |
|------|------|----------|----------|----------|
| UDF | `object` | `evaluate()` | `return` | 1行→1行，字段转换/计算 |
| UDTF | `BaseUDTF` | `process()` + `close()` | `self.forward()` | 1行→多行，数据拆分/生成 |

## UDF 模板

```python
# coding:utf-8
# resources: numpy.zip,a_utils_v17_zth.zip
from odps.udf import annotate
import json
import sys
sys.path.insert(0, 'work/numpy.zip')
import numpy as np

@annotate("<input_signature> -> <output_signature>")
class <udf_class_name>(object):
    """函数说明"""
    def evaluate(self, <params>):
        # 处理逻辑
        return result
```

**签名格式说明：**
- 基本类型: `string`, `bigint`, `double`, `boolean`, `datetime`
- 复杂类型: `array<string>`, `map<string,string>`, `struct<x:double,y:double>`
- 通配: `*` 表示任意输入

## UDTF 模板

```python
# coding:utf-8
# resources: numpy-1.21.6.zip,udf_env.py,...
import os, sys, json, gc, time, traceback
from odps.udf import annotate
from odps.udf import BaseUDTF

@annotate("<input_signature> -> <output_columns>")
class <udtf_class_name>(BaseUDTF):
    def __init__(self):
        self._inited = False

    def process(self, <params>):
        """每行输入调用一次"""
        if not self._inited:
            self._inited = True
            # 初始化逻辑（加载模型、建立连接等）

        # 处理逻辑
        self.forward(col1, col2, ...)  # 输出一行

    def close(self):
        """所有输入处理完毕后调用"""
        # flush 剩余数据
        pass
```

## 资源依赖管理

### 常用资源列表

| 资源名 | 用途 |
|--------|------|
| `numpy.zip` / `numpy-1.21.6.zip` | NumPy |
| `a_utils_v17_zth.zip` | cpp_utils (Geometry等) |
| `udf_env.py` | ODPS 环境初始化工具 |
| `modelLocalization_lane.zip` | 定位模型基础库 |
| `scipy.zip` | SciPy |
| `shapely.zip` | Shapely 几何计算 |

### 资源引用方式

```python
# 方式1: sys.path (zip包)
sys.path.insert(0, 'work/numpy.zip')
import numpy as np

# 方式2: get_cache_archive (archive资源)
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

# 方式3: importOdpsFileWithNewName (.so文件)
from udf_env import *
importOdpsFileWithNewName('_py3_sqlite3.3.31', '_sqlite3.so')
sys.path.insert(0, os.path.abspath('./'))
```

## create_func.sh 部署脚本

**重要规则：不要为每个 UDF 单独写创建脚本，统一使用 `UDFs/create_func.sh`，只需修改 `udf_prefix` 和 `additional_res` 变量。**

```bash
# set -x
source ~/.bashrc

# ========== 修改以下两个变量即可复用创建流程 ==========
# <function_name>: additional_res='<comma_separated_resources>'
# ==================================================

function create() {
  udf_prefix=<function_name>
  additional_res='<resources>'        # 逗号分隔的其他依赖资源列表，无依赖则留空

  class_name=${udf_prefix}
  py_resource=${udf_prefix}.py

  if [ -z "${additional_res}" ]; then
    using_clause="\"${py_resource}\""
  else
    using_clause="\"${py_resource},${additional_res}\""
  fi

  odpscmd -e "use autonavi_location_dev;
      add py ${py_resource} -f;
      drop function if exists ${udf_prefix};
      create function ${udf_prefix} as \"${udf_prefix}.${class_name}\" using ${using_clause};
  "
}

create
```

## 注意事项

1. **不要 hardcode 凭证** — access_id/key/endpoint 等信息必须通过 config 文件读取
2. **避免引入重依赖** — ODPS 环境中 import 大包（如 quaternion, scipy）可能失败，优先内联需要的常量/枚举值
3. **UDTF 中处理分组** — 利用 `process()` 中检测 key 变化来分组处理，`close()` 中 flush 最后一组
4. **Python 文件名 = 类名 = 函数名** — 保持三者一致，如 `udf_auto_lane_train_data_simplify.py` 中的类 `udf_auto_lane_train_data_simplify`
5. **本地测试** — 在 `if __name__ == "__main__":` 中通过 ODPS SDK 拉取样本数据进行本地验证

## 本地测试模板

```python
if __name__ == "__main__":
    import configparser
    from odps import ODPS

    obj = <udf_class_name>()

    config = configparser.ConfigParser()
    config.read('config.cfg')
    access_id = config['odps']['access_id']
    access_key = config['odps']['access_key']
    project_name = config['odps']['project_name']
    end_point = config['odps']['end_point']
    o = ODPS(access_id, access_key, project_name, endpoint=end_point)

    sql = "select ... from <table> limit 1;"
    result = o.run_sql(sql)
    result.wait_for_success()
    with result.open_reader(tunnel=True) as reader:
        for record in reader:
            ret = obj.evaluate(record.column_name)
            print(ret)
```

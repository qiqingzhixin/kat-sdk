# kat-sdk

KAT 的独立 Python 作者库，提供 Workflow / Provider 声明、Context 合同、时间类型和表数据工具。distribution 名称为 `kat-sdk`，import 名称保持 `kat`。

## 安装与使用

当前支持 Python 3.14。首次交付从本仓库构建和安装，不要求存在 PyPI 发布：

```sh
python -m pip install .
python -m pip wheel --no-deps --wheel-dir dist .
```

其他目录可通过 `python -m pip install /path/to/kat_sdk-0.1.0-py3-none-any.whl` 安装构建产物。安装器处理 DataFusion / PyArrow 依赖。

```python
from kat import Context, workflow
from kat import dataprovider as dp
import pyarrow as pa

@workflow(name="example", description="返回示例数据。")
def example(ctx: Context):
    return dp.Table.from_arrow(pa.table({"value": [1]}))
```

SDK 可以独立导入、声明 Workflow 和执行表工具操作。PACK 发现、参数编译、执行、子 Run 调度、结果发布和 `kat.pack` 动态挂载由 kat-cli 私有 Runtime 负责；SDK 不包含或导入 `_kat_runtime`。未绑定的 Context 不能调用执行能力。

`kat.dataprovider.ftrace` 使用原生转换时需要另行安装 `kat-datasource`；Trace Streamer Provider 需要调用方提供可执行程序。这些来源工具不随 SDK wheel 打包。

## 验证

先安装测试依赖：`python -m pip install ".[test]"`。

```sh
python -I -B -m pytest tests
python -m pip check
```

SDK 独立版本化。CLI 锁定已验证的 SDK 版本及源码提交，在 Payload 构建期安装 wheel，执行期无需联网安装。

源码与已有表工具测试从 `maokelong/kat-cli` 迁移，继续采用原仓库 LICENSE；拆分设计见 [kat-cli #280](https://github.com/maokelong/kat-cli/issues/280)。

# 模块2：命令行测试流程

## 1. 测试对象

本次测试围绕 `pyinstrument` 的命令行模块展开，测试范围如下：

- CLI 入口与主流程：`pyinstrument/__main__.py`
- 采样与执行控制：`pyinstrument/profiler.py`
- session 存储与加载：`pyinstrument/session.py`
- 通用工具函数：`pyinstrument/util.py`
- 平台目录逻辑：`pyinstrument/vendor/appdirs.py`
- 参数 keypath 处理：`pyinstrument/vendor/keypath.py`

## 2. 原测试代码

项目中已有的 CLI 相关测试主要分成两组。

### 2.1 黑盒测试原代码

文件：[test_cmdline.py](/D:/LHY/SoftWare_Test/test/test_cmdline.py)

这组测试以子进程方式从用户视角调用 CLI，主要覆盖：

- 直接执行脚本
- 通过 `-m` 执行模块
- 通过 `-c` 执行字符串程序
- 参数透传与执行细节一致性
- session 文件保存与 `--load` 读取
- `--interval`、`--target-description`、`--renderer=pstats`
- 程序退出码传播

典型测试点如下：

```python
def test_command_line(self, pyinstrument_invocation, tmp_path: Path):
    busy_wait_py = tmp_path / "busy_wait.py"
    busy_wait_py.write_text(BUSY_WAIT_SCRIPT)
    output = subprocess.check_output([*pyinstrument_invocation, str(busy_wait_py)])
    assert "busy_wait" in str(output)
    assert "do_nothing" in str(output)
```

```python
def test_session_save_and_load(self, pyinstrument_invocation, tmp_path: Path):
    session_file = tmp_path / "session.pyisession"
    subprocess.check_call(
        [
            *pyinstrument_invocation,
            "--renderer=session",
            f"--outfile={session_file}",
            str(busy_wait_py),
        ]
    )
    Session.load(session_file)
    output = subprocess.check_output([*pyinstrument_invocation, f"--load={session_file}"])
    assert "busy_wait" in str(output)
```

### 2.2 白盒偏黑盒混合原代码

文件：[test_cmdline_main.py](/D:/LHY/SoftWare_Test/test/test_cmdline_main.py)

这组测试通过替换 `sys.argv` 和注入 `FakeRenderer`，直接验证 CLI 内部的 renderer 参数处理逻辑，主要覆盖：

- `-p time=percent_of_total`
- JSON 风格渲染参数
- dotted keypath 风格渲染参数

典型测试点如下：

```python
def test_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pyinstrument",
            "-r",
            "test.test_cmdline_main.FakeRenderer",
            "-p",
            "time=percent_of_total",
            "test_program.py",
        ],
    )
    main()
    assert fake_renderer_instance.time == "percent_of_total"
```

## 3. 新增测试代码

新增文件：[test_cli_module_white_box.py](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/test_cli_module_white_box.py)

该文件用于补齐原有测试未覆盖的内部逻辑，重点支撑课程作业对白盒测试的要求。

### 3.1 新增测试覆盖点

- `compute_render_options()` 的等价类与决策表冲突分支
- `get_renderer_class()` 的边界后缀与非法 renderer 分支
- `create_renderer()` 的异常路径
- `report_dir()`、`save_report_to_temp_storage()`、`load_report_from_temp_storage()`
- `main()` 对冲突入口模式的处理
- `Profiler.start()/stop()/reset()`
- `_sampler_saw_call_stack()` 的 async 分支
- `Session.from_json()/combine()/resample()/shorten_path()`
- `util` 中编码、TTY、颜色、数值格式逻辑
- `appdirs` 和 `keypath` 的辅助逻辑

### 3.2 典型新增测试片段

```python
def test_compute_render_options_rejects_invalid_decision_table_combinations():
    with pytest.raises(OptionsParseError):
        compute_render_options(
            make_options(hide_fnmatch="*.py", hide_regex=".*"),
            renderer_class=renderers.ConsoleRenderer,
            unicode_support=False,
            color_support=False,
        )
```

```python
def test_profiler_start_stop_reset_and_error_paths(monkeypatch: pytest.MonkeyPatch):
    profiler = Profiler(interval=0.002, async_mode="strict", use_timing_thread=True)
    profiler.start(target_description="CLI target")
    profiler._sampler_saw_call_stack(["sync"], 0.2, None)
    session = profiler.stop()
    assert session.target_description == "CLI target"
    profiler.reset()
    with pytest.raises(RuntimeError):
        profiler.stop()
```

```python
def test_session_json_combine_resample_and_shorten_path(monkeypatch: pytest.MonkeyPatch):
    combined = Session.combine(
        dummy_session(start_time=3.0, sys_path=["a", "b"]),
        dummy_session(start_time=1.0, sys_path=["b", "c"]),
    )
    assert combined.start_time == 1.0
    assert combined.sample_count == 2
```

## 4. 测试执行流程

### 4.1 需求分析

根据课程要求，需要同时覆盖黑盒与白盒测试，并在测试计划、测试代码和测试报告中体现：

- 黑盒：边界值、等价类、决策表
- 白盒：代码覆盖、基本路径覆盖、数据流分析

### 4.2 阅读源码与原测试

先阅读以下文件，明确已有覆盖点和缺口：

- [__main__.py](/D:/LHY/SoftWare_Test/pyinstrument/__main__.py)
- [profiler.py](/D:/LHY/SoftWare_Test/pyinstrument/profiler.py)
- [session.py](/D:/LHY/SoftWare_Test/pyinstrument/session.py)
- [util.py](/D:/LHY/SoftWare_Test/pyinstrument/util.py)
- [appdirs.py](/D:/LHY/SoftWare_Test/pyinstrument/vendor/appdirs.py)
- [keypath.py](/D:/LHY/SoftWare_Test/pyinstrument/vendor/keypath.py)
- [test_cmdline.py](/D:/LHY/SoftWare_Test/test/test_cmdline.py)
- [test_cmdline_main.py](/D:/LHY/SoftWare_Test/test/test_cmdline_main.py)

### 4.3 识别测试空白

原测试更偏用户视角和集成行为，未充分覆盖以下内容：

- `compute_render_options()` 冲突逻辑
- `get_renderer_class()` 异常分支
- 报告目录与历史 session 管理
- `Profiler` 生命周期错误路径
- `Session.combine/resample/shorten_path`
- `util/appdirs/keypath` 的内部边界逻辑

### 4.4 新增白盒测试

新增测试文件补足以上缺口，并保证：

- 黑盒设计方法在新增测试中仍可体现
- 白盒关键路径有直接断言
- 不依赖复杂外部环境即可执行

### 4.5 测试执行

执行命令：

```powershell
python -m pytest hw_tests/module2_cli/test_cli_module_white_box.py -q
```

执行结果：

```text
12 passed
```

### 4.6 覆盖验证

如需进一步验证白盒覆盖，可使用：

```powershell
python -m trace --count --coverdir D:\LHY\SoftWare_Test\module2_trace D:\LHY\SoftWare_Test\hw_tests\module2_cli\run_pytest_for_trace.py
```

## 5. 黑盒与白盒的对应关系

### 5.1 黑盒测试体现

- 等价类：不同 CLI 入口模式、合法和非法 renderer
- 边界值：文件后缀、session 数量、空占位符与未知占位符
- 决策表：`hide/hide_regex` 冲突、`show/show_regex/show_all` 冲突

### 5.2 白盒测试体现

- 代码覆盖：主流程、异常路径、工具函数逻辑
- 基本路径覆盖：`main()`、`Profiler.start/stop/reset`、renderer 构造
- 数据流分析：`argv -> options -> renderer/session/profiler`

## 6. 本模块最终测试材料清单

- 测试流程说明：[TEST_WORKFLOW.md](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/TEST_WORKFLOW.md)
- 测试计划：[TEST_PLAN.md](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/TEST_PLAN.md)
- 测试报告：[TEST_REPORT.md](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/TEST_REPORT.md)
- 新增测试代码：[test_cli_module_white_box.py](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/test_cli_module_white_box.py)
- 覆盖率辅助脚本：[run_pytest_for_trace.py](/D:/LHY/SoftWare_Test/hw_tests/module2_cli/run_pytest_for_trace.py)

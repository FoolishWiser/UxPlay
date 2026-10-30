# 中文本地化（i18n）说明

本仓库是 [FDH2/UxPlay](https://github.com/FDH2/UxPlay) 的简体中文汉化 fork。
**程序逻辑与上游一致**，只增加了 `lib/i18n.c` / `lib/i18n.h` 与一张翻译表，以及由此带来的
`-zh` / `-en` 两个选项；所有字符串仍是原本的 `printf`/日志格式串，翻译在运行期查表完成。

## 语言选择

| 方式 | 说明 |
| --- | --- |
| `-zh` / `--zh` | 强制中文（帮助、启动信息、运行日志） |
| `-en` / `--en` | 强制英文（与上游输出完全一致） |
| 环境变量 `UXPLAY_LANG=zh` / `en` | 与上面等价，适合写在 `~/.uxplayrc` 或 systemd 单元里（注意：`~/.uxplayrc` 里**不能**写这两个选项，配置文件的解析早于它们） |
| 未指定 | 依次看 `LC_ALL`、`LC_MESSAGES`、`LANG`：以 `zh` 开头用中文，其余用英文 |

例：

```bash
uxplay -zh            # 中文帮助/日志
uxplay -en -h         # 中文系统上强制英文帮助
UXPLAY_LANG=zh uxplay # 通过环境变量
```

## 运行期机制

- `lib/i18n.c` 里 `tr(msgid)` 用**二分查找**在 `lib/i18n_zh.inc` 中查找中文译文，
  查不到就返回原文——所以未翻译的串、以及上游新增的串都会自然退回英文，不会崩溃、不会乱码。
- 因此 `lib/i18n_zh.inc` **必须按英文 msgid 的字节序（`strcmp` 顺序）严格递增**；
  `i18n/tool.py build` 生成的表自动满足这一点，请不要手工编辑该文件。
- 翻译点有三处：`uxplay.cpp` 的 `log()`（解析后的日志）、`lib/logger.c` 的 `logger_log()`
  （lib/ 与 renderers/ 里的日志）、以及 `uxplay.cpp` 中被 `_(...)` 包裹的 `printf`/`fprintf`
  调用点（帮助与用法提示）。

## 目录内容

| 文件 | 作用 |
| --- | --- |
| `i18n/catalog.jsonl` | **唯一的翻译数据源**，每行 `{"en": 英文msgid, "zh": 中文}` |
| `i18n/untranslated.jsonl` | 有意保留英文的 msgid 清单（纯格式片段、`AAC`/`ALAC` 等 caps 名称）及原因 |
| `i18n/tool.py` | 维护工具：`build` / `check` / `extract` |
| `lib/i18n_zh.inc` | 由 `tool.py build` 生成的查找表，不要手工修改 |

## 维护流程

**改一条翻译 / 加一条翻译**

1. 编辑 `i18n/catalog.jsonl`（改 `zh` 即可；新增则加一整行，`en` 必须是源码里逐字节相同的格式串）。
2. `python3 i18n/tool.py build` —— 校验 `%` 说明符一致、无冲突、无空值，然后重写 `lib/i18n_zh.inc`。
3. 重新编译即可生效。

**跟随上游更新**

```bash
git remote add upstream https://github.com/FDH2/UxPlay
git fetch upstream && git merge upstream/master
python3 i18n/tool.py check    # 列出漏翻（应只有 DEBUG 级别）与失效条目
```

若 `git merge` 在 `uxplay.cpp` 里产生冲突，通常是上游改了帮助文本或 `printf`：把上游的新文案
直接合并进来，然后在 `catalog.jsonl` 里补一行英文→中文，再跑 `build`。

`check` 的输出解释：

- `missing translations: N visible, M debug-only`：可见串 N 必须为 0；`M` 是 `LOGGER_DEBUG`
  级别的调试日志，**有意不翻译**（便于与上游日志/issue 逐字对照）。
- `stale catalog entries`：源码里已不存在的 msgid，删掉对应行。
- `skipped (format built from macros, ...)`：形如 `"…: %"PRIu64` 的格式串在运行期会被拼成
  平台相关的数字，无法按 msgid 查表，这类调用保持英文（当前 12 处：`lib/mirror_buffer.c`、
  `lib/raop_ntp.c`、`renderers/video_renderer.c` 里用 `PRIu64` / `GST_TIME_FORMAT` 拼接的格式串）。

## 覆盖情况（1.74）

| 项目 | 数量 |
| --- | --- |
| 词条总数 | 463（帮助文本 115 + 程序消息 348） |
| 可见 msgid 漏翻 | 0 |
| 有意保留英文 | 22 |
| DEBUG 日志（不翻译） | 104 |
| 宏拼接格式（无法查表） | 12 |

## 实现细节

- 所有译文都是 UTF-8；`tr()` 未命中时原样返回英文 msgid，因此英文模式与上游完全一致。
- `uxplay.cpp` 用 `printf`/`fprintf` 输出；`lib/*.c` 走 `logger_log()`（在格式化之前查表）；
  `renderers/*.c` 原本用 GLib 的 `g_print`——GLib 会按当前 locale 的字符集转码，在 `LANG=C`
  下中文会变成 `?`，所以这些消息改成 `printf`/`fprintf`，与程序其它输出一致（Windows 下
  `main()` 里已有 `SetConsoleOutputCP(CP_UTF8)`，控制台能直接显示 UTF-8）。
- 用 `GST_TIME_FORMAT` 等宏拼接格式的 4 处 `g_print` 保持原样（英文）。

## 已知限制

- `LOGGER_DEBUG` 级别的调试输出、以及 README 中的 Changelog 段落保留英文。
- `Bluetooth_LE_beacon/` 下的独立 Python 信标脚本（`uxplay-beacon.py`）不在本次汉化范围内。
- `man` 手册页的中文版是 `uxplay.zh.1`，安装到 `${CMAKE_INSTALL_MANDIR}/zh_CN/man1/uxplay.1`，
  因此 `LANG=zh_CN.UTF-8 man uxplay` 会显示中文；英文版不受影响。

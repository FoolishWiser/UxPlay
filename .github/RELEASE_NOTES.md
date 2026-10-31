# UxPlay 简体中文版（Windows 便携包）

这是 [UxPlay](https://github.com/FDH2/UxPlay)（AirPlay 镜像服务器）的汉化 fork 的 **Windows x64 便携包**，由 GitHub Actions 在 MSYS2 UCRT64 环境中构建。

## 与官方版的关系

- 功能与官方 v1.74 一致，协议栈、编解码、mDNS 广播逻辑均未改动；
- 仅新增简体中文本地化，可用 `-zh` / `-en` 在运行期切换，默认按系统语言（`LANG`/`LC_ALL`/`UXPLAY_LANG`）自动选择，检测不到时用英文；
- 不加 `-zh` 时，所有输出与原版逐字一致（已与上游二进制逐行 diff 核对）。

## 下载与使用

1. 下载 `uxplay-windows-ucrt64.zip`，解压到任意目录（路径可含中文/空格）；
2. 双击 `run-zh.bat` 以中文界面启动，`run-en.bat` 为英文界面；
3. iPhone / iPad 打开"控制中心"→"屏幕镜像"，选择电脑名称即可投屏；
4. 全部参数（已汉化）：`uxplay.exe -zh -h`。

包里已内置运行所需的 DLL、GStreamer 插件与插件扫描器（`plugins/`、`gst-plugin-scanner.exe`），无需另外安装 MSYS2 或 GStreamer。

## 汉化范围

| 内容 | 状态 |
| --- | --- |
| `-h` 帮助文本（115 行） | 已汉化 |
| 启动/运行日志、错误与警告（含 renderers 的 GStreamer 报错） | 已汉化（463 条词条） |
| `README.zh-CN.md` | 全文中译（2632 行） |
| `uxplay.1` → `uxplay.zh.1` man 手册页 | 已汉化 |
| 调试级日志（LOG_DEBUG） | 保留英文，便于对照上游排错 |
| README 的 Changelog 段 | 保留英文原文 |

## 已知限制

- 未做代码签名，Windows SmartScreen 可能提示"未知发布者"，选择"仍要运行"即可；
- 仅提供 x64（UCRT64）便携包；ARM64 任务为尽力而为，失败不影响本包；
- 投屏显示依赖系统 D3D11/OpenGL 支持，虚拟机内可能无法出画面。

## 上游同步

本项目维护脚本见仓库 `i18n/` 目录：`python3 i18n/tool.py check` 可检查是否有新增的未翻译消息，`build` 会重新生成 `lib/i18n_zh.inc`。

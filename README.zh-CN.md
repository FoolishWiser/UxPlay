# UxPlay 1.74（实验版）：面向 Linux、macOS 和 Unix 的 AirPlay 镜像（投屏）与 AirPlay 音频服务器（也可在 Windows 上运行）。

> 🌐 **简体中文**（本页） | [English](README.md)

本仓库是 [FDH2/UxPlay](https://github.com/FDH2/UxPlay) 的简体中文汉化 fork：程序代码保持原样，只新增 i18n 模块与中文翻译表，因此与上游行为一致。

- **语言选择**：命令行 `-zh` / `--zh` 强制中文，`-en` / `--en` 强制英文；也可用环境变量 `UXPLAY_LANG=zh`，未指定时按系统 `LANG`/`LC_ALL` 自动判断（中文系统自动中文）。
- **已汉化**：`-h` 帮助、启动信息、用法提示、选项解析错误、运行期日志（INFO 及以上）、GStreamer 管道与渲染器提示、配对/网络诊断等共 463 条字符串（维护方式见 [i18n/README.md](i18n/README.md)）。
- **未汉化**：`LOGGER_DEBUG` 级别的调试日志与下方 Changelog 保留英文，便于对照上游排查问题。
- **同步上游**：`git remote add upstream https://github.com/FDH2/UxPlay && git fetch upstream`，合并后执行 `python3 i18n/tool.py check` 检查新增的未翻译字符串。

<a name="now-developed-at-the-github-site--where-all-user-issues-should-be-posted-and-latest-versions-can-be-found"></a>
### **目前开发工作位于 GitHub 站点 <https://github.com/FDH2/UxPlay>（所有用户问题都应在此提交，最新版本也可在此找到）。**

-   **v 1.74（实验版）新增内容（2026 年 6 月）

     **这是未来版本的一次试验性发布，其中包含新贡献的代码，提供
     一个极简的内部 mDNSResponder 实现，从而不再依赖
     avahi（Linux）或 Apple 的 Bonjour（Windows 和 macOS）。此前
     基于 Apple dns_sd.h 的实现仍可通过在编译
     UxPlay 时使用 `cmake -DUSE_DNS_SD=1` 来获得**    （默认情况下，macOS 上的 UxPlay 继续使用
     Bonjour：要在 macOS 上测试 UxPlay 内部 mDNS 实现，请使用 `cmake -DUSE_MDNS=1`）。

     *关于这个新的内部 mDNS 实现存在哪些问题，以及
     它是否应成为默认实现（将外部 Avahi/Bonjour
     实现保留为替代编译选项），抑或相反，
     我们非常欢迎你的意见。*（问题 [#529](https://github.com/FDH2/UxPlay/issues/529)

     完全重写了 HLS 语言选择逻辑（不需要的语言渲染现在会在
     播放前从主播放列表清单（master playlist manifest）中移除）：（1）现在可以独立设置字幕语言偏好，例如 `-slang pt-BR:pt`；
     （2）不带参数的 `-lang`、``-slang`` 会清除已选语言。（若未提供 -slang，则使用 -lang 的条目）；
     已移除对配音与未配音音频呈现（rendition）的检测。

     新增仅适用于 macOS 的 AWDL（Apple Wireless Direct Link）点对点客户端连接选项（需要 Bonjour）：它
     提供与客户端直接建立无线连接的方式。该功能仅在 macOS 中存在，因此其他操作系统上不可用。
     

-  **v1.73 至 v1.73.6 新增内容**（2026 年 3 月）：

-   部分 YouTube 应用的 HLS 视频现在提供其他语言音轨（由 AI 配音生成）。语言选择将按照
    通过选项 -lang 设置的偏好顺序进行（或按环境变量 $LANGUAGE 的顺序，“-lang”会覆盖它）。格式为 `-lang fr:es:en`，其中法语（"fr"）是
    首选（如果可用），然后是西班牙语（"es"），依此类推。$LANGUAGE 使用相同格式：单独使用 `-lang` 会禁止播放
    配音音频（当设置了 $LANGUAGE 时）。

-   支持将镜像模式/音频模式（但不包括 HLS）的音频和视频录制到 mp4 文件（新选项 -mp4 [fn]）。

-   为 Linux/\*BSD 和 Windows 支持**使用蓝牙 LE“信标”（beacon）进行服务发现**（作为 Bonjour/Rendezvous DNS-SD
    服务发现的替代方案），该功能在 v1.73 中引入，并在 1.73.4 - 1.73.6 中改进。它可用于不允许用户运行 DNS_SD 服务的网络。**
    用户必须运行一个蓝牙 LE“信标”（需要蓝牙 4.0 或更高版本，便宜的 USB“适配器”即可）。该
    信标由 Python >= 3.6 脚本 `uxplay-beacon.py` 管理。可加载的 Python 模块为 Linux、Windows
    和 FreeBSD 提供相应的蓝牙 LE 支持；_macOS 仅支持 BleuIO USB 适配器，它独有地自带基于 Renesas SoC 的蓝牙 LE 协议栈，在
    主机上被视为串行调制解调器（可在 UxPlay 支持的所有操作系统上使用，包括其他 BSD 变体）。_  该信标独立
    于 UxPlay 运行。当 UxPlay 运行时，信标会定期广播一个蓝牙 LE（“低功耗”）46 字节的
    传统类型广播，告知附近的 iOS/macOS 设备
    UxPlay 服务器的本地 IPv4 网络地址，以及应使用哪个 TCP 端口连接 UxPlay。相关说明
    见[下文](#bluetooth-le-beacon-setup)。

-   选项 `-vrtp <rest-of-pipeline>` 绕过 UxPlay 的渲染，改为
    将解密后的 h264 或 h265 视频的 rtp 数据包发送到
    外部渲染器（例如 OBS Studio），地址在 `rest-of-pipeline` 中指定。
    类似地，`-artp <rest-of-pipeline>` 将解码后的音频以 L16 RTP 数据包转发。
    两个选项可以一起使用，将视频和音频（作为各自独立的并发流）转发到外部
    应用程序。更多细节和 GStreamer 接收端管道示例请参见[用法](#usage)。
    
-   （适用于使用 D-Bus 的 Linux/*BSD 桌面环境）。新选项 `-scrsv <n>` 提供屏幕保护程序抑制功能（例如，为了
    在无键盘或鼠标操作的情况下观看镜像视频时防止屏幕保护程序启动）：
    n = 0（关闭）、n = 1（视频活动期间开启）、n = 2（UxPlay 运行期间始终开启）。
    已在 Gnome/KDE/Cinnamon/Mate/Xfce 4 上测试：其他桌面环境可能需要调整（请反馈）。
    （观察 `dbus-monitor` 的输出以确认抑制功能是否生效）。_在 Wayland 上可能无法工作_。

-   选项 -ca（不给文件名）现在会在
    UxPlay 内部渲染 Apple Music 封面图（在纯音频模式下）。
    （-ca `<filename>` 仍会导出封面图，供
    外部查看器显示）。

-   对（YouTube）HLS（HTTP Live Streaming）
    视频的支持得到改进，新增“-hls”选项（在 1.71 中引入）。* **目前仅支持从 YouTube iOS 应用
    （采用 \"m3u8\" 协议）推流**：（使用浏览器窗口中的 AirPlay 图标进行推流
    尚**不**支持）。在 YouTube 应用中点击 AirPlay 图标即可
    串流视频。
    **如遇此 UxPlay 新功能的任何问题，请反馈**。

    _HLS 的默认视频播放器是
    GStreamer playbin v3：如果
    某些视频无法播放，请使用“-hls 2”回退到较旧的 GStreamer 播放器 playbin v2_。

-   用户请求的功能：新增设置密码（作为屏幕上
    一次性 PIN 码的替代方式）以控制客户端访问的支持（-pw 选项，详见“man pw”或本 README）；新增对
    设置客户端初始音频串流音量（-vol 选项）的支持，以及将音频模式
    元数据输出到文件（供某些外部进程显示，-md 选项）的支持。

<a name="highlights"></a>
## 亮点：

-   GPLv3，开源。
-   最初仅支持 AirPlay 镜像协议，现在还新增了
    对来自当前 iOS/iPadOS 客户端的 AirPlay 纯音频（Apple Lossless ALAC）串流的
    支持。**现在还支持 AirPlay HLS
    视频串流（目前仅支持 YouTube 视频）。**
-   macOS 电脑（2011 年及以后，包括 Intel 和“Apple Silicon”M1/M2
    系统）既可充当 AirPlay 客户端，也可作为运行
    UxPlay 的服务器。通过 AirPlay，UxPlay 可为 macOS
    客户端模拟第二块显示屏。
-   支持较旧的 iOS 客户端（例如升级到 iOS 9.3.5 的 32 位第二代 iPad、第五代 iPod
    Touch 和 iPhone 4S，或之后的
    64 位设备），以及 Windows AirPlay 客户端模拟器 AirMyPC。
-   使用 GStreamer 插件进行音频和视频渲染（提供
    选项来选择适合不同硬件的输出“videosinks”和
    “audiosinks”，以及完全可由用户配置的视频串流
    管道）。
-   支持位于防火墙之后的服务器。
-   支持 Raspberry Pi，**无论是否使用 Broadcom GPU 的硬件视频
    解码**。*已在 Raspberry Pi Zero 2 W、3
    Model B+、4 Model B 和 5 上测试。*
-   支持在 Microsoft Windows 上运行（可在类 Unix 的 MSYS2 环境中
    使用 MinGW-64 编译器编译）。

注意：不支持 AirPlay2 多房间音频串流：请使用
[shairport-sync](https://github.com/mikebrady/shairport-sync) 实现该功能。

<a name="packaging-status-linux-and-bsd-distributions"></a>
## 打包状态（Linux 和 \*BSD 发行版）

[![Current Packaging
status](https://repology.org/badge/vertical-allrepos/uxplay.svg)](https://repology.org/project/uxplay/versions).

-   在基于 Debian 的 Linux 系统上安装 uxplay：
    “`sudo apt install uxplay`”；在 FreeBSD 上：
    “`sudo pkg install uxplay`”；在 OpenBSD 上：
    “`doas pkg_add uxplay`”。在基于 Arch 的系统上
    也可通过 AUR 获取。自 v. 1.66 起，uxplay 还以 RPM
    格式由 Fedora 38 打包（“`sudo dnf install uxplay`”）。

-   对于尚未打包
    UxPlay 的其他基于 RPM 的发行版，最近的
    [releases](https://github.com/FDH2/UxPlay/releases) 现已提供 RPM “specfile” **uxplay.spec**（见其
    “Assets”），也可在 UxPlay 源码顶层目录中找到。
    关于使用此 specfile [构建可安装的
    RPM 软件包](#building-an-installable-rpm-package) 的说明，请参见相应章节。

-   如果你的发行版未提供 UxPlay，或者你想要最新版本，自行编译非常容易：请参阅
    本文档后面的
    [从源码编译 UxPlay 的详细说明](#building-uxplay-from-source)
    一节。

<a name="after-installation"></a>
## 安装之后：

-   （在 Linux 和 \*BSD 上）：如果托管
    UxPlay 的服务器上启用了防火墙，请确保
    用于 mDNS/DNS-SD 查询的默认网络端口（UDP 5353）已开放（更多细节
    见下文的[故障排查](#troubleshooting)）；同时为
    UxPlay 开放三个 UDP 端口和三个 TCP 端口，并使用“uxplay -p `<n>`{=html}”选项（参见
    “`man uxplay`”或“`uxplay -h`”）。

-   即使你安装的是发行版预编译的 uxplay 二进制
    软件包，也可能需要阅读下文关于[运行
    UxPlay](#running-uxplay) 的说明，以了解需要额外安装发行版中的哪些
    **GStreamer 插件包**。

-   对于纯音频模式（Apple Music 等），使用“uxplay -async”选项可获得最佳音质，
    但此时 iOS 会带来 2 秒延迟。
    使用“uxplay -ca”选项可显示音频附带的任何
    “封面图”（Cover Art）。

-   如果你使用 UxPlay 只是为了镜像客户端屏幕（而不
    播放需要音频与视频同步的视频），最好
    使用“uxplay -vsync no”选项。

-   将你希望作为默认值使用的 UxPlay 选项添加到启动文件
    `~/.uxplayrc` 中（格式和其他可能的位置请参见“`man uxplay`”或“`uxplay -h`”；
    位置也可用“uxplay -rc _location_”设置）。
    特别是，如果你的系统使用
    PipeWire 音频或 Wayland 视频系统，你可能希望在该文件中加入
    “as pipewiresink”或“vs waylandsink”作为默认值。*（终端命令“ps waux \| grep pulse”或
    “pactl info”的输出将
    包含“pipewire”，前提是你的 Linux/BSD 系统在使用它）。*

-   对于使用 D-Bus 的 Linux/*BSD 系统，`-scrsv 1` 选项会在
    UxPlay 有视频活动时抑制屏幕保护程序（`-scrsv 2` 则在 UxPlay 运行期间始终抑制）。

-   对于使用 systemd 的 Linux 系统，发行版的 UxPlay 顶层目录中提供了一个 **systemd** 服务文件 **uxplay.service**，
    它同时也安装在
    `<DOCDIR>/uxplay/systemd/`（其中 DOCDIR 通常是 ``/usr/local/share/doc``），可让用户以
    非 root 守护进程的方式启动自己的 UxPlay 实例：应将其添加到
    /etc/systemd/user 目录，或者用户也可以自行创建
    systemd 目录 `~/.config/systemd/user/`，然后把 uxplay.service 复制进去。要将
    uxplay 的终端输出保存到文件 ~/uxplay.log，请取消 uxplay.service 中
    StandardOutput 条目的注释。然后

    `systemctl --user [start/stop/enable/disable/status] uxplay`

    可用于控制该守护进程。如果已启用，守护进程会在用户
    首次登录时启动，并在其不再有任何打开的会话时停止。有关
    systemd 用户服务的更多信息，请参见 https://www.baeldung.com/linux/systemd-create-user-services。如果
    多个用户可能同时以这种方式运行 uxplay，他们应在各自的启动文件中
    指定不同的 -p 和 -m 选项（端口和 deviceID）。
    **注意：不建议将 UxPlay 作为 root 服务运行。**

-   在 Raspberry Pi 上：使用 Broadcom GPU 进行硬件 h264 视频解码的
    型号（4B 及更早）可能需要 uxplay 选项 -bt709。
    如果使用 Ubuntu 22.10 或更早版本，必须对 GStreamer
    进行[修补](https://github.com/FDH2/UxPlay/wiki/Gstreamer-Video4Linux2-plugin-patches)，
    才能使用 Broadcom GPU 的硬件视频解码（对于 Raspberry Pi OS（Bullseye）也是推荐但可选的：打过补丁的 GStreamer
    不需要“ -bt709`”选项。使用硬件视频
    解码时对 -bt709 的需求似乎
    从 GStreamer-1.22 起
    又重新出现了。

-   如果在公共场所使用 UxPlay，提供了一些安全选项：可以要求输入显示在终端上的 AppleTV 风格
    一次性 PIN 码或密码，并按设备 ID 禁止/允许
    客户端访问。参见选项 -pin、-reg、-pw、-restrict、-allow、-block。
    
<a name="detailed-description-of-uxplay"></a>
# UxPlay 详细说明

本项目是一个 GPLv3 开源 Unix AirPlay2 镜像服务器，面向
Linux、macOS 和 \*BSD。它最初由
[antimof](http://github.com/antimof/Uxplay) 开发，使用了
基于 OpenMAX 的 [RPiPlay](https://github.com/FD-/RPiPlay) 的代码，而后者又源自
[AirplayServer](https://github.com/KqsMea8/AirplayServer)、
[shairplay](https://github.com/juhovh/shairplay) 和
[playfair](https://github.com/EstebanKubata/playfair)。（antimof 站点
已不再参与开发，但会定期发布从新的主
[UxPlay 站点](https://github.com/FDH2/UxPlay) 拉取的更新）。

UxPlay 已在多个系统上测试，其中包括 Debian
（10 "Buster"、11 "Bullseye"、12 "Bookworm"）、Ubuntu（20.04 LTS、22.04
LTS、23.04（以及 Ubuntu 衍生版 Linux Mint、Pop!\_OS））、Red Hat 及
其衍生版（Fedora 38、Rocky Linux 9.2）、openSUSE Leap 15.5、Mageia 9、
OpenMandriva "ROME"、PCLinuxOS、Arch Linux、Manjaro，并且应能在
任何 Linux 系统上运行。还在 macOS Catalina 和 Ventura（Intel）以及
Sonoma（M2）、FreeBSD 14.0、Windows 10 和 11（64 位）上测试过。

在 Raspberry Pi 4 Model B 上，已在 Raspberry Pi OS（Bullseye 和
Bookworm）（32 位和 64 位）、Ubuntu 22.04 LTS 和 23.04、Manjaro RPi4
23.02，以及（不使用硬件视频解码时）openSUSE 15.5 上测试过。还
在 Raspberry Pi Zero 2 W、3 Model B+ 以及现在的 5 上测试过。

其主要用途是像 AppleTV 一样，为
iOS/iPadOS/macOS 客户端（iPhone、iPod Touch、iPad、Mac 电脑）提供屏幕镜像（含音频），显示在
运行 Linux、macOS 或其他 Unix（以及现在也包括 Microsoft Windows）的主机的服务器屏幕上。UxPlay 使用“Legacy Protocol”
支持 Apple 的 AirPlay2 协议，
但缺少部分功能。（关于 Apple AirPlay 2 协议
已知的公开细节可在
[此处](https://openairplay.github.io/airplay-spec/)、
[此处](https://github.com/SteeBono/airplayreceiver/wiki/AirPlay2-Protocol)
和[此处](https://emanuelecozzi.net/docs/airplay2)找到；另请参见
[pyatv](https://pyatv.dev/documentation/protocols)，它可作为
添加现代协议的参考资源。）虽然不能保证
未来的 iOS 版本会继续支持“Legacy Protocol”，但 iOS 17
仍然保持支持。

UxPlay 服务器与其客户端必须位于同一局域网内，
该网络上还必须运行 **Bonjour/Zeroconf mDNS/DNS-SD 服务器**（严格来说
只需要 DNS-SD“服务发现”（Service Discovery）服务，并不
要求本地网络也属于基于 ".local" 的 mDNS
类型）。在 Linux 和 BSD Unix 服务器上，这通常由
[Avahi](https://www.avahi.org) 通过 avahi-daemon 服务提供，并且
包含在大多数 Linux 发行版中（该服务也可以由
macOS、iOS 或 Windows 服务器提供）。现在还提供另一种服务
发现方式，即使用蓝牙 LE“信标”。参见下文
的[说明](#bluetooth-le-beacon-setup)。


iOS/macOS 客户端与 UxPlay 服务器的连接可以
在 **AirPlay Mirror** 模式下发起（该模式在镜像客户端屏幕的同时串流有损压缩的 AAC
音频），也可以在另一种 **AirPlay
Audio** 模式下发起（该模式在不进行屏幕镜像的情况下串流 Apple Lossless（ALAC）音频）。
在 **Audio** 模式下，元数据显示在 uxplay
终端中；如果使用了 UxPlay 选项 `-ca <name>`，附带的封面图
也会输出到定期更新的文件 `<name>` 中，可通过
你选择的（可重新加载）图形查看器查看。*在活动连接期间
在* **Mirror** *和* **Audio** *模式之间切换
是可行的：在* **Mirror** *模式下，停止镜像（或关闭镜像
窗口）并启动* **Audio** *模式连接，通过
发起* **Mirror** *模式连接可切换回来；封面图显示
会随着你离开/重新进入* **Audio** *模式而停止/重启。*

-   **请注意，Apple 视频 DRM（如客户端上“Apple TV 应用”内容中所见）
    无法由 UxPlay 解密，Apple TV 应用
    也无法通过 UxPlay 的 AirPlay Mirror 模式观看（只会
    串流未受保护的音频，格式为 AAC）。**

-   **借助新的“-hls”选项，UxPlay 现在还支持非镜像的
    AirPlay 视频串流（此时客户端控制 AirPlay 服务器上的一个 Web 服务器，
    由后者直接接收 HLS 内容，以避免其
    被客户端解码并重新编码）。该功能目前仅
    支持 YouTube 视频串流。不使用 -hls 选项时，在
    诸如 YouTube 应用中使用 AirPlay 视频图标，只会
    发送音频（采用无损 ALAC 格式），而不附带
    视频。**

<a name="possibility-for-using-hardware-accelerated-h264h265-video-decoding-if-available"></a>
### 使用硬件加速的 h264/h265 视频解码（如可用）的可能性。

UxPlay 使用 [GStreamer](https://gstreamer.freedesktop.org) “插件”进行
音频和视频渲染。这意味着视频和音频
“开箱即用”，并可通过选择插件来实现。AirPlay 以
h264 格式串流视频：gstreamer 解码与具体插件无关，并在可用时使用加速的
GPU 硬件 h264 解码器。如果不可用，则
使用软件解码。

-   **面向 Intel 和 AMD 集成显卡的 VA-API，以及使用“Nouveau”
    开源驱动的 NVIDIA**

    使用 Intel 或 AMD GPU 时，最好使用开源
    VA-API gstreamer 插件进行硬件解码。（推荐使用名称类似“vah264dec”的
    较新“va”版本插件，
    而不是名称类似“vaapih264dec”的旧“vaapi”版本。）
    NVIDIA 显卡的开源“Nouveau”
    驱动原则上也受支持：请参见
    [此处](https://nouveau.freedesktop.org/VideoAcceleration.html)，但这需要
    VAAPI 辅以从
    NVIDIA 专有驱动中提取的固件。

-   **使用专有驱动的 NVIDIA**

    `nvh264dec` 插件（自 GStreamer-1.18.0 起包含在 gstreamer1.0-plugins-bad 中）
    可用于在
    安装 NVIDIA 的 CUDA 驱动 `libcuda.so` 之后，在 NVIDIA GPU 上进行加速视频解码。对于
    GStreamer-1.16.3 或更早版本，该插件名为 `nvdec`，必须
    由[用户
    自行编译](https://github.com/FDH2/UxPlay/wiki/NVIDIA-nvdec-and-nvenc-plugins)。

-   **在 Raspberry Pi（Pi 4B 及更早）上通过 Video4Linux2 支持 h264 硬件解码
    **

    Raspberry Pi（RPi）电脑（已在 Pi 4 Model B 上测试）现在可以
    使用软件视频解码运行 UxPlay，但更推荐使用 Pi 的 Broadcom 2835 GPU 中
    由固件完成的硬件加速
    h264/h265 解码。UxPlay 通过 GStreamer-1.22 的 Video4Linux2
    （v4l2）插件访问该功能；它使用由 Raspberry Pi 维护、尚未进入主线 Linux 内核的模块
    bcm2835-codec，目前仅包含在
    Raspberry Pi OS 和另外两个发行版（Ubuntu、Manjaro）中，
    这些发行版可通过 Raspberry Pi Imager 获取。*（对于 GStreamer \< 1.22，请参见
    [UxPlay
    Wiki](https://github.com/FDH2/UxPlay/wiki/Gstreamer-Video4Linux2-plugin-patches))*.
    Pi Model 5 不支持硬件 H264 解码，因为其 CPU
    足够强大，可令人满意地进行软件 H264 解码。

-   **在 Raspberry Pi（Pi 4 Model B 和 Pi 5）上支持 h265（HEVC）硬件解码
    **

    这些 Raspberry Pi 型号拥有专用的 HEVC 解码模块（不是
    GPU），其驱动“rpivid”尚未进入主线
    Linux 内核（但计划将来加入）。遗憾的是，
    它输出的解码视频采用非标准像素格式（NC30 或
    “SAND”），在该驱动进入
    主线内核之前，GStreamer 不会支持该格式；缺少这一支持，UxPlay 对
    Raspberry Pi 上 HEVC 硬件解码的支持将无法工作。

<a name="note-to-packagers"></a>
### 致打包者：

UxPlay 的 GPLv3 许可证没有附加明确的“GPL 例外”，
允许其在链接到 OpenSSL
**v. 3.0.0 之前**的版本时以编译形式分发（较旧版本的 OpenSSL 有一个许可证
条款，除非 OpenSSL 可被视为“System Library”（系统库），否则与 GPL 不兼容，而在 \*BSD 中它正是如此）。
    许多 Linux 发行版将 OpenSSL 视为“System Library”，但有些（例如 Debian）并不这样：在
    这种情况下，通过链接 OpenSSL-3.0.0 或更高版本
    即可解决该问题。


<a name="building-uxplay-from-source"></a>
# 从源码编译 UxPlay

你可以下载并解压
[UxPlay-master.zip](https://github.com/FDH2/UxPlay/archive/refs/heads/master.zip)，
或者（如果已安装 git）："git clone https://github.com/FDH2/UxPlay"。
你也可以下载其中列出的近期或更早的版本：
[Releases](https://github.com/FDH2/UxPlay/releases)。

-   较新的 UxPlay 也可以在原版 [antimof
    站点](https://github.com/antimof/UxPlay) 找到；那个原始项目
    已停止活动，但通常与
    [活跃的 UxPlay github 站点](https://github.com/FDH2/UxPlay) 保持同步或基本同步（感谢
    antimof！）。

<a name="building-uxplay-on-linux-or-bsd"></a>
## 在 Linux（或 \*BSD）上编译 UxPlay：

<a name="debian-based-systems"></a>
### 基于 Debian 的系统：

（请根据情况调整这些说明，以适应非 Debian 系的 Linux 或 \*BSD；对于
macOS，请参见下面的专门说明）。如果遇到任何
困难，可参见下面的 [故障排查](#troubleshooting)
一节获取帮助。

你需要一个 C/C++ 编译器（例如 g++），并安装标准开发
库。基于 Debian 的系统提供了一个软件包
「build-essential」用于编译软件。你还需要
pkg-config：如果 "`which pkg-config`" 找不到它，请安装
pkg-config 或其等价替代品 pkgconf。还要确保
已安装 cmake\>=3.10："`sudo apt install cmake`"（如有需要，可将
`build-essential` 和 `pkg-config`（或 `pkgconf`）加入此命令）。

确保你的发行版提供 OpenSSL 1.1.1 或更高版本，以及
libplist 2.0 或更高版本。（这意味着基于 Debian 10「Buster」的系统
（例如 Ubuntu 18.04）或更新的系统；在 Debian 10 系统上 "libplist" 是
较旧的版本，你需要 "libplist3"。）如果情况并非如此，你可能需要
从源码编译并安装这些库（参见本
README 末尾的说明）。

如果你使用的是非标准位置的 OpenSSL 安装，你可能需要设置
环境变量 OPENSSL_ROOT_DIR（*例如*，
"`export OPENSSL_ROOT_DIR=/usr/local/lib64`"，如果它安装在那里）。
同样，对于非标准（或多个）GStreamer
安装，请将环境变量 GSTREAMER_ROOT_DIR 设置为
UxPlay 所应使用的 gstreamer 安装中 ".../gstreamer-1.0/" 目录
所属的那个目录（如果它是 *例如*
"\~/my_gstreamer/lib/gstreamer-1.0/"，请用下面的命令设置该位置：
"`export GSTREAMER_ROOT_DIR=$HOME/my_gstreamer/lib`"）。

-   大多数用户会使用发行版提供的 GStreamer，
    但少数用户（特别是使用 Raspberry Pi OS Lite Legacy
    （Buster）、机型为 Raspberry Pi 4B，且希望为兼容其他应用而继续留在该
    不再受支持的 Legacy 系统上的用户）应当
    改为按照 [以下
    说明](https://github.com/FDH2/UxPlay/wiki/Building-latest-GStreamer-from-source-on-distributions-with-older-GStreamer-(e.g.-Raspberry-Pi-OS-).) 从源码编译较新的 Gstreamer
    。**请务必在编译 UxPlay *之前* 完成此操作**。

在终端窗口中，切换目录到
已下载源码的源码目录（"UxPlay-\*"，"\*" 为 "master" 或 zip
压缩包下载对应的发布标签，"git clone" 下载则为 "UxPlay"），然后按照
下面的说明操作：

**注意：** 默认情况下，UxPlay 会针对构建它的
计算机进行优化；如果情况并非如此，例如在为
发行版打包时，请使用 cmake 选项
`-DNO_MARCH_NATIVE=ON`。

如果你在 Linux 或 \*BSD 上使用 X11 窗口系统，并希望通过按键
（F11 或 Alt_L+Enter）在全屏模式之间切换，则 UxPlay 需要在
编译时加入对 X11 的依赖。从 UxPlay-1.59 开始，这将默认
完成，**前提是**已安装并检测到 X11 开发库。请用
"`sudo apt install libx11-dev`" 安装这些库。如果检测到
GStreamer \< 1.20，还会加入屏幕共享类应用（*例如*
Zoom）所需的修复。

-   如果存在 X11 开发库，但你希望编译出*不*依赖任何 X11 的
UxPlay，请使用 cmake 选项
`-DNO_X11_DEPS=ON`。

1.  "`sudo apt install libssl-dev libplist-dev`"。（*除非你需要
    从源码编译 OpenSSL 和 libplist*）。

2.  "`sudo apt install libavahi-compat-libdnssd-dev`"（*仅在
     你使用 `cmake -DUSE_DNS_SD=1` 编译，以将 Avahi 作为外部 DNS_SD 服务
     来提供服务发现（Service Discovery）时才需要*）。

3.  "`sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev`"。
    （\**如果你从源码编译了 Gstreamer，请跳过此项*）
    
4.  "`cmake .`"（*为了获得更干净的构建，这在修改源码时很有用，可将此命令替换为*
    "`mkdir build; cd build; cmake ..`"：*这样
    你就可以在需要时删除 `build` 目录的内容，
    而不会影响源码。*）此外，在此处按需添加任意 cmake "`-D`" 选项
    （例如 `-DNO_X11_DEPS=ON` 或 `-DNO_MARCH_NATIVE=ON`）。
5.  `make`
6.  "`sudo make install`"（之后你可以在运行此命令的同一目录中使用
    "`sudo make uninstall`" 来卸载）。

这会将可执行文件 "`uxplay`" 安装到 `/usr/local/bin`（并且
将手册页安装到某个标准位置，例如
`/usr/local/share/man/man1`，以及将 README 文件安装到类似
`/usr/local/share/doc/uxplay` 的位置）。（如果 "man uxplay" 失败，请检查
\$MANPATH 是否已设置：如果是，则需要把手册页的路径（通常是
/usr/local/share/man/）添加到 \$MANPATH 。）在构建过程结束后，
uxplay 可执行文件也可以在构建目录中找到，
如果你希望在安装前测试（在这种情况下，必须
先安装 GStreamer 插件）。

<a name="building-on-non-debian-linux-and-bsd"></a>
### 在非 Debian 的 Linux 和 \*BSD 上编译

\*\*对于使用基于 RPM 的发行版的用户，还提供了一个 RPM spec 文件 uxplay.spec：
请参见 [构建可安装的 rpm
软件包](#building-an-installable-rpm-package)。

-   **Red Hat，或 CentOS 之类的克隆版（现在延续为 Rocky Linux 或
    Alma Linux）：** (sudo dnf install，或 sudo yum install) openssl-devel
    libplist-devel avahi-compat-libdns_sd-devel gstreamer1-devel
    gstreamer1-plugins-base-devel（+libX11-devel，用于全屏 X11）
    *（其中一些可能位于「CodeReady」附加软件仓库中，克隆版称之为
    「PowerTools」）*

-   **Mageia、PCLinuxOS、OpenMandriva：** 与 Red Hat 相同，只是
    名称有所变化：（Mageia）"gstreamer1.0-devel"、
    "gstreamer-plugins-base1.0-devel"；（OpenMandriva）
    "libopenssl-devel"、"gstreamer-devel"、
    "libgst-plugins-base1.0-devel"。PCLinuxOS：与 Mageia 相同，但使用
    synaptic（或 apt）作为其软件包管理器。

-   **openSUSE：** (sudo zypper install) libopenssl-3-devel（原为
    libopenssl-devel） libplist-2_0-devel（原为 libplist-devel）
    avahi-compat-mDNSResponder-devel gstreamer-devel
    gstreamer-plugins-base-devel（+ libX11-devel，用于全屏 X11）。

-   **Arch Linux**（*在 AUR 中也有可用的软件包*）：(sudo pacman
    -Syu) openssl libplist avahi gst-plugins-base。

-   **FreeBSD：** (sudo pkg install) libplist gstreamer1。还必须
    安装 avahi-libdns 或 mDNSResponder 以提供
    dns_sd 库。OpenSSL 已作为系统库（System Library）安装。

-   **OpenBSD：** (doas pkg_add) libplist gstreamer1-plugins-base。
    还必须安装 avahi-libs 以提供 dns_sd 库；
    （还必须安装 avahi-main）。
    OpenSSL 已作为系统库（System Library）安装。

<a name="building-an-installable-rpm-package"></a>
#### 构建可安装的 RPM 软件包

首次构建 RPM 的用户应先安装 rpm-build 和
rpmdevtools 软件包，然后用
"`rpmdev-setuptree`" 创建 rpmbuild 目录树。然后下载并复制 uxplay.spec 到 `~/rpmbuild/SPECS`。在
该目录中运行 "`rpmdev-spectool -g -R  uxplay.spec`" 以下载对应的
源码文件 `uxplay-*.tar.gz` 到 `~/rpmbuild/SOURCES`
（"rpmdev-spectool" 也可能直接叫作 "spectool"）；然后运行
"`rpmbuild -ba uxplay.spec`"（你需要安装它报告的
任何必需依赖）。这应该会在
`~/rpmbuild/RPMS` 的子目录中创建 uxplay RPM 软件包。（**uxplay.spec**
已在 Fedora 38、Rocky Linux 9.2、openSUSE Leap 15.5、Mageia 9、OpenMandriva、
PCLinuxOS 上测试；它很容易修改，以包含
其他基于 RPM 的发行版的依赖列表。）

<a name="running-uxplay"></a>
## 运行 UxPlay

<a name="installing-plugins-debian-based-linux-distributions-including-ubuntu-and-raspberry-pi-os-skip-if-you-built-a-complete-gstreamer-from-source"></a>
### 安装插件（基于 Debian 的 Linux 发行版，包括 Ubuntu 和 Raspberry Pi OS）（*如果你从源码编译了完整的 GStreamer，请跳过*）

接下来用以下命令安装所需的 GStreamer 插件：
`sudo apt install gstreamer1.0-<plugin>`。所需的 `<plugin>` 取值
为：

1.  「**plugins-base**」
2.  「**libav**」（用于声音），
3.  「**plugins-good**」（用于 v4l2 硬件 h264 解码）
4.  「**plugins-bad**」（用于 h264 解码）。

**基于 Debian 的发行版会将部分插件包拆分成
更小的片段：** 可能还需要的一些包括用于 OpenGL 支持的「**gl**」
（它提供 "-vs glimagesink" 视频输出端（videosink），这在
许多系统上（包括 Raspberry Pi）非常有用，并且在使用
NVIDIA GPU 进行 h264/h265 解码时应当始终使用）、
「**gtk3**」（它提供 "-vs gtksink" 视频输出端），以及用于 X11 支持的
「**x**」，不过这些可能已经安装。如果
声音不工作，则可能需要安装「**alsa**」、「**pulseaudio**」或「**pipewire**」
插件，具体取决于你的音频设置方式。

* 有一个软件包「**vaapi**」
可用于 Intel 或 AMD 显卡的硬件加速 h264 视频解码
（但不适用于使用专有驱动的 NVIDIA）。
然而该软件包包含较旧的驱动（vaapisink、vaapih264dec 等），
它们已不再开发，**除非确实需要，否则不应安装**。
取代 "vaapi" 插件的 "va" 插件（vah264dec 等）由 「**plugins-bad**」提供：
并且使用标准视频输出端（xvimagesink、glimagesink 等），而不是
"vaapi" 插件使用的特殊视频输出端 "vaapisink"。


-   还要安装「**gstreamer1.0-tools**」以获取实用工具
    gst-inspect-1.0，用于检查 GStreamer 安装。

<a name="installing-plugins-non-debian-based-linux-or-bsd-skip-if-you-built-a-complete-gstreamer-from-source"></a>
### 安装插件（非 Debian 的 Linux 或 \*BSD）（*如果你从源码编译了完整的 GStreamer，请跳过*）

在某些情况下，由于专利问题，
镜像（mirroring）模式下解码 AAC 音频所需的 libav 插件功能 **avdec_aac**
并未包含在官方发行版中：请从这些发行版的社区
软件仓库中获取。_注意：下面列出的（已弃用的）"vaapi" 软件包
已不再推荐：面向 Intel/AMD 显卡的更新 "va" 版 VA-API 插件
由 *-plugins-bad 提供。_

-   **Red Hat，或 CentOS 之类的克隆版（现在延续为 Rocky Linux 或
    Alma Linux）：** 安装 gstreamer1-libav gstreamer1-plugins-bad-free
    （_已弃用：_ gstreamer1-vaapi，用于 Intel/AMD 显卡）。在近期的 Fedora 中，
    gstreamer1-libav 已改名为 gstreamer1-plugin-libav。**要获取
    avdec_aac，请从
    [rpmfusion.org](https://rpmfusion.org) 安装软件包**：（从
    rpmfusion 获取 ffmpeg-libs；在 RHEL 或克隆版上（但不包括近期 Fedora），还要从
    那里获取 gstreamer1-libav）。

-   **Mageia、PCLinuxOS、OpenMandriva：** 安装 gstreamer1.0-libav
    gstreamer1.0-plugins-bad（_已弃用：_ gstreamer1.0-vaapi，用于 Intel/AMD
    显卡）。**在 Mageia 上，要获取 avdec_aac，请从
    「tainted」软件仓库安装 ffmpeg**（该仓库还提供更完整的
    gstreamer1.0-plugins-bad）。

-   **openSUSE：** 安装 gstreamer-plugins-libav gstreamer-plugins-bad
    （_已弃用：_ gstreamer-plugins-vaapi，用于 Intel/AMD 显卡）。**要获取
    avdec_aac，请从下面这个来源安装适用于 openSUSE 的 libav\* 软件包：
    [Packman](https://ftp.gwdg.de/pub/linux/misc/packman/suse/)
    「Essentials」**；建议：添加 Packman 仓库后，
    使用 YaST 软件管理中的选项，将所有多媒体
    系统软件包切换到 Packman）。

-   **Arch Linux** 安装 gst-plugins-good gst-plugins-bad gst-libav（_已弃用：_
    gstreamer-vaapi，用于 Intel/AMD 显卡）。

-   **FreeBSD：** 安装 gstreamer1-libav、gstreamer1-plugins、
    gstreamer1-plugins-\*（\* = core, good, bad, x, gtk, gl, vulkan,
    pulse, v4l2, ...），（_已弃用：_ gstreamer1-vaapi，用于 Intel/AMD 显卡）。

-   **OpenBSD：** 安装 gstreamer1-libav、gstreamer-plugins-\*
    （\* = core, bad, base, good）。

<a name="starting-and-running-uxplay"></a>
### 启动并运行 UxPlay


* 必须设置一种启用服务发现（Service Discovery）的方法（以便本地网络中的 AirPlay 客户端能够找到
UxPlay 提供的 AirPlay 服务）。UxPlay 使用的标准方法是
在 **mDNS 网络端口 UDP 5353 上通告该服务；如果
主机电脑上启用了防火墙，则必须为 mdns 查询开放该端口 **。    以前，UxPlay 需要外部 `DNS_SD` 服务
（Apple 的 Bonjour 服务，在 Linux/\*BSD 上通常由 Avahi 或 mDNSResponder 实现，但
UxPlay 现在还自带一个内置的 mDNSResponder「最小」版本。   在
使用内置版本还是外部服务之间的选择，是一个编译时选项。

* 如果你无法在自己的网络中
使用 mdns，或者你更愿意不使用它，那么现在有一种
使用蓝牙 LE 信标（beacon）的替代服务发现方法。
请参见 [蓝牙信标设置](#bluetooth-le-beacon-setup) 的说明。


从 UxPlay-1.64 起，UxPlay 可以使用从配置文件中读取的选项来启动，
该文件将是以下位置中最先找到的一个：（1）路径由环境变量
`$UXPLAYRC` 指定的文件；（2）用户主目录（"\~"）中的 `~/.uxplayrc`；
（3）`~/.config/uxplayrc`。格式为
每行一个选项，省略命令行选项开头的
`"-"`。配置文件中以 `"#"` 开头的行
被视为注释并忽略。

**在终端窗口中运行 uxplay**。在某些系统上，你可以用
`-fs` 选项指定全屏模式，或用 F11 或（按住左 Alt）+Enter 键
在全屏模式之间切换。完成时按 Ctrl-C
（或关闭窗口）来终止它。

如果 iOS 客户端的下拉「屏幕镜像」面板中
看不到 UxPlay 服务器，
则说明服务发现没有正常工作。   如果你使用的是
外部 DNS_SD 服务（通常是 avahi-daemon），
请检查
它是否正在运行：在终端窗口中执行
`systemctl status avahi-daemon`。如果它显示
avahi-daemon 未运行，请用
`sudo systemctl [start,stop,enable,disable] avahi-daemon` 来控制它（在
非 systemd 系统上（例如 \*BSD），使用
`sudo service avahi-daemon [status, start, stop, restart, ...]`）。

如果
能看到 UxPlay，但选中后客户端无法连接，
则服务器上可能有防火墙，阻止 UxPlay
接收客户端连接请求，除非额外开放一些网络端口：
参见下面的 [故障排查](#troubleshooting)
以获取关于此问题或其他问题的帮助。

-   与 Apple TV 不同，UxPlay 服务器默认不要求
    客户端最初使用服务器显示的 PIN 码与它进行「配对」
    （之后客户端会「信任」该服务器，不再
    需要重复此过程）。自 v1.67 起，Uxplay 提供这种
    「PIN 认证」作为选项：如果你想使用它，请参见 [用法](#usage) 中的
    "`-pin`" 和 "`-reg`" 的详情。*某些
    启用了 MDM（移动设备管理，常见于雇主拥有的
    设备）的客户端必须使用 PIN 认证：即使未使用 pin 选项运行，
    UxPlay 也会提供该功能。*密码认证
    （-pw _pwd_）也被提供作为 PIN 码的替代方案：
    用户需要知道密码 _pwd_，并在 iOS/macOS 设备上的
    提示下输入它以访问 UxPlay（如果未设置 _pwd_，则必须在**每次**新连接时输入
    显示出来的随机 PIN 码）。

-   默认情况下，UxPlay 会锁定在当前客户端上，直到该客户端
    断开连接；自 UxPlay-1.58 起，选项 `-nohold`
    修改了此行为：当有新客户端请求
    连接时，它会移除当前客户端并接管。UxPlay
    1.66 引入了一种机制（`-restrict`、`-allow <id>`、
    `-block <id>`），用于控制允许哪些客户端连接，
    依据是它们的 "deviceID"（在 Apple 设备上这似乎是
    不可变的）。

-   在镜像（Mirror）模式下，GStreamer 播放视频及其伴随音频时有 **两种** 方法可选：
    在 UxPlay-1.64 之前，视频流和音频流都在到达后尽快
    播放（即 GStreamer 的 "*sync=false*" 方法），并用 GStreamer
    内部时钟来尽量让它们保持同步。**从
    UxPlay-1.64 开始，另一种方法（GStreamer 的 "*sync=true*" 模式），
    它使用客户端发送的音频流和视频流中的时间戳，
    成为新的默认值**。在解码能力较弱的 UxPlay 主机
    （例如 Raspberry Pi Zero W 或 3 B+ 机型）上，这会丢弃
    无法及时解码以与音频一同播放的视频帧，
    使视频变得卡顿，
    但仍保持同步。

不丢弃迟到视频帧的旧方法在
性能更强的系统上效果良好，且仍可通过 UxPlay 选项
"`-vsync no`" 使用；该方法适用于「直播串流」（live streaming），在
例如将 UxPlay 用作 Mac 电脑的第二显示器时可能更好，
而新的基于时间戳的默认方法最适合
观看视频，以保持口型动作与声音同步。
（如果不使用时间戳，当视频无法足够快地解码时，
视频最终会落后于音频：以前在不使用时间戳时，
硬件加速的视频解码有助于防止这种情况。）

-   在纯音频（Audio-only）模式下，GStreamer 的 "sync=false" 模式（不使用
    时间戳）仍是默认值，但如果你希望保持
    服务器上播放的音频与客户端上显示的视频同步，
    请使用基于时间戳的 `-async` 选项。（一个例子可能
    是：你希望在客户端跟随 Apple Music 歌词，同时在
    UxPlay 服务器上聆听更出色的声音）。这会使
    客户端上的视频延迟以匹配服务器上的音频，因此会
    导致在客户端发起的暂停或切歌操作生效到服务器播放的音频之前，
    出现轻微延迟。

AirPlay 音量控制会将音量（增益）衰减最多 -30dB：
分贝范围 -30:0 可以通过选项 `-db`（"-db *Low*" 或 "-db *Low*:*High*"）
重新映射为 *Low*:0 或 *Low*:*High*，其中 *Low* 必须为
负值。重新映射在分贝上是线性的。注意，GStreamer 的音频
格式会对任何高于 +20db 的音频增益进行「削波」（clip），因此请将 *High* 保持在
该电平以下。选项 `-taper` 提供了一种「渐变」（tapered）的 AirPlay 音量控制
曲线，一些用户可能更喜欢。

-vsync 和 -async 选项还允许可选的（正或
负）音频延迟调整，单位为*毫秒*，用于微调：
`-vsync 20.5` 使音频相对视频延迟 0.0205 秒；负
值则会使其提前。）

-   你可能会发现 -fps 60 设置能让某些视频以 60 帧每秒
    播放，从而改善视频效果。（你可以使用 -vs fpsdisplaysink 和/或
    -FPSdata 查看实际串流的帧率。）使用此设置时，
    你应使用默认的
    基于时间戳的同步选项 `-vsync`。

-   现在你可以在纯音频（ALAC）模式下，于 UxPlay 内部显示来自 Apple Music 等
    来源的附带「封面图」（Cover Art），并使用选项
    `uxplay -ca`。_将封面图导出到外部查看器的旧方法仍然可用：在
    后台运行
    "`uxplay -ca <name> &`"，然后运行一个
    具备自动重载功能的图片查看器：一个例子是 "feh"，在前台运行
    "`feh -R 1 <name>`"；用
    "`ctrl-C fg ctrl-C`" 终止 feh，再终止 Uxplay_。

默认情况下，GStreamer 会使用一种算法来搜索最佳的
"videosink"（GStreamer 对用于显示图像的图形驱动的称呼）
来使用。你可以用 uxplay 选项 `-vs <videosink>` 覆盖此选择。
可用的视频输出端取决于你的操作系统和
图形硬件：使用
"`gst-inspect-1.0 | grep sink | grep -e video -e Video -e image`" 查看
有哪些可用。在 Linux/\*BSD 上的一些可能性包括：

-   **glimagesink**（OpenGL）、**waylandsink**

-   **xvimagesink**、**ximagesink**（X11）

-   **kmssink**、**fbdevsink**（无 X11 的控制台图形）

-   **vaapisink**（_已弃用_，用于 Intel/AMD 硬件加速图形）已被淘汰：
    请改用 **glimagesink** 或 **xvmagesink**（配合由 "vah264dec"
    进行的硬件解码，该解码器可能被自动选中，但也可以用 "-vd " 选项显式指定。）

-    对于
    使用 CUDA 的 NVIDIA 硬件图形，请将 **glimagesink** 与
    "`-vd nvh264dec`" 组合使用。

-   如果服务器是「无头」的（没有连接显示器，只渲染
    音频），请使用 `-vs 0`。

注意：videosink 选项可以通过给 -vs 传入带引号的参数来设置：
_例如_，`-vs "xvimagesink display=:0"`：ximagesink 和 xvimagesink 允许
指定 X11 display 名称，waylandsink 也有类似的选项。
Videosink 选项（"properties"）可以在其 GStreamer 描述页面中找到，例如
https://gstreamer.freedesktop.org/documentation/xvimagesink 。

GStreamer 也会搜索最佳的「音频输出端」（audiosink）；用
`-as <audiosink>` 覆盖它的选择。Linux 上的选项包括 pulsesink、alsasink、
pipewiresink、oss4sink；用以下命令查看有哪些可用：
`gst-inspect-1.0 | grep sink | grep -e audio -e Audio`。

**一个常见问题涉及 GStreamer 试图使用
配置不正确或不存在的加速硬件 h264 视频
解码（例如 VAAPI）。尝试用 "`uxplay -avdec`" 强制使用软件视频
解码；如果这有效，你可以接着尝试修复加速硬件
视频解码（如果你需要），或者直接卸载已安装的 GStreamer vaapi
插件。**

更多运行时选项请参见 [用法](#usage)。


<a name="special-instructions-for-raspberry-pi-tested-on-raspberry-pi-zero-2-w-3-model-b-4-model-b-and-5-only"></a>
### **Raspberry Pi 专用说明（仅在 Raspberry Pi Zero 2 W、3 Model B+、4 Model B 和 5 上测试）**：

-   对于 Framebuffer 视频（用于 Raspberry Pi OS "Lite" 及其他非 X11
    发行版），请使用 KMS videosink "-vs kmssink"（DirectFB
    的 framebuffer videosink "dfbvideosink" 在 Pi 上已损坏，会
    发生段错误）。*在这种情况下，你应当显式使用 "-vs
    kmssink" 选项，因为若不使用它，autovideosink 找不到
    正确的 videosink。*

-   Raspberry Pi 5 不提供硬件 H264 解码（也
    不需要）。

-   Pi Zero 2 W、3 Model B+ 和 4 Model B 应当使用
    由 Broadcom GPU 提供的硬件 H264 解码，但这需要一个非主流的内核模块
    bcm2835_codec，该模块维护在 [Raspberry Pi kernel
    tree](https://github.com/raspberrypi/linux) 中；已知会提供该模块的发行版
    包括 Raspberry Pi OS、Ubuntu 和 Manjaro-RPi4。如果该模块
    不可用，请使用软件解码
    （选项 -avdec）。

-   Uxplay 使用 GStreamer-1.22 及更高版本中的 Video4Linux2（v4l2）插件
    来在启用硬件 H264 解码时访问 GPU。这一过程
    应当自动发生。可以使用选项 -v4l2，但通常
    最好是让 GStreamer 自己去寻找最佳的
    视频管道。

-   在较旧的发行版（GStreamer \< 1.22）上，v4l2 插件需要一个
    补丁：见 [UxPlay
    Wiki](https://github.com/FDH2/UxPlay/wiki/Gstreamer-Video4Linux2-plugin-patches)。
    Legacy Raspberry Pi OS（Bullseye）自带一个只打过部分补丁的
    GStreamer-1.18.4，需要 uxplay 选项 -bt709（并且不要使用
    -v4l2）；在这种情况下，更好的做法仍然是应用 UxPlay
    Wiki 上的完整补丁。

-   **看起来在使用硬件 h264 视频解码时，选项
    -bt709 在 GStreamer-1.22 及更高版本中又变得必需了。**

-   对于「双重 legacy」的 Raspberry Pi OS（Buster），GStreamer-1.14 并没有
    可用的补丁。作为替代方案，请先根据 [下面这些
    说明](https://github.com/FDH2/UxPlay/wiki/Building-latest-GStreamer-from-source-on-distributions-with-older-GStreamer-(e.g.-Raspberry-Pi-OS-).) 从源码编译一个
    较新的完整 GStreamer-1.18.6，
    然后再编译 UxPlay。

-   运行 32 位操作系统的 Raspberry Pi 3 Model B+ 也可以借助 GStreamer OMX
    插件访问 GPU（使用选项 "`-vd omxh264dec`"），但
    这一方式在 Pi 4 Model B 的固件下已经失效。OMX 支持已从
    Raspberry Pi OS（Bullseye）中移除，但在 Buster 中仍然存在。

-   **H265（4K）** 视频有可能在 Raspberry Pi 5 机型以及 Raspberry Pi 4 model B 上
    通过硬件解码获得支持：二者都使用一个
    专用的 HEVC 解码模块，但与之配套的 "rpivid" 内核驱动
    目前尚不被 GStreamer 支持（该驱动会把视频
    解码成一种非标准格式，GStreamer 无法支持它，
    除非该驱动进入 Linux 主线内核）。Raspberry Pi
    提供了一个可以使用这种格式的 ffmpeg 版本，但
    目前 UxPlay 还无法利用它。最好的解决方案是
    把该驱动「上游化」进内核，从而让 GStreamer 能够支持。
    （软件 HEVC 解码可以工作，但似乎无法在 Pi 上
    给出令人满意的结果）。

即使启用了 GPU 视频解码，性能较弱的机型仍可能丢弃部分帧，
以便利用时间戳让音频与视频保持同步。在 Legacy Raspberry Pi OS（Bullseye）中，raspi-config
的「Performance Options」允许指定分配给 GPU 的
内存量，但这一设置在 Bookworm 中似乎已经不存在（不过仍可
通过在 /boot/config.txt 中添加一行 "gpu_mem=128"，把它设为
例如 128MB）。一台 Pi Zero 2 W（内存为 512MB）在
32 位 Bullseye 或 Bookworm Lite 上、为 GPU 分配 128MB 的条件下
测试运行良好
（默认值似乎是 64MB）。

R Pi 上的基本 uxplay 选项是 `uxplay [-vs <videosink>]`。
选择 `<videosink>` = `glimagesink` 有时很有用。在使用
Wayland 视频合成器时，请使用 `<videosink>` = `waylandsink`。使用
framebuffer 视频时，请使用 `<videosink>` = `kmssink`。

* 提示：通过 ssh 在远程主机（例如 Raspberry Pi）上启动
    UxPlay：

```
ssh user@remote_host
       export DISPLAY=:0
       nohup uxplay [options] > FILE &
```

声音和视频将在远程主机上播放；如果 ssh 会话关闭，"nohup" 会让 uxplay
继续运行。终端输出会保存到 FILE
（可以把它设为 /dev/null 以丢弃这些输出）。

<a name="building-uxplay-on-macos-intel-x86_64-and-apple-silicon--macs"></a>
## 在 macOS 上编译 UxPlay：**（Intel X86_64 和 "Apple Silicon" Mac）**

*注：自 macOS 12 Monterey 起，macOS 已内置原生 AirPlay 服务器功能，
但它仅限较新的硬件使用。除了能在最新的 macOS 上运行，
UxPlay 也可以在无法运行 Monterey 的较旧 macOS
系统上运行，或者运行在能跑 Monterey
但无法使用 AirPlay 的系统上。*

以下 macOS 说明假定已经安装了 Xcode 命令行
开发者工具（如果已安装 Xcode，请打开终端，
输入 "sudo xcode-select --install" 并接受相关条款）。

同时还假定已安装 CMake \>= 3.13：这可以通过包管理器
[MacPorts](http://www.macports.org)
（`sudo port install cmake`）、[Homebrew](http://brew.sh)
（`brew install cmake`）完成，也可以从
<https://cmake.org/download/> 下载。如果你要用 `git` 来获取
UxPlay，也请一并安装它。

接下来安装 libplist 和 openssl-3.x。请注意，在 macOS 编译中
将使用这两个库的静态版本，因此如果你愿意，可以在
编译完 uxplay 之后把它们卸载。

-   如果使用 Homebrew：`brew install libplist openssl@3`

-   如果使用 MacPorts：`sudo port install libplist-devel openssl3`

否则，请从源码编译 libplist 和 openssl：参见本 README
末尾附近的说明；这需要安装开发工具（autoconf、automake、
libtool、*等等*）。

接下来获取适用于 macOS 的最新 GStreamer-1.0 发行版。

**使用「官方」GStreamer（推荐 MacPorts 和 Homebrew 用户
使用）**：请安装适用于 macOS 的 GStreamer 发行版，下载地址为
<https://gstreamer.freedesktop.org/download/>。（该发行版自带 pkg-config，因此你
无需另外安装。）请同时安装 gstreamer-1.0 和
gstreamer-1.0-devel 两个软件包。下载完成后，
按住 Shift 点击它们即可安装（它们会
安装到 /Library/FrameWorks/GStreamer.framework）。

* **由于 GStreamer 软件包未签名，较新的 macOS 会拒绝你
最初使用「Shift 点击」进行的安装：
此时你需要前往「System Settings」->「Privacy & Security」->「Security」，
然后点击「Open Anyway」以继续安装。**

如果你使用「官方」发行版，那么 Homebrew 或 MacPorts 用户
**不应**安装（或应当卸载）由
其包管理器提供的 GStreamer。

-   自 GStreamer v1.22 起，「官方」（gstreamer.freedesktop.org）
    的 macOS 二进制文件需要一个包在实际主程序（uxplay）外面的
    包装器 "gst_macos_main"。这一包装应当在
    UxPlay 编译过程中已经应用，并且 UxPlay 启动时的终端信息
    应当确认它正在被使用。（UxPlay 也可以使用
    「官方」GStreamer v.1.20.7 二进制文件编译，该版本
    无需包装器即可工作。）

**使用 Homebrew 的 GStreamer**：需要 pkg-config：（"brew install
pkg-config gstreamer"）。这会导致 Homebrew 安装大量
额外的软件包作为依赖。[Homebrew gstreamer
安装](https://formulae.brew.sh/formula/gstreamer#default) 最近
被重构成单个名为 `gstreamer` 的「formula」，它
现在无需设置 GST_PLUGIN_PATH 环境变量即可工作。
Homebrew 会把 gstreamer 安装到 `HOMEBREW_PREFIX/lib/gstreamer-1.0`，其中
默认情况下 `HOMEBREW_PREFIX/*` 在 Apple Silicon Mac 上是 `/opt/homebrew/*`，
在 Intel Mac 上是 `/usr/local/*`；请不要把你自己编译的额外
非 Homebrew 插件放在那里，而应改为把
GST_PLUGIN_PATH 设置为指向它们所在的位置（Homebrew 并不提供
完整的 GStreamer，但似乎已具备 UxPlay 所需的全部内容）。
**新增：UxPlay 的编译脚本现在还会检测安装于非标准
位置的 Homebrew，这些位置由下述环境
变量 `$HOMEBREW_PREFIX` 指明。**

**使用从 MacPorts 安装的 GStreamer**：MacPorts 现在提供
较新的 GStreamer 发行版：请安装
pkgconf（"sudo port install pkgconf"），然后执行 "sudo port install gstreamer1
gstreamer1-gst-plugins-base gstreamer1-gst-plugins-good
gstreamer1-gst-plugins-bad gstreamer1-gst-libav"。
（以下内容可能已不再适用：*若要在
macOS 上支持 X11，请使用特殊的 cmake 选项 `-DUSE_X11=ON` 编译 UxPlay，并
在 XQuartz 终端中以 -vs ximagesink 运行它；较旧的非 Retina
Mac 在使用 X11 时需要较低的分辨率：`uxplay -s 800x600`。）*

安装好 GStreamer 之后，编译并安装 uxplay：打开一个终端，
进入 UxPlay 源码目录（zipfile 下载为 "UxPlay-master"，
"git clone" 下载为 "UxPlay"），然后执行
"cmake . ; make ; sudo make install" 来编译并安装（与 Linux 相同）。


-   **新增**：UxPlay 现在可以选择提供自己的最小 mDNSResponder
    实现，它可以取代 Apple 内置的 Apple
    Bonjour 服务。由于在 Apple 平台上使用它似乎没有优势，
    因此在 macOS 上默认使用原生的 Bonjour 服务。若要
    使用 UxPlay 的实现（该实现已在 macOS 上测试并可用），请使用
    `cmake -DUSE_MDNS=1` 编译。
    

-   在检查 GStreamer 警告的同时运行 UxPlay（可以在运行 UxPlay 之前
    执行 "export GST_DEBUG=2"）会显示：由于
    默认（自 UxPlay 1.64 起）使用时间戳进行视频
    同步，大量视频帧被丢弃（只发生在 macOS 上），
    这也许是由另一个错误（与 videometa 有关）导致的，该错误会出现在
    GStreamer 的警告中。**建议：使用 UxPlay 的「无
    时间戳」选项 "`-vsync no`"**（你可以在
    uxplayrc 配置文件中添加一行 "vsync no"）。

-   在装有这套 GStreamer 的 macOS 上，可用的 videosink
    只有 glimagesink（由
    autovideosink 选出的默认值）和 osxvideosink。
    窗口标题不会显示
    AirPlay 服务器名称，但该窗口可以在 Zoom 上共享。
    由于 glimagesink 存在一些问题，你可能会发现
    osxvideosink 工作得更好。唯一可用的 audiosink 是
    osxaudiosink。

-   目前在 macOS 上默认使用选项 -nc。这
    是针对 macOS 上 GStreamer videosink 窗口关闭问题的变通做法。
    如果不需要，可以用 "-nc no" 取消这一选项。

-   对于 glimagesink，分辨率设置 "-s wxh" 可能不会
    影响（较小的）初始 OpenGL 镜像（投屏）窗口尺寸，但窗口
    可以用鼠标或触控板放大。

-   使用 `-vs osxvideosink` 时，图像会扩展以填满窗口，而不保持
    图像的宽高比。你可能
    希望改用 `-vs "osxvideosink force-aspect-ratio=true"` 来保持
    原始宽高比。

-   *在较旧的 GStreamer 版本中，存在窗口无法
    正常关闭的问题，需要 UxPlay 的 "-nc" 选项：这些问题
    在 GStreamer 中似乎已经修复，但如果你遇到它们，可以试试 "-nc"。*

遗憾的是，macOS 的蓝牙协议栈似乎不允许用户广播蓝牙 LE 服务发现所需的
那类蓝牙 LE 广播（即「厂商特定」广播），
但如果你购买一个自带蓝牙 LE 协议栈的 BleuIO USB 加密狗
（它以 USB 串行 modem 的形式工作），就可以实现这一点。蓝牙服务发现可以替代 Rendezvous/Bonjour DNS_SD，
并可用于不允许 DNS_SD 的网络。请参阅[下面的说明](#bluetooth-le-beacon-setup)。

**新增**：（仅限 macOS）当 UxPlay 编译为使用 Bonjour 时，macOS 主机现已支持来自客户端的 AWDL（Apple Wireless Direct Link）点对点 AirPlay 连接。
请确保 macOS 主机已启用 AirPlay 接收器（在「System Settings」->「General」->「AirDrop & Continuity」->「AirPlay」中；你可能需要
先将 AirPlay Receiver 关闭再重新打开才能让它工作）。请使用选项 `-p2p`，它的表现如同已使用 ``-pin`` 选项一样，
在客户端此前未通过 pin 与 UxPlay 认证过的情况下，要求输入一个随机的 一次性 pin（显示在 UxPlay 终端上）。
首次完成 pin 认证后，客户端无需再次认证，除非 UxPlay 的 deviceID 被更改。
（若要把固定的非随机 pin 设为例如 3939，请使用组合 `-p2p -pin 3939`。）


<a name="building-uxplay-on-microsoft-windows-using-msys2-with-the-mingw-64-compiler"></a>
## 在 Microsoft Windows 上使用 MSYS2 搭配 MinGW-64 编译器编译 UxPlay。

-   已在 64 位 x86_64 的 Windows 10 和 11 上、以及 ARM 上的 Windows 11 测试。

* **新增：Uxplay >=1.74 现在自带一个自包含的 mdns 替代实现来取代 Bonjour，因此除非
    你选择使用 Bonjour，第 1 步是不必要的。**  若要使用 Bonjour，请用 `cmake -DUSE_DNS_SD=1` 编译。

1.  在 UxPlay < 1.74 上（以及想在 UxPlay >= 1.74 上继续选用 Bonjour 时），你必须
    下载并安装 **Bonjour SDK for Windows v3.0**。你可以
    在无需任何注册的情况下从
    [softpedia.com](https://www.softpedia.com/get/Programming/SDK-DDK/Bonjour-SDK.shtml) 下载该 SDK，
    也可以从 Apple 官方站点获取
    [https://developer.apple.com/download](https://developer.apple.com/download/all/?q=Bonjour%20SDK%20for%20Windows)
    （从 Apple 站点获取需要先注册为开发者）。
    安装后 Bonjour SDK 应位于
    `C:\Program Files\Bonjour SDK`。

  * **新增：现在还提供另一种（非 mdns 的）服务发现方法：
    在 Windows 上使用蓝牙低功耗（BLE）信标。见[下面的说明](#bluetooth-le-beacon-setup)。



2.  （以下针对 64 位 Windows；32 位 Windows 的编译应当
    可行，但尚未测试。）我们将使用类 Unix 的 MSYS2 编译环境：
    请从官方站点下载并安装 MSYS2
    [https://www.msys2.org/](https://www.msys2.org)。接受默认的
    安装位置 `C:\mysys64`。

3.  [MSYS2 软件包](https://packages.msys2.org/package/) 使用 Arch Linux 所用 "pacman" 包管理器的
    一个变体来安装。请从 Windows
    开始菜单的 MSYS2 标签页打开一个 "MSYS2" 终端，
    并用 "pacman
    -Syu" 更新新装好的 MSYS2。 

    * _新增：在 Intel x84-64 系统上，MSYS2 现在建议使用较新的 UCRT64 终端环境（它使用较新的 Microsoft
    UCRT「Universal C RunTime Library」，自 Windows 10 起它已作为 Windows 操作系统的一部分提供）
    而不是 MINGW64 终端环境
    （后者使用较旧的 Microsoft MSVCRT C 库，该库处于「legacy」状态，但在所有 Windows 系统上都可用）。
    如果你希望使用 legacy 的 MSVCRT 库以支持较旧的 Windows 版本，请按如下方式修改下面的说明：
    (1) 把 MSYS2 终端类型从 UCRT64 改为 MINGW64；(2) 把 mingw-w64-ucrt-x86_64-* 软件包名改为 mingw-w64-x86_64-*（即去掉 "-ucrt"）；
    (3) 在路径和目录名中把 `ucrt64` 替换为 ``mingw64``。_

    * _新增：在 ARM 上（例如基于 Snapdragon 的 PC）：请按如下方式修改下面的所有说明：
    (1) 把 MSYS2 终端类型从 UCRT64 改为 CLANGARM64；(2) 把 mingw-w64-ucrt-x86_64-* 软件包名改为 mingw-w64-clang-aarch64-*；
    (3) 在路径和目录名中把 `ucrt64` 替换为 ``clangarm64``。_

    打开一个新的 MSYS2 终端（根据情况选择 UCRT64、CLANGARM64 或 MINGW64），并安装 gcc 编译器和 cmake：

       `pacman -S mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-gcc`

    我们就在 MSYS2 环境的命令行中直接编译
    UxPlay（编译系统使用 "`ninja`" 代替 "`make`"
    ）。

4.  从 github 下载最新的 UxPlay **（若要使用 `git`，请用
    `pacman -S git` 安装它，然后执行
    "`git clone https://github.com/FDH2/UxPlay`"）**，接着安装 UxPlay
    的依赖（openssl 已随 MSYS2 一并安装）：

    ```
        pacman -S mingw-w64-ucrt-x86_64-libplist mingw-w64-ucrt-x86_64-gstreamer mingw-w64-ucrt-x86_64-gst-plugins-base
    ```

    如果你在尝试其他 Windows 编译系统，GStreamer 为 Windows 提供的 MSVC
    版本可从 [GStreamer 官方
    站点](https://gstreamer.freedesktop.org/download/) 获取，但只有
    MSYS2 上的 MinGW 64 位编译版本经过测试。

5.  进入 UxPlay 源码目录，然后执行 "`mkdir build`" 和
    "`cd build`"。编译过程假定 Bonjour SDK 已
    安装在 `C:\Program Files\Bonjour SDK`。如果它在
    别的位置，请设置环境变量 BONJOUR_SDK_HOME 指向其
    所在位置。然后用下面的命令编译 UxPlay：

    `cmake ..`

    `ninja`

6.  假定这两步都没有出错，你就在当前的（"build"）目录中
    编译出了可执行文件 **uxplay.exe**。其他编译方式中提供的
    "sudo make install" 和 "sudo make uninstall" 功能
    在 Windows 上不可用；作为替代，你可以用下面的命令把
    uxplay.exe 可执行文件安装到 `C:/msys64/ucrt64/bin`（同时把 manpage 和
    文档安装到 `C:/msys64/ucrt64/share/...`）：

    `cmake --install . --prefix $HOME/../../ucrt64`
    之后如果要卸载 uxplay，可以回到 build 目录并运行

    `ninja uninstall`

    （这假定 build 目录中的某些文件自编译 UxPlay 以来没有被删除）。 

    若要查看 manpage，你需要安装 manpage
    查看器："`pacman -S man`"。

要运行 **uxplay.exe**，你需要安装一些 gstreamer 插件软件包，
使用 `pacman -S mingw-w64-ucrt-x86_64-gst-<plugin>` 安装，其中必需的
`<plugin>` 如下：

1.  **libav**
2.  **plugins-good**
3.  **plugins-bad**

你可能还会用到的其他 MSYS2 gstreamer 插件软件包列在
[MSYS2 软件包](https://packages.msys2.org/package/) 中。

你还需要授予 uxplay
可执行文件 uxplay.exe 通过 Windows 防火墙访问数据的权限。首次运行
uxplay 时，系统可能会自动询问你是否允许，你也可能需要手动设置：使用 **Windows Settings-\>Update and
Security-\>Windows Security-\>Firewall & network protection -\> allow an
app through firewall**。如果你的杀毒软件把 uxplay.exe 标记为
"suspicious"（但没有真正的恶意软件特征），
你可能需要为它添加
例外。

现在，在相应的 MSYS2 终端窗口（UCRT64/CLANGARM64/MINGW64）中运行 "`uxplay`" 进行测试。
如果 UxPlay 启动时没有报错，但客户端看不到它，这
几乎总是 Windows 防火墙的问题。除了上面的防火墙设置之外，
你可能还需要为 uxplay.exe 添加一条显式的 "Inbound-Allow"
规则，这可以在**管理员权限**的 PowerShell 中完成：

    ```powershell
    New-NetFirewallRule -DisplayName "UxPlay" -Direction Inbound `
        -Program "C:\path\to\uxplay.exe" -Action Allow `
        -Profile Private -Protocol Any
    ```

同时请检查：你的 PC 网络连接是否处于 **Private**
网络配置文件，而不是 Public（在 PowerShell 中运行 `Get-NetConnectionProfile` 可以
看到这一点 —— Windows 在 Public 网络上会更
激进地限制发现流量）；iPhone/iPad 与 PC 是否在
*同一个* Wi-Fi 网络上（没有一台使用蜂窝网络/VPN，也没有
启用「客户端/AP 隔离」的路由器/AP —— 在访客网络上
启用该功能会阻止设备互相发现，即使它们连的是同一个
SSID）；以及是否没有第三方杀毒软件/防火墙单独
阻止该应用。


如果需要
指定 audiosink，在 Windows 上有两个主要选择：较旧的
DirectSound 插件 "`-as directsoundsink`"，以及更现代的
Windows Audio Session API（wasapi）插件 "`-as wasapisink`"，它
支持[额外的
选项](https://gstreamer.freedesktop.org/documentation/wasapi/wasapisink.html)
例如

    uxplay -as 'wasapisink device=\"<guid>\"' 

其中 `<guid>` 用 GUID 指定一个可用的音频设备，该 GUID
可以用 "`gst-device-monitor-1.0 Audio`" 查出来：`<guid>` 的形式
类似 `\{0.0.0.00000000\}.\{98e35b2b-8eba-412e-b840-fd2c2492cf44\}`。如果
没有指定 "`device`"，则使用默认音频设备。

如果你想用 `-vs <videosink>` 选项指定 videosink，
`<videosink>` 的可选项有 `d3d12videosink`、``d3d11videosink``、```d3dvideosink```、
`glimagesink`、``gtksink``、```autovideosink```。   _有报告称
较新的 d3d12 videodecoder 在某些较旧的 Nvidia 显卡上、
当图像分辨率发生变化时（例如 iOS 客户端
在竖屏与横屏模式之间旋转时）会出现段错误：这是 GStreamer 的一个问题，
显然现在已经修复（一个变通办法是改用 d3d11）。_

-   在 Windows 上，使用 Direct3D 11.0 或更高版本时，可以通过
    例如 `-vs "d3d11videosink <options>"` 来设置各种选项（请参见这些 videosink 的 gstreamer
    文档）。
    为方便起见，如果没有设置 `<options>`，则会加入
    用 Alt-Enter 组合键进入和退出全屏模式的切换选项。
    **建议 Windows 用户在自己的 UxPlay 启动文件中加入一行 `-vs d3d12videosink`，
    以获得这个切换选项（autovideosink 通常会选中 d3d12videosink，
    但不会提供该切换选项**）。


可执行文件 uxplay.exe 也可以在不进入 MSYS2 环境的情况下运行，
即在 Windows Terminal 中使用完整路径，例如 `C:\msys64\ucrt64\bin\uxplay`。（这样 Windows 会在
可执行文件所在目录中查找所需的 MSYS2 DLL 库。）要避免使用完整路径，可以 
把 `C:\msys64\ucrt64\bin`（按需对 ``ucrt64`` 作相应修改）永久加入你的用户 path：
（在 Windows Settings -> System -> About -> Advanced System Settings -> Environment Varianbles 中操作：该设置
只在打开新的用户终端后才生效）。

Microsoft 提供了一个新的现代化 Windows Terminal 应用，它
可以提供多种终端，也可以定制为同时提供 MSYS2 终端。
请参阅 https://www.msys2.org/docs/terminals/ （为让那些说明更清楚：
在下拉的 "Settings" 菜单中，左下角还有第二个 "settings" 图标：
点击它即可按说明编辑 settings.json 文件）。

服务器名称（-n <name> 选项）可以用国际化的 UTF-8 编码给出：
要在 MSYS2 或其他 Windows 终端中输入 UTF-8 字符，请使用数字小键盘，
并打开 "Num Lock"：按住 "Alt" 键，先在小键盘上输入 "+"，然后
输入该字符的 UTF-8 十六进制编码（数字用小键盘输入），最后松开 "Alt" 键。
（UTF-8 十六进制编码有 4 位十六进制数字：例如 "copyright" 符号的十六进制编码是 00a9。）
_这个方法必须在 Windows 注册表中启用：使用
regedit 找到注册表项 'HKEY_Current_User/Control Panel/Input Method"，
并新增一个值为 "1" 的键 "EnableHexNumpad"，然后重启计算机。_

**新增（v1.74 中）**：重写后的 NTP 子系统可以使用内核（而非用户空间）的报文到达时间戳，
从而获得更高的 NTP 精度。它受大多数现代 Windows 系统支持。当 UxPlay 与客户端连接并
启动 NTP 时，控制台可能会输出一条消息，告知你服务器上的 Windows 支持内核时间戳，
但这些时间戳尚未启用。要启用它们：以管理员身份运行 Windows PowerShell，并执行下面的命令

```
Set-NetAdapterAdvancedProperty -Name "<name>" -DisplayName "Software Timestamp" -DisplayValue "RxAll"
```
这里的 "`<name>`" 是 Windows 上的适配器名称：_例如_ "Ethernet"、"Wi-Fi"、"Ethernet 2"、_等等_。	如果你的 Windows 系统**不**支持内核
时间戳，那么在使用 "`uxplay -d`" 调试选项时，你会看到一条确认这一点的消息。使用该选项时你还会看到 NTP 报文的到达
时间，它们被标记为 `(kernel)` 或 ``(clock)``，以表明是否正在使用内核时间戳。


<a name="usage"></a>
# 用法

> 本汉化版本新增两个选项：`-zh` / `--zh` 输出中文，`-en` / `--en` 输出英文（也可用环境变量 `UXPLAY_LANG`，详见页首说明）。

选项：

-   这些选项也可以写入 UxPlay 启动文件（每行一个选项，不带开头的
    "`-`" 字符），启动文件由
    环境变量 `$UXPLAYRC` 指定，或者是 `~/.uxplayrc` 或
    `~/.config/uxplayrc`；以 "`#`" 开头的行会被视为
    注释并被忽略。命令行选项会覆盖
    启动文件中的同名选项。

**-rc _file_** 也可用于指定启动文件的位置：这会
覆盖 `$UXPLAYRC`、``~/.uxplayrc`` 等设置。

**-n server_name**（默认值：UxPlay）；server_name@\_hostname\_ 将成为
向你的 iPad、iPhone
等设备提供 AirPlay 服务时显示的名称，其中 *hostname* 是运行 uxplay 的服务器名称。这
也将成为镜像显示（X11）窗口上方显示的名称。
**接受以 UTF-8 编码的国际化服务器名称。**

**-nh** 不在 AirPlay 服务器名称
末尾追加 "@_hostname_"。

**-h265** 启用 "ScreenMultiCodec" 支持（AirPlay "Features" 位
42），从而在屏幕镜像模式下除 h264（1080p）视频外还接受 h265（4K/HEVC）视频。
使用该选项时会创建两个"视频管道"
（一个用于 h264，一个用于 h265）。如果管道中的任何
GStreamer 插件是 h264 或 h265 专用的，则在每个管道中会使用
正确的版本。对于 4K 视频，有线客户端-服务器以太网连接优于
Wifi，客户端可能也会要求这样做。在请求高度 h \> 1080 的
分辨率 "-s wxh" 时，只有较新的 Apple 设备（M1/M2 Mac 或 iPad，以及部分 iPhone）
才能发送 h265 视频。
"-h265" 选项会把默认分辨率（"-s" 选项）从
1920x1080 改为 3840x2160，并将默认最大帧率（"-fps"
选项）保持为 30fps。

**-mp4 \[fn\]**  在观看/收听的同时，把镜像模式和音频模式的音视频
录制到 mp4 文件。文件名为 fn.n.(format).mp4，
（默认 "fn" = "recording"）。数字 `n` = 1,2,... 会随
每次新连接递增。"format"（例如 "H264.AAC"）表示 H264/H265 视频、
AAC/ALAC 音频。

**-hls \[v\]** 启用 HTTP Live Streaming 支持。使用该选项后，可以在 YouTube app 中
点击 AirPlay 图标，让 YouTube 视频直接从 YouTube 服务器
串流到 UxPlay（不经过客户端）。
可选的 \[v\]（允许值 2 或 3，默认：3）
用于选择播放 HLS 视频时使用的 GStreamer
"playbin" 视频播放器版本。_（Playbin v3
是推荐的播放器，但如果某些视频无法播放，可以尝试
使用版本 2。）_

**-lang \[list\]**  为 YouTube app 的 HLS 视频指定语言偏好，
其中一些现在提供多语言版本选择（对原声使用 AI 配音）。如果未使用该选项，
则偏好将取自环境变量（$LANGUAGE、$LC_ALL、$LC_MESSAGES、$LANG，按
该顺序查找，直到找到为止）。通过冒号分隔的列表
指定优先顺序：例如 `fr:en-US:en`，表示法语（第一
选择，任意变体）、英语（第二选择，美国地区变体）、英语（第三选择，任意变体）。
处理前会移除字符串中的所有空白字符；如果 `-lang` 选项后
没有跟列表，则会清除之前的所有语言选择。

**-slang \[list\]**。与 `-lang` 类似，但用于指定字幕语言的偏好。
（如果未指定，则使用 `-lang ...` 指定的偏好。）

**-scrsv n**。（自 1.73 起）（目前仅在
使用 D-Bus 的 Linux/*BSD 系统上实现）。在无键盘输入时
（例如观看视频时）抑制屏保，使用
org.freedesktop.ScreenSaver D-Bus 服务：
n = 0：（关闭）n= 1（视频活动期间开启）n=2（始终开启）。
_注意：要验证此功能是否生效，可以使用 `dbus-monitor`
查看 D-Bus 上的事件；视桌面环境而定，
像
`gnome-session-inhibit -l`、``xfce4-screensaver-commannd -q`` 等命令，
应会在 UxPlay 抑制屏保时
列出 UxPlay。_

**-pin \[nnnn\]**：（自 v1.67 起）在新客户端首次连接时
使用 Apple 风格的（一次性）"pin" 认证：终端会
显示四位 PIN 码，客户端屏幕上
会显示输入该码的登录提示。当单独使用 "-pin" 时，
每次认证都会生成新的随机 PIN 码；如果使用
"-pin nnnn"（例如 "-pin 3939"），则会设置一个固定不变的
码。认证会把服务器加入客户端的
"受信任服务器"列表，只要客户端和服务器公钥
保持不变，客户端就不需要重新认证。（自 v1.68 起，
默认情况下服务器公钥由 MAC
地址生成，可用 -m 选项更改；密钥生成的另一种方法请参见 -key 选项
）。*（如果希望 UxPlay 服务器采用 pin
认证协议，请在 UxPlay 启动文件中
添加一行 "pin"。）*

**-p2p**：（仅限使用 Apple Bonjour DNS-SD 后端的 macOS）还会在 Apple 点对点
接口（包括 AWDL）上公告 UxPlay，并接受
从这些接口发起的连接。当客户端和服务器不共享可用局域网时，
这可以让 UxPlay 仍可使用。该选项
必须与 **-pin \[nnnn\]** 一起使用，后者启用了此功能所需的
旧式配对路径。由于 **-p2p** 会让接收端可被附近的 Apple 设备发现，
因此使用固定或随机 PIN 码也是一项重要的访问
控制措施。此功能使用 macOS 私有套接字选项
`SO_RECV_ANYIF`；当 UxPlay 以 `-DUSE_MDNS=1` 构建时该功能不可用。

* ** 要使用此功能，请确保运行 UxPlay 的 macOS 主机已
启用 AirPlay 接收功能，并允许相应类别的用户使用它。
在 macOS 16 中，可通过系统设置->通用->隔空投送与接力->AirPlay 完成此设置


**-reg \[*filename*\]**：（自 v1.68 起）。如果使用了 "-pin"，该选项
会在 \$HOME/.uxplay.register 中维护一份经 pin 认证的
"受信任客户端"登记表（也可以选择存放在 *filename* 中）。如果不使用此
选项，那么跳过 pin 认证的回头客户端会被直接信任，
而不做检查。如果 UxPlay 用于更
公开的环境，此选项可用于记录客户端详细信息；登记表是文本文件，每行
一个客户端，包含客户端公钥（base-64 格式）、设备 ID
和设备名称；注释掉（用 "\#"）或删除某一行
即注销对应客户端（控制客户端访问的更多方法请参见 -restrict、-block、
-allow 选项）。*（如果希望使用此功能，
请在启动文件中添加一行 "reg"。）*

**-pw** [*pwd*]。 （自 1.72 起）。作为 -pin 的替代方案，客户端访问
可以用密码控制。如果在 uxplay 启动时
设置了一个密码 *pwd*（长度至少为
六个字符，通常设置在启动文件中，以
明文存储），那么所有用户都必须知道此密码才能连接到 UxPlay
（客户端会提示输入）。
此方法使用 HTTP md5 Digest 认证，
现在被认为安全性较弱，但它仅用于
校验 uxplay 密码，不会暴露任何用户凭据。
认证成功后，客户端会保存该密码，并在后续认证中
首先使用它而不再提示，只要
UxPlay 的 deviceID 未发生变化（如果 UxPlay 密码已更改，
这次初始认证会失败）。
如果 UxPlay 启动时 -pw 选项**未**指定 *pwd*，则
会为**每次**新连接生成新的随机 4 位 PIN 码，并显示在 UxPlay 终端上，
该码必须在客户端
输入（在更换之前
有三次输入机会）。
_注意：-pin 与 -pw 是互斥的替代方案：如果启动时两者都指定，则
这两个选项中较早的那个会被丢弃。_

**-vsync \[x\]**（在镜像模式下：）此选项（**现在是默认值**）
在服务器上使用时间戳同步音频与视频，并可指定
可选的音频延迟，单位为（十进制）毫秒（*x* = "20.5" 表示
0.0205 秒延迟：允许小于一秒的正延迟或负延迟。）
在缺少硬件视频解码的低功耗系统（如 Raspberry Pi）上
需要使用该选项。

**-vsync no**（在镜像模式下：）这会关闭基于时间戳的
音视频同步，恢复 UxPlay-1.64 之前的
默认行为。标准桌面系统在不使用时间戳时似乎
工作良好：此模式适用于"实时串流"场景，例如把
UxPlay 用作 Mac 电脑的第二显示器，或监控网络摄像头；
使用该模式时不会丢弃任何视频帧。

**-async \[x\]**（在纯音频（ALAC）模式下：）此选项
使用时间戳在服务器上同步音频与客户端上的视频，
并可指定可选的音频延迟，单位为（十进制）毫秒（*x* = "20.5"
表示 0.0205 秒延迟：允许小于一秒的
正延迟或负延迟。）由于客户端会加入视频延迟以补偿
时延，因此在 -async 模式下服务器会加入等效的音频延迟，
这意味着暂停或切换曲目等音频变化
不会立即生效。*原则上，这可以通过
使用 `-al` 音频延迟设置来改变服务器向客户端报告
的延迟（默认 0.25 秒）来缓解，但就目前而言
改变它似乎没有任何效果*。

**-async no**。这仍是纯音频
模式的默认行为，但作为命令行选项，它可用于关闭
"uxplayrc" 配置文件中设置的 `-async` 选项。

**-db *low*\[:*high*\]** 把 AirPlay 音量控制衰减（增益）
从 -30dB:0dB 重新缩放为 *low*:0dB 或 *low*:*high*。下限
*low* 必须为负（衰减）；上限 *high* 可以
为任意符号。（GStreamer 会限制由 *high* 带来的音量提升，
使其不能超过 +20dB）。缩放是"线性"的，因此对于 -db
-50:10，AirPlay 衰减变化 -7dB 会换算为 -7 x
(60/30) = -14dB 的衰减，而最大音量（AirPlay 0dB）则变为
10dB 的提升，AirPlay -30dB 会变成 -50dB。注意，
AirPlay 的最小值（恰好 -30dB）会被转换为"静音"。

**-taper** 提供"渐变式"AirPlay 音量控制曲线（与
名为 "dasl-tapering" 的曲线一致，见
[shairport-sync](https://github.com/mikebrady/shairport-sync)）：每次
音量滑块长度（或静音以上的档位数，
其中 16 档 = 满音量）减少 50%，感知音量就
减半（衰减 10dB）。（在低音量时会做调整，
如果"非渐变"音量更响则使用后者。）

**-vol *v*** 设置初始音频串流音量（在客户端上）：范围为 [0:1]，
其中 0.0 = 静音，1.0 = 满音量（*v* 为十进制数）。

**-s wxh** 例如 -s 1920x1080（= "1080p"），指 h264 视频的
默认宽度和高度分辨率（单位像素）。（使用 -h265 选项时
默认值变为 3840x2160（= "4K"）。）这只是向
AirPlay 客户端发出的请求，最终得到的可能并不是该分辨率。w
和 h 是不超过四位的整数。注意，
**高度**像素值才是客户端用来
决定串流格式的控制项；宽度会根据
图像形状动态调整（竖屏或横屏格式，例如取决于
iPad 的持握方式）。

**-s wxh@r** 同上，但还会告知 AirPlay 客户端
显示器的屏幕刷新率。默认为 r=60（60 Hz）；r 必须是
小于 256 的整数。

**-o** 为显示窗口开启"过扫描"选项。这会
占用一部分由 -s wxh 选项请求的像素
（或其默认值 1920x1080），通过添加一圈未使用的空像素边界
来降低图像分辨率（在会过扫描的全屏显示中
这部分像素本会丢失，且 gstreamer 不会显示它们）。
建议：除非有特殊
理由，**不要使用此选项**。

**-fs** 使用全屏模式，但目前仅支持 X11、Wayland、vaapi、
kms 和 D3D11（Windows）。

**-p** 允许选择 UxPlay 使用的网络端口（如果服务器位于
防火墙之后，这些端口需要开放）。单独使用 -p 会设置
"旧式"端口 TCP 7100、7000、7001，UDP 6000、6001、7011。-p n（例如 -p
35000）会设置 TCP 和 UDP 端口 n、n+1、n+2。-p n1,n2,n3（逗号分隔
的值）会分别设置每个端口；-p n1,n2 会设置端口 n1、n2、n2+1。-p
tcp n 或 -p udp n 则只设置 TCP 或 UDP 端口。端口必须位于
范围 \[1024-65535\] 内。

如果不使用 -p 选项，端口会被动态
（随机）选择，这在有防火墙运行时将无法正常工作。

**-avdec** 强制使用 GStreamer 元素
avdec_h264（libav h264 解码器）进行软件 h264 解码。此选项应能阻止
autovideosink 选择硬件加速的 videosink 插件，例如
vaapisink。

**-vp *parser*** 选择 GStreamer 管道的 h264 解析器元素，
默认为 h264parse。使用引号 "..." 可以附加选项。

**-vd *decoder*** 选择 GStreamer 管道的 h264 解码器元素，
而不是使用默认值 "decodebin"（由它替你选择）。
软件解码由 avdec_h264 完成；各种硬件解码器
包括：vah264dec（vaapih264dec 的替代品）、nvdec、nvh264dec、v4l2h264dec（这些需要
具备相应的硬件）。使用引号 "..." 可以在解码器名称中
附带一些参数。

**-vc *converter*** 选择 GStreamer 管道的视频转换器
元素，而不是使用默认值 "videoconvert"。当通过 GPU 使用
Video4Linux2 硬件解码时，`-vc  v4l2convert` 也会
使用 GPU 进行视频转换。使用引号 "..." 可以在转换器名称中
附带一些参数。

**-vs *videosink*** 选择 GStreamer 的 videosink，而不是
使用默认值 "autovideosink"（由它替你选择）。一些 videosink
可选值包括：ximagesink、xvimagesink、vaapisink（用于 Intel 显卡）、
gtksink、glimagesink、waylandsink、osxvideosink（用于 macOS）、kmssink
（用于没有 X11 的系统，如 Raspberry Pi OS lite）或 fpsdisplaysink
（以 fps 显示串流帧率）。使用引号 "..." 可以
在 videosink 名称中附带一些参数。例如，
**fullscreen**（全屏）模式由 vaapisink 插件支持，可通过
`-vs "vaapisink fullscreen=true"` 获得；这同样适用于
`waylandsink`。此类选项的语法因插件而异
（参见 GStreamer 文档），某些 videosink 选择可能在你的系统上
无法工作。 _注意，vaapisink 已被标记为 "deprecated"
（已过时），不再推荐。_

**-vs 0** 抑制串流视频的显示。在镜像模式下，
客户端屏幕仍会以每秒 1 帧的降低后的帧率被镜像，但
不会被渲染或显示。如果服务器是"无头"的（没有连接用于显示视频的
屏幕），并且只用于渲染音频，
就应始终使用此选项；此时在镜像模式下（视频未渲染）音频为 AAC
有损压缩音频，而在 AirPlay 纯音频模式下则为
质量更高的 ALAC Apple Lossless 音频。

**-vrtp *pipeline***：  把解密后视频的 rtp 包转发到别处，而不进行渲染。
会根据情况使用 rtph264pay 或 rtph265pay：*pipeline* 应以任意
rtph26xpay 选项开头（例如 config_interval= 或 aggregate-mode =），后面接
发送方式：  *例如*，`"config-interval=1 ! udpsink host=127.0.0.1 port=XXXX`"。
一个基于 GStreamer 的测试接收端如下

```
gst-launch-1.0 -v \
udpsrc port=XXXX \
! 'application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96' \
! rtph264depay   ! h264parse   ! decodebin   ! videoconvert   !
autovideosink sync=false 
```
_（把 XXXX 替换为你要使用的端口：确保它没有被防火墙拦截；如果你是
在串流 h265 视频，请把 "264" 替换为 "265"。）_

* 要在 OBS-studio 中使用 -vrtp 选项，请安装 [obs-gstreamer](https://github.com/fzwoch/obs-gstreamer) 插件；安装
插件后，
OBS-studio "来源"窗口中的 "+" 图标会显示一个名为 "GStreamer Source" 的条目，你应在其中添加 GStreamer 解码器管道
"``udpsrc port=XXXX ! application/x-rtp,media=video,encoding-name=H264,payload=96 ! rtph264depay ! decodebin ! videoconvert ! video.``".

**-artp *pipeline***：  把解码后的音频以 L16 RTP 包（PCM 格式 S16BE）转发到别处，而不进行渲染。
使用 rtpL16pay（16 位有符号大端 PCM，44100Hz 立体声）：*pipeline* 应以任意
rtpL16pay 选项开头（例如 pt=96），后面接一种发送方式：
*例如*，`"pt=96 ! udpsink host=127.0.0.1 port=5002"`。  通过 RTP 时 iOS 音量控制仍然有效。
一个可播放该流的基于 GStreamer 的测试接收端如下


```
gst-launch-1.0 -v \
udpsrc port=5002 \
! application/x-rtp, media=audio, payload=96, clock-rate=44100, encoding-name=L16, format=S16BE, channels=2 \
! rtpL16depay ! audioconvert !
autoaudiosink sync=false
```

**-v4l2** 通过 Video4Linux2 由 GPU 进行硬件 h264 视频解码的视频设置。
等同于 `-vd v4l2h264dec -vc v4l2convert`。

**-bt709** 一项变通方案，用于解决旧版 Video4Linux2 插件无法
识别 Apple 对数字电视 bt709 色彩标准所采用的一种不常见（但被允许）的
"全范围色彩"变体的问题。GStreamer-1.20.4 及其向后移植版本
中已不再需要，但在 GStreamer-1.22 及更高版本中似乎
又再次成为必需。

**-srgb** 一项变通方案，用于解决无法显示全范围 8 位色彩
[0-255]、反而被限制为有限范围 [16-235] "合法 BT709"
HDTV 格式的问题。    该变通方案在 x86_64 桌面系统上有效，但
在 Raspberry Pi 上尚不可用。  该问题可能在未来的 GStreamer
版本中修复：它只出现在 Linux 和 \*BSD 上。

**-srbg no**。禁用 -srgb 选项；该选项在
Linux 和 *BSD 上默认启用，但在 Raspberry Pi 上可能无效，也可能并不需要，
因为它会增加额外的处理负载。

**-as *audiosink*** 选择 GStreamer 的音频接收器（audiosink），而不是让
autoaudiosink 替你挑选。一些 audiosink 可选值包括：pulsesink、
alsasink、pipewiresink、osssink、oss4sink、jackaudiosink、osxaudiosink
（用于 macOS）、wasapisink、directsoundsink（用于 Windows）。使用引号
"..." 或许可以附带一些可选参数
（例如 `-as "alsasink device=..."` 用于指定非默认的输出
设备）。此类选项的语法因具体插件而异（参见
GStreamer 文档），并且某些 audiosink 选择可能无法在你的
系统上工作。

**-as 0**（或仅用 **-a**）会禁止播放串流的音频，但仍
显示串流视频。

**-al *x*** 在仅音频（ALAC）模式下指定向客户端报告的音频延迟 *x*，单位为
（十进制）秒。允许的取值范围为
\[0.0, 10.0\] 秒，并且会被换算为整数
微秒。默认值为 0.25 秒（250000 微秒）。*（不过，
客户端似乎会忽略这个上报的延迟，因此该选项看起来
并不起作用。）*

**-ca**（不指定文件名）现在会显示
  在"仅音频"（ALAC）模式下播放 Apple Music 时随附的"封面图"。

**-ca *filename*** 提供一个文件（*filename* 可以包含完整
路径），用于在仅音频 ALAC 模式下输出"封面图"（来自 Apple Music 等）。
每当新的封面图到达时，该文件都会被覆盖。
如果未使用该选项，封面图（jpeg 格式）会被丢弃。
请配合在图像变化时重新加载的查看器使用，或定期重新加载
（*例如* 每秒一次）。为此，
请在后台运行 "`uxplay -ca [path/to/]filename &`"，然后在前台运行
图像查看器。例如，使用 `feh` 作为查看器：运行
"`feh -R 1 [path/to/]filename`"（在与
把 uxplay 放到后台的同一个终端窗口中）。要退出，使用 `ctrl-C fg ctrl-C` 来
终止图像查看器、把 `uxplay` 切回前台，然后
也终止它。

**-md *filename*** 类似 -ca 选项，但会把音频元数据文本
（Artist、Title、Genre 等）导出到文件，以便监视该文件变化的进程
进行显示。每当收到新的元数据时，之前的文本会被覆盖，
并且该文件会在 uxplay 终止时删除。

**-reset n** 设置客户端连续发送反馈请求失败的上限为 *n* 次
（这些"心跳信号"由客户端每秒发送一次，
用于请求一个表明服务器仍在线的响应）。
在缺失 *n* 个信号之后，客户端将被推定为离线，
连接会被重置以允许新的连接。*n* 的默认
值为 15 秒；*n* = 0 表示"无限制"。

**-nofreeze** 在因客户端离线而重置之后关闭视频窗口
（默认保持窗口打开，以便更平滑地重新连接到
同一客户端）。该选项在全屏模式下可能有用。

**-nc** 保持 UxPlay \< 1.45 之前的行为，即在客户端发送
"停止镜像"信号时**不关闭**视频窗口。*该选项目前在 macOS 上
默认启用，因为由 GStreamer 在 macOS 中创建的窗口
如果在 GStreamer 管道关闭时仍然打开，就
无法正确终止（它会
导致段错误）。*

**-nohold** 当有新客户端尝试连接时，丢弃当前连接。
不使用该选项时，当前客户端会独占 UxPlay
的所有权，直到它断开连接。

**-restrict** 将允许连接的客户端限制为
由 `-allow <deviceID>` 指定的那些。deviceID 的形式是 MAC 地址，
它会在客户端尝试连接时由 UxPlay 显示，并且似乎是
不可更改的。其格式为 `XX:XX:XX:XX:XX:XX`，X = 0-9、A-F，并且
很可能是该设备"真正的"硬件 MAC 地址。请注意，iOS
客户端通常会对不同网络暴露不同的随机"私有 Wi-Fi 地址"
（"假的" MAC 地址）（出于隐私原因，为了
防止被追踪），这些地址可能会变化，并且与
deviceID 并不对应。

**-restrict no** 移除限制（默认）。将其用作
命令行参数来覆盖启动文件中设置的限制会很方便。

**-allow *id*** 在正在执行客户端限制时，将 deviceID = *id* 加入允许的
客户端列表。通常这会作为 uxplayrc 启动文件中的
一个条目。

**-block *id*** 始终阻止 deviceID = *id* 的客户端，即使
总体上并未执行客户端限制。通常这会
作为 uxplayrc 启动文件中的一个条目。

**-FPSdata** 开启对客户端定期发送的视频串流
性能报告的监视。如果使用该选项，这些报告
会显示在终端窗口中。数据由客户端
以 1 秒的间隔更新。

**-fps n** 设置 AirPlay 客户端串流视频的最大帧率（单位：帧/秒）；
n 必须是小于 256 的整数。
（客户端可以选择以低于此值的任意帧率提供视频；
默认值为 30 fps。）设置为 60 fps 可能会带来更好的画质，但
不建议在 Raspberry Pi 上使用。如果你同时运行多个
uxplay 实例，把该值设为低于 30 fps 可能
有助于降低延迟。*该设置只是对客户端
设备的建议，因此设置较高的值并不会强制产生高帧率。*（你
可以用 "-vs fpsdisplaysink" 来测试，看看实际接收到的
帧率，或使用 -FPSdata 选项，它会显示客户端在
视频串流期间持续发送的串流
性能数据。）

**-f {H\|V\|I}** 实现 "videoflip" 图像变换：H = 水平
翻转（左右翻转，或镜像）；V = 垂直翻转；I = 180
度旋转或倒置（即 H 与 V 的组合）。

**-r {R\|L}** 90 度向右（顺时针）或向左（逆时针）
旋转；这些图像变换会在任何 **-f**
变换之后执行。

**-m \[mac\]** 更改 UxPlay 使用的 MAC 地址（Device ID）
（默认使用宿主机网卡所报告的真正硬件
MAC 地址）。（如果你尝试在同一台计算机上运行
多个 uxplay 实例，那么每个运行中的 uxplay 都需要不同的 server_name、MAC 地址和
网络端口。）如果未给出 \[mac\]（格式为
xx:xx:xx:xx:xx:xx，6 个十六进制字节），则会生成
一个随机 MAC 地址。如果 UxPlay 无法找到网卡的
真正 MAC 地址（更具体地说，是检测到的第一个活动
网络接口所使用的 MAC 地址），那么即使未指定选项
**-m**，也会使用随机 MAC 地址。（请注意，随机 MAC 地址
在每次启动 UxPlay 时都会不同）。

**-key \[*filename*\]**：这个（更安全的）用于生成并
保存持久公钥（-pin 选项需要用到）的选项，默认已被
一个（较不安全的）方法取代，该方法从服务器的
"device ID"（即 MAC 地址，可用 -m 选项更改，
方便地作为启动文件选项）生成密钥。当使用
-key 选项时，如果该文件不存在，就会生成一对
安全生成的密钥对并存放于 `$HOME/.uxplay.pem`；如果
它已存在，则从该文件中读取。（可选地，密钥可以
存放在 *filename* 中。）该方法比新的默认方法更安全
（因为 Device ID 会在 DNS_SD 广播中公开），但仍然
会让私钥暴露给任何能够访问该 pem 文件的人。该选项
应当作为一行 "key" 或 "key *filename*"（不带开头的
"-"）设置在 UxPlay 启动文件中，其中 *filename* 是完整
路径，如果包含任何空格，就应当用引号（`"...."`）括起来。
**因为默认方法更简单，而且客户端接入 uxplay 的安全性
不太可能是重要问题，所以 -key 选项已不再
被推荐**。

**-dacp \[*filename*\]**：将当前客户端的 DACP-ID 和
Active-Remote 密钥导出到文件：默认为 \$HOME/.uxplay.dacp。（可选地
可改为 *filename*）。可供遥控
应用程序使用。文件是临时的：仅在客户端连接期间存在。

**-vdmp** 把 h264 视频转储到文件 videodump.h264。-vdmp n 会把
不超过 n 个 NAL 单元转储到 videodump.x.h264；x= 1,2,... 每当有
SPS/PPS NAL 单元到达时就递增。要更改 *videodump* 这个名称，请使用
-vdmp \[n\] *filename*。

**-admp** 把音频转储到文件 audiodump.x.aac（AAC-ELD 格式音频）、
audiodump.x.alac（ALAC 格式音频）或 audiodump.x.aud（其它格式
音频），其中 x = 1,2,3... 每当音频格式改变时就递增。
-admp *n* 会把转储到文件的包数量限制为 *n* 个
或更少。要更改 *audiodump* 这个名称，请使用 -admp \[n\] *filename*。*注意
（与转储的视频不同）转储的音频目前只对
调试有用，因为它没有被封装成容器，无法用标准
音频播放器播放。*

**-ble [*filename*]**。  启用蓝牙信标服务发现。
UxPlay 进程的端口、PID 和进程名默认记录在
`~/.uxplay.ble` 中：（该文件在
UxPlay 启动时创建，在它停止时删除。）
也可以选择改用文件
*filename*，它必须是可写文件的完整路径。
__有关信标设置的说明__
__请见下文。__

**-d \[n\]** 启用调试输出；可选参数 n=1 会抑制调试输出中的音频/视频
包数据。
注意：这不会显示 GStreamer 的错误或
调试消息。要查看 GStreamer 的错误和警告消息，请在运行
uxplay 之前用 "export GST_DEBUG=2" 设置环境变量
GST_DEBUG。要查看 GStreamer 的信息消息，设置 GST_DEBUG=4；要查看
DEBUG 消息，设置 GST_DEBUG=5；调高该值可以看到更多
GStreamer 内部运作细节。

<a name="bluetooth-le-beacon-setup"></a>
# 蓝牙 LE 信标设置

用于运行蓝牙 LE 服务发现信标的 python>=3.6 脚本是 uxplay-beacon.py。
除了标准的 python 库之外，它还需要 python3-psutils。

它提供了四种可能的蓝牙 LE 实现（以模块 `uxplay_beacon_module_*.py` 的形式加载），它们可能需要额外的库：

* **BlueZ** 用于带 D-Bus 的 Linux 系统：需要 **GLib**（来自 python3-gi 或 PyGObject）和 **python-dbus**。

* **winrt**  用于 Windows：需要一些 **winrt-Windows-\*** 库。

* **BleuIO** 用于所有操作系统：需要 **pyserial**。  它还需要 [BleuIO（或 BleuIO Pro）USB 适配器](https://www.bleuio.com)，这是一个 USB 串行设备，
    带有自己的板载蓝牙 LE 协议栈，不使用宿主操作系统的协议栈（宿主会将该设备视为一个 USB 串行调制解调器）。它
    适用于所有提供串行设备访问的操作系统，包括 macOS 和 \*BSD。    在某些 Linux 上，需要把用户加入
    `dialout` 组，在另一些上则是 ``uucp``；在 FreeBSD 上是 ```dialer``` 组，在其它 \*BSD 上，它
    可能是 `uucp`。 

* **HCI** 用于 Linux 和 FreeBSD：不需要额外的库，但需要以 root 身份访问蓝牙设备的 HCI（主机控制器接口），使用工具
    `hcitool` 和 ``hciconfig``（Linux）或 ```hccontrol```（FreeBSD）。  关于如何提供此类访问权，见下文。      此外，
    FreeBSD 的 `hccontrol` 需要一个补丁才能输入通用的 LE 广播数据。我们已经把它作为 Pull Request 提交给 FreeBSD，
    你可以在 [UxPlay Wiki](https://github.com/FDH2/UxPlay/wiki/hccontrol-patch-for-FreeBSD-15.0) 上找到它。_注意，macOS
    有一个工具 `/usr/sbin/bluetool`，它类似 ``hcitool``，可能可以让 HCI 模块
    扩展以支持 macOS，但由于 BleuIO 模块在 macOS 上已经可用，这一尝试尚未进行（欢迎提交可用的
    实现 Pull Request！）。_

在 Linux 上，必须安装蓝牙支持（使用官方 Linux 蓝牙协议栈 BlueZ 和 D-Bus）（在基于 Debian 的系统上：`sudo apt install bluez bluez-tools`；
较新的 Ubuntu 发行版以 snap 包形式提供 bluez）。  BlueZ 工具 'hcitool' 和 'hciconfig'（如果你在 Linux 上使用 HCI 模块则
需要它们）被 BlueZ 开发者声明为"已废弃"：一些 Linux 发行版
已把它们从默认的 BleuZ 包中移到名为 "bluez-deprecated" 之类的"额外"包中。
此外还要安装 uxplay-beacon.py 所使用的
psutil Python 库。
在基于 Debian 的系统上：

```
sudo apt install  python3-psutil
```


对于 **BlueZ** 模块（Linux），安装 python3-gi（GLib 由它导入）和 python3-dbus。
如果你的 Linux 发行版中没有 python3-gi 包，可以改用 `pip` 安装 PyGObject。

对于 **winrt** 模块，要在 MSYS2 UCRT64 环境中支持 Windows，请使用 pacman -S
安装 `mingw-w64-ucrt-x86_64-python`、`*-python-psutil` 和 ``*-python-pip``。  然后
使用 pip（或 pip3）安装 **winrt** 绑定：

```
pip install winrt-Windows.Foundation 
pip install winrt-Windows.Foundation.Collections 
pip install winrt-Windows.Devices.Bluetooth.Advertisement 
pip install winrt-Windows.Storage.Streams
```
对于 python >= 3.11，在"外部管理"的 python 安装（例如 MSYS2 提供的那个）上，pip 命令应当为

```
pip install ....  --break-system-packages
```
`--break-system-packages` 选项是作为一项要求加上去的，目的是让用户在添加
并非由"外部管理"提供的包之前有所迟疑：
_这其实不必要地吓人，因为在 winrt 包这种情况下，不会发生任何损坏_。

对于 **BleuIO** 模块，安装 pyserial。

对于 **HCI** 模块，创建一个组 `hciusers`，赋予组成员免密码使用 ``sudo -n hci*`` 的权限（```hci*``` 指的是
`hcitool` 和 ``hciconfig``（Linux）或 ```hccontrol```（FreeBSD）），然后把使用该模块的用户加入这个组
（_应当考虑其安全影响_）。  在 Linux 上，使用 "`sudo visudo /etc/sudoers.d/hciusers`"（在 FreeBSD 上，
文件是 `/usr/local/etc/sudoers.d/hciusers`）来创建一个包含以下某一行内容的文件：

```
%hciusers ALL=(ALL) NOPASSWD: /usr/bin/hcitool, /usr/bin/hciconfig       (Linux)
%hciusers ALL=(ALL) NOPASSWD: /usr/sbin/hccontrol                        (FreeBSD)
```

必须使用 "`uxplay -ble [path_to_file]`" 选项运行 UxPlay（这样它会把蓝牙信标的数据写入默认的 BLE
数据文件 `~/.uxplay.ble`，或可选地写入由其路径指定的文件），然后在一个单独的终端中运行 ``uxplay-beacon.py [HCI, BleuIO] [--path path_to_file]``。
如果没有给出 HCI 或 BleuIO 选项，就会使用该操作系统的默认模块（Linux 用 BlueZ、Windows 用 winrt、其它系统用 BleuIO）。

该 python 脚本会在检测到 UxPlay 正在运行（通过检查 BLE 数据文件是否存在）时
开始蓝牙 LE 服务发现广播，并在不再检测到运行中的
UxPlay 时停止（如果 UxPlay 之后重新出现，它会重新开始广播）。  该脚本会一直保持活动，直到在其
终端窗口中用 Ctrl+C 停止它（或关闭其终端窗口）。

信标脚本可以用某些选项进行更精细的控制：这些选项可以在命令行上给出，也可以从
配置文件 `~/.uxplay.beacon`（如果存在）中读取。配置文件条目的写法与命令行形式相同，每行一个（例如
`--ipv4 192.168.1.100`）。  以 ``#`` 开头的注释行会被忽略。  命令行选项会覆盖配置文件
中的选项。  使用 `man uxplay-beacon` 或 ``uxplay-beacon.py --help`` 获取帮助。


选项包括

* ```<module>```，其中 "module" 是 BleuIO 或 HCI（开头不带 ``--``）。  如果不使用该选项，所用默认模块将是 **BlueZ**（Linux）、**winrt**（Windows）、**BleuIO**（其它所有操作系统）。


* `--file <config file>` 从 ``<config file>`` 而不是
`~/.uxplay.beacon` 读取信标选项。

* `--ipv4  <ipv4 address>`。  该选项可用于指定客户端应当联系 UxPlay 服务器的 ipv4 地址。如果
没有给出，地址将被自动获取（如果自动选择失败，请用该选项指定地址）。  仅支持 ipv4 地址。

* `--path <BLE data file>`。  这会覆盖信标脚本所监视的默认 BLE 数据文件（``~/.uxplay.ble``）选择。  这同样要求
uxplay 以 "`uxplay -ble <BLE data file>`" 选项运行。

这些是 Windows 上 **winrt** 模块唯一接受的选项。  其它模块还接受

* `--advmin x`、``--advmax y``。  它们控制 BLE 广播之间的间隔。  该间隔位于
[x, y] 范围内，单位为毫秒。  允许的范围是 100 <= x <= y <= 10240。  如果 advmin=advmax，间隔是固定的；如果 advmin < advmax，
它会在该范围内灵活选择，以避免干扰蓝牙设备正在执行的其它任务。  默认值为
advmin = advmax = 100。  广播会在全部三个蓝牙 LE 广播信道上发送：37,38,39。

在 Windows 系统上，这些参数的值由操作系统设置，用户无法设置。

**BlueZ** 模块（Linux）还接受

* `--index x`（默认 x = 0，x >= 0）。  这可以让 DBus 区分多个同时运行的
uxplay-beacon.py 实例（它们用于支持多个 UxPlay 实例）。  每个实例都必须有自己的 BLE 数据
文件（正如每个 UxPlay 实例也必须有自己的 MAC 地址和端口一样）。  _注意：在同一台主机上同时运行
多个信标尚未经过测试，该选项可能并没有用或并不需要。_

**BleuIO** 和 **HCI** 模块接受

* `--device x`，它允许覆盖对串口（**BleuIO**）或 hci 设备（**HCI**）的自动选择。这
可能只在宿主系统有多个可用设备时才有用。


macOS 原生蓝牙协议栈不允许非特权用户发送"厂商特定"的蓝牙 LE 广播（例如
为 AirPlay 服务发现所发送的那种），而目前在 macOS 上对 uxplay-beacon.py 的唯一支持是使用 BleuIO USB 串行设备。



为了测试蓝牙 LE 服务发现，你可能希望禁用 DNS_SD 服务发现（不过如果启用了 DNS_SD，
蓝牙 LE 服务似乎仍能工作）。在 Linux 上，用以下命令禁用提供 DNS_SD 的 avahi-daemon：

```
$ sudo systemctl mask avahi-daemon.socket
$ sudo systemctl stop avahi-daemon
```

（在 FreeBSD 上，用 "`service avahi-daemon stop`"）。 
要恢复 DNS_SD 服务发现，把 "mask" 换成 "unmask"、把 "stop" 换成 "start"。


在 Windows 上，Bonjour 服务通过 **服务管理** 控制：按 "Windows + R" 打开"运行"对话框，
运行 `services.msc`，然后在按字母排序的列表中点击 **Bonjour Service**。这
会显示用于停止和重新启动它的链接。

有关蓝牙 LE 支持（包括 HCI 命令）的更多信息，请参阅 [wiki 页面](https://github.com/FDH2/UxPlay/wiki/Bluetooth_LE_beacon)。



* **请注意，蓝牙 LE AirPlay 服务发现只支持
广播 IPv4 地址**。


<a name="troubleshooting"></a>
# 故障排查
注意：`uxplay` 在终端命令行中运行，信息性
消息会输出到终端。

<a name="0-problems-in-compiling-uxplay"></a>
### 0. 编译 UxPlay 时的问题。

一位用户（在 Ubuntu 上）发现编译失败，报错信息涉及
链接到 "usr/local/lib/libcrypto.a" 和 "zlib"。原因是（除
标准的 ubuntu 版 libssl-dev 安装之外），该用户
并不知道 /usr/local 中还存在第二份包含 libcrypto 的安装。
解决办法：当存在不止一份 OpenSSL 安装时，
将环境变量 OPEN_SSL_ROOT_DIR 设置为指向
正确的那一份；在 64 位 Ubuntu 上，这通过运行
`export OPENSSL_ROOT_DIR=/usr/lib/X86_64-linux-gnu/` 后再运行
cmake。

<a name="1-avahidns_sd-bonjourzeroconf-issues"></a>
### 1. **Avahi/DNS_SD Bonjour/Zeroconf 问题**

DNS_SD 服务发现（"Bonjour" 或 "Zeroconf"）服务是
UxPlay 正常工作所必需的。在 Linux 上，它通常由
Avahi 提供；排查此类问题时，应使用工具 `avahi-browse`。
（你可能需要安装一个名称类似
`avahi-utils` 的独立软件包才能获得它。）

在 Linux 上，请确保已安装 Avahi，并在运行 uxplay 的系统上启动 avahi-daemon
服务（你的发行版会说明
如何操作，例如：`sudo systemctl <cmd> avahi-daemon` 或
`sudo service avahi-daemon <cmd>`，其中 `<cmd>` 为 enable、disable、
start、stop、status 之一。你可能需要编辑 avahi-daemon.conf 文件
（它通常位于 /etc/avahi/，用
"`sudo find /etc -name avahi-daemon.conf`" 找到它）：确保
"disable-publishing" **不是**被选中的选项）。有些系统可能
改用 mdnsd 守护进程来提供 DNS-SD
服务。（FreeBSD 同时提供这两种方案，但只测试了 Avahi；
见[此处](https://gist.github.com/reidransom/6033227)，
或 [FreeBSD 手册第 32.8.1 节](https://docs.freebsd.org/en/books/handbook/network-servers/#_configuring_and_starting_avahi)）
注意，如果你改用 Bluetooth LE 信标（见[上文](#bluetooth-le-beacon-setup)）进行服务发现，则不需要 avahi 服务。


-   **uxplay 启动后，在出现 "Initialized
    server socket(s)" 之后要么卡住要么停止（*客户端上没有显示服务器
    名称*）**。

如果 UxPlay 因 "No DNS-SD Server found" 消息而停止，这说明
你的网络**没有正在运行的 Bonjour/zeroconf DNS-SD
服务器。** 在 v1.60 之前，如果 DNS-SD 服务
注册失败，UxPlay 会静默卡住，但现在会因
DNSServiceRegister 函数返回的错误消息而停止：若找不到 DNS-SD 服务器则为 kDNSServiceErr_Unknown：
*（一位 NixOS 用户发现，在 NixOS 中，这个错误也可能在
avahi-daemon 服务确实在运行时出现，且发布功能已启用，但报告称
"通过在 NixOS 中设置 services.avahi.openFirewall
为 true，该错误消失了"。）* 其他 mDNS 错误码位于 FFFE FF00 (-65792)
到 FFFE FFFF (-65537) 的范围内，列于 dnssd.h 文件中。较旧的
版本（avahi 所使用的那个）可在
[此处](https://github.com/lathiat/avahi/blob/master/avahi-compat-libdns_sd/dns_sd.h) 找到。
另有一些额外的错误码定义在
[Apple](https://opensource.apple.com/source/mDNSResponder/mDNSResponder-544/mDNSShared/dns_sd.h.auto.html) 的后续版本中。

如果 UxPlay 卡住，*没有任何错误消息*，且*客户端上没有显示服务器名称*，
**这就是网络问题**（如果你的 UxPlay
版本早于 1.60，那么在找不到 DNS-SD
服务器时也是这种表现。）

在客户端一侧排查这类网络问题的实用工具是
（免费的）Discovery DNS-SD 浏览器，
[可在 Apple App Store 获取](https://apps.apple.com/us/developer/lily-ballard/id305441020)，适用于
iOS（也适用于 iPadOS）和 macOS。

-   一些使用双频（2.4GHz/5GHz）路由器的用户报告称，
    使用 5GHz 频段的客户端（有时）"看不到 UxPlay"（即
    它们的 mDNS 查询得不到响应），而 2.4GHz 频段
    正常。其他使用 Bonjour/mDNS 的项目也收到过类似报告；
    该问题似乎与特定路由器有关，可能和"自动"选择信道
    而非固定信道（5GHz 有更多可供
    切换的信道）、或信道宽度选择有关；一种推测是，
    由于 mDNS 使用 UDP 协议（"丢失"的消息不会
    重发），如果在查询期间发生信道切换，
    mDNS 查询就可能丢失。

如果你的路由器有这个问题，据报告的一种"修复"方法是（至少在
5GHz 上）使用固定信道和/或固定（非动态）信道宽度。

-   **Avahi 一开始工作正常，但新客户端看不到 UxPlay，或者
    最初能看到它的客户端在断开连接后就看不到了**。

这通常是因为 Avahi 只使用了"回环"网络
接口，收不到那些在 UxPlay 启动时
尚未监听的新客户端的 mDNS 查询。

要检查这一点，请在启动 uxplay 之后，在服务器上
**另开一个终端窗口**，使用工具 `avahi-browse -a -t`
验证 UxPlay 的 AirTunes 和 AirPlay 服务是否已正确
注册（在 UxPlay 使用的 "Legacy" AirPlay
镜像模式下只使用 AirTunes 服务，但 AirPlay 服务用于
初次联系）。

avahi-browse 返回的结果中应该能看到类似这样的 uxplay 条目

    +   eno1 IPv6 UxPlay                                        AirPlay Remote Video local
    +   eno1 IPv4 UxPlay                                        AirPlay Remote Video local
    +     lo IPv4 UxPlay                                        AirPlay Remote Video local
    +   eno1 IPv6 863EA27598FE@UxPlay                           AirTunes Remote Audio local
    +   eno1 IPv4 863EA27598FE@UxPlay                           AirTunes Remote Audio local
    +     lo IPv4 863EA27598FE@UxPlay                           AirTunes Remote Audio local

如果只显示了回环（"lo"）条目，那么 UxPlay
主机上的防火墙很可能在阻止完整的 DNS-SD 服务，你需要为 mDNS 请求
开放默认的 UDP 端口 5353，因为基于回环的 DNS-SD
服务并不可靠。

如果 avahi-browse 如上所列显示了 UxPlay 服务，但客户端
看不到它们，那么问题很可能出在本地
网络上。

<a name="2-uxplay-starts-but-stalls-after-initialized-server-sockets-appears-with-the-server-name-showing-on-the-client-but-the-client-fails-to-connect-when-the-uxplay-server-is-selected"></a>
### 2. uxplay 启动后，在出现 "Initialized server socket(s)" 之后卡住，*且客户端上显示了服务器名称*（但选中 UxPlay 服务器时客户端连接失败）。

这说明 *DNS-SD* 服务工作正常，客户端能得知 UxPlay
可用，但 UxPlay 服务器收不到客户端的
响应。这通常是因为服务器上的防火墙阻止了
来自客户端的连接请求。（有一位坚持认为
防火墙已关闭的用户，结果发现服务器上*同时*运行着
*两个*活动的防火墙（*firewalld* 和 *ufw*）！）如果
可能，要么关闭防火墙看看是否就是这个问题，要么
获取从端口 n 开始的三个连续网络端口，且这三个端口都位于
1024-65535 范围内，同时开放 tcp 和 udp，并使用 "uxplay -p n"
（或开放 UDP 7011,6001,6000、TCP 7100,7000,7001 并使用 "uxplay -p"）。

如果你*真的*确定没有防火墙，可能就需要
用 netstat 之类的工具检查你的网络传输，但
几乎总是防火墙的问题。

<a name="3-problems-after-the-client-server-connection-has-been-made"></a>
### 3. 客户端与服务器连接建立*之后*的问题：

如果你*没有*看到 `raop_rtp_mirror starting mirroring` 这条消息，
说明在客户端与服务器的协商完成
之前就出了问题。对于这类问题，使用 "uxplay -d"（调试日志选项）来查看
发生了什么：它会显示连接过程在失败之前
进行到了哪一步。你可以把自己的调试输出与
[UxPlay
Wiki](https://github.com/FDH2/UxPlay/wiki) 中成功启动 UxPlay 时的调试输出进行对比。

**如果 UxPlay 报告镜像已开始，但你收不到视频或
音频，问题很可能来自某个在你的系统上无法工作的 GStreamer 插件**
（默认情况下，GStreamer 使用 "autovideosink" 和
"autoaudiosink" 算法来猜测在你的系统上要使用哪些"最佳"插件）。
此外还有一位用户没有音频的原因是，
其防火墙只开放了两个 udp 网络端口：实际上需要**三个**
（第三个用于接收音频数据）。

**Raspberry Pi** 设备（*Pi 4B 及更早机型：这不适用于
Pi 5，它不提供硬件 h264 解码，也不需要
硬件解码*）在以下条件下使用 GPU 硬件 h264 视频解码效果最佳：
GStreamer v1.20.x 或更早版本中的 Video4Linux2 插件已打上补丁
（补丁见 UxPlay
[Wiki](https://github.com/FDH2/UxPlay/wiki/Gstreamer-Video4Linux2-plugin-patches)
）。在 GStreamer-1.22 中该问题已修复，而在 Raspberry Pi OS（Bullseye）等发行版中
通过将相关补丁回移（backport）也已修复：**在使用 Raspberry Pi OS 提供的
GStreamer-1.18.4 时请使用选项 `-bt709`**。这
还需要 bcm2835-codec 内核模块，该模块不在标准
Linux 内核中（在 Raspberry Pi OS、Ubuntu 和 Manjaro 中可用）。

-   **如果你的 Raspberry Pi
    操作系统没有该内核模块，或者 GStreamer \< 1.22 未打补丁，请使用选项
    `-avdec` 进行软件 h264 解码。**

有时 "autovideosink" 可能会选择 OpenGL 渲染器 "glimagesink"，
而它在你的系统上可能无法正常工作。请尝试选项 "-vs
ximagesink" 或 "-vs xvimagesink"，看看使用其中之一能否修复
该问题。

其他已报告的问题与已过时的 GStreamer VAAPI 插件有关（该插件用于
硬件加速的 Intel 显卡，而不适用于 NVIDIA 显卡）。使用
选项 "-avdec" 强制使用软件 h264 视频解码：这应该能
阻止 autovideosink 选择 vaapisink 视频输出。
或者，查明是否安装了 gstreamer1.0-vaapi 插件，
如果已安装就卸载它。（如果这样没有解决问题，你可以
重新安装它。）

还有一些报告提到与
硬件加速的 Intel HD 显卡有关的其他 GStreamer 问题。一位用户（在 Debian 上）通过
"sudo apt install intel-media-va-driver-non-free" 解决了该问题。这是
适用于第八代（或更晚）"\*-lake" Intel 芯片的驱动，似乎与
VAAPI 加速图形有关。

如果你*确实*有 Intel HD 显卡，并且安装了已过时的 vaapi 插件，
但 `-vs vaapisink` 无法工作，请检查 vaapi 是否在你的 GStreamer 安装中被"列入黑名单"：
运行 `gst-inspect-1.0 vaapi`，如果它
报告 `0 features`，你需要在运行 uxplay 之前执行 `export GST_VAAPI_ALL_DRIVERS=1`，
或者在默认环境中设置它。
推荐使用较新的 "va" 解码器，例如 vah264dec，GStreamer 应该会自动使用它们，
但也可以通过 `-vd` 选项指定。



你可以尝试通过
"`-as <audiosink>`" 或 "`-vs <videosink>`" 选项来选择
GStreamer 音频输出或视频输出，而不是让 GStreamer 为你
选择。（参见上文 [启动和运行
UxPlay](#starting-and-running-uxplay) 中关于 `<audiosink>` 或
`<videosink>` 的选项。）

在 Linux 上由 "-vs glimagesink" 创建的 "OpenGL renderer" 窗口，
有时在点击其"关闭"按钮后无法正常关闭。
（这是 GStreamer 的问题）。你可能需要用
Ctrl-C 终止 uxplay 来关闭"僵尸"OpenGl 窗口。如果在客户端
发送 "Stop Mirroring" 信号时出现类似问题，请尝试
使视频窗口保持打开的 no-close 选项 "-nc"。

<a name="4-gstreamer-issues-missing-plugins-etc"></a>
### 4. GStreamer 问题（插件缺失等）：

如果 UxPlay 没有发出任何错误消息，但 GStreamer 视频似乎没有工作，
请在终端窗口中用以下命令测试你的 GStreamer 安装

```
gst-launch-1.0 videotestsrc ! autovideosink

```
如果 autovideosink 找到可用的视频输出，就应该会显示一个视频测试图案。
然后测试各种视频输出（列表参见 `man uxplay` 中的 -vs 条目），看
哪些在你的系统上可用。另外使用

```
gst-inspect-1.0 | grep sink | grep [V,v]ideo
```

查看 GStreamer 认为已安装了哪些视频输出。重复执行 gst-launch-1.0 命令，
把你想要测试的每个视频输出的名称替换掉 "autovideosink"。


-   清除用户的 GStreamer 缓存（使用
    `rm -rf ~/.cache/gstreamer-1.0/*`），这可能是解决以下问题的办法：
    gst-inspect-1.0 没有显示你确信已安装的插件。
    缓存会在下次 GStreamer 启动时重新生成。
    **这是解决那些最终发现源自缓存损坏的疑难问题的办法，
    应当首先尝试。**

如果 UxPlay 启动失败，并提示找不到某个必需的 GStreamer
插件（例如 "libav"），请先用 GStreamer
工具 gst-inspect-1.0 检查 GStreamer 知道哪些可用。（你可能
需要安装某些额外的 GStreamer "tools" 包才能获得
gst-inspect-1.0）。例如，对于 libav 问题，用
"`gst-inspect-1.0 libav`" 检查。如果 GStreamer 没有显示它可用，
但你的包管理器显示相关软件包已安装（正如一位
用户所发现的），请尝试彻底删除并重新安装该软件包。那位
用户发现，对于反复出现的 "**Required gstreamer plugin 'libav' not
found**" 消息，一个解决办法是清除用户的 gstreamer
缓存。

如果启动失败并出现类似 '`no element "avdec_aac"`' 的错误，这
是因为尽管已安装 gstreamer-libav，但它并不完整，
缺少某些插件功能：
"`gst-inspect-1.0 | grep avdec_aac`" 会显示 avdec_aac 是否
可用。与其他 GStreamer 插件不同，libav 插件是 FFmpeg 编解码器的前端，
而这些编解码器提供 avdec\_\*。

-   一些发行版（RedHat、SUSE 等）提供不完整的
    FFmpeg 版本，因为某些插件所用编解码器存在专利问题。
    在这种情况下，会有一些"额外软件包"提供方，
    例如 [RPM fusion](https://rpmfusion.org)（RedHat）、
    [packman](http://packman.links2linux.org/)（SUSE），你可以从中获取
    完整的软件包（你的发行版通常会提供
    相关说明，Mageia 则把它们放在可选的 "tainted"
    仓库中）。所需的软件包可能是 "ffmpeg\*" 或 "libav\*" 包：
    GStreamer libav 插件包本身不包含任何编解码器，
    它只是提供一种让 GStreamer 使用 ffmpeg/libav
    编解码器库的方式，而这些库必须单独安装。出于类似
    原因，发行版可能随附不完整的 GStreamer
    "plugins-bad" 软件包。一位 Fedora 用户以为已经从
    rpmfusion 安装，但系统并没有照做：*"在重启后，向
    dnf 命令添加 --allowerasing 解决了问题"*。

-   从 UxPlay-1.65.3 版本开始，如果缺少 avdec_aac，
    UxPlay 仍会继续运行，但镜像模式下没有音频。

要排查 GStreamer 问题，请执行 "export GST_DEBUG=2"，在将要运行 uxplay 的终端中
设置 GStreamer 调试级别环境变量，
这样你就能看到警告和错误消息；有关如何更深入地了解
GStreamer 内部情况，请参阅 [GStreamer 调试
工具](https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html)。
运行
"gst-inspect-1.0" 可以查看你的系统上安装了哪些 GStreamer
插件。

某些用于特殊插件的额外 GStreamer 包可能需要
安装（或重新安装：一位使用 Wayland 显示系统作为
X11 替代方案的用户报告称，在重新安装 Lubuntu 18.4 之后，
UxPlay 一直无法工作，直到安装了 gstreamer1.0-x，推测是为了
Wayland 的 X11 兼容模式）。不同的发行版可能以不同方式
把 GStreamer 1.x 拆分为软件包；上面构建说明中列出的包
应该会作为依赖引入其他必需的 GStreamer
包，但不会安装所有可能的插件。

GStreamer 视频管道（显示在
`uxplay -d` 的初始输出中）默认形式为

    appsrc name=video_source ! queue ! h264parse ! decodebin ! videoconvert ! autovideosink name=video_sink sync=false

该管道完全可配置：默认元件 "h264parse"、
"decodebin"、"videoconvert" 和 "autovideosink" 可以分别通过
uxplay 选项 `-vp`、`-vd`、`-vc` 和 `-vs` 来替换，如果
有修改它的需要（条目可以放在引号 "..." 中，
以包含选项）。

<a name="5-mirror-screen-freezes-a-network-problem"></a>
### 5. 镜像画面冻结（网络问题）：

如果来自客户端的 TCP 视频流不再到达
服务器，就可能发生这种情况，原因很可能是网络问题（UDP 音频
流可能仍在继续到达）。UxPlay 每隔 3 秒检查一次
客户端是否仍然连接，方法是向它发送一个 NTP
时间信号请求。如果在 0.3 秒的
时间窗口内没有收到客户端的回复，就会记录一次 "ntp timeout"。如果连续出现一定数量
（目前是 5 次）的 ntp 超时，UxPlay 就认为
客户端已经"死亡"，并重置连接，从而可以
接受新客户端连接，或与之前的客户端重新连接。
有时连接可能在达到超时限制之前恢复，
如果默认限制不适合你的网络，可以
使用选项 "-reset *n*" 修改它，其中 *n* 是所需的
超时上限值（*n* = 0 表示"无限制"）。如果连接在 ntp 超时之后
开始恢复，那么超时之前的一个损坏视频包
可能触发 "connection reset by peer" 错误，这也会
导致 UxPlay 重置连接。

-   连接被重置时，上一次连接的"冻结"镜像画面会
    保留在原处，但**不会**阻止新的
    连接；当新的客户端连接建立时，它会被
    接管。

<a name="6-protocol-issues-with-decryption-of-the-encrypted-audio-and-video-streams-sent-by-the-client"></a>
### 6. 协议问题（涉及解密客户端发送的加密音频和视频流）。

协议故障可能引发源源不断的错误消息，
这意味着音频解密密钥（也用于视频解密）
没有从客户端发送的数据中正确提取出来。

UxPlay-1.65 修改了协议：后来发现，只要在 UxPlay 于 DNS-SD
服务发现中广播的 "features" 代码里禁用 "Supports Legacy
Pairing"（第 27 位），就可以跳过客户端与服务器的
"配对"步骤（从而快得多地完成连接建立，
不再有 5 秒延迟）。这样，大多数客户端在配对时
就不会尝试建立"共享密钥"，而 AppleTV 正是用该密钥
来同时处理多个客户端（UxPlay 一次只支持一个
客户端）。**这一改动现已经过充分测试，但如果它
导致任何协议故障，可以在 lib/dnssdint.h 中取消注释
原来的 "FEATURES_1" 设置（并注释掉新的设置），
然后重新构建 UxPlay，从而恢复之前的行为。**（当使用
UxPlay 1.67 引入的 "-pin" 选项运行 UxPlay、启用
新的 Apple 风格一次性 "pin" 认证时，
"配对"会重新启用。）

对于 iOS 9.3 及更高版本的客户端，不应发生协议故障。
不过，如果某个客户端使用了与
基于 Windows 的 AirPlay 客户端模拟器 *AirMyPC* 相同的旧版协议，
可以通过设置
`UxPlay/lib/global.h` 中的 `OLD_PROTOCOL_CLIENT_USER_AGENT_LIST`，把协议切换为旧版本。UxPlay
会在客户端连接时报告其 "User Agent" 字符串。如果其他某个
客户端也未能解密所有音频和视频，请尝试把它的 "User
Agent" 字符串替换到 global.h 中 "AirMyPC/2.0;xxx" 条目里的 "xxx"
位置，然后重新构建 uxplay。

注意，在 DNS-SD 服务发现中，Uxplay 声明自己为
AppleTV3,2（一个 32 位设备），sourceVersion 为 220.68；这一点也可以
在 global.h 中修改。如果 UxPlay 声明自己为
AppleTV6,2、sourceVersion 380.20.1（第一代 AppleTV 4K，
2017 年推出，运行 tvOS 12.2.1），它同样可以工作，所以 UxPlay 声称的
版本似乎并不重要。


<a name="changelog"></a>
# Changelog

> **说明（汉化 fork 添加）**：以下更新记录（Changelog）保留英文原文，以便与上游提交记录逐条对照；不影响程序输出与使用。
1.74  2026-09-14  Optional minimal internal mDNSResponder to replace
Bonjour/Avahi.  Reworked language selection for HLS video.  Added AWDL direct
connection option (only for macOS hosts).  Added use of kernel timestamps
for NTP, and a rebuilt NTP subsystem.

1.73.6 2026-03-22  Fix "not a socket" message uxplay bug.
Futher uxplay-beacon.py improvements (Only use GLib in BlueZ module)

1.73.4 2026-03-15 Modularize Bluetooth support for uxplay-beacon.
Add modules for BLeuIO serial-modem Bluetooth LE device, and HCI
access (Linux/FreeBSD).   Fix broken -vol option.

1.73 2026-01-25 Render Audio cover-art inside UxPlay with -ca option (no file
specified). (D-Bus based) option -scrsv <n> to inhibit screensaver while UxPlay
is running (Linux/*BSD only). Add password support (-pw)  using a displayed
pin code as a password that changes every time (and not as a one-time
pin). Add support for Service  Discovery using a
Bluetooth LE beacon.   Add -vrtp option for forwarding decrypted h264/5 video
to an external renderer (e.g., OBS Studio), and -artp for audio.  Check that
option input strings have valid UTF-8 encoding.   New option `-lang fr:es:en`
to specify language preferences for YouTube  HLS videos when they offer a choice. 
New option -mp4 for recording to a mp4 file (Mirror and Audio mode, not HLS)

1.72.3 2025-12-20 Fix bug reported in CVE-2025-60458 whereby a specially-crafted
client TEARDOWN request can crash UxPlay (denial of service attack).

1.72.2 2025-07-07  Fix bug (typo) in DNS_SD advertisement introduced with -pw
option.  Update llhttp to v 9.3.0

1.72.1 2025-06-06  minor update: fix regression in -reg option; add option
-rc <rcfile> to specify initialization file; add "-nc no" to unset "-nc"
option (for macOS users, where -nc is default); add user-installable
systemd script for running UxPlay as an always-available "rootless daemon"

1.72 2025-05-07. Improved HLS Live Streaming (YouTube) support, including
"scrub".
Add requested options -md \<filename\> to output audio
metadata text to a file for possible display (complements -ca option),
and -vol <v> option to set initial audio-streaming volume.  Add support
password user access control with HTTP digest Authentication (-pw [pwd]).
If no pwd is set, a random pin is displayed for entry at each new connection.

1.71 2024-12-13 Add support for HTTP Live Streaming (HLS), initially
only for YouTube movies. Fix issue with NTP timeout on Windows.

1.70 2024-10-04 Add support for 4K (h265) video (resolution 3840 x
2160). Fix issue with GStreamer \>= 1.24 when client sleeps, then wakes.

1.69 2024-08-09 Internal improvements (e.g. in -nohold option,
identifying GStreamer videosink selected by autovideosink, finding X11
display) in anticipation of future HLS video support. New -nofreeze
option to not leave frozen video in place when a network connection is
reset. Fixes for GStreamer-1.24.x changes.

1.68 2023-12-31 New simpler (default) method for generating a persistent
public key from the server MAC address (which can now be set with the -m
option). (The previous method is still available with -key option). New
option -reg to maintain a register of pin-authenticated clients.
Corrected volume-control: now interprets AirPlay volume range -30dB:0dB
as decibel gain attenuation, with new option -db low\[:high\] for "flat"
rescaling of the dB range. Add -taper option for a "tapered" AirPlay
volume-control profile.

1.67 2023-11-30 Add support for Apple-style one-time pin authentication
of clients with option "-pin": (uses SRP6a authentication protocol and
public key persistence). Detection with error message of (currently)
unsupported H265 video when requesting high resolution over wired
ethernet. Removed rpi\* options (which are not valid with new Raspberry
Pi model 5, and can be replaced by combinations of other options). Added
optional argument "mac" to "-m" option, to specify a replacement MAC
address/Device ID. Update llhttp to v. 9.1.3. Add -dacp option for
exporting current client DACP info (for remotes).

1.66 2023-09-05 Fix IPV6 support. Add option to restrict clients to
those on a list of allowed deviceIDs, or to block connections from
clients on a list of blocked deviceIDs. Fix for #207 from @thiccaxe
(screen lag in vsync mode after client wakes from sleep).

1.65.3 2023-07-23 Add RPM spec file; add warning if required gstreamer
libav feature "avdec_aac" is missing: (this occurs in RPM-based
distributions that ship an incomplete FFmpeg for Patent or License
reasons, and rely on users installing an externally-supplied complete
FFmpeg). Mirror-mode airplay will now work without audio if avdec_aac is
missing.

1.65 2023-06-03 Eliminate pair_setup part of connection protocol to
allow faster connections with clients (thanks to @shuax #176 for this
discovery); to revert, uncomment a line in lib/dnssdint.h. Disconnect
from audio device when connection closes, to not block its use by other
apps if uxplay is running but not connected. Fix for AirMyPC client
(broken since 1.60), so its older non-NTP timestamp protocol works with
-vsync. Corrected parsing of configuration file entries that were in
quotes.

1.64 2023-04-23 Timestamp-based synchronization of audio and video is
now the default in Mirror mode. (Use "-vsync no" to restore previous
behavior.) A configuration file can now be used for startup options.
Also some internal cleanups and a minor bugfix that fixes #192.

1.63 2023-02-12 Reworked audio-video synchronization, with new options
-vsync (for Mirror mode) and -async (for Audio-Only mode, to sync with
client video). Option -vsync makes software h264 decoding of streamed
videos with option -avdec viable on some recent Raspberry Pi models.
Internal change: all times are now processed in nanoseconds units.
Removed -ao option introduced in 1.62.

1.62 2023-01-18 Added Audio-only mode time offset -ao x to allow user
synchronization of ALAC audio playing on the server with video, song
lyrics, etc. playing on the client. x = 5.0 appears to be optimal in
many cases. Quality fixes: cleanup in volume changes, timestamps, some
bugfixes.

1.61 2022-12-30 Removed -t option (workaround for an Avahi issue,
correctly solved by opening network port UDP 5353 in firewall). Remove
-g debug flag from CMAKE_CFLAGS. Postpend (instead of prepend) build
environment CFLAGS to CMAKE_CFLAGS. Refactor parts of uxplay.cpp

1.60 2022-12-15 Added exit with error message if DNSServiceRegister
fails (instead of just stalling). Test for Client's attempt to using
unsupported AirPlay 2 "REMOTE CONTROL" protocol (with no timing
channel), and exit if this occurs. Reworked metadata processing to
correctly parse DMAP header (previous version worked with DMAP messages
currently received, but was not correct).

1.59 2022-12-12 remove "ZOOMFIX" compile option and make compilation
with X11-dependence the default if X11 development libraries are
detected (this now also provides fullscreen mode with a F11 or Alt+Enter
key toggle); ZOOMFIX is now automatically applied for GStreamer \< 1.20.
New cmake option -DNO_X11_DEPS compiles uxplay without X11 dependence.
Reworked internal metadata handling. Fix segfault with "-vs 0".

1.58 2022-10-29 Add option "-nohold" that will drop existing connections
when a new client connects. Update llhttp to v8.1.0.

1.57 2022-10-09 Minor fixes: (fix coredump on AUR on "stop mirroring",
occurs when compiled with AUR CFLAGS -DFORTIFY_SOURCE); graceful exit
when required plugins are missing; improved support for builds on
Windows. Include audioresample in GStreamer audio pipeline.

1.56 2022-09-01 Added support for building and running UxPlay-1.56 on
Windows (no changes to Unix (Linux, \*BSD, macOS) codebase.)

1.56 2022-07-30 Remove -bt709 from -rpi, -rpiwl, -rpifb as GStreamer is
now fixed.

1.55 2022-07-04 Remove the bt709 fix from -v4l2 and create a new -bt709
option (previous "-v4l2" is now "-v4l2 -bt709"). This allows the
currently-required -bt709 option to be used on its own on RPi without
-v4l2 (sometimes this give better results).

1.54 2022-06-25 Add support for "Cover Art" display in Audio-only (ALAC)
mode. Reverted a change that caused VAAPI to crash with AMD POLARIS
graphics cards. Minor internal changes to plist code and uxplay option
parsing.

1.53 2022-06-13 Internal changes to audio sync code, revised
documentation, Minor bugfix (fix assertion crash when resent audio
packets are empty).

1.52 2022-05-05 Cleaned up initial audio sync code, and reformatted
streaming debug output (readable aligned timestamps with decimal points
in seconds). Eliminate memory leaks (found by valgrind). Support for
display of ALAC (audio-only) metadata (soundtrack artist names, titles
etc.) in the uxplay terminal.

1.51 2022-04-24 Reworked options forVideo4Linux2 support (new option
-v4l2) and short options -rpi, -rpifb, -rpiwl as synonyms for -v4l2,
-v4l2 -vs kmssink, and -v4l2 -vs waylandsink. Reverted a change from
1.48 that broke reconnection after "Stop Mirroring" is sent by client.

1.50 2022-04-22 Added -fs fullscreen option (for Wayland or VAAPI
plugins only), Changed -rpi to be for framebuffer ("lite") RPi systems
and added -rpigl (OpenGL) and -rpiwl (Wayland) options for RPi Desktop
systems. Also modified timestamps from "DTS" to "PTS" for latency
improvement, plus internal cleanups.

1.49 2022-03-28 Addded options for dumping video and/or audio to file,
for debugging, etc. h264 PPS/SPS NALU's are shown with -d. Fixed
video-not-working for M1 Mac clients.

1.48 2022-03-11 Made the GStreamer video pipeline fully configurable,
for use with hardware h264 decoding. Support for Raspberry Pi.

1.47 2022-02-05 Added -FPSdata option to display (in the terminal)
regular reports sent by the client about video streaming performance.
Internal cleanups of processing of video packets received from the
client. Added -reset n option to reset the connection after n ntp
timeouts (also reset after "connection reset by peer" error in video
stream).

1.46 2022-01-20 Restore pre-1.44 behavior (1.44 may have broken hardware
acceleration): once again use decodebin in the video pipeline; introduce
new option "-avdec" to force software h264 decoding by libav h264, if
needed (to prevent selection of vaapisink by autovideosink). Update
llhttp to v6.0.6. UxPlay now reports itself as AppleTV3,2. Restrict
connections to one client at a time (second client must now wait for
first client to disconnect).

1.45 2022-01-10 New behavior: close video window when client requests
"stop mirroring". (A new "no close" option "-nc" is added for users who
wish to retain previous behavior that does not close the video window).

1.44 2021-12-13 Omit hash of aeskey with ecdh_secret for an AirMyPC
client; make an internal rearrangement of where this hash is done. Fully
report all initial communications between client and server in -d debug
mode. Replace decodebin in GStreamer video pipeline by h264-specific
elements.

1.43 2021-12-07 Various internal changes, such as tests for successful
decryption, uniform treatment of informational/debug messages, etc.,
updated README.

1.42 2021-11-20 Fix MAC detection to work with modern Linux interface
naming practices, MacOS and \*BSD.

1.41 2021-11-11 Further cleanups of multiple audio format support
(internal changes, separated RAOP and GStreamer audio/video startup)

1.40 2021-11-09 Cleanup segfault in ALAC support, manpage location fix,
show request Plists in debug mode.

1.39 2021-11-06 Added support for Apple Lossless (ALAC) audio streams.

1.38 2021-10-8 Add -as *audiosink* option to allow user to choose the
GStreamer audiosink.

1.37 2021-09-29 Append "@hostname" to AirPlay Server name, where
"hostname" is the name of the server running uxplay (reworked change in
1.36).

1.36 2021-09-29 Implemented suggestion (by @mrbesen and @PetrusZ) to use
hostname of machine runing uxplay as the default server name

1.35.1 2021-09-28 Added the -vs 0 option for streaming audio, but not
displaying video.

1.35 2021-09-10 now uses a GLib MainLoop, and builds on macOS (tested on
Intel Mac, 10.15 ). New option -t *timeout* for relaunching server if no
connections were active in previous *timeout* seconds (to renew Bonjour
registration).

1.341 2021-09-04 fixed: render logger was not being destroyed by
stop_server()

1.34 2021-08-27 Fixed "ZOOMFIX": the X11 window name fix was only being
made the first time the GStreamer window was created by uxplay, and not
if the server was relaunched after the GStreamer window was closed, with
uxplay still running. Corrected in v. 1.34

<a name="building-openssl--111-from-source"></a>
### Building OpenSSL \>= 1.1.1 from source.

If you need to do this, note that you may be able to use a newer version
(OpenSSL-3.0.1 is known to work). You will need the standard development
toolset (autoconf, automake, libtool). Download the source code from
<https://www.openssl.org/source/>. Install the downloaded openssl by
opening a terminal in your Downloads directory, and unpacking the source
distribution: ("tar -xvzf openssl-3.0.1.tar.gz ; cd openssl-3.0.1").
Then build/install with "./config ; make ; sudo make install_dev". This
will typically install the needed library `libcrypto.*`, either in
/usr/local/lib or /usr/local/lib64.

*(Ignore the following for builds on MacOS:)* On some systems like
Debian or Ubuntu, you may also need to add a missing entry
`/usr/local/lib64` in /etc/ld.so.conf (or place a file containing
"/usr/local/lib64/libcrypto.so" in /etc/ld.so.conf.d) and then run "sudo
ldconfig".

<a name="building-libplist--200-from-source"></a>
### Building libplist \>= 2.0.0 from source.

*(Note: on Debian 9 "Stretch" or Ubuntu 16.04 LTS editions, you can
avoid this step by installing libplist-dev and libplist3 from Debian 10
or Ubuntu 18.04.)* As well as the usual build tools (autoconf, automake,
libtool), you may need to also install some libpython\*-dev package.
Download the latest source with git from
<https://github.com/libimobiledevice/libplist>, or get the source from
the Releases section (use the \*.tar.bz2 release, **not** the \*.zip or
\*.tar.gz versions): download
[libplist-2.3.0](https://github.com/libimobiledevice/libplist/releases/download/2.3.0/libplist-2.3.0.tar.bz2),
then unpack it ("tar -xvjf libplist-2.3.0.tar.bz2 ; cd libplist-2.3.0"),
and build/install it: ("./configure ; make ; sudo make install"). This
will probably install libplist-2.0.\* in /usr/local/lib. The new
libplist-2.3.0 release should be compatible with UxPlay;
[libplist-2.2.0](https://github.com/libimobiledevice/libplist/releases/download/2.2.0/libplist-2.2.0.tar.bz2)
is also available if there are any issues.

*(Ignore the following for builds on MacOS:)* On some systems like
Debian or Ubuntu, you may also need to add a missing entry
`/usr/local/lib` in /etc/ld.so.conf (or place a file containing
"/usr/local/lib/libplist-2.0.so" in /etc/ld.so.conf.d) and then run
"sudo ldconfig".


<a name="disclaimer"></a>
# 免责声明

本仓库中的所有资源都只使用了互联网上
可免费获取的信息编写。代码及相关资源
仅供教育目的使用。用户有责任
确保遵守当地所有法律。

本项目使用一个第三方 GPL 库来处理
FairPlay。该库的法律地位尚不明确。如果你是
Apple 的代表，并且对该库的合法性
及其在本项目中的使用有任何异议，请联系开发者，
我们将采取适当的措施。

鉴于市面上有大量第三方 AirPlay 接收器（大多为
闭源）可供购买，我们认为
相同功能的开源实现也不会侵犯
Apple 的任何权利。

<a name="uxplay-authors"></a>
# UxPlay 作者

*\[改编自 fdraschbacher 关于 RPiPlay 前身的笔记\]*

本仓库中的代码随时间的推移从各种来源汇集而成。
以下尝试列出各位作者以及他们
所创建的组件：

UxPlay 最初由 **antimof** 基于 RPiPlay 创建，做法是把
它适配 Raspberry Pi 的 OpenMAX 视频和音频渲染系统替换为
面向桌面 Linux 系统的 GStreamer 渲染；antimof 在
`renderers/` 中代码上的工作后来被回移至 RPiPlay，而 antimof 项目
一度停滞，但后来在 [当前的 GitHub
站点](http://github.com/FDH2/UxPlay) 上重新活跃起来，以服务更广泛的
用户社区。

通过继承自 RPiPlay 而包含在 UxPlay 中的
先前代码作者包括：

-   **EstebanKubata**：创建了一个名为
    [PlayFair](https://github.com/EstebanKubata/playfair) 的 FairPlay 库。位于
    `lib/playfair` 文件夹中。许可证：GNU GPL
-   **Juho Vähä-Herttua** 及贡献者：创建了一个名为
    [ShairPlay](https://github.com/juhovh/shairplay) 的 AirPlay 音频
    服务器，其中包括基于 PlayFair 的 Fairplay 支持。`lib/` 中的
    大部分代码最初源自该项目。许可证：GNU LGPLv2.1+
-   **dsafa22**：创建了一个 AirPlay 2 镜像（投屏）服务器
    [AirplayServer](https://github.com/dsafa22/AirplayServer)（似乎
    现已消失），面向 Android，基于 ShairPlay。代码保存在
    [此处](https://github.com/jiangban/AirplayServer)，并参阅[
    此处](https://github.com/FDH2/UxPlay/wiki/AirPlay2)中由 AirplayServer 作者
    对 AirPlay 2 镜像协议分析所作的描述，
    正是这项分析使 RPiPlay 得以实现。`lib/` 中
    与镜像（投屏）相关的所有代码都是 dsafa22 的工作。许可证：GNU
    LGPLv2.1+
-   **Florian Draschbacher**（FD-）及贡献者：把 dsafa22 的
    Android 项目适配到 Raspberry Pi，并做了大量清理、
    调试和改进。项目
    [RPiPlay](https://github.com/FD-/RPiPlay) 基本上就是把
    dsafa22 的代码移植到 Raspberry Pi，利用 OpenMAX 和 OpenSSL
    来提升在 Pi 上的性能。许可证 GPL v3。FD- 写了一篇
    关于 [Airplay 协议
    版本](http://github.com/FD-/RPiPlay#airplay-protocol-versions)的
    历史的有趣笔记，可在 RPiPlay 的 github 仓库中找到。

独立于 UxPlay，但被其使用并与之捆绑：

-   **Fedor Indutny**（Node.js 项目，曾任职于 Joyent, Inc）及
    贡献者：创建了一个名为
    [llhttp](https://github.com/nodejs/llhttp) 的 http 解析库。位于
    `lib/llhttp/`。许可证：MIT

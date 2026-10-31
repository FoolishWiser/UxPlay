#!/usr/bin/env bash
# Assemble a portable Windows bundle for UxPlay (run inside MSYS2).
#
#   .github/scripts/win-bundle.sh ucrt64
#
# The result is dist/uxplay-windows-<prefix>/, containing uxplay.exe, every
# DLL it (transitively) needs, the GStreamer plugins and their scanner, the
# Chinese README, a short run guide and two .bat launchers.
set -euo pipefail

PREFIX_NAME="${1:?usage: win-bundle.sh <ucrt64|mingw64|clangarm64>}"
PREFIX="/${PREFIX_NAME}"
OUT="dist/uxplay-windows-${PREFIX_NAME}"

echo "==> prefix: ${PREFIX}"
echo "==> output: ${OUT}"

rm -rf "$OUT"
mkdir -p "$OUT/plugins"

cp -f build/uxplay.exe "$OUT/uxplay.exe"
ls -l "$OUT/uxplay.exe"

# Plugins first, so their file names are part of the bundle layout.
plugin_count=0
for p in "$PREFIX"/lib/gstreamer-1.0/*.dll; do
    [ -f "$p" ] || continue
    cp -f "$p" "$OUT/plugins/$(basename "$p")"
    plugin_count=$((plugin_count + 1))
done
echo "==> plugins: ${plugin_count}"

scanner="$PREFIX/libexec/gstreamer-1.0/gst-plugin-scanner.exe"
if [ -f "$scanner" ]; then
    cp -f "$scanner" "$OUT/gst-plugin-scanner.exe"
    echo "==> plugin scanner: yes"
else
    echo "==> plugin scanner: NOT FOUND (relies on system GStreamer)"
fi

# Dependencies: ship every DLL that lives in $PREFIX/bin. Walking the import
# graph with ntldd is slow on Windows (1-3s per file, and -R recurses the whole
# tree: a few hundred files take 10+ minutes) and easy to get wrong -- a
# missing transitive DLL (avcodec-63.dll needs swresample-7.dll, libx264-165.dll,
# ...) makes the GStreamer libav plugin fail to load with a confusing
# "plugin 'libav' not found". Copying the runtime set is instant and complete.
dlls=0
for dll in "$PREFIX"/bin/*.dll; do
    [ -f "$dll" ] || continue
    cp -f "$dll" "$OUT/"
    dlls=$((dlls + 1))
done
echo "==> dlls copied: ${dlls}"

# Documentation and launchers.
if [ -f README.zh-CN.md ]; then
    cp -f README.zh-CN.md "$OUT/README.zh-CN.md"
fi

write_bat() { # $1 = target file, $2 = language flag
    {
        printf '@echo off\r\n'
        printf 'setlocal\r\n'
        printf 'set "HERE=%%~dp0"\r\n'
        printf 'set "PATH=%%HERE%%;%%PATH%%"\r\n'
        printf 'set "GST_PLUGIN_PATH=%%HERE%%plugins"\r\n'
        printf 'set "GST_PLUGIN_SYSTEM_PATH_1_0=%%HERE%%plugins"\r\n'
        printf 'if exist "%%HERE%%gst-plugin-scanner.exe" set "GST_PLUGIN_SCANNER=%%HERE%%gst-plugin-scanner.exe"\r\n'
        printf '"%%HERE%%uxplay.exe" %s %%*\r\n' "$2"
        printf 'echo.\r\n'
        printf 'pause\r\n'
    } >"$1"
}

write_bat "$OUT/run-zh.bat" "-zh"
write_bat "$OUT/run-en.bat" "-en"

{
  # UTF-8 BOM so Windows Notepad detects the encoding, ASCII name so
  # Compress-Archive keeps it intact inside the zip.
  printf '\xef\xbb\xbf'
  cat <<'EOT'
UxPlay 简体中文版（Windows 便携包）
=====================================

1. 解压整个文件夹到任意位置（目录里有中文或空格也没关系）。
2. 双击 run-zh.bat 以中文界面启动；需要英文界面时双击 run-en.bat。
   也可以自己开命令行，先执行：
       set PATH=%~dp0;%PATH%
       set GST_PLUGIN_PATH=%~dp0plugins
   然后 uxplay.exe -zh
3. 启动后，在 iPhone / iPad 上打开"控制中心"→"屏幕镜像"，选择本机名称即可投屏。
4. 常用选项：uxplay.exe -zh -h   查看全部参数（已汉化）
5. 本包已内置解码与显示所需插件；如需录制/特殊编码，可再装 GStreamer 插件。
6. 未做代码签名，Windows SmartScreen 可能提示"未知发布者"，选择"仍要运行"即可。

说明：本程序是 UxPlay（https://github.com/FDH2/UxPlay）的汉化 fork，
汉化内容与切换方式见包内 README.zh-CN.md。
EOT
} >"$OUT/HOWTO.txt"

echo "==> bundle contents"
find "$OUT" -maxdepth 1 -type f -printf '%12s  %f\n' | sort -k2
echo "==> plugins: $(ls "$OUT/plugins" | wc -l) files, $(du -sh "$OUT/plugins" | cut -f1)"
echo "==> total: $(du -sh "$OUT" | cut -f1)"

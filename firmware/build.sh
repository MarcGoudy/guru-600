#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments
# Build Felucca on macOS (see BUILDING.md).
#   ./build.sh [--release X.Y]
#   JIELI_TOOLCHAIN  JieLi Linux toolchain (default: ~/.jieli/toolchain)
#   AC79_SDK         JieLi AC79 SDK checkout (default: ~/fw-AC79_AIoT_SDK)
set -e
cd "$(dirname "$0")"
export JIELI_TOOLCHAIN="${JIELI_TOOLCHAIN:-$HOME/.jieli/toolchain}"
export AC79_SDK="${AC79_SDK:-$HOME/fw-AC79_AIoT_SDK}"
PY="${PYTHON:-python3}"

"$PY" -c 'import PIL' 2>/dev/null || { echo "build.sh: $PY has no Pillow (pip3 install Pillow)"; exit 1; }
[ -x "$JIELI_TOOLCHAIN/pi32v2/bin/clang" ] || { echo "build.sh: no toolchain in $JIELI_TOOLCHAIN (run tools/get_toolchain.sh)"; exit 1; }
[ -f "$AC79_SDK/cpu/wl82/tools/uboot.boot" ] || { echo "build.sh: no JieLi AC79 SDK in $AC79_SDK"; exit 1; }
if [ "$(uname -s)" != Linux ] || [ "$(uname -m)" != x86_64 ]; then
    docker info >/dev/null 2>&1 || { echo "build.sh: Docker is not running"; exit 1; }
fi
# Guru-600 (17/11/2026, Marc): the power-on screen's version, an image (p600_splash.h), made again from guru_version.h
# at every build, so that it always says the firmware's number (it said 1.3.0 in 1.3.1). p600/make_splash.py beside
# Felucca (FM-1/p600); absent (Felucca alone): nothing done
SPL=../p600/make_splash.py
if [ -f "$SPL" ]; then
    (cd .. && "$PY" p600/make_splash.py p600/fonts/vimongrong/MONRON1T.TTF p600/splash Felucca/firmware/src/p600_splash.h >/dev/null) ||
        { echo "build.sh: make_splash.py failed"; exit 1; }
    (cd .. && "$PY" p600/make_ldr_screen.py p600/fonts/vimongrong/MONRON1T.TTF Felucca/firmware/loader/ldr_art.h >/dev/null) ||
        { echo "build.sh: make_ldr_screen.py failed"; exit 1; }   # (the update screen's version: the same)
fi
exec "$PY" tools/build.py "$@"

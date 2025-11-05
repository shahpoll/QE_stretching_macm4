#!/usr/bin/env bash
set -euo pipefail
OUT="work/env_mac.txt"
{
  echo "[date] $(date -Iseconds)"
  echo "[uname] $(uname -a)"
  echo "[hw]    $(sysctl -n machdep.cpu.brand_string 2>/dev/null || true)"
  echo "[cores] $(sysctl -n hw.physicalcpu 2>/dev/null || getconf _NPROCESSORS_ONLN)"
  echo "[qe]    $(command -v pw.x)"
  pw.x -h 2>&1 | head -n 1 || true
  echo "[python] $(python3 -V 2>&1)"
  python3 - <<'PY'
import hashlib,glob,platform
print("[python-platform]", platform.platform())
for f in sorted(glob.glob("pseudos/*.UPF")):
    with open(f,'rb') as fh:
        h=hashlib.sha256(fh.read()).hexdigest()
    print("[pp-sha256]", f, h)
PY
} > "$OUT"
echo "wrote $OUT"

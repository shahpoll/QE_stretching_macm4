#!/usr/bin/env bash
set -euo pipefail
PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$PROJ/tmp"; WORK="$PROJ/work"; SCRIPTS="$PROJ/scripts"
mkdir -p "$WORK"
export OMP_NUM_THREADS=1
NP=$( (sysctl -n hw.physicalcpu 2>/dev/null || getconf _NPROCESSORS_ONLN || echo 4) )
PWX=${PWX:-"$HOME/q-e-qe-7.4.1/build/bin/pw.x"}
run_one () {
  s="$1"
  in_rel="./tmp/al_scf_${s}.in"
  in="$TMP/al_scf_${s}.in"; out="$WORK/al_scf_${s}.out"
  [ -s "$in" ] || { echo "missing $in"; return; }
  if grep -q "! *total energy" "$out" 2>/dev/null; then
     echo "[SKIP ] $(date +'%F %T') S=$s (already converged)" | tee -a "$WORK/session.log"
     return
  fi
  echo "[START] $(date +'%F %T') S=$s  IN=$(basename "$in")" | tee -a "$WORK/session.log"
  CMD="cd \"$PROJ\" && \"$PWX\" -in \"$in_rel\""
  if command -v mpirun >/dev/null 2>&1; then
     CMD="cd \"$PROJ\" && mpirun -np $NP \"$PWX\" -in \"$in_rel\""
  fi
  /usr/bin/time -p bash -lc "$CMD" < /dev/null 2>&1 | tee "$out"
  echo "[DONE ] $(date +'%F %T') S=$s" | tee -a "$WORK/session.log"
}
# order: coarse→fine around S=1.00 to get a fit early if interrupted
python3 - <<'PY' | tr ' ' '\n' > "$WORK/_scales.txt"
import numpy as np; s=np.round(np.linspace(0.90,1.18,15),2)
order=list(np.array(sorted(range(len(s)), key=lambda i:abs(s[i]-1.0))))
print(" ".join(f"{s[i]:.2f}" for i in order))
PY
while read -r S; do run_one "$S"; done < "$WORK/_scales.txt"
echo "[END  ] $(date +'%F %T') EOS sweep" | tee -a "$WORK/session.log"

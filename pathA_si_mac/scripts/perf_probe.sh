#!/usr/bin/env bash
set -euo pipefail
CSV="tables/perf_pathA_mac.csv"
: > "$CSV"
echo "run,ecutwfc,ecutrho,kmesh,wall_s" >> "$CSV"
for r in 1 2 3; do
  tmp_time=$(mktemp)
  tmp_out="work/si_scf_run${r}.out"
  ( /usr/bin/time -p pw.x -in si_scf.in > "$tmp_out" ) 2> "$tmp_time" || true
  wall=$(awk '/^real/ {print $2}' "$tmp_time")
  rm -f "$tmp_time"
  echo "$r,30,240,8x8x8,$wall" >> "$CSV"
done
echo "wrote $CSV"

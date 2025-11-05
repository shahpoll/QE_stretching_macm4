#!/usr/bin/env python3
import re
import glob
import pathlib

root = pathlib.Path(__file__).resolve().parents[1]
work = root / "work"
outs = sorted(glob.glob(str(work / "al_scf_*.out")))

patE = re.compile(r"!\s*total energy\s*=\s*([-\d\.Ee+]+)\s*Ry")
patV = re.compile(r"unit-cell volume\s*=\s*([-\d\.Ee+]+)\s*\(a\.u\.\)\^3")

rows = []
for fname in outs:
    text = pathlib.Path(fname).read_text(errors="ignore")
    mE = patE.search(text)
    mV = patV.search(text)
    if not (mE and mV):
        continue
    energy = float(mE.group(1))           # Ry / cell (1 atom here)
    volume = float(mV.group(1))           # bohr^3 / cell
    scale = float(pathlib.Path(fname).stem.split("_")[-1])
    rows.append((scale, volume, energy))

rows.sort(key=lambda r: r[0])

csv_path = work / "e_v.csv"
dat_path = work / "e_v.dat"

if not rows:
    csv_path.write_text("scale,volume_bohr3_per_atom,energy_Ry_per_atom\n")
    dat_path.write_text("")
    print("[HARVEST] points=0 → work/e_v.csv header only")
else:
    csv_lines = ["scale,volume_bohr3_per_atom,energy_Ry_per_atom"]
    csv_lines += [f"{s:.2f},{V:.6f},{E:.9f}" for s, V, E in rows]
    csv_path.write_text("\n".join(csv_lines) + "\n")
    with open(dat_path, "w") as fh:
        for _, V, E in rows:
            fh.write(f"{V:.8f} {E:.10f}\n")
    print(f"[HARVEST] points={len(rows)} → work/e_v.csv & work/e_v.dat")

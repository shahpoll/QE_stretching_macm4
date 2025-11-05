# Path A – Silicon (SCF → Bands → DOS/PDOS)

This workflow reproduces the Path A silicon reference run on the local Mac mini (Apple M4).  It performs self-consistent and non-self-consistent DFT calculations with Quantum ESPRESSO, generates band structures and DOS/PDOS data, and plots the resulting spectra.

## Highlights
- PSLibrary `Si.pbe-n-rrkjus_psl.1.0.0.UPF` pseudopotential (SHA256 captured in `work/pp_checksums.txt`).
- SCF mesh `8×8×8`, NSCF mesh `12×12×12`, `ecutwfc=30 Ry`, `ecutrho=240 Ry` (dual=8).
- Marzari–Vanderbilt smearing (`degauss=0.02 Ry`).
- Post-processing via `bands.x`, `dos.x`, `projwfc.x`.
- Python helper scripts in `scripts/` for plotting bands, total DOS, and element-resolved PDOS, plus a simple timing probe.

## Directory Layout
- `docs/README.md` – detailed run notes and key files.
- `pseudos/` – pseudopotential used for the run.
- `scripts/` – plotting utilities (`plot_bands.py`, `plot_dos.py`, `plot_pdos_sp.py`) and provenance helpers.
- `plots/` – generated PNGs (bands, DOS, PDOS, workflow flowchart).
- `tables/perf_pathA_mac.csv` – wall-clock timings (3× SCF).
- `work/` – QE output logs (`si_*_out`), perf probe outputs, environment capture.

## How to Reproduce
```bash
# adjust QE_BIN if your Quantum ESPRESSO build lives elsewhere
QE_BIN=~/q-e-qe-7.4.1/build/bin

$QE_BIN/pw.x   -in si_scf.in   > work/si_scf.out
$QE_BIN/pw.x   -in si_nscf.in  > work/si_nscf.out
$QE_BIN/pw.x   -in si_bands.in > work/si_bands.out
$QE_BIN/bands.x -in bands.pp.in > work/si_bands_pp.out
$QE_BIN/dos.x  -in dos.in      > work/si_dos.out
$QE_BIN/projwfc.x -in pdos.in  > work/si_pdos.out

python3 scripts/plot_bands.py
python3 scripts/plot_dos.py
python3 scripts/plot_pdos_sp.py
python3 scripts/perf_probe.sh      # optional timing sweep
```

Key plots and provenance artefacts live in `plots/` and `work/`.

# Path B — fcc Al Equation of State (macOS)

Completed E(V) sweep for fcc aluminium using Quantum ESPRESSO 7.4.1 (PBE) on a Mac mini M4. Outputs include publication-grade figures, LaTeX snippets, and machine-readable summaries of the Birch–Murnaghan (BM3) fit.

## Contents
- `work/e_v.csv`, `work/e_v.dat` – 15 volume/energy points (bohr³/atom, Ry/atom)
- `work/eos_fit.json` – BM3 parameters with 1σ uncertainties & fit metrics (`a₀=4.0373 Å`, `B₀=76.20 GPa`, `B′=4.830`, RMS ≈ 1.48 meV/atom)
- `plots/eos_E_vs_V.{png,svg}`, `plots/eos_residuals.{png,svg}`, `plots/eos_P_vs_V.{png,svg}` – publication-ready graphics (300 dpi PNG + SVG)
- `tables/eos_summary.csv` – tabular summary
- `latex/eos_table.tex`, `latex/eos_methods.tex` – drop-in snippets for reports
- `scripts/harvest.py`, `scripts/fit_bm3_plot.py` – data harvest & BM3 fit/plot pipeline

## Method snapshot
- QE 7.4.1 built with PAW support (local build under `~/q-e-qe-7.4.1/build/bin/pw.x`)
- Potential: `pseudos/Al.pbe-n-kjpaw_psl.1.0.0.UPF`
- SCF settings: `ibrav=2`, `ecutwfc=40 Ry`, `ecutrho=320 Ry`, `k=24×24×24`, Methfessel–Paxton (cold) smearing `0.02 Ry`
- 15 uniform scales (0.90–1.18) around the fitted equilibrium volume
- Energies per atom; volumes are bohr³ per atom (primitive cell holds one Al atom)
- BM3 fit via non-linear least squares (`scipy.optimize.curve_fit`); uncertainties from covariance matrix

## Reproduce / refresh artifacts
```bash
cd "$HOME/QE_BASICS/pathB_eos_al_mac"
python3 scripts/harvest.py        # parse work/al_scf_*.out → e_v.{csv,dat}
python3 scripts/fit_bm3_plot.py   # fit BM3, regenerate plots/latex/tables
```
All scripts assume the SCF outputs already exist in `work/`. To rerun the DFT sweep, use `scripts/run_eos.sh` (uses the local PAW-enabled `pw.x`).

## Citation
- Quantum ESPRESSO 7.4.1 — P. Giannozzi *et al.*, *J. Chem. Phys.* **152**, 154105 (2020)
- PSLibrary pseudopotentials — A. Dal Corso, *Comput. Mater. Sci.* **95**, 337 (2014)

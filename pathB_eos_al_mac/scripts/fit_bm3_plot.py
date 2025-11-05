#!/usr/bin/env python3
import json, csv, pathlib
import numpy as np
from math import pi
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

root = pathlib.Path(__file__).resolve().parents[1]
work = root/"work"; plots = root/"plots"; latex = root/"latex"; tables = root/"tables"
plots.mkdir(exist_ok=True); latex.mkdir(exist_ok=True); tables.mkdir(exist_ok=True)
PNG_DPI = 300

# --- Load data ---
try:
    Edata = np.loadtxt(work/"e_v.dat", ndmin=2)
except OSError as exc:
    raise SystemExit(f"[FIT] missing data file: {exc}")

if Edata.size == 0:
    raise SystemExit("[FIT] no data points found in work/e_v.dat; run harvest first.")

V = Edata[:,0]
E = Edata[:,1]

# --- Birch-Murnaghan 3rd order for E(V) ---
def bm3_E(V, E0, V0, B0, B1):
    x = (V0 / V) ** (2.0 / 3.0)
    eta = x - 1.0
    return E0 + (9.0 / 16.0) * B0 * V0 * (B1 * eta**3 + (6.0 - 4.0 * x) * eta**2)

p0 = (E.min(), V[np.argmin(E)], 0.005, 4.0)  # rough guesses in Ry/bohr^3 and unitless B1
popt, pcov = curve_fit(bm3_E, V, E, p0=p0, maxfev=10000)
E0, V0, B0, B1 = popt
sig = np.sqrt(np.diag(pcov))
Efit = bm3_E(V, *popt)
res = E - Efit
rms_meV = np.sqrt(np.mean((res*13.605698066)**2))*1000.0  # meV

# conversions
RY_PER_BOHR3_to_GPa = 14710.5
B0_GPa = B0 * RY_PER_BOHR3_to_GPa

# --- Save summary in JSON + CSV ---
BOHR = 0.529177210903
a0_bohr = (4.0 * V0) ** (1.0 / 3.0)
a0_A = a0_bohr * BOHR
da0dV0 = (4.0 / 3.0) * (4.0 * V0) ** (-2.0 / 3.0)
sigma_a0_A = BOHR * abs(da0dV0) * sig[1]

summary = {
 "timestamp": datetime.now().isoformat(timespec="seconds"),
 "model": "Birch–Murnaghan 3rd-order",
 "V0_bohr3_per_atom": V0, "sigma_V0": float(sig[1]),
 "a0_A": a0_A, "sigma_a0_A": float(sigma_a0_A),
 "B0_GPa": B0_GPa, "sigma_B0_GPa": sig[2]*RY_PER_BOHR3_to_GPa,
 "B1": B1, "sigma_B1": float(sig[3]),
 "E0_Ry_per_atom": E0, "sigma_E0": float(sig[0]),
 "rms_error_meV_per_atom": rms_meV,
 "max_abs_residual_meV": float(np.max(np.abs(res))*13.605698066*1000.0)
}
(work/"eos_fit.json").write_text(json.dumps(summary, indent=2))

with open(tables/"eos_summary.csv","w",newline="") as fh:
    w=csv.writer(fh); 
    w.writerow(["param","value","units","sigma"])
    w.writerow(["V0",summary["V0_bohr3_per_atom"],"bohr^3/atom",summary["sigma_V0"]])
    w.writerow(["a0",summary["a0_A"],"Angstrom",summary["sigma_a0_A"]])
    w.writerow(["B0",summary["B0_GPa"],"GPa",summary["sigma_B0_GPa"]])
    w.writerow(["B'",summary["B1"],"",summary["sigma_B1"]])
    w.writerow(["E0",summary["E0_Ry_per_atom"],"Ry/atom",summary["sigma_E0"]])
    w.writerow(["RMS",summary["rms_error_meV_per_atom"],"meV/atom",""])

# --- Figures ---
Vfine = np.linspace(V.min()*0.95, V.max()*1.05, 600)
Ecurve = bm3_E(Vfine, *popt)

plt.figure(figsize=(12,7))
plt.plot(Vfine, Ecurve, lw=2.5, label="BM3 fit")
plt.scatter(V, E, s=18, zorder=3, label="DFT points")
plt.axvline(V0, ls="--", lw=1, label="V$_0$")
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("Energy (Ry/atom)")
plt.legend()
plt.tight_layout()
plt.savefig(plots/"eos_E_vs_V.png", dpi=PNG_DPI, bbox_inches="tight")
plt.savefig(plots/"eos_E_vs_V.svg", bbox_inches="tight")
plt.close()

plt.figure(figsize=(12,7))
plt.axhline(0, color="k", lw=1)
plt.scatter(V, res, s=22, label="Residuals")
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("$E - E_{fit}$ (Ry)")
plt.legend()
plt.tight_layout()
plt.savefig(plots/"eos_residuals.png", dpi=PNG_DPI, bbox_inches="tight")
plt.savefig(plots/"eos_residuals.svg", bbox_inches="tight")
plt.close()

# Pressure curve (BM3 analytical derivative)
def bm3_P(V):
    x = (V0 / V) ** (2.0 / 3.0)
    return (3.0 * B0 / 2.0) * (x**(3.0 / 2.0) - x**(5.0 / 2.0)) * (1.0 + (3.0 / 4.0) * (B1 - 4.0) * (x - 1.0))
Vpv = np.linspace(0.9*V0, 1.2*V0, 400)
P_GPa = bm3_P(Vpv)*RY_PER_BOHR3_to_GPa
plt.figure(figsize=(12,7))
plt.plot(Vpv, P_GPa, lw=2.2, label="BM3 P(V)")
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("Pressure (GPa)")
plt.legend()
plt.tight_layout()
plt.savefig(plots/"eos_P_vs_V.png", dpi=PNG_DPI, bbox_inches="tight")
plt.savefig(plots/"eos_P_vs_V.svg", bbox_inches="tight")
plt.close()

# LaTeX snippets
(open(latex/"eos_table.tex","w")).write(
  "\\begin{tabular}{lcc}\n\\hline\n"
  "Parameter & Value & Uncertainty\\\\\\hline\n"
  f"$V_0$ & {V0:.6f}~\\text{{bohr}}^3/\\text{{atom}} & {sig[1]:.6f}\\\\\n"
  f"$a_0$ & {summary['a0_A']:.4f}~\\text{{\\AA}} & {summary['sigma_a0_A']:.4f}\\\\\n"
  f"$B_0$ & {B0_GPa:.3f}~\\text{{GPa}} & {summary['sigma_B0_GPa']:.3f}\\\\\n"
  f"$B'$ & {B1:.3f} & {sig[3]:.3f}\\\\\n"
  f"$E_0$ & {E0:.6f}~\\text{{Ry/atom}} & {sig[0]:.6f}\\\\\\hline\n"
  "\\end{tabular}\n")
(open(latex/"eos_methods.tex","w")).write(
  "% Methods snippet (auto)\n"
  "We computed $E(V)$ for 15 volumes (0.90--1.18 $V_0$) using QE 7.4.1 with PBE and the PSLibrary PAW Al potential.\n"
  "Energies were fit to the 3rd-order Birch--Murnaghan equation of state.\n")

print("[FIT] Wrote plots/*.png, latex/*.tex, tables/eos_summary.csv, work/eos_fit.json")

# Visual Guide — Path B (Aluminium EOS)

This document explains each graphic generated for the aluminium equation-of-state workflow, why it matters, the meaning of axes/annotations, and the conclusions we draw.

---

## Energy vs Volume (`plots/eos_E_vs_V.png`, `.svg`, `_pub.*`)
- **Purpose:** Compares the discrete DFT energy points against the fitted Birch–Murnaghan (BM3) curve.
- **Axes:**  
  *x-axis* – atomic volume in bohr³ (primitive cell containing one Al atom).  
  *y-axis* – total energy per atom in Ry relative to a reference offset.
- **Why this plot?** EOS fitting demands that the analytic curve tracks the raw data; visualising both ensures the fit is sensible before quoting parameters.
- **Annotations:** Fit line (solid) vs. discrete markers (DFT); the minimum identifies `V₀`.
- **Conclusions:** The BM3 curve reproduces the ab‑initio points smoothly, with the minimum near 111 bohr³; this volume feeds directly into the equilibrium lattice constant reported in `eos_fit.json`.

---

## Residuals (`plots/eos_residuals.png`, `.svg`, `_pub.*`)
- **Purpose:** Highlights the difference `E_DFT − E_fit` for each volume point to expose systematic bias.
- **Axes:**  
  *x-axis* – volume (bohr³).  
  *y-axis* – residual energy in Ry.
- **Why include it?** Small residuals (≪ 1 meV) indicate the fit captures the physics; patterns (e.g., oscillations) would hint at insufficient k-point convergence or poor window selection.
- **Conclusions:** Residuals stay within ±2 meV/atom, supporting the RMS figure reported in the summary and validating the 3rd-order BM choice.

---

## BM3 Pressure Curve (`plots/eos_P_vs_V.png`, `.svg`, `_pub.*`)
- **Purpose:** Converts the fit into `P(V)` to visualise the derived bulk modulus and pressure response.
- **Axes:**  
  *x-axis* – volume (bohr³).  
  *y-axis* – pressure in GPa computed from BM3 derivative.
- **Why plot it?** Researchers often need pressure vs volume without recomputing the EOS; the plot also visually encodes `B₀` (slope near `V₀`) and the effect of `B′`.
- **Conclusions:** The curve is smooth and monotonic, suitable for interpolation; the slope at `V₀` corresponds to ≈76 GPa (reported in the summary).

---

## Publication Variants (`*_pub.png`, `*.svg`)
- **What are they?** Higher-resolution (300 dpi) PNGs and vector SVGs derived from the same data as the default PNGs.  They exist so you can drop them into manuscripts or presentations without rerunning scripts.
- **Interpretation:** Identical conclusions to the standard plots; choice depends on output medium (print vs. web).

---

## Tabular Artefacts
- While not graphics, remember `tables/eos_summary.csv` and `latex/eos_table.tex` mirror the information extracted from the plots (equilibrium parameters, uncertainties) for reuse in documents.

---

## Summary Takeaways
- The plotted curves verify the numerical consistency of the workflow.  
- `E(V)` → sanity check for the fit, locate `V₀`.  
- Residuals → validate RMS error stated in the README.  
- `P(V)` → communicate material response and bulk modulus graphically.


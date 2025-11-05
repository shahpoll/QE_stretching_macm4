# Visual Guide — Path A (Silicon)

This note explains every visual artefact in `plots/`, why each plot matters, and what the axes/terms mean.

---

## Path Flowchart (`plots/pathA_flowchart.png`)
- **Why show it?** Summarises the computational workflow so a newcomer can see the order of executables without wading through scripts.
- **What’s plotted?** Rectangular nodes for each QE or post-processing step (`pw.x` SCF/NSCF/Bands, `bands.x`, `dos.x`, `projwfc.x`, Python plotting). Arrows show data dependencies.
- **Key terms:**  
  *`SCF`* – self-consistent field run establishing charge density.  
  *`NSCF`* – non-self-consistent run on denser k-mesh for DOS/PDOS.  
  *`projwfc.x`* – projection onto atomic orbitals for PDOS.
- **Takeaways:** The diagram makes it clear that all downstream artefacts originate from the initial SCF density and highlights when MPI (`pw.x`) versus serial utilities are employed.

---

## QE Band Structure (`plots/si_bands.png`)
- **Why show it?** Provides the baseline DFT band structure along the FCC high-symmetry path used later for comparisons.
- **Axes/terms:**  
  *x-axis* – cumulative k-path distance from Γ→X→W→K→Γ→L.  
  *y-axis* – eigenvalues relative to Fermi energy (eV).  
  *Colour* – uniform (single data source from QE).
- **Conclusions:** Silicon is a semiconductor; the band gap between the highest valence band near Γ and the conduction band along Γ→X is evident. This plot is the ground truth reference for any Wannier or interpolation study.

---

## Python Band Plot (`plots/si_bands_mac.png`)
- **Why show it?** Demonstrates the locally re-generated bands from `scripts/plot_bands.py`, confirming that our Python tooling reproduces the QE plot.
- **Differences vs. `si_bands.png`:** Annotated with path segments and automatically derived valence/conduction information (through Fermi-referenced energies).
- **Conclusions:** Validates that the helper scripts interpret the QE `si.bands.dat.gnu` data correctly and are ready for sharing or automation.

---

## DOS (`plots/si_dos.png`) & Local DOS (`plots/si_dos_mac.png`)
- **Purpose:** Visualise the total electronic density of states to confirm smearing, bandwidth, and gap behaviour.
- **Axes:**  
  *x-axis* – energy relative to Fermi level (eV).  
  *y-axis* – states per eV per cell.
- **Why two plots?** `si_dos.png` is directly from QE, while `si_dos_mac.png` is the re-rendered version produced locally via `plot_dos.py`. The duplicated view (plus `si_idos_mac.png` for the integrated DOS) illustrates reproducibility across machines.
- **Conclusions:** The DOS is zero inside the band gap; peaks correspond to van Hove singularities. The integrated DOS plot confirms electron counting (8 valence electrons per cell).

---

## PDOS (`plots/si_pdos_sp_mac.png`)
- **Why show it?** Separates the s and p contributions on each silicon atom, giving chemical insight (hybridisation).
- **Axes:** Same as DOS plot but resolved by orbital character.
- **Key terms:**  
  *`Si s`* vs. *`Si p (sum)`* – the projected density onto atomic s and three p orbitals summed over both atoms in the primitive cell.
- **Conclusions:** The valence band is dominantly p-like (expected for sp³ bonding), while the conduction band edge shows mixed character. Supports the narrative when discussing Wannierisation later.

---

## Band & DOS Flowchart Vector (`plots/pathA_flowchart.dot`)
- **Purpose:** Source Graphviz file for the PNG. Included so others can regenerate/edit the diagram.
- **No visual output** by itself but documented here for completeness.

---

## Integrated DOS (`plots/si_idos_mac.png`)
- **Why show it?** Accumulates the DOS over energy to confirm total electron count and check smoothing.
- **Interpretation:** The plateau at 8 electrons (per primitive cell) below the Fermi level verifies the SCF charge count. Smoothness indicates that the tetrahedral smearing parameters are well chosen.

---

## Additional Notes
- Files like `si_bands.dat.gnu`, `si.dos`, and `si.pdos.*` are the raw data feeding the plots; the explanatory text above applies to their rendered versions.
- Duplicate “mac” versions demonstrate reproducibility on the local machine—use whichever suits your pipeline (PNG for presentations, data files for further analysis).


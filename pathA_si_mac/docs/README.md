# Path A (Mac) — Silicon SCF → Bands → DOS/PDOS

- Code: Quantum ESPRESSO 7.x (CPU-only on macOS).
- PP: `pseudos/Si.pbe-n-rrkjus_psl.1.0.0.UPF` (SSSP Efficiency).
- SCF: 8×8×8 Monkhorst–Pack, `ecutwfc=30 Ry`, `ecutrho=240 Ry`.  
- NSCF: 12×12×12 (DOS/PDOS); Bands along Γ–X–W–K–Γ–L–U–W–L–K.
- Post: `bands.x`, `dos.x` (`DeltaE≈0.05 eV`, Gaussian broadening), `projwfc.x`.

Artifacts:
- Bands (labeled): `plots/si_bands_mac.png`
- DOS, integrated DOS: `plots/si_dos_mac.png`, `plots/si_idos_mac.png`
- PDOS s vs p: `plots/si_pdos_sp_mac.png`
- Env and PP checksums: `work/env_mac.txt`

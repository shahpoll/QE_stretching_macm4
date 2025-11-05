# QE_stretching_macm4

This repository collects the Quantum ESPRESSO “Path A” and “Path B” workflows executed on a Mac mini M4 (CPU-only). Each path mirrors the corresponding server-side exercises and ships with the inputs, scripts, provenance logs, and publication-ready plots needed to understand or reproduce the calculations locally.

## Repository Layout

| Path | Folder | Purpose |
|------|--------|---------|
| A | [`pathA_si_mac`](pathA_si_mac) | Diamond Si: SCF → bands → DOS/PDOS, plus Python plotting helpers and perf probes |
| B | [`pathB_eos_al_mac`](pathB_eos_al_mac) | fcc Al: equation of state sweep, Birch–Murnaghan fits, plots, LaTeX snippets |

Path C is being prototyped separately and is excluded from this repository for now.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/shahpoll/QE_stretching_macm4.git
cd QE_stretching_macm4

# (Optional) load your QE build path
export QE_BIN=~/q-e-qe-7.4.1/build/bin

# Explore the individual paths
ls pathA_si_mac pathB_eos_al_mac
```

Each path directory has its own README with run instructions, directory overview, and plotting helpers. The scripts assume a QE ≥ 7.4.1 build with MPI-enabled executables available on your `PATH` (or via `QE_BIN`).

## Highlights

- **Provenance everywhere** – environment captures, pseudopotential checksums, wall-clock timings, and raw QE outputs live in `work/`.
- **Re-usable plots** – Python scripts in each `scripts/` folder rebuild the PNG figures in `plots/` (bands, DOS, EOS curves, residuals, flowcharts, etc.).
- **Git-friendly layout** – scratch directories (`tmp/`, wavefunction blobs) are ignored so only portable artefacts remain in version control.
- **Summary docs** – see [`pathA_si_mac/docs/README.md`](pathA_si_mac/docs/README.md) and [`pathB_eos_al_mac/README.md`](pathB_eos_al_mac/README.md) for deeper notes on numerics and key files.

## Requirements

- Quantum ESPRESSO 7.4.1 (or newer) compiled with MPI support.
- Python 3.9+ with the standard scientific stack (`numpy`, `matplotlib`, `pandas`).
- Wannier90 is *not* required for Paths A/B.

## Contributing

Open an issue or PR if you spot gaps, want to extend to other materials, or wish to help polish the Path C workflow once it lands.

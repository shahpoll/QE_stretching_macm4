import numpy as np
import matplotlib.pyplot as plt

FN = "si.bands.dat.gnu"

bands = []
kgrid = None
current_e = []
current_k = []
with open(FN) as fh:
    for raw in fh:
        line = raw.strip()
        if not line:
            if current_e:
                if kgrid is None:
                    kgrid = np.array(current_k, dtype=float)
                bands.append(np.array(current_e, dtype=float))
                current_e = []
                current_k = []
            continue
        parts = raw.split()
        k_val = float(parts[0])
        e_val = float(parts[1])
        current_e.append(e_val)
        if kgrid is None:
            current_k.append(k_val)
    if current_e:
        if kgrid is None:
            kgrid = np.array(current_k, dtype=float)
        bands.append(np.array(current_e, dtype=float))

if kgrid is None or not bands:
    raise SystemExit(f"No band data parsed from {FN}")

bands_arr = np.vstack(bands)

plt.figure(figsize=(12, 5))
for band in bands_arr:
    plt.plot(kgrid, band, linewidth=1.0, color="tab:blue")

# Label FCC path Γ–X–W–K–Γ–L–U–W–L–K
labels = ['Γ','X','W','K','Γ','L','U','W','L','K']
k_nodes = np.array([
    [0.0000, 0.0000, 0.0000],
    [0.5000, 0.0000, 0.5000],
    [0.5000, 0.2500, 0.7500],
    [0.3750, 0.3750, 0.7500],
    [0.0000, 0.0000, 0.0000],
    [0.5000, 0.5000, 0.5000],
    [0.6250, 0.2500, 0.6250],
    [0.5000, 0.2500, 0.7500],
    [0.5000, 0.5000, 0.5000],
    [0.3750, 0.3750, 0.7500],
])
segment_lengths = np.linalg.norm(np.diff(k_nodes, axis=0), axis=1)
cumulative = np.concatenate(([0.0], np.cumsum(segment_lengths)))
if cumulative[-1] > 0:
    scale = (kgrid[-1] - kgrid[0]) / cumulative[-1]
else:
    scale = 1.0
xticks = kgrid[0] + cumulative * scale
plt.xticks(xticks, labels)
plt.xlim(kgrid[0], kgrid[-1])

flat = bands_arr.ravel()
occupied = flat[flat <= 0.0]
unoccupied = flat[flat > 0.0]
if occupied.size and unoccupied.size:
    ho = occupied.max()
    lu = unoccupied.min()
    gap = lu - ho
    ax = plt.gca()
    ax.text(0.02, 0.95, f"HO={ho:.4f} eV", transform=ax.transAxes, ha='left')
    ax.text(0.02, 0.90, f"LU={lu:.4f} eV", transform=ax.transAxes, ha='left')
    ax.text(0.02, 0.85, f"Gap={gap:.3f} eV", transform=ax.transAxes, ha='left')

plt.axhline(0.0, linestyle='--', linewidth=0.8, color='tab:gray')
plt.ylabel("E - $E_F$ (eV)")
plt.xlabel("k-path")
plt.title("Si bands")
plt.tight_layout()
plt.savefig("plots/si_bands_mac.png", dpi=180)
print("wrote plots/si_bands_mac.png")

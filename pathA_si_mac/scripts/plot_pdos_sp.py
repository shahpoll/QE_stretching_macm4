import glob
import numpy as np
import matplotlib.pyplot as plt


def sum_pdos(patterns):
    energy = None
    total = None
    matched = []
    for pattern in patterns:
        for fn in sorted(glob.glob(pattern)):
            matched.append(fn)
            data = np.loadtxt(fn)
            if energy is None:
                energy = data[:, 0]
                total = np.zeros_like(energy)
            total += data[:, 1]
    if not matched:
        raise SystemExit(f"No PDOS files matched {patterns}")
    return energy, total

E_s, pdos_s = sum_pdos(["si.pdos.pdos_atm#*(Si)_wfc#*(s)"])
E_p, pdos_p = sum_pdos(["si.pdos.pdos_atm#*(Si)_wfc#*(p)"])

emin, emax = -8.0, 8.0
mask = (E_s >= emin) & (E_s <= emax)
if not np.any(mask):
    mask = slice(None)

plt.figure(figsize=(12, 6))
plt.plot(E_s[mask], pdos_s[mask], label="Si s", color="tab:green")
plt.plot(E_p[mask], pdos_p[mask], label="Si p (sum)", color="tab:red")
plt.xlabel("E - $E_F$ (eV)")
plt.ylabel("PDOS (states/eV)")
plt.legend()
plt.tight_layout()
plt.savefig("plots/si_pdos_sp_mac.png", dpi=180)
print("wrote plots/si_pdos_sp_mac.png")

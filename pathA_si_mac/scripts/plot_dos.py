import numpy as np
import matplotlib.pyplot as plt

E, DOS, IDOS = np.loadtxt("si.dos", unpack=True)

emin, emax = -8.0, 8.0
mask = (E >= emin) & (E <= emax)
if not np.any(mask):
    mask = slice(None)

plt.figure(figsize=(12, 6))
plt.plot(E[mask], DOS[mask], label="Total DOS", color="tab:blue")
plt.xlabel("E - $E_F$ (eV)")
plt.ylabel("DOS (states/eV)")
plt.legend()
plt.tight_layout()
plt.savefig("plots/si_dos_mac.png", dpi=180)

plt.figure(figsize=(12, 6))
plt.plot(E[mask], IDOS[mask], label="Integrated DOS", color="tab:orange")
plt.xlabel("E - $E_F$ (eV)")
plt.ylabel("States")
plt.legend()
plt.tight_layout()
plt.savefig("plots/si_idos_mac.png", dpi=180)

print("wrote plots/si_dos_mac.png and plots/si_idos_mac.png")

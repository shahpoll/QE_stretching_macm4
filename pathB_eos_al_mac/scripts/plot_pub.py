import json, os, matplotlib.pyplot as plt
import numpy as np, pandas as pd
PROJ=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
WORK=os.path.join(PROJ,"work"); PLOTS=os.path.join(PROJ,"plots"); LAT=os.path.join(PROJ,"latex")
os.makedirs(LAT, exist_ok=True)
df=pd.read_csv(os.path.join(WORK,"e_v.csv")); J=json.load(open(os.path.join(WORK,"eos_fit.json")))
V=df["V_bohr3"].values; E=df["E_Ry"].values

def bm3_E(V, E0, V0, B0, Bp):
    eta=(V0/V)**(2/3)-1
    return E0+(9/16)*B0*V0*((Bp*eta**3)+(6-4*(V0/V)**(2/3))*eta**2)
p=(J["E0_Ry"],J["V0_bohr3"],J["B0_Ry_per_bohr3"],J["Bp"])
v=np.linspace(V.min()*0.95,V.max()*1.05,400)
plt.figure(figsize=(10,6)); plt.plot(V,E,'o',ms=3); plt.plot(v,bm3_E(v,*p),'-',lw=2)
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("Energy (Ry/atom)"); plt.tight_layout()
plt.savefig(os.path.join(PLOTS,"eos_E_vs_V_pub.png"),dpi=300); plt.savefig(os.path.join(PLOTS,"eos_E_vs_V_pub.svg"))
res=E-bm3_E(V,*p); plt.figure(figsize=(10,6)); plt.plot(V,res,'o',ms=3); plt.axhline(0,color='k',lw=1,alpha=0.5)
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("$E - E_{fit}$ (Ry)"); plt.tight_layout()
plt.savefig(os.path.join(PLOTS,"eos_residuals_pub.png"),dpi=300); plt.savefig(os.path.join(PLOTS,"eos_residuals_pub.svg"))

def bm3_P(V,V0,B0,Bp):
    x=(V0/V)**(2/3)
    return (3/2)*B0*(x**(3/2)-x**(5/2))*(1+(3/4)*(Bp-4)*(x-1))
v2=np.linspace(J["V0_bohr3"]*0.9,J["V0_bohr3"]*1.2,400)
GPa=14710.5; plt.figure(figsize=(10,6)); plt.plot(v2,bm3_P(v2,J["V0_bohr3"],J["B0_Ry_per_bohr3"],J["Bp"])*GPa,'-',lw=2)
plt.xlabel("Volume (bohr$^3$/atom)"); plt.ylabel("Pressure (GPa)"); plt.tight_layout()
plt.savefig(os.path.join(PLOTS,"eos_P_vs_V_pub.png"),dpi=300); plt.savefig(os.path.join(PLOTS,"eos_P_vs_V_pub.svg"))
table_tex = (
  "\\begin{tabular}{lrr}\\hline\n"
  f"$a_0$ (\\AA) & {J['a0_A']:.4f} \\\\\n"
  f"$B_0$ (GPa) & {J['B0_GPa']:.2f} \\\\\n"
  f"$B'$ & {J['Bp']:.3f} \\\\\n"
  f"RMS (meV/atom) & {J['rms_meV_per_atom']:.2f} \\\\\n"
  "\\hline\\end{tabular}\n"
)
open(os.path.join(LAT,"eos_table.tex"),"w").write(table_tex)
open(os.path.join(LAT,"eos_methods.tex"),"w").write(
  "% Path B (Al EOS, PBE, PSL 1.0.0, MV smearing 0.02 Ry, k=24^3, 40/320 Ry)\n"
)

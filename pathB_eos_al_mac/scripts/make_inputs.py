import numpy as np, os, pathlib
A0 = 4.05                 # Angstrom
SCALES = np.round(np.linspace(0.90, 1.18, 15), 2)
ECUTWFC, ECUTRHO = 40, 320
KGRID = int(os.environ.get("KGRID","24"))
DEGAUSS = 0.02            # Ry
PP_BASENAME = "Al.pbe-n-kjpaw_psl.1.0.0.UPF"
PSEUDO_DIR = "./pseudos"
TMP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","tmp"))
pathlib.Path(TMP).mkdir(parents=True, exist_ok=True)

TEMPLATE = """&CONTROL
  calculation='scf', prefix='al', pseudo_dir='{PSEUDO_DIR}', outdir='./tmp',
  disk_io='none'
/
&SYSTEM
  ibrav=2, celldm(1)={ALAT_BOHR:.8f},
  nat=1, ntyp=1,
  ecutwfc={ECUTWFC}, ecutrho={ECUTRHO},
  occupations='smearing', smearing='mv', degauss={DEGAUSS},
  input_dft='pbe'
/
&ELECTRONS
  conv_thr=1.0d-9, electron_maxstep=200
/
ATOMIC_SPECIES
 Al  26.9815  {PP}
ATOMIC_POSITIONS (alat)
 Al 0.0 0.0 0.0
K_POINTS automatic
 {K} {K} {K}   1 1 1
"""
ANG2BOHR = 1.0/0.529177210903
for s in SCALES:
    a = A0*s
    alat_bohr = a*ANG2BOHR
    fname = os.path.join(TMP, f"al_scf_{s:.2f}.in")
    with open(fname,"w") as f:
        f.write(TEMPLATE.format(ALAT_BOHR=alat_bohr, ECUTWFC=ECUTWFC, ECUTRHO=ECUTRHO,
                                DEGAUSS=DEGAUSS, PSEUDO_DIR=PSEUDO_DIR,
                                PP=PP_BASENAME, K=KGRID))
print("Wrote inputs in tmp/:", " ".join([f"al_scf_{s:.2f}.in" for s in SCALES]))

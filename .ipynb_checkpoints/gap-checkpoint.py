from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.core import Spin
import matplotlib.pyplot as plt

# Load vasprun.xml file
vasprun = Vasprun("vasprun.xml", parse_dos=True)
complete_dos = vasprun.complete_dos

# Get spin-polarized DOS
densities = complete_dos.densities

# Extract energies and densities for spin-up and spin-down
energies = complete_dos.energies - complete_dos.efermi
spin_up_dos = densities[Spin.up]
spin_down_dos = densities[Spin.down]

# Find the band gap
conduction_band_min = None
valence_band_max = None

for i, energy in enumerate(energies):
    if (spin_up_dos[i] > 0 or spin_down_dos[i] > 0) and energy < 0:
        valence_band_max = energy
    elif (spin_up_dos[i] > 0 or spin_down_dos[i] > 0) and energy > 0 and conduction_band_min is None:
        conduction_band_min = energy

if valence_band_max is not None and conduction_band_min is not None:
    band_gap = conduction_band_min - valence_band_max
    print(f"Band Gap: {band_gap:.3f} eV")
else:
    print("No band gap found.")

# Plotting the DOS
# plt.plot(energies, spin_up_dos, label="Spin Up DOS")
# plt.plot(energies, spin_down_dos, label="Spin Down DOS")
# plt.axvline(x=0, color='r', linestyle='--', label="Fermi Level")
# plt.xlabel("Energy (eV)")
# plt.ylabel("DOS")
# plt.legend()
# plt.show()
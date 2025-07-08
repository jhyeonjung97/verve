from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import write
import subprocess
import os

def main():
    api_key = '####'
    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb'],
    }
        
    materials = get_zero_hull_energy_materials(api_key, metal_rows)
        
def get_zero_hull_energy_materials(api_key, metal_rows):
    adaptor = AseAtomsAdaptor()
    with MPRester(api_key) as mpr:
        for row in metal_rows:
            row_dir = f"./{row}"
            os.makedirs(row_dir, exist_ok=True)
            for i, element in enumerate(metal_rows[row]):
                dir_name = f'{i:02d}_{element}'
                element_dir = os.path.join(row_dir, dir_name)
                os.makedirs(element_dir, exist_ok=True)
                
                search_results = mpr.materials.summary.search(chemsys=element, theoretical=False,
                                                              fields=['structure', 'energy_above_hull'])
                search_results = [material for material in search_results if len(material.structure) <= 2]

                min_hull = None
                for material in search_results:
                    if min_hull is None or material.energy_above_hull < min_hull:
                        min_structure = material.structure
                        min_hull = material.energy_above_hull
                        
                if min_hull is not None:
                    atoms = adaptor.get_atoms(min_structure)
                    filename = os.path.join(element_dir, 'start.traj')
                    write(filename, atoms, format='traj')
                    
                    hull_filename = os.path.join(element_dir, 'hull_energy.txt')
                    with open(hull_filename, 'w') as f:
                        f.write(f"{row} {element} \tEnergy above hull: {min_hull}")
                else:
                    print(f"No suitable material found for {element}.")
                
if __name__ == "__main__":
    main()
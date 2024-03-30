from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import write
import os

def main():
    api_key = '3jSckrUWEJ94DEo93ZOlCwNd2B1BHerV'
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
            for element in metal_rows[row]:
                element_dir = os.path.join(row_dir, element)
                os.makedirs(element_dir, exist_ok=True)
                
                search_results = mpr.materials.summary.search(chemsys=element, energy_above_hull=(0, 0), fields=['structure'])
                if len(search_results) == 1:
                    atoms = adaptor.get_atoms(search_results[0].structure)
                    filename = os.path.join(element_dir, 'start.traj')
                    write(filename, atoms)
                    print(f"Saved {filename}")
                else:
                    raise ValueError(f'There are more than one material of {element}')                    

if __name__ == "__main__":
    main()
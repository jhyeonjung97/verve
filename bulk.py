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
            for i, element in enumerate(metal_rows[row]):
                dir_name = f'{i:02d}_{element}'
                element_dir = os.path.join(row_dir, dir_name)
                os.makedirs(element_dir, exist_ok=True)
                
                search_results = mpr.materials.summary.search(chemsys=element, 
                                                              theoretical=False,
                                                              fields=['structure', 'energy_above_hull'])
                for material in search_results:
                    structure = material.structure
                    hull = material.energy_above_hull
                    if hull == 0 and len(structure) <= 2:
                        atoms = adaptor.get_atoms(structure)
                        filename = os.path.join(element_dir, f'start.traj')
                        write(filename, atoms)
                    else:
                        for material in search_results:
                            atoms = adaptor.get_atoms(material.structure)
                            hull = material.energy_above_hull
                            filename = os.path.join(element_dir, f'start_{hull}.traj')
                            write(filename, atoms)
                
if __name__ == "__main__":
    main()
from pymatgen.ext.matproj import MPRester
from pymatgen.core.structure import Structure

# Your Materials Project API Key
API_KEY = '3jSckrUWEJ94DEo93ZOlCwNd2B1BHerV'

metal_rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb'],
    }

def get_zero_hull_energy_materials(api_key):
    with MPRester(api_key) as m:
        materials = m.materials.summary.search(e_above_hull=0, fields=['material_id', 'formula', 'structure'])
        return materials

def main():
    materials = get_zero_hull_energy_materials(API_KEY)
    for material in materials:
        print(f"Material ID: {material['material_id']}, Formula: {material['formula']}")
        print("Structure:", material['structure'])

if __name__ == "__main__":
    main()

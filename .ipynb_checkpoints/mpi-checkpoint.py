import argparse
from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import write
import os

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Download structures from the Materials Project by material IDs and save as .traj files.")
parser.add_argument('ids', nargs='+', help="Material IDs to download")
args = parser.parse_args()

# Your API key for the Materials Project
api_key = '3jSckrUWEJ94DEo93ZOlCwNd2B1BHerV'
adaptor = AseAtomsAdaptor()

with MPRester(api_key) as mpr:
    for material_id in args.ids:
        try:
            search_results = mpr.materials.get_data_by_id(material_id=material_id, fields=['structure'])
            if search_results:
                atoms = adaptor.get_atoms(search_results.structure)
                filename = os.path.join("./", f'{material_id}.traj')
                write(filename, atoms)
                print(f"Saved {material_id}.traj")
            else:
                print(f"No data found for material ID: {material_id}")
        except Exception as e:
            print(f"Error fetching data for material ID {material_id}: {e}")
import argparse
from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import write
import os
import sys

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Download structures from the Materials Project by material IDs and save as .traj files.")
parser.add_argument('ids', nargs='+', help="Material IDs to download")
args = parser.parse_args()

# Your API key for the Materials Project
API_KEY = os.getenv('MAPI_KEY')
if not API_KEY:
    sys.exit("Error: MAPI_KEY environment variable not set.")

# Create AseAtomsAdaptor instance
adaptor = AseAtomsAdaptor()

with MPRester(API_KEY) as mpr:
    for i in args.ids:
        id = f'mp-{i}'
        try:
            material_data = mpr.get_structure_by_material_id(f'{id}')
            if material_data:
                atoms = adaptor.get_atoms(material_data)
                filename = os.path.join("./", f'{id}.cif')
                write(filename, atoms)
                print(f"Saved {id}.cif")
            else:
                print(f"No data found for material ID: {id}")
        except Exception as e:
            print(f"Error fetching data for material ID {id}: {e}")
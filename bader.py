import subprocess
import os
from ase import io
import glob
import numpy as np

# Define the dictionary for reference charges of each element
chargedict = {
    'Pt': 10, 'Ce': 12, 'W': 6, 'Sm': 11, 'Ti': 4, 'V': 5, 'Cr': 6, 'Mn': 7,
    'Fe': 8, 'Co': 9, 'Ni': 10, 'Cu': 11, 'Zn': 12, 'Ga': 3, 'Ge': 4, 'As': 5,
    'Zr': 12, 'Nb': 11, 'Mo': 14, 'Tc': 7, 'Ru': 8, 'Rh': 9, 'Pd': 10, 'Ag': 11,
    'Cd': 12, 'In': 3, 'Sn': 4, 'Sb': 5, 'Ir': 9, 'Al': 3, 'Au': 11, 'S': 6,
    'O': 6, 'N': 5, 'C': 4, 'P': 5, 'B': 3, 'Na': 1, 'K': 7, 'Li': 1, 'Cl': 7,
    'Y': 11, 'Bi': 5, 'La': 11, 'H': 1
}

def get_bader_charges(traj='OUTCAR'):
    # Check for the existence and non-emptiness of CHGCAR
    if not os.path.exists('CHGCAR') or os.path.getsize('CHGCAR') == 0:
        quit('ERROR: No or empty CHGCAR present')

    # Run Bader analysis
    if os.path.exists('AECCAR0'):
        subprocess.call('/global/homes/j/jiuy97/bin/vtstscripts/chgsum.pl AECCAR0 AECCAR2', shell=True)
        subprocess.call('bader CHGCAR -ref CHGCAR_sum', shell=True)
    elif not os.path.exists('AECCAR0'):
        print("AECCAR0 does not exist")
        subprocess.call('bader CHGCAR', shell=True)
    else:
        print(homebin+'/{}/ -> does not exist'.format(vtst))
    print('# Run Bader analysis')
    
    # Read charge data from ACF.dat
    with open("ACF.dat", "r") as file:
        lines = file.readlines()[4:]  # Skip the first 4 lines
    print('# Read charge data from ACF.dat')

    # Extract charge information
    charge_data = np.array([list(map(float, line.split())) for line in lines])
    charge = charge_data[:, 4]
    print('# Extract charge information')

    # Read atom names and positions from the trajectory file
    atoms = io.read(traj)
    atom_names = [atom.symbol for atom in atoms]
    print('# Read atom names and positions from the trajectory file')

    # Remove unnecessary lines from the trajectory file
    filelist = glob.glob('*.xyz')
    xyzfile = filelist[0]
    with open(xyzfile, "r") as file:
        lines = file.readlines()[2:]
    print('# Remove unnecessary lines from the trajectory file')

    # Extract atom names from the trajectory file
    atom_names_traj = [line.split()[0] for line in lines]
    print('# Extract atom names from the trajectory file')

    # Write Bader charges to a TSV file
    outfilename = 'bader_charges.tsv'
    with open(outfilename, 'w') as f:
        f.write("# index\t name\t charge\n")
        for i, (name_i, charge_i) in enumerate(zip(atom_names_traj, charge)):
            net_charge = -(charge_i - chargedict.get(name_i, 0))
            net_charge_round = round(net_charge, 2)
            print(net_charge_round)
            f.write("%d\t %s\t %f\n" % (i, name_i, net_charge))
            print('index: ' + str(i) + ' name: ' + name_i + ' charge: ' + str(net_charge))
    print('Bader charges written to {}'.format(outfilename))

    return [round(charge_i, 2) for charge_i in charge]

if __name__ == '__main__':
    print('Argument List:', str(sys.argv))
    traj = 'OUTCAR'
    Len = len(sys.argv)
    if Len > 1:
        for i in range(1, Len):
            if sys.argv[i] == "-t":
                traj = sys.argv[i+1]

    atoms_charge = get_bader_charges(traj)
    write_charge_traj = True
    if write_charge_traj:
        atoms = io.read(traj)
        atoms.set_initial_charges(atoms_charge)
        io.write('atoms_bader_charge.json', atoms)

    print('DONE with BADER')
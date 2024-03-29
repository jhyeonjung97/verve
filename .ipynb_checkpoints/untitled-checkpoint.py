
def get_bader_charges(traj='OUTCAR'):
    # Check for the existence and non-emptiness of CHGCAR
    if not os.path.exists('CHGCAR') or os.path.getsize('CHGCAR') == 0:
        quit('ERROR: No or empty CHGCAR present')

    # Run Bader analysis
    if os.path.exists('AECCAR0'):
        subprocess.call('/global/homes/j/jiuy97/bin/vtstscripts/chgsum.pl AECCAR0 AECCAR2', shell=True)
        subprocess.call('bader CHGCAR -ref CHGCAR_sum', shell=True)
    else:
        print("AECCAR0 does not exist")
        subprocess.call('bader CHGCAR', shell=True)
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
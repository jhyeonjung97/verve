# prints out excess charge associated with each atom

from ase.io import read, write
import numpy as np
import os
import subprocess
import sys
import glob

home=os.path.expanduser('~')
homebin=home+'/bin'

def zvals_from_outcar(path='OUTCAR'):
    """{symbol: ZVAL} as the run itself used them, read from OUTCAR.

    Bader gives the number of electrons on an atom; turning that into a net charge
    needs the valence count of the POTCAR that was actually used, and that is a
    property of the run, not of the element.  A hardcoded table cannot know which
    variant was chosen -- plain Sn is 4 while Sn_d is 14, and this file assumed the
    _d ones for Sn and Pb while the runs used plain, putting every Sn and Pb charge
    off by 10 e.  Ti/Hf/Mo/W are the same trap in the other direction (plain 4/4/6/6
    vs _pv 10/10/12/12).

    OUTCAR lists, per POTCAR block, a VRHFIN line naming the element and a ZVAL line
    giving its valence count, in the same order, so the two can be zipped.
    Returns {} when OUTCAR is missing or unparsable, and the caller falls back.
    """
    import re
    if not os.path.exists(path):
        return {}
    try:
        with open(path, errors='ignore') as fh:
            txt = fh.read(400000)          # the POTCAR blocks are all in the header
        syms = re.findall(r'VRHFIN\s*=\s*([A-Za-z]+)\s*:', txt)
        zs = [float(x) for x in re.findall(r'ZVAL\s*=\s*([\d.]+)\s+mass', txt)]
    except Exception:
        return {}
    if not syms or len(syms) != len(zs):
        return {}
    out = {}
    for sym, z in zip(syms, zs):
        if sym in out and out[sym] != z:    # same element with two POTCARs: refuse to guess
            return {}
        out[sym] = z
    return out


def get_bader_charges(traj):
    # Check for the existence and non-emptiness of CHGCAR
    if not os.path.exists('CHGCAR') or os.path.getsize('CHGCAR') == 0:
        quit('ERROR: No or empty CHGCAR present')

    # Run Bader analysis
    if os.path.exists('AECCAR0'):
        subprocess.call('~/bin/vtstscripts/chgsum.pl AECCAR0 AECCAR2', shell=True)
        subprocess.call('bader CHGCAR -ref CHGCAR_sum', shell=True)
    else:
        print("AECCAR0 does not exist")
        subprocess.call('bader CHGCAR', shell=True)
    print('# Run Bader analysis')
    
    file = open('ACF.dat', 'r')
    lines = file.readlines()
    file.close()
    for j in [1, 0, -4, -3, -2, -1]:
        del lines[j]
        
    newlines = []
    for line in lines:
        newline = map(float,line.split())
        newlines.append(list(newline))
        
    newlines = np.array(newlines)
    charge = newlines[:,4]
    
    # Try to read CONTCAR first, if not available try OUTCAR
    if os.path.exists('CONTCAR'):
        atoms = read('CONTCAR')
    elif os.path.exists('POSCAR'):
        atoms = read('POSCAR')
    else:
        try:
            atoms = read(traj)
        except Exception as e:
            print(f"Error reading {traj}: {str(e)}")
            print("Please make sure CONTCAR, POSCAR, or a valid OUTCAR exists.")
            sys.exit(1)
    
    write('qn.xyz',atoms)
    
    filelist = glob.glob('*.xyz')
    xyzfile = filelist[0]
    file = open(xyzfile,"r")
    lines = file.readlines()
    file.close()
    for j in [1, 0]:
        del lines[j]
        
    del newlines
    newlines = []
    for line in lines:
        newline =line.split()
        newlines.append(newline)
        
    newarray = np.array(newlines)
    name = newarray[:,0]
    
    # Define the dictionary for reference charges of each element
    chargedict = {'Ca': 10, 'Sr': 10, 'Ba': 10,
                'Sc': 11, 'Ti': 4, 'V': 5, 'Cr': 6, 'Mn': 7, 'Fe': 8,
                'Co': 9, 'Ni': 10, 'Cu': 11, 'Zn': 12, 'Ga': 13, 'Ge': 14,
                'Y': 11, 'Zr': 12, 'Nb': 11, 'Mo': 6, 'Tc': 7, 'Ru': 8,
                'Rh': 9, 'Pd': 10, 'Ag': 11, 'Cd': 12, 'In': 13, 'Sn': 14,
                'La': 11, 'Hf': 4, 'Ta': 5, 'W': 6, 'Re': 7, 'Os': 8,
                'Ir': 9, 'Pt': 10, 'Au': 11, 'Hg': 12, 'Tl': 13, 'Pb': 14,
                'S': 6, 'O': 6, 'N': 5, 'C': 4, 'P': 5, 'B': 3, 
                'Li': 3, 'Na': 7, 'K': 9, 'Rb': 9, 'Cs': 9, 'Cl': 7, 'Bi': 5, 'H': 1}
    
    # ZVAL from the run itself wherever OUTCAR is readable; the table above is only a
    # fallback.  Any disagreement is printed rather than silently preferred, because a
    # wrong valence count shifts every charge of that element by a whole electron or ten.
    zval = dict(chargedict)
    from_outcar = zvals_from_outcar()
    for sym, z in from_outcar.items():
        if sym in chargedict and abs(chargedict[sym] - z) > 1e-6:
            print(f'# ZVAL {sym}: OUTCAR says {z:g}, table said {chargedict[sym]:g}'
                  f' -- using OUTCAR')
        zval[sym] = z
    if not from_outcar:
        print('# WARNING: could not read ZVAL from OUTCAR, falling back to the table')

    write_charge=[]
    outfilename = 'bader_charges.tsv'
    with open(outfilename, 'w') as f:
        f.write("# index\t name\t charge\n")
        for i in range(0,len(charge)):
            name_i = name[i]
            index = i
            charge_i = charge[i]
            netcharge = -(charge_i-zval[name_i])
            netcharge_round = round(netcharge,2)
            print (netcharge_round)
            f.write("%d\t %s\t %f\n" % (index, name_i, netcharge))
            write_charge.append(netcharge_round)
            print('index: '+str(index)+' name: '+name_i+' charge: '+str(netcharge))
    f.close()
    
    return write_charge

if __name__ == '__main__':
	print ('Argument List:', str(sys.argv))
	traj='OUTCAR'
	Len = len(sys.argv)
	if Len > 1:
		for i in range(1,Len): 
			if sys.argv[i] == "-t":
				traj = sys.argv[i+1]

	atoms_charge=get_bader_charges(traj)
	write_charge_traj=True
	if write_charge_traj:
		# Try to read CONTCAR first, if not available try OUTCAR
		if os.path.exists('CONTCAR'):
			atoms = read('CONTCAR')
		elif os.path.exists('POSCAR'):
			atoms = read('POSCAR')
		else:
			try:
				atoms = read(traj)
			except Exception as e:
				print(f"Error reading {traj}: {str(e)}")
				print("Please make sure CONTCAR, POSCAR, or a valid OUTCAR exists.")
				sys.exit(1)
		
		atoms.set_initial_charges(atoms_charge)
		write('atoms_bader_charge.json',atoms)

print('DONE with BADER')
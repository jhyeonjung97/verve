# prints out excess charge associated with each atom

from ase.io import read, write
import numpy as np
import os
import subprocess
import sys
import glob

home=os.path.expanduser('~')
homebin=home+'/bin'

def get_bader_charges(traj):
    # Check for the existence and non-emptiness of CHGCAR
    if not os.path.exists('CHGCAR') or os.path.getsize('CHGCAR') == 0:
        quit('ERROR: No or empty CHGCAR present')

    # Run Bader analysis
    if os.path.exists('AECCAR0'):
        subprocess.call('/global/homes/j/jiuy97/bin/vtstscripts/chgsum.pl AECCAR0 AECCAR2',
                        shell=True)
        subprocess.call('bader CHGCAR -ref CHGCAR_sum', shell=True)
    else:
        print("AECCAR0 does not exist")
        subprocess.call('bader CHGCAR', shell=True)
    print('# Run Bader analysis')

	file = open("ACF.dat", "r")
	lines = file.readlines() # This is what you forgot
	file.close()
	for j in [1, 0, -4,-3, -2, -1]:
		del lines[j]

	newlines = []
	for line in lines:
		newline = map(float,line.split())
		newlines.append(list(newline))

	newlines = np.array(newlines)
	#print ((newlines[:,4]))
	charge = newlines[:,4]

	#atoms=io.read('OUTCAR')
	atoms=read(traj)
	write('qn.xyz',atoms)

	# get xyz file  
	filelist = glob.glob('*.xyz')
	xyzfile = filelist[0]		
	file = open(xyzfile,"r")
	lines = file.readlines() # This is what you forgot
	file.close()
	for j in [1, 0]:
		del lines[j]
	

	del newlines
	newlines = []
	for line in lines:
		newline =line.split() # map(float,line.split())
		newlines.append(newline)

	newarray = np.array(newlines)
	name = newarray[:,0]

	# Define the dictionary for reference charges of each element
    chargedict = {
        'Pt': 10, 'Ce': 12, 'W': 6, 'Sm': 11, 'Ti': 4, 'V': 5, 'Cr': 6, 'Mn': 7,
        'Fe': 8, 'Co': 9, 'Ni': 10, 'Cu': 11, 'Zn': 12, 'Ga': 3, 'Ge': 4, 'As': 5,
        'Zr': 12, 'Nb': 11, 'Mo': 14, 'Tc': 7, 'Ru': 8, 'Rh': 9, 'Pd': 10, 'Ag': 11,
        'Cd': 12, 'In': 3, 'Sn': 4, 'Sb': 5, 'Ir': 9, 'Al': 3, 'Au': 11, 'S': 6,
        'O': 6, 'N': 5, 'C': 4, 'P': 5, 'B': 3, 'Na': 1, 'K': 7, 'Li': 1, 'Cl': 7,
        'Y': 11, 'Bi': 5, 'La': 11, 'H': 1}

	write_charge=[]
	outfilename = 'bader_charges.tsv'
	with open(outfilename, 'w') as f:
		f.write("# index\t name\t charge\n")
		for i in range(0,len(charge)):
			name_i = name[i]
			index = i	
			charge_i=charge[i]
			netcharge=-(charge_i-chargedict[name_i])
			netcharge_round=round(netcharge,2)
			print (netcharge_round)
			f.write("%d\t %s\t %f\n" % (index, name_i, netcharge))
			write_charge.append(netcharge_round)
			print ('index: '+str(index)+' name: '+name_i+' charge: '+str(netcharge))
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
		atoms=read(traj)
		#atoms_charge.set_initial_magnetic_moments(write_charge)
		atoms.set_initial_charges(atoms_charge)
		write('atoms_bader_charge.json',atoms)

print ('DONE with BADER')
exit 0
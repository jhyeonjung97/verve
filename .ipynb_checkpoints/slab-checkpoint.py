import os
import glob
import argparse
from ase.io import read, write
from ase.build import surface
from ase.build.tools import sort
from ase.constraints import FixAtoms
from ase.io.vasp import read_vasp_xdatcar, write_vasp_xdatcar

parser = argparse.ArgumentParser(description='Command-line options example')
parser.add_argument('filename', type=str, default='', help='input filename (e.g., a for a1~a3.vasp, OR you can type POSCAR, CONTCAR, XDATCAR)')
parser.add_argument('-t', '--type', type=str, default='vasp')
parser.add_argument('-a', '--add', type=float, default=0)
parser.add_argument('-z', '--height', type=float, default=None)
parser.add_argument('-f', '--fix', action='store_true', default=False)
parser.add_argument('-s', '--sort', action='store_true', default=False)
parser.add_argument('-w', '--wrap', action='store_true', default=False)
parser.add_argument('-c', '--center', action='store_true', default=False)
parser.add_argument('--facet', type=str, default=None)
parser.add_argument('-l', '--layers', type=int, default=1)
parser.add_argument('-v', '--vacuum', type=float, default=None)
parser.add_argument('-r', '--repeat', type=str, default=None)

args = parser.parse_args()
filename = args.filename
type = args.type

add = args.add
height = args.height
vacuum = args.vacuum

facet = args.facet
repeat = args.repeat

pattern = os.path.join('./', f'{filename}*.{type}')
matching_files = glob.glob(pattern)
for file in matching_files:
    atoms = read(f'{file}')
    # l = atoms.cell.lengths()[2]
    # atoms.positions += (0, 0, -l/4)
    if facet:
        x, y, z = map(int, facet.split(','))
        atoms = surface(lattice=atoms, indices=(x,y,z), layers=args.layers)
    if repeat:
        a, b, c = map(int, repeat.split(','))
        atoms = atoms.repeat((a,b,c))
    if args.wrap:
        atoms.wrap()
    if add:
        l1 = atoms.cell.lengths()[0]
        l2 = atoms.cell.lengths()[1]
        l3 = atoms.cell.lengths()[2]
        a1 = atoms.cell.angles()[0]
        a2 = atoms.cell.angles()[1]
        a3 = atoms.cell.angles()[2]
        atoms.cell = (l1, l2, l3+add, a1, a2, a3)
    if vacuum:
        min_z = atoms.positions[:,2].min()
        max_z = atoms.positions[:,2].max()
        height = max_z - min_z + vacuum
    if height:
        l1 = atoms.cell.lengths()[0]
        l2 = atoms.cell.lengths()[1]
        # l3 = atoms.cell.lengths()[2]
        a1 = atoms.cell.angles()[0]
        a2 = atoms.cell.angles()[1]
        a3 = atoms.cell.angles()[2]
        atoms.cell = (l1, l2, height, a1, a2, a3)
    if args.fix:
        min_z = atoms.positions[:,2].min()
        max_z = atoms.positions[:,2].max()
        mid_z = (min_z + max_z) / 3
        print(mid_z)
        fixed = FixAtoms(indices=[atom.index for atom in atoms if atom.position[2] < mid_z])
        atoms.set_constraint(fixed)
    if args.center:
        atoms.center()
    if args.sort:
        atoms = sort(atoms)
    write(f'{file}',atoms)
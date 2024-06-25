from mendeleev import element
import pandas as pd

elements_3d = ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
elements_4d = ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn']
elements_5d = ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']

for e in elements_3d:
    elem = element(e)  # Avoid variable shadowing
    for radius in elem.ionic_radii:
        if radius.most_reliable:
            print(radius)

for e in elements_4d:
    elem = element(e)  # Avoid variable shadowing
    for radius in elem.ionic_radii:
        if radius.most_reliable:
            print(radius)

for e in elements_5d:
    elem = element(e)  # Avoid variable shadowing
    for radius in elem.ionic_radii:
        if radius.most_reliable:
            print(radius)
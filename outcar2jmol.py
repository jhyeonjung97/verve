#!/usr/bin/env python3
import sys
import re

# usage 
# python outcar2jmol.py POSCAR OUTCAR vibrations.jmol

def read_poscar_symbols(poscar_path):
    """
    Read element symbols and counts from a VASP5 POSCAR.
    Returns a list of element symbols, one per atom, in order.
    """
    with open(poscar_path, "r") as f:
        lines = [l.rstrip() for l in f if l.strip()]

    # VASP5 POSCAR:
    # 1: comment
    # 2: scale
    # 3-5: lattice vectors
    # 6: element symbols
    # 7: element counts
    symbols_line = lines[5].split()
    counts_line = list(map(int, lines[6].split()))

    elements = []
    for sym, n in zip(symbols_line, counts_line):
        elements.extend([sym] * n)

    return elements

def parse_outcar_modes(outcar_path, natoms):
    """
    Parse phonon modes from OUTCAR 'Eigenvectors and eigenvalues of the dynamical matrix' section.
    Returns a list of dicts:
      {
        "index": int,
        "freq_thz": float,
        "freq_cm1": float,
        "atoms": [(x,y,z,dx,dy,dz), ...]  # length natoms
      }
    """
    with open(outcar_path, "r") as f:
        lines = f.readlines()

    modes = []
    i = 0
    #mode_header_re = re.compile(r"\s*(\d+)\s+f\s*=\s*([0-9Ee\+\-\.]+)\s*THz.*([0-9Ee\+\-\.]+)\s*cm-1")
    mode_header_re = re.compile(r"^\s*(\d+)\s+f(?:/i)?\s*=\s*([0-9Ee+\-\.]+)\s*THz.*?([0-9Ee+\-\.]+)\s*cm-1")
 
    while i < len(lines):
        line = lines[i]

        m = mode_header_re.match(line)
        if m:
            mode_index = int(m.group(1))
            freq_thz = float(m.group(2))
            freq_cm1 = float(m.group(3))
            #print(m.group(0), type(m.group(0)))
            #print(m.group(2)),
            #print(m.group(3))
            #print(int(m.group(1)))
            #print(float(m.group(4)))
            #print(float(m.group(6)))
            # Next line should be header 'X Y Z dx dy dz'
            i += 1
            if i < len(lines) and "dx" in lines[i] and "dy" in lines[i] and "dz" in lines[i]:
                i += 1  # move to first atom line

            atoms = []
            for _ in range(natoms):
                if i >= len(lines):
                    raise ValueError("Unexpected end of file while reading mode %d" % mode_index)
                parts = lines[i].split()
                if len(parts) < 6:
                    raise ValueError("Bad atom line in OUTCAR near mode %d: %s" % (mode_index, lines[i]))
                x, y, z = map(float, parts[0:3])
                dx, dy, dz = map(float, parts[3:6])
                atoms.append((x, y, z, dx, dy, dz))
                i += 1

            modes.append({
                "index": mode_index,
                "freq_thz": freq_thz,
                "freq_cm1": freq_cm1,
                "atoms": atoms
            })
        else:
            i += 1

    return modes

def write_jmol_vibxyz(out_path, elements, modes, scale=1.0):
    """
    Write modes in Jmol's VibXYZ format.
    Each mode becomes a separate model:
      N
      vibration <index> <freq_cm-1> cm-1
      El x y z dx dy dz
    `scale` scales the displacement vectors for visualization.
    """
    natoms = len(elements)
    with open(out_path, "w") as out:
        for mode in modes:
            out.write(f"{natoms}\n")
            out.write(f"vibration {mode['index']} {mode['freq_cm1']:.6f} cm-1\n")
            for elem, (x, y, z, dx, dy, dz) in zip(elements, mode["atoms"]):
                out.write(
                    f"{elem:2s} "
                    f"{x: .8f} {y: .8f} {z: .8f} "
                    f"{dx*scale: .8f} {dy*scale: .8f} {dz*scale: .8f}\n"
                )

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python outcar2jmol.py POSCAR OUTCAR vibrations.jmol")
        sys.exit(1)

    poscar_path = sys.argv[1]
    outcar_path = sys.argv[2]
    out_path = sys.argv[3]

    elements = read_poscar_symbols(poscar_path)
    natoms = len(elements)

    print(f"Found {natoms} atoms from POSCAR.")
    modes = parse_outcar_modes(outcar_path, natoms)
    print(f"Parsed {len(modes)} vibrational modes from OUTCAR.")

    # You can change scale if the displacements look too small/large in Jmol
    write_jmol_vibxyz(out_path, elements, modes, scale=1.0)
    print(f"Wrote Jmol vibration file: {out_path}")



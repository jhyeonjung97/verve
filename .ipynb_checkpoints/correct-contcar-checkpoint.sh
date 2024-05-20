first_line=$(sed -n '6p' POSCAR)
sed -i "6s/.*/$first_line/" CONTCAR
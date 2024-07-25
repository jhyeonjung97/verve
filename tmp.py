python ~/bin/verve/lr.py -o Ef_rel \
--Y concat_norm_formation_rel.tsv \
-i \
ICOHP_per_metal \
ICOHP_per_bond \
ICOBI_per_metal \
ICOBI_per_bond \
MadelungL \
GrossPopulationL \
bond \
volume \
chg \
mag \
atomic_number \
group_id \
mass \
atomic_volume \
redoxP \
ionenergies1 \
ionenergies2 \
ionenergies12 \
ionenergies3 \
dipole_polarizability \
en_pauling \
density \
covalent_radius \
metallic_radius \
vdw_radius \
melting_point \
boiling_point \
evaporation_heat \
fusion_heat \
sublimation_heat \
heat_of_formation \
--X \
concat_ICOHP_rel.tsv \
concat_norm_ICOHP_rel.tsv \
concat_ICOBI_rel.tsv \
concat_norm_ICOBI_rel.tsv \
concat_norm_MadelungL_rel.tsv \
concat_GrossPopulationL_rel.tsv \
concat_bond_rel.tsv \
concat_norm_volume_rel.tsv \
concat_chg_rel.tsv \
concat_mag_rel.tsv \
concat_atomic_number.tsv \
concat_group_id.tsv \
concat_mass.tsv \
concat_atomic_volume.tsv \
concat_redoxP.tsv \
concat_ionenergies_1.tsv \
concat_ionenergies_2.tsv \
concat_ionenergies_12.tsv \
concat_ionenergies_3.tsv \
concat_dipole_polarizability.tsv \
concat_en_pauling.tsv \
concat_density.tsv \
concat_covalent_radius.tsv \
concat_metallic_radius.tsv \
concat_vdw_radius.tsv \
concat_melting_point.tsv \
concat_boiling_point.tsv \
concat_evaporation_heat.tsv \
concat_fusion_heat.tsv \
concat_sublimation_heat.tsv \
concat_heat_of_formation.tsv

# python ~/bin/verve/gpr.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
# python ~/bin/verve/gpr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv

# python ~/bin/verve/gpr.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
# python ~/bin/verve/gpr-optuna.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv

# python ~/bin/verve/gbr.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
# python ~/bin/verve/gbr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 

# python ~/bin/verve/gbr.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 
# python ~/bin/verve/gbr-optuna.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv  

# python ~/bin/verve/nn-hyperopt.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 

# python ~/bin/verve/nn-hyperopt.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 

# python ~/bin/verve/gbr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv  

# python ~/bin/verve/nn-hyperopt.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 


# python ~/bin/verve/gbr-optuna.py -i ICOHP_per_bond ICOHP_per_MO ICOBI MadelungL GrossPopulationL volume bond chg atomic_number group_id row mass atomic_volume ionenergies1 ionenergies2 ionenergies12 ionenergies3 dipole_polarizability en_pauling density covalent_radius metallic_radius vdw_radius melting_point boiling_point heat_of_formation sublimation_heat evaporation_heat fusion_heat --Y concat_norm_formation_rel.tsv --X concat_ICOHP_per_bond.tsv concat_ICOHP_per_MO.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_GrossPoluationL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_atomic_number.tsv concat_group_id.tsv concat_row.tsv concat_mass.tsv concat_atomic_volume.tsv concat_ionenergies_1.tsv concat_ionenergies_2.tsv concat_ionenergies_12.tsv concat_ionenergies_3.tsv concat_dipole_polarizability.tsv concat_en_pauling.tsv concat_density.tsv concat_covalent_radius.tsv concat_metallic_radius.tsv concat_vdw_radius.tsv concat_melting_point.tsv concat_boiling_point.tsv concat_heat_of_formation.tsv concat_sublimation.tsv concat_evaporation_heat.tsv concat_fusion_heat.tsv
    
# python ~/bin/verve/nn-hyperopt.py -i ICOHP_per_bond ICOHP_per_MO ICOBI MadelungL GrossPopulationL volume bond chg atomic_number group_id row mass atomic_volume ionenergies1 ionenergies2 ionenergies12 ionenergies3 dipole_polarizability en_pauling density covalent_radius metallic_radius vdw_radius melting_point boiling_point heat_of_formation sublimation_heat evaporation_heat fusion_heat --Y concat_norm_formation_rel.tsv --X concat_ICOHP_per_bond.tsv concat_ICOHP_per_MO.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_GrossPoluationL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_atomic_number.tsv concat_group_id.tsv concat_row.tsv concat_mass.tsv concat_atomic_volume.tsv concat_ionenergies_1.tsv concat_ionenergies_2.tsv concat_ionenergies_12.tsv concat_ionenergies_3.tsv concat_dipole_polarizability.tsv concat_en_pauling.tsv concat_density.tsv concat_covalent_radius.tsv concat_metallic_radius.tsv concat_vdw_radius.tsv concat_melting_point.tsv concat_boiling_point.tsv concat_heat_of_formation.tsv concat_sublimation.tsv concat_evaporation_heat.tsv concat_fusion_heat.tsv
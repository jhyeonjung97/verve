python ~/bin/verve/sumup.py \
-x energy_norm_ICOHP.tsv \
-y energy_norm_TOTEN.tsv \
--xlabel ICOHP \
--ylabel TOTEN

python ~/bin/verve/sumup.py \
-x energy_norm_Madelung_Loewdin.tsv \
-y energy_norm_TOTEN.tsv \
--xlabel MadelungL \
--ylabel TOTEN

python ~/bin/verve/sumup.py \
-x energy_norm_ICOHP.tsv energy_norm_Madelung_Loewdin.tsv \
-y energy_norm_TOTEN.tsv \
--xlabel ICOHP+MadelungL \
--ylabel TOTEN
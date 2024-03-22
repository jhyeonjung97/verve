import numpy as np
import pandas as pd
from scipy.stats import linregress
from matplotlib import pyplot as plt
from collections import defaultdict
from mendeleev import element
import matplotlib
import os
import json
import time
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from cathub.cathubsql import CathubSQL

read = False #True

db_file = 'ComerGeneralized2024.db' #sys.argv[1]
db = CathubSQL(filename=db_file)

dataframe_all = db.get_dataframe()#pub_id='ComerGeneralized2023'
#dataframe_extra = db_extra.get_dataframe()

metal_rows = {
    '3d': ['Sc', 'Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge'],
    '4d': ['Y', 'Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn'],
    '5d': ['La', 'Hf', 'Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb'],
    }

chemical_comps = {'2_100' : ['10O10'],
                  '3_012': ['12O18'],
                  '4_110': ['8O16'],
                  '4_100': ['6O12'],
                  '5_18': ['8O18'],
                  '5_19': ['8O19'],
                  '6_001': ['4O12', '16O5', '16O48']}

reconstructed = [('W', 3),
                 ('Os', 3),
                 ('Sc', 2),
                 #('Ni', 2)
                 ]

def get_adsorption_energy(metal, oxidation_state, adsorbate, facet=None):
    t1 = time.time()
    os_facet_match = {2:'100', 3:'012', 4:'110', 5:'18'}
    # oxidation_state == 3 and metal in ['Os', 'Nb', 'Cr', 'W', 'Mo']:
    #    dataframe = dataframe_extra
    #else:
    dataframe = dataframe_all
    if facet is None:
        facet = os_facet_match[oxidation_state]

    key = '{}_{}'.format(oxidation_state, facet)
    loc_c = 0
    for c in chemical_comps[key]:
        loc_c = loc_c | (dataframe['chemical_composition'].str.contains(metal+c))

    loc_O = (dataframe['equation'].str.contains('-> {}\*'.format('O'))) | \
        (dataframe['equation'].str.contains('-> 2.0{}\*'.format('O')))

    loc_O = loc_c & loc_O

    loc_OH = (dataframe['equation'].str.contains('-> {}\*'.format('OH'))) | \
        (dataframe['equation'].str.contains('-> 2.0{}\*'.format('OH')))
    loc_OH = loc_c & loc_OH

    #print(dataframe[loc_O][['reaction_id', 'chemical_composition', 'reaction_energy']])
    #return
    try:
        #if adsorbate == 'O-OH':
        #    adsO = dataframe[loc_O]['reaction_energy'][0] #dataframe_filter[]
        #    adsOH = dataframe[loc_OH]['reaction_energy'][0]
        #    return adsO - adsOH
        if adsorbate == 'O':
            adsO = dataframe[loc_O]['reaction_energy'].values[0]
            #if metal=='Ni' and oxidation_state == 2:
            #    adsO += 1.7490 * 2
            if metal=='Cu' and oxidation_state == 2:
                adsO = None
            #print(adsO)
            return adsO
        elif adsorbate == 'OH':
            adsOH = dataframe[loc_OH]['reaction_energy'].values[0]
            #if metal=='Ni' and oxidation_state == 2:
            #    adsOH += 1.7490 * 2
            if metal=='Cu' and oxidation_state == 2:
                adsOH = None
            #print(adsOH)
            return adsOH

            #return ads_data[metal][str(oxidation_state)][facet]['O'] - ads_data[metal][str(oxidation_state)][facet]['OH']
        #else:
        #    return ads_data[metal][str(oxidation_state)][facet][adsorbate]
    except:
        return None

def get_outer_electrons(atomic_symbol, oxidation_state):
    return int(element(atomic_symbol).group.group_id) - oxidation_state

systems = ['afm_rock_salt', 'corundum', 'rerun_new_version_rutile', 'A2O5', 'MO3']

d3 = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
d4 = ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn']
d5 = ['La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']

colors = {2:{'100':'#d62728'},
          3:{'012':'#ff7f0e'},
          4:{'110':'#2ca02c', '100': '#39d439'},
          5:{'19':'#279ff2', '18':'#1f77b4'},
          6:{'001':'#9467bd'}}

markers = {2:{'100':'s'},
           3:{'012':'d'},
           4:{'110':'o', '100':'p'},
           5:{'19':'>', '18':'<'},
           6:{'001':'D'}}

linestyle = {2:{'100':'-'},
            3:{'012':'-'},
            4:{'110':'-', '100':'--'},
            5:{'19':'-', '18':'--'},
            6:{'001':'-'}}

formula_dict = {2: 'MO',
                3: 'M$_2$O$_3$',
                4: 'MO$_2$',
                5: 'M$_2$O$_5$',
                6: 'MO$_3$'
                }

limit_dict = {'OH':1.95,
              'O':4.65}

font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 10}

matplotlib.rc('font', **font)
plt.rcParams["figure.figsize"] = (8,9)

facet_dict = {2:['100'], 3:['012'], 4:['110', '100'], 5:['18', '19'], 6:['001']}

facet_translation_dict = {'O': {'18':'(100) 0.5ML O', '19': '(100) 1.0ML O', '012':'(012) 0.5ML O',
                                '110':'(110) 1.0ML O','100':'(100) 1.0ML O',
                                '001': '(001) 1.0ML O'},
                          'OH': {'18':'(100) 0.5ML OH', '19': '(100) 0.5ML O 0.5ML OH', '012':'(012) 0.5ML OH',
                                 '110':'(110) 1.0ML OH','100':'(100) 1.0ML OH',
                                 '001': '(001) 1.0ML OH'}
                         }

ads_models = {}

fig1, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2)

axs = [ax1, ax3, ax5, ax2, ax4, ax6]

i = 0

if read:
    with open("ads_backup.json", "r") as outfile:
        all_data = json.load(outfile)
else:
    all_data = defaultdict(dict)
    all_data['O']= defaultdict(dict)
    all_data['OH'] = defaultdict(dict)

for ads in ['O', 'OH']:
    for row_name, row in zip(['3d', '4d', '5d'], [d3, d4, d5]):
        for system, oxidation_state in zip(systems[::-1],[2,3,4,5,6][::-1]):

            if row_name in ['5d'] and oxidation_state == 2:
                continue
            print(system, oxidation_state)
            t1 = time.time()
            for facet in facet_dict[oxidation_state]:
                #print(metal_symbol)
                if facet in facet_translation_dict[ads]: # not an amazing solution but it works
                    facet_ = facet_translation_dict[ads][facet]
                else:
                    facet_ = facet

                oxidation_states = []
                if not read:
                    if not str(oxidation_state) in all_data[ads][row_name]:
                        all_data[ads][row_name][str(oxidation_state)] = {}
                    if not str(facet) in all_data[ads][row_name][str(oxidation_state)]:
                        all_data[ads][row_name][str(oxidation_state)][str(facet)] = 0
                    adsorption_energies = []
                    groups = []
                    #outer_electrons = []

                    for j, metal_symbol in enumerate(row[::-1]):
                        oxidation_states.append(oxidation_state)

                        adsorption_energy = get_adsorption_energy(metal_symbol, oxidation_state, ads, facet=facet)
                        if oxidation_state == 2 and adsorption_energy is not None:
                            adsorption_energy /= 2
                        if adsorption_energy is None and oxidation_state == 2:
                            continue
                        adsorption_energies.append(adsorption_energy)
                        groups.append(int(element(metal_symbol).group.group_id))
                        #outer_electrons.append(get_outer_electrons(metal_symbol, oxidation_state))

                    all_data[ads][row_name][str(oxidation_state)][str(facet)] = [groups, adsorption_energies]
                x = all_data[ads][row_name][str(oxidation_state)][str(facet)][0]
                y = all_data[ads][row_name][str(oxidation_state)][str(facet)][1]

                #print(x,y)
                axs[i].plot(x, y,
                        linestyle='-',#linestyle[oxidation_state][facet],
                        linewidth=1,
                        color=colors[oxidation_state][facet],
                        marker=markers[oxidation_state][facet],
                        label='{} {}'.format(formula_dict[oxidation_state], facet_))


            t2 = time.time()
            print('time',t2-t1)

        if ads == 'O':
            axs[i].set_ylabel('$\Delta\mathrm{E_O}$(eV)',fontsize=11)
        else:
            axs[i].set_ylabel('$\Delta\mathrm{E_{OH}}$(eV)',fontsize=11)

        if i in[2,5]:
            axs[i].set_xlabel('Group Number', fontsize=11)
        else:
            axs[i].set_xticklabels([], fontsize=11)
        if i == 0 or i == 3:
            axs[i].legend(prop={'size': 7}, ncol=1)

        axs[i].text(0.05, 0.88, row_name + ' oxides', transform=axs[i].transAxes, fontsize=10)
        axs[i].set_xlim(float(element(row[0]).group.group_id) -1, float(element(row[-1]).group.group_id)+1)


        axs[i].set_xticks(list(range(element(row[0]).group.group_id, element(row[-1]).group.group_id+1)))

        axs[i].hlines(limit_dict[ads],
                     float(element(row[0]).group.group_id) -1, float(element(row[-1]).group.group_id)+1,
                     linestyles='dashed', color='k')

        if ads == 'O':
            axs[i].set_ylim(-3, 6.5)
            axs[i].set_yticks(range(-3,7))
        else:
            axs[i].set_ylim(-3, 3.25)
        if i == 0:
            axs[i].set_title('O adsorption')
        elif i == 3:
            axs[i].set_title('OH adsorption')


        axs[i].yaxis.set_minor_locator(MultipleLocator(0.2))
        par1 = axs[i].twiny()
        par1.set_xlim(float(element(row[0]).group.group_id) -1, float(element(row[-1]).group.group_id)+1)
        par1.set_xticks(list(range(element(row[0]).group.group_id, element(row[-1]).group.group_id+1)))
        par1.set_xticklabels(row)

        i += 1


plt.tight_layout()
plt.savefig('../Submission_ACS_Catalysis/Resubmission_no_1/Figures/Figure2.pdf')
plt.show()

import sys
import os
sys.path.append(os.getcwd())

from lobster_analysis import parse_list_file, get_normal_oxidation_states, predict_cohp, check_d_zero, get_outer_electrons, get_dos_center, predict_cohp_log, predict_cohp_kr

import numpy as np
import pandas as pd
from scipy.stats import linregress
from matplotlib import pyplot as plt
from collections import defaultdict
from mendeleev import element
import pickle
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, ElasticNetCV, ElasticNet
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import cross_validate
from sklearn.metrics import r2_score
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import SVR
from sklearn.feature_selection import SequentialFeatureSelector as SFS
from cathub.cathubsql import CathubSQL
import matplotlib
import json

nested_dict = lambda: defaultdict(nested_dict)

curdir = os.getcwd()

base_dir = os.getcwd() + '/../DFT_Data/bulk_data/'

saved_cohps_dict = nested_dict()
saved_bond_length_cohp_lists = nested_dict()

df = pd.DataFrame(columns=['Adsorption Energy', 'Bulk ICOHP', 'Oxidation State','Metal Symbol', 'Outer Electrons', 'Adsorbate', 'Bulk File'])


db_file = '../DFT_Data/surface_data/all_organized/ComerGeneralized2023.db'#sys.argv[1]
db = CathubSQL(filename=db_file)

db_file_extra = '../DFT_Data/surface_data/organized_redos/wintherorganized2022.db'#sys.argv[1]
db_extra = CathubSQL(filename=db_file_extra)

dataframe_all = db.get_dataframe()
dataframe_extra = db_extra.get_dataframe()
chemical_comps = {'2_100' : ['10O10'],
                  '3_012': ['12O18'],
                  '4_110': ['8O16'],
                  '4_100': ['6O12'],
                  '5_18': ['8O18'],
                  '5_19': ['8O19'],
                  '6_001': ['4O12', '16O5', '16O48']}


def get_adsorption_energy(metal, oxidation_state, adsorbate, facet=None):
    os_facet_match = {2:'100', 3:'012', 4:'110', 5:'18'}
    if oxidation_state == 3 and metal in ['Os', 'Nb', 'Cr', 'W', 'Mo']:
        dataframe = dataframe_extra
    else:
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
    if oxidation_state == 2:
        ads_factor = 2
    else:
        ads_factor = 1

    try:
        if adsorbate == 'O-OH':
            adsO = dataframe[loc_O]['reaction_energy'].values[0] #dataframe_filter[]
            adsOH = dataframe[loc_OH]['reaction_energy'].values[0]
            return (adsO - adsOH) / ads_factor
        if adsorbate == 'O':
            adsO = dataframe[loc_O]['reaction_energy'].values[0]
            #print(adsO)
            return adsO / ads_factor
        elif adsorbate == 'OH':
            adsOH = dataframe[loc_OH]['reaction_energy'].values[0]
            #print(adsOH)
            return adsOH / ads_factor

            #return ads_data[metal][str(oxidation_state)][facet]['O'] - ads_data[metal][str(oxidation_state)][facet]['OH']
        #else:
        #    return ads_data[metal][str(oxidation_state)][facet][adsorbate]
    except:
        return None



#df = pd.read_csv('all_data.csv', index_col=0)
#print(df['Adsorbate'])
#sys.exit()
#with open(base_dir+'gather_results/bulk_cohps.json') as f:
#    bulk_cohps = json.load(f)


#with open(base_dir+'gather_results/bond_length_and_cohp.json') as f:
#    bond_length_cohps = json.load(f)

#systems = ['corundum_recommended', 'rerun_new_version_rutile', 'A2O5_recommended', 'MO3', 'afm_rock_salt_3']
systems = ['+3', '+4', '+5', '+6', '+2']

outliers_remove = [#('Mo', 3),
                   ('W', 3),
                   ('Os', 3),
                   #('V', 3),
                   #('Ti', 2),
                   #('Hg', 4),
                   #('Co', 2),
                   #('Co', 3),
                   ('Sc', 2),
                   #('Pd', 4),
                   #('Fe', 2),
                   #('Co', 2)
                   ]
re_bond_dict = {3:{'012':0.833333}, 4:{'110':1,'100':0.666666}, 5:{'100':0.777777}}

d3 = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
d4 = ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn']
d5 = ['La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
#d3 = ['Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',]
#d4 = ['Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In']
#d5 = ['Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']

#ocd = {2:'#ffb6c0',3:'#fdcfa2',4:'#c7e9c0',5:'#add8e6',6:'#bcbddc'}
ocd = {2:'#e25154',3:'#fe9639',4:'#2ea12f',5:'#3f8abe',6:'#966abf'}

font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 9}

matplotlib.rc('font', **font)
plt.rcParams["figure.figsize"] = (4.3,6.46)

facet_dict = {2:['100'], 3:['012'], 4:['110', '100'], 5:['18', '19'], 6:['001']}
facet_surface_os_dict = {3:{'012':2.833}, 4:{'110':3.333, '100':4.0}, 5:{'18':4, '19':5.0}, 6:{'001':5}, 2:{'100':1.93}}

parameters_dict = defaultdict(dict)


def overpot(O_OH):
    #O_OH += 0.001 - 0.339
    return max([O_OH, 3.2-O_OH]) - 1.23

ads_models = {}

#fig1, (ax1, ax2, ax7) = plt.subplots(3, 1)
#fig2, (ax3, ax4, ax8) = plt.subplots(3, 1)
fig1, (ax1, ax4) = plt.subplots(2, 1)
fig2, (ax2, ax3) = plt.subplots(2, 1)
fig5, (ax7, ax8) = plt.subplots(2, 1)
fig3, (ax5, ax6) = plt.subplots(2, 1)
fig4 = plt.figure(figsize=(4.3, 3.4))
ax9 = fig4.add_axes([0.2,0.2,0.8,0.8])

for fg, ax, ax_, ads in zip([fig5, fig1, fig2],[ax7, ax1, ax2],[ax8, ax4, ax3], ['O-OH', 'O', 'OH']): #making several figures at once in this loop
    print(ads)
    all_ads = []
    all_normalized_cohp = []
    all_oxidation_state = []
    all_bond_lengths = []
    all_per_bond_icohps = []
    all_metals = []
    all_icohp = []
    all_plus_2_integrals = []
    all_outer_electrons = []
    all_directories = []
    all_psi = []
    all_en = []
    all_p_ints = []
    all_2p = []
    all_rows = []
    all_avg_cn = []
    all_rem_bond = []
    all_row = []
    all_surface_oxidation_states = []
    ranges = []


    for row_name, row in zip(['3d', '4d', '5d'], [d3, d4, d5]):
        print(row_name)
        #if row_name != '3d':
        #    continue
        for j, metal_symbol in enumerate(row[::-1]):
            print(metal_symbol)
        #    if metal_symbol in ['Zr']:
        #        continue
            fermi_integrals = []
            maxes = []
            oxidation_states = []
            bond_lengths = []
            adsorption_energies = []
            predict_total_integral = []
            adsorption_energy = []
            cleaned_ads = []
            plus_2_integrals = []
            outer_electrons = []
            normal_oxi_states = get_normal_oxidation_states(metal_symbol)
            for system, oxidation_state in zip(systems,[3,4,5,6,2]):
                for facet in facet_dict[oxidation_state]:
                    os.chdir(base_dir + system)

                    dire = [a for a in os.listdir('.') if metal_symbol in a]
                    if dire == []:
                        continue
                    dire = [a for a in dire if len(a.split('_')) < 3][0]
                    if not os.path.isfile(dire+ '/no_sym/ICOHPLIST.lobster'):
                        print(metal_symbol, system)
                        continue
                    print(dire + '/no_sym/ICOHPLIST.lobster')
                    total_integral, bond_length = parse_list_file(dire+ '/no_sym/ICOHPLIST.lobster', return_avg_bond_len=True)
                    bond_order_integral, bo_bond_length = parse_list_file(dire+ '/no_sym/ICOBILIST.lobster', return_avg_bond_len=True)
                    p_total_integral, p_bond_length = parse_list_file(dire+ '/no_sym/ICOHPLIST.lobster',
                                                  return_avg_bond_len=True, orbital_interaction='valence_p')
                    #O2p_center = get_dos_center(dire+ '/no_sym/dos_data.json', bound_eng=3)
                    #print(total_integral, bond_length)
                    O2p_center = 0
                    #total_integral += p_total_integral
                    #print(metal_symbol, get_outer_electrons(metal_symbol, oxidation_state), p_total_integral)
                    saved_bond_length_cohp_lists[metal_symbol][oxidation_state]= bond_length
                    saved_cohps_dict[metal_symbol][oxidation_state] = total_integral

                    fermi_integrals.append(total_integral)
                    predicted_per_bond = [predict_cohp(metal_symbol,a[0]) for a in bond_length]
                    #predicted_per_bond = [None]
                    #print(predicted_per_bond, [a[1] for a in  bond_length])
                    if None not in predicted_per_bond:
                        predict_total_integral.append(sum(predicted_per_bond))
                    else:
                        predict_total_integral.append(None)
                    oxidation_states.append(oxidation_state)
                    adsorption_energy = get_adsorption_energy(metal_symbol, oxidation_state, ads, facet=facet)
                    #print(oxidation_state, adsorption_energy)
                    #if ads == 'O-OH' and adsorption_energy is not None:
                    #    adsorption_energy += 0.001 - 0.339
                        #adsorption_energy -= 0.22232967836120565
                    #if adsorption_energy == None and oxidation_state != 6:
                    #    print(metal_symbol, oxidation_state, ads)
                    bond_lengths += bond_length
                    adsorption_energies.append(adsorption_energy)
                    if adsorption_energy is not None:# and \ #not check_d_zero(metal_symbol, oxidation_state) and \
                            #(metal_symbol, oxidation_state) not in outliers_remove:
                        cleaned_ads.append(adsorption_energy)
                        #plt.text(total_integral / oxidation_state, adsorption_energy, metal_symbol)
                        all_rows.append(int(row_name[0]))
                        all_ads.append(adsorption_energy)
                        all_normalized_cohp.append(total_integral / oxidation_state / 6)
                        all_oxidation_state.append(oxidation_state)
                        all_bond_lengths.append([a[0] for a in bond_length])
                        all_per_bond_icohps.append([a[1] for a in bond_length])
                        all_metals.append(metal_symbol)
                        all_icohp.append(total_integral)
                        all_row.append(row_name)
                        all_p_ints.append(p_total_integral/oxidation_state)
                        all_avg_cn.append(12/oxidation_state)
                        #all_plus_2_integrals.append(plus_2_total_integral)
                        all_2p.append(O2p_center)
                        all_outer_electrons.append(get_outer_electrons(metal_symbol, oxidation_state))
                        all_surface_oxidation_states.append(facet_surface_os_dict[oxidation_state][facet])
                        all_directories.append(base_dir+system +'/'+dire+ '/no_sym/ICOHPLIST.lobster')
                        #all_rem_bond.append(re_bond_dict[oxidation_state][facet])
                        num = (get_outer_electrons(metal_symbol, oxidation_state) * 6**4) ** (2/5)
                        denom = (element(metal_symbol).en_pauling*element('O').en_pauling**4) ** (1/5)
                        if metal_symbol in ['Au', 'Ag']:
                            #psi = get_outer_electrons(metal_symbol, oxidation_state) ** 2/element(metal_symbol).en_pauling ** 0.5
                            #num = (int(element(metal_symbol).group.group_id) * 6**5) ** (1/3)
                            #denom = (element(metal_symbol).en_pauling*element('O').en_pauling **5 ) ** (1/6)
                            psi = num/denom
                            #psi = int(element(metal_symbol).group.group_id) **c 2/element(metal_symbol).en_pauling ** 0.5
                        else:
                            #psi = get_outer_electrons(metal_symbol, oxidation_state) ** 2/element(metal_symbol).en_pauling
                            #psi = int(element(metal_symbol).group.group_id) ** 2/element(metal_symbol).en_pauling
                            psi = num/denom
                        all_psi.append(psi)
                        all_en.append(element(metal_symbol).en_pauling)
                    #plt.scatter([a[0] for a in bond_length], [a[1] for a in bond_length], color=ocd[oxidation_state])

            slope, intercept, r, p, se = linregress([1/a[0] ** 6 for a in bond_lengths], [a[1] for a in bond_lengths])

            #model = LR(fit_intercept=False)
            six_roots = np.array([1/a[0] ** 6 for a in bond_lengths])
            six_roots = six_roots.reshape(len(six_roots), -1)
            icohps = np.array([a[1] for a in bond_lengths])
            icohps = icohps.reshape(len(icohps), -1)
            #print(mae(six_roots*slope+intercept, icohps))
            #model.fit(six_roots, bls)
            #r = model.score(six_roots, bls)
            #intercept = 0
            #print(dir(model))
            #slope = model.coef_
            #print(metal_symbol, r ** 2)
            #print(metal_symbol, r ** 2)
            #if r ** 2 > 0.95:
            if True:
                parameters_dict[metal_symbol]['slope'] = slope
                parameters_dict[metal_symbol]['intercept'] = intercept
                parameters_dict[metal_symbol]['R Squared'] = r ** 2
            minimum = min([a[0] for a in bond_lengths])
            maximum = max([a[0] for a in bond_lengths])
            #plt.plot([slope*1/a**6 + intercept for a in [minimum, maximum]], [minimum, maximum])
            #plt.scatter([a[0] for a in bond_lengths], [a[1] for a in bond_lengths], color=)
            #plt.text(min(oxidation_states), max(ploted_quant), 'normal oxidation states: ' + ' '.join([str(a) for a in normal_oxi_states]))
            #plt.ylim([0,1])
            #plt.savefig(base_dir+ '/gather_results/plots/misc/total_ratios.png')
            #plt.savefig(base_dir+ '/gather_results/plots/bond_lengths_summed_cohp/{}.png'.format(metal_symbol))
            #plt.legend()
            #plt.show()
            #plt.close()

            #plt.scatter(fermi_integrals, adsorption_energies, color='k')
    #with open(base_dir+ '/gather_results/metal_fits.json', 'w') as f:
    #    json.dump(parameters_dict, f)
    #print(np.mean(ranges)/2)
    pred_cohp = [sum([predict_cohp_kr(c,a) for a in b]) for b,c in zip(all_bond_lengths, all_metals)]
    df_ = pd.DataFrame([[a,b,c,d,e,f,g,h,i,j,k,l,m] for a,b,c,d,e,f,g,h,i,j,k,l,m in \
                       zip(all_ads, all_icohp, all_oxidation_state, all_metals, all_outer_electrons,
                           [ads]*len(all_ads),all_psi, all_2p, pred_cohp, all_row, all_p_ints,all_surface_oxidation_states,
                           all_directories)],
                       columns=['Adsorption Energy', 'Bulk ICOHP', 'Oxidation State','Metal Symbol',
                           'Outer Electrons', 'Adsorbate', 'Psi','O 2p-center', 'predicted COHP', 'row', 'p ICOHP',
                           'Surface Oxidation State', 'Bulk File'])
    #print(all_metals.count('Ti'))
    df = df.append(df_)
    all_ads = np.array(all_ads).reshape(len(all_ads), -1)
    ax5.scatter(all_psi, all_ads, color=[ocd[a] for a in all_oxidation_state])
    ax6.scatter(all_2p, all_ads, color=[ocd[a] for a in all_oxidation_state])
    ax6.set_ylabel('Adsorption Energy (eV)')
    ax5.set_ylabel('Adsorption Energy (eV)')
    ax6.set_xlabel('All Psi')
    ax5.set_xlabel('Oxygen 2p center')
    for p2, psi, me, oxs, co in zip(all_2p, all_psi,all_metals, all_oxidation_state, all_normalized_cohp):
        if me in d3:
            row = '3d'
        elif me in d4:
            row = '4d'
        elif me in d5:
            row = '5d'
        ax5.text(co, psi, row)
        ax6.text(co, p2, row)
    #fig3.savefig(curdir + '/2p_psi.pdf')

    #plt.show()
    #print(len(all_ads))

    all_normalized_cohp = np.array(all_normalized_cohp).reshape(len(all_ads), -1)
    all_icohp = np.array(all_icohp).reshape(len(all_icohp), -1)
    #bl_derived_COHP = [sum([predict_cohp(c,a) for a in b])/d for b,c,d in zip(all_bond_lengths, all_metals, all_oxidation_state)]
    bl_derived_COHP = [sum([predict_cohp(c,a)/d for a in b]) for b,c,d in zip(all_bond_lengths, all_metals, all_oxidation_state)]
    bl_derived_COHP = np.array(bl_derived_COHP).reshape(len(bl_derived_COHP), -1)
    two_feature_norm = [[a,b] for a,b in zip(all_icohp, all_oxidation_state)]
    #ax.scatter(all_normalized_cohp, all_ads, color=[ocd[a] for a in all_oxidation_state])
    descriptor = [[sum([predict_cohp(c,a) for a in b])/d, m] for b,c,d,e,f,g,h,j,k,l,m \
                   in zip(all_bond_lengths, all_metals, all_oxidation_state, all_psi, all_p_ints, all_2p,
                          all_outer_electrons, all_rows, all_avg_cn, all_normalized_cohp,all_surface_oxidation_states)]
    #descriptor = [[a,b] for a,b in zip(all_normalized_cohp, all_surface_oxidation_states)]

    descriptor = np.array(descriptor).reshape(len(all_normalized_cohp), -2)
    ax.scatter(all_normalized_cohp, all_ads, color=[ocd[a] for a in all_oxidation_state])
    #ax.scatter(bl_derived_COHP, all_ads, color=[ocd[a] for a in all_oxidation_state])
    #ax.scatter(all_2p,all_ads, color=[ocd[a] for a in all_oxidation_state])
    #ax.scatter([a-b for a,b in zip(all_icohp, all_plus_2_integrals)],all_ads, color=[ocd[a] for a in all_oxidation_state])
    #ax.scatter(all_psi, all_ads, color=[ocd[a] for a in all_oxidation_state])
    ax.set_ylabel('Energy (eV)')
    ax.set_xlabel(r'ICOHP$_{norm}$ (eV/$e^-$)')
    #ax.set_xlabel('O-2p descriptor')
    ax.set_title(ads)
    #for ad, nic, me, oxs in zip(all_ads, all_normalized_cohp, all_metals, all_oxidation_state):
    #for ad, nic, me, oxs in zip(all_ads, bl_derived_COHP, all_metals, all_oxidation_state):
    #for ad, nic, me, oxs in zip(all_ads, [a-b for a,b in zip(all_icohp, all_plus_2_integrals)], all_metals, all_oxidation_state):
    #for ad, nic, me, oxs in zip(all_ads, all_psi, all_metals, all_oxidation_state):
    #    if me in d3:
    #        row = '3d'
    #    elif me in d4:
    #        row = '4d'
    #    elif me in d5:
    #        row = '5d'
    #    ax.text(nic, ad, me)
    #fg.tight_layout()
    #plt.savefig(base_dir + '/gather_results/plots/misc/{}_normalized_vs_ads.pdf'.format(ads))
    #plt.show()
    #if ads == 'OH':
    #    fig1.savefig(base_dir + '/gather_results/plots/misc/normalized_vs_ads.pdf')
        #fig1.savefig(base_dir + '/gather_results/plots/misc/psi_vs_ads.pdf')
        #fig1.show()
        #fig1.close()

    rs = 27
    X = descriptor
    y = all_ads
    print(len(y))
    X,y,al_met = shuffle(X,y,all_metals, random_state=rs)
    X_train, X_test, y_train, y_test = train_test_split(descriptor, all_ads, test_size=0.3, random_state=rs)
    X__, X_, m_train, m_test = train_test_split(descriptor, al_met, test_size=0.3, random_state=rs)
    #X_train, X_test, y_train, y_test = train_test_split(bl_derived_COHP, all_ads, test_size=0.3, random_state=rs)
    #X_train, X_test, y_train, y_test = train_test_split(descriptor, all_ads, test_size=0.5, random_state=rs)
    #X_train, X_test, y_train, y_test = train_test_split(all_normalized_cohp, all_ads, test_size=0.3, random_state=rs)
    params = [{'alpha':np.logspace(-3,2,200)}]
    model = GridSearchCV(GPR(normalize_y=True), params, cv=5)
    #model = ElasticNetCV(cv=4)
    #model = GridSearchCV(ElasticNet(), [{'l1_ratio':np.linspace(0,1,100)}], cv=4)

    degree=2

    poly = PolynomialFeatures(degree)
    pipe = Pipeline([
                    ('scaler', StandardScaler()),
                    #('PCA', PCA(n_components=2)),
                    ('model', model),
                    #('poly',poly),
                    #('linear',LinearRegression()),
                             ])
    #pipe = model
    score = cross_validate(pipe, X_train, y_train,scoring=['r2', 'neg_mean_absolute_error'], cv=5)
    print(score)
    print('CV scores:')
    print(np.mean(score['test_neg_mean_absolute_error']))
    print(np.mean(score['test_r2']))
    pipe.fit(X_train, y_train)
    #pipe.fit(X,y)
    #print(dir(pipe['model']))
    #print(pipe['model'].best_score_)
    opt_alpha = float(pipe['model'].best_estimator_.get_params()['alpha'])
    #print(opt_alpha)
    model = GPR(normalize_y=True, alpha=opt_alpha)
    pipe = Pipeline([
                    ('scaler', StandardScaler()),
                    #('PCA', PCA()),
                    #('feature_selection', SFS(GPR(alpha=0.02),n_features_to_select=2, direction="forward")),
                    ('model', model),
                    #('poly',poly),
                    #('linear',LinearRegression()),
                             ])

    pipe.fit(X_train, y_train)
    #sfs_forward = SFS(pipe,n_features_to_select=3, direction="forward").fit(X_train, y_train)
    #print(pipe['feature_selection'].get_support())
    #mean_prediction, std_prediction = pipe.predict(X_train)
    ads_models[ads] = pipe
    #with open(base_dir + '/gather_results/{}_model.pkl'.format(ads), 'wb') as f:
    #    pickle.dump(pipe, f)
    tr_pred, tr_pred_std = pipe.predict(X_train, return_std=True)
    ax_.errorbar(y_train,tr_pred, yerr=tr_pred_std, lw=0, marker='o',markersize=5,
               label=r'training data, mae={}, $R^2$={}'.format(round(mae(pipe.predict(X_train), y_train), 2), round(pipe.score(X_train, y_train), 2)))
    te_pred, te_pred_std = pipe.predict(X_test, return_std=True)
    #ax_.scatter(y_test, pipe.predict(X_test), label='test data, mae={}, R^2={}'.format(round(mae(pipe.predict(X_test), y_test), 2), round(pipe.score(X_test, y_test), 2)))
    ax_.errorbar(y_test,te_pred,yerr=te_pred_std, lw=0, marker='o',elinewidth=2,capsize=2,capthick=1,markersize=5,
            label=r'test data, mae={}, $R^2$={}'.format(round(mae(pipe.predict(X_test), y_test), 2), round(pipe.score(X_test, y_test), 2)))
    #ax_.scatter(y_train,pipe.predict(X_train), label='training data, mae={}, R^2={}'.format(round(mae(pipe.predict(X_train), y_train), 2), round(pipe.score(X_train, y_train), 2)))

    #ax_.scatter(pipe.predict(X), y, label='all data, mae={}, R^2={}'.format(round(mae(pipe.predict(X), y), 2), round(pipe.score(X, y), 2)))
    ax_.set_xlabel('adsorption energy')
    ax_.set_ylabel('predicted adsorption energy')
    if ads in ['O', 'OH']:
        ax_.set_title(ads + '*')
    else:
        ax_.set_title(ads)
    ax_.legend()
    #ax_.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)])
    ax_.plot([min(y), max(y)], [min(y), max(y)], color='k')
    #print(pipe.score(X_test, y_test))
    print('Test set:')
    print(mae(pipe.predict(X_test), y_test))
    print(np.sqrt(mse(pipe.predict(X_test), y_test)))
    #print(pipe.score(X, y))
    #print(mae(pipe.predict(X), y))
    #print(np.sqrt(mse(pipe.predict(X), y)))
    print(pipe.score(X_test, y_test))
    #norm_all_normalized_cohp = (all_normalized_cohp-np.mean(all_normalized_cohp))/np.std(all_normalized_cohp)
    #norm_all_psi = (all_psi-np.mean(all_psi))/np.std(all_psi)
    #print(np.corrcoef(np.array(all_normalized_cohp).flatten(), np.array(all_psi).flatten()))
    #print(np.cov(np.array(norm_all_normalized_cohp).flatten(), np.array(norm_all_psi).flatten(), bias=False))
    if ads == 'O-OH':
        plt_rng = np.arange(-0.5,2.7,0.05)
        ax9.plot(plt_rng, [-1 * overpot(a) for a in plt_rng])
        #ax9.errorbar(tr_pred, [overpot(a) for a in tr_pred], xerr=tr_pred_std,
        ax9.errorbar(tr_pred, [-1 * overpot(a) for a in y_train], xerr=tr_pred_std,
                lw=0, marker='o',elinewidth=2,capsize=2,capthick=1,markersize=5, label='training set', alpha=0.35)
        #ax9.errorbar(te_pred, [overpot(a) for a in te_pred], xerr=te_pred_std,
        ax9.errorbar(te_pred, [-1 * overpot(a) for a in y_test], xerr=te_pred_std,
                lw=0, marker='o',elinewidth=2,capsize=2,capthick=1,markersize=5, label='test set')
        #for t,o,m in zip(te_pred, [overpot(a) for a in y_test],m_test):
            #if m in ['Ir', 'Pd', 'Cr', 'Pt', 'Ru','Ti', 'Rh']:
            #if m in ['Ir', 'Ru']:
                #print(t,o,m)
            #    ax9.text(t,o,m)
        #for t,o,m in zip(tr_pred, [overpot(a) for a in tr_pred],m_train):
            #if m in ['Ir', 'Pd', 'Cr', 'Pt', 'Ru', 'Ti', 'Rh']:
            #if m in ['Ir', 'Ru']:
            #    ax9.text(t,o,m)
            #print(t,o,m)
        ax9.set_xlabel(r'$\Delta G_{O-OH}$ Energy (eV)')
        ax9.set_ylabel('Overpotential (V)')
        ax9.legend()
        fig4.tight_layout()
        fig4.savefig(curdir + '/volcano_pred.pdf'.format(ads))

    print('\n')
    #plt.tight_layout()
    #plt.savefig(base_dir + '/gather_results/plots/misc/{}_normalized_icohp.png'.format(ads))
    #plt.show()

    """
    ax_.scatter(all_icohp, all_ads, color=[ocd[a] for a in all_oxidation_state])
    ax_.set_ylabel('Adsorption Energy (eV)')
    ax_.set_xlabel('Approximated Normalized ICOHP (eV/$e^-$)')
    plot_range = np.linspace(min(X_train), max(X_train), 100).reshape(100,-1)
    ax_.plot(plot_range, pipe.predict(plot_range))
    #for ad, nic, me, os in zip(all_ads, all_normalized_cohp, all_metals, all_oxidation_state):
    #    plt.text(nic, ad, me + str(os))
    """
    #plt.tight_layout()
    #if ads == 'OH':
    #    fig2.tight_layout()
    #    fig2.savefig(base_dir + '/gather_results/plots/misc/model.pdf'.format(ads))
        #fig2.show()
        #fig2.close()
    fg.tight_layout()
    fg.savefig(curdir + '/{}_combined.pdf'.format(ads))

with open(curdir + '/all_data.csv', 'w') as f:
    df.to_csv(f)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

actual_data_m = pd.read_csv('37-taxon-mammalian-simulated-actual.csv')
actual_data_a = pd.read_csv('48-taxon-avian-simulated-actual.csv')

astral_data_m = pd.read_csv('astral_results_combined_mammalian.csv')
astral_data_a = pd.read_csv('astral_results_combined_avian.csv')

mpest_data_m = pd.read_csv('mpest_results_combined_mammalian.csv')
mpest_data_a = pd.read_csv('mpest_results_combined_avian.csv')

trips_data_m = pd.read_csv('trips_results_combined_mammalian.csv')
trips_data_a = pd.read_csv('trips_results_combined_avian.csv')

summary_stats_a = pd.DataFrame(columns=['METHOD', 'SCAL', 'NGEN', 'NBPS', 'BIPA', 'BIPB', 'MEAN_BRLEN', 'VAR_BRLEN'])
summary_stats_m = pd.DataFrame(columns=['METHOD', 'SCAL', 'NGEN', 'NBPS', 'BIPA', 'BIPB', 'MEAN_BRLEN', 'VAR_BRLEN'])

# different params for the models (more here so i remember them)
# Avian
reps = ['R'+str(x) for x in range(1,21)]
scals = ['0.5X', '1X', '2X']
ngens = ['50', '100', '200', '500', '1000'] # 1000 works with all scales, rest only work for 1X
nbps = ['true', '500']

# make map that maps bipartitions to their brlens
brlen_astral_a = dict()
brlen_mpest_a = dict()
brlen_trips_a = dict()

#all scales, set ngens = 10000
ngen = '1000'

for rep in reps:
    for scal in scals:
        for nbp in nbps:
            model = scal+'-'+ngen+'-'+nbp
            #astral
            temp_df_astral = astral_data_a.loc[(astral_data_a['REPL'] == rep) &
                                               (astral_data_a['SCAL'] == scal) &
                                               (astral_data_a['NBPS'] == nbp)]
            for index, row in temp_df_astral.iterrows():
                key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                if not key in brlen_astral_a:
                    brlen_astral_a[key] = []
                brlen_astral_a[key].append(float(row['ASTRAL_BRLEN']))
            #mpest
            temp_df_mpest = mpest_data_a.loc[(mpest_data_a['REPL'] == rep) &
                                             (mpest_data_a['SCAL'] == scal) &
                                             (mpest_data_a['NBPS'] == nbp)]
            for index, row in temp_df_mpest.iterrows():
                key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                if not key in brlen_mpest_a:
                    brlen_mpest_a[key] = []
                brlen_mpest_a[key].append(float(row['TRIPS_BRLEN']))
            #trips
            temp_df_trips = trips_data_a.loc[(trips_data_a['REPL'] == rep) &
                                             (trips_data_a['SCAL'] == scal) &
                                             (trips_data_a['NBPS'] == nbp)]
            for index, row in temp_df_trips.iterrows():
                key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                if not key in brlen_trips_a:
                    brlen_trips_a[key] = []
                brlen_trips_a[key].append(float(row['TRIPS_BRLEN']))                                            

#all gens, set scals = 1X
scal = '1X'

for rep in reps:
    for ngen in ngens:
        if ngen != '1000':
            for nbp in nbps:
                model = scal+'-'+ngen+'-'+nbp
                #astral
                temp_df_astral = astral_data_a.loc[(astral_data_a['REPL'] == rep) &
                                                (astral_data_a['SCAL'] == scal) &
                                                (astral_data_a['NBPS'] == nbp)]
                for index, row in temp_df_astral.iterrows():
                    key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                    if not key in brlen_astral_a:
                        brlen_astral_a[key] = []
                    brlen_astral_a[key].append(float(row['ASTRAL_BRLEN']))
                #mpest
                temp_df_mpest = mpest_data_a.loc[(mpest_data_a['REPL'] == rep) &
                                                (mpest_data_a['SCAL'] == scal) &
                                                (mpest_data_a['NBPS'] == nbp)]
                for index, row in temp_df_mpest.iterrows():
                    key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                    if not key in brlen_mpest_a:
                        brlen_mpest_a[key] = []
                    brlen_mpest_a[key].append(float(row['TRIPS_BRLEN']))
                #trips
                temp_df_trips = trips_data_a.loc[(trips_data_a['REPL'] == rep) &
                                                (trips_data_a['SCAL'] == scal) &
                                                (trips_data_a['NBPS'] == nbp)]
                for index, row in temp_df_trips.iterrows():
                    key = model + ':' + row['BIPA'] + '|' + row['BIPB']
                    if not key in brlen_trips_a:
                        brlen_trips_a[key] = []
                    brlen_trips_a[key].append(float(row['TRIPS_BRLEN']))

#astral
for key in brlen_astral_a.keys():
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'astral','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_astral_a[key]), 
           'VAR_BRLEN': np.var(brlen_astral_a[key])}
    summary_stats_a = summary_stats_a.append(row, ignore_index = True)

#mpest
for key in brlen_mpest_a.keys():
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'mpest','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_mpest_a[key]), 
           'VAR_BRLEN': np.var(brlen_mpest_a[key])}
    summary_stats_a = summary_stats_a.append(row, ignore_index = True)

#trips
for key in brlen_trips_a.keys():  
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'trips','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_trips_a[key]), 
           'VAR_BRLEN': np.var(brlen_trips_a[key])}
    summary_stats_a = summary_stats_a.append(row, ignore_index = True)   

summary_stats_a.to_csv('48-taxon-avian-simulated-summary-stats.csv')

# Mammalian
scals = ['noscale', 'scale2d', 'scale2u'] #noscale works for all, rest only work for 200g and 500b
ngens = ['25g', '50g', '100g', '200g', '400g', '800g'] #200g works for all, rest only work for no scale and 500b
nbps = ['250b', '500b', '1000b', '1500b', 'true'] #500b works for all, rest only work for noscale and 200g

# make map that maps bipartitions to their brlens
brlen_astral_m = dict()
brlen_mpest_m = dict()
brlen_trips_m = dict()

#vary scale
ngen = '200g'
nbp = '500b'
for scal in scals:
    model = scal+'-'+ngen+'-'+nbp
    #astral
    temp_df_astral = astral_data_m.loc[(astral_data_m['REPL'] == rep) &
                                       (astral_data_m['NGEN'] == ngen) &
                                       (astral_data_m['NBPS'] == nbp)]
    for index, row in temp_df_astral.iterrows():
        key = model + ':' + row['BIPA'] + '|' + row['BIPB']
        if not key in brlen_astral_m:
            brlen_astral_m[key] = []
        brlen_astral_m[key].append(float(row['ASTRAL_BRLEN']))
    #mpest
    temp_df_mpest = mpest_data_m.loc[(mpest_data_m['REPL'] == rep) &
                                     (mpest_data_m['NGEN'] == ngen) &
                                     (mpest_data_m['NBPS'] == nbp)]
    for index, row in temp_df_mpest.iterrows():
        key = model + ':' + row['BIPA'] + '|' + row['BIPB']
        if not key in brlen_mpest_m:
            brlen_mpest_m[key] = []
        brlen_mpest_m[key].append(float(row['TRIPS_BRLEN']))
    #trips
    temp_df_trips = trips_data_m.loc[(trips_data_m['REPL'] == rep) &
                                     (trips_data_m['NGEN'] == ngen) &
                                     (trips_data_m['NBPS'] == nbp)]
    for index, row in temp_df_trips.iterrows():
        key = model + ':' + row['BIPA'] + '|' + row['BIPB']
        if not key in brlen_trips_m:
            brlen_trips_m[key] = []
        brlen_trips_m[key].append(float(row['TRIPS_BRLEN']))                                            

#vary gens
scal = 'noscale'
nbp = '500b'
for ngen in ngens:
    if ngen != '200g':
        model = scal+'-'+ngen+'-'+nbp
        #astral
        temp_df_astral = astral_data_m.loc[(astral_data_m['REPL'] == rep) &
                                        (astral_data_m['SCAL'] == scal) &
                                        (astral_data_m['NBPS'] == nbp)]
        for index, row in temp_df_astral.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_astral_m:
                brlen_astral_m[key] = []
            brlen_astral_m[key].append(float(row['ASTRAL_BRLEN']))
        #mpest
        temp_df_mpest = mpest_data_m.loc[(mpest_data_m['REPL'] == rep) &
                                        (mpest_data_m['SCAL'] == scal) &
                                        (mpest_data_m['NBPS'] == nbp)]
        for index, row in temp_df_mpest.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_mpest_m:
                brlen_mpest_m[key] = []
            brlen_mpest_m[key].append(float(row['TRIPS_BRLEN']))
        #trips
        temp_df_trips = trips_data_m.loc[(trips_data_m['REPL'] == rep) &
                                        (trips_data_m['SCAL'] == scal) &
                                        (trips_data_m['NBPS'] == nbp)]
        for index, row in temp_df_trips.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_trips_m:
                brlen_trips_m[key] = []
            brlen_trips_m[key].append(float(row['TRIPS_BRLEN']))  

#vary nbps
scal = 'noscale'
ngen = '200g'
for nbp in nbps:
    if nbp != '500b':
        model = scal+'-'+ngen+'-'+nbp
        #astral
        temp_df_astral = astral_data_m.loc[(astral_data_m['REPL'] == rep) &
                                        (astral_data_m['SCAL'] == scal) &
                                        (astral_data_m['NBPS'] == nbp)]
        for index, row in temp_df_astral.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_astral_m:
                brlen_astral_m[key] = []
            brlen_astral_m[key].append(float(row['ASTRAL_BRLEN']))
        #mpest
        temp_df_mpest = mpest_data_m.loc[(mpest_data_m['REPL'] == rep) &
                                        (mpest_data_m['SCAL'] == scal) &
                                        (mpest_data_m['NBPS'] == nbp)]
        for index, row in temp_df_mpest.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_mpest_m:
                brlen_mpest_m[key] = []
            brlen_mpest_m[key].append(float(row['TRIPS_BRLEN']))
        #trips
        temp_df_trips = trips_data_m.loc[(trips_data_m['REPL'] == rep) &
                                        (trips_data_m['SCAL'] == scal) &
                                        (trips_data_m['NBPS'] == nbp)]
        for index, row in temp_df_trips.iterrows():
            key = model + ':' + row['BIPA'] + '|' + row['BIPB']
            if not key in brlen_trips_m:
                brlen_trips_m[key] = []
            brlen_trips_m[key].append(float(row['TRIPS_BRLEN']))  

#astral
for key in brlen_astral_m.keys():
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'astral','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_astral_m[key]), 
           'VAR_BRLEN': np.var(brlen_astral_m[key])}
    summary_stats_m = summary_stats_m.append(row, ignore_index = True)

#mpest
for key in brlen_mpest_m.keys():
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'mpest','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_mpest_m[key]), 
           'VAR_BRLEN': np.var(brlen_mpest_m[key])}
    summary_stats_m = summary_stats_m.append(row, ignore_index = True)

#trips
for key in brlen_trips_m.keys():  
    temp = key.split(':')
    model = temp[0].split('-')
    bip = temp[1].split('|')

    row = {'METHOD': 'trips','SCAL': model[0], 'NGEN': model[1], 'NBPS': model[2], 
           'BIPA': bip[0], 'BIPB': bip[1], 'MEAN_BRLEN': np.mean(brlen_trips_m[key]), 
           'VAR_BRLEN': np.var(brlen_trips_m[key])}
    summary_stats_m = summary_stats_m.append(row, ignore_index = True)   

summary_stats_m.to_csv('37-taxon-mammalian-simulated-summary-stats.csv')
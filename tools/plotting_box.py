import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

letters = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)','(j)','(k)','(l)','(m)','(n)','(o)', '(p)','(q)','(r)','(s)','(t)','(u)','(v)','(w)','(x)','(y)','(z)']

def plot_avian(option):
    actual_data = pd.read_csv('48-taxon-avian-simulated-actual.csv')
    summary_stats = pd.read_csv('48-taxon-avian-simulated-summary-stats.csv')

    astral_data = pd.read_csv('astral_results_combined_avian.csv')

    mpest_data = pd.read_csv('mpest_results_combined_avian.csv')

    trips_data = pd.read_csv('trips_results_combined_avian.csv')

    if option == 0:
        fig = plt.figure(figsize=(8.5, 6))
    elif option == 1:
        fig = plt.figure(figsize=(8.5, 7))
    else:
        fig = plt.figure(figsize=(8.5, 4))

    # reps = ['R'+str(x) for x in range(1,21)]
    # methods = ['astral','mpest','trips']

    # different params for the models (more here so i remember them)
    # Avian
    scals = ['0.5X', '1X', '2X']
    ngens = [50, 100, 200, 500, 1000] # 1000 works with all scales, rest only work for 1X
    nbps = ['True', '500']
    categories = {0: '<0.25', 1: '[0.25,0.5)', 2: '[0.5,2)', 3: '[2,6)', 4: '>=6'}

    brlen_actual = dict()

    # get actual branch lengths to calculate errors
    for i, row in actual_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb

        brlen_actual[key] = row['DATA_BRLEN']

    #calculate errors and assign category
    # error = estimated - true
    astral_data['error'] = np.nan
    astral_data['category'] = np.nan
    for i, row in astral_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['ASTRAL_BRLEN']

        # assign error
        actual = brlen_actual[key]
        astral_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            astral_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            astral_data.loc[i, 'category'] = '1'
        elif actual < 2:
            astral_data.loc[i, 'category'] = '2'
        elif actual < 6:
            astral_data.loc[i, 'category'] = '3'
        else:
            astral_data.loc[i, 'category'] = '4'

    mpest_data['error'] = np.nan
    mpest_data['category'] = np.nan
    for i, row in mpest_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['TRIPS_BRLEN'] #note: mpest csv seems to have some stuff missing
        actual = 7
        if key in brlen_actual:
            actual = brlen_actual[key]
            mpest_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            mpest_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            mpest_data.loc[i, 'category'] = '1'
        elif actual < 2:
            mpest_data.loc[i, 'category'] = '2'
        elif actual < 6:
            mpest_data.loc[i, 'category']  = '3'
        else:
            mpest_data.loc[i, 'category']  = '4'

    trips_data['error'] = np.nan
    trips_data['category'] = np.nan
    for i, row in trips_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['TRIPS_BRLEN']
        actual = brlen_actual[key]
        trips_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            trips_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            trips_data.loc[i, 'category'] = '1'
        elif actual < 2:
            trips_data.loc[i, 'category'] = '2'
        elif actual < 6:
            trips_data.loc[i, 'category'] = '3'
        else:
            trips_data.loc[i, 'category'] = '4'

    axs = []
    # set up plots
    if option == 0: # vary scals
        gs = gridspec.GridSpec(len(scals),4) #3 scals
        for i in range(len(scals)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        ngen = 1000
        nbp = '500'
        for i, scal in enumerate(scals):
            axs[i][0].set_ylabel(scal)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']

                if i == len(scals)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)
                

    elif option == 1: #vary ngens
        gs = gridspec.GridSpec(len(ngens),4) #5 gens
        for i in range(len(ngens)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        scal = '1X'
        nbp = '500'
        for i, ngen in enumerate(ngens):
            axs[i][0].set_ylabel(ngen)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']

                if i == len(ngens)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)

    else: #vary npbs
        gs = gridspec.GridSpec(len(nbps),4) #2 nbps
        for i in range(len(nbps)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        ngen = 1000
        scal = '1X'
        for i, nbp in enumerate(nbps): 
            axs[i][0].set_ylabel(nbp)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data            

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']

                if i == len(nbps)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)

    axs = [ax for sub in axs for ax in sub] # flatten the 2D list
    plt.tight_layout()
    plt.show()

def plot_mammalian(option):
    actual_data = pd.read_csv('37-taxon-mammalian-simulated-actual.csv')

    summary_stats = pd.read_csv('37-taxon-mammalian-simulated-summary-stats.csv')

    astral_data = pd.read_csv('astral_results_combined_mammalian.csv')

    mpest_data = pd.read_csv('mpest_results_combined_mammalian.csv')

    trips_data = pd.read_csv('trips_results_combined_mammalian.csv')

    if option == 0:
        fig = plt.figure(figsize=(8.5, 6))
    elif option == 1:
        fig = plt.figure(figsize=(8.5, 8))
    else:
        fig = plt.figure(figsize=(8.5, 8))

    # reps = ['R'+str(x) for x in range(1,21)]
    # methods = ['astral','mpest','trips']

    # different params for the models (more here so i remember them)
    # Mammalian
    scals = ['noscale', 'scale2d', 'scale2u'] #noscale works for all, rest only work for 200g and 500b
    ngens = ['25g', '50g', '100g', '200g', '400g', '800g'] #200g works for all, rest only work for no scale and 500b
    nbps = ['250b', '500b', '1000b', '1500b', 'True'] #500b works for all, rest only work for noscale and 200g
    categories = {0: '<0.25', 1: '[0.25,0.5)', 2: '[0.5,2)', 3: '[2,6)', 4: '>=6'}

    brlen_actual = dict()

    # get actual branch lengths to calculate errors
    for i, row in actual_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb

        brlen_actual[key] = row['DATA_BRLEN']

    #calculate errors and assign category
    # error = estimated - true
    astral_data['error'] = np.nan
    astral_data['category'] = np.nan
    for i, row in astral_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['ASTRAL_BRLEN']
        actual = brlen_actual[key]
        # assign error
        astral_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            astral_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            astral_data.loc[i, 'category'] = '1'
        elif actual < 2:
            astral_data.loc[i, 'category'] = '2'
        elif actual < 6:
            astral_data.loc[i, 'category'] = '3'
        else:
            astral_data.loc[i, 'category'] = '4'

    mpest_data['error'] = np.nan
    mpest_data['category'] = np.nan
    for i, row in mpest_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['TRIPS_BRLEN'] #note: mpest csv seems to have some stuff missing
        actual = 7
        if key in brlen_actual:
            actual = brlen_actual[key]
            mpest_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            mpest_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            mpest_data.loc[i, 'category'] = '1'
        elif actual < 2:
            mpest_data.loc[i, 'category'] = '2'
        elif actual < 6:
            mpest_data.loc[i, 'category']  = '3'
        else:
            mpest_data.loc[i, 'category']  = '4'

    trips_data['error'] = np.nan
    trips_data['category'] = np.nan
    for i, row in trips_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb
        brlen = row['TRIPS_BRLEN']
        actual = brlen_actual[key]
        trips_data.loc[i, 'error'] = brlen - actual

        # assign category note: might need to adjust categorys when varying scale
        if actual < 0.25:
            trips_data.loc[i, 'category'] = '0'
        elif actual < 0.5:
            trips_data.loc[i, 'category'] = '1'
        elif actual < 2:
            trips_data.loc[i, 'category'] = '2'
        elif actual < 6:
            trips_data.loc[i, 'category'] = '3'
        else:
            trips_data.loc[i, 'category'] = '4'

    axs = []
    # set up plots
    if option == 0: # vary scals
        gs = gridspec.GridSpec(len(scals),4) 
        for i in range(len(scals)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        ngen = '200g'
        nbp = '500b'
        for i, scal in enumerate(scals):
            axs[i][0].set_ylabel(scal)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']


                if i == len(scals)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)

    elif option == 1: #vary ngens
        gs = gridspec.GridSpec(len(ngens),4) 
        for i in range(len(ngens)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        scal = 'noscale'
        nbp = '500b'
        for i, ngen in enumerate(ngens):
            axs[i][0].set_ylabel(ngen)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']


                if i == len(ngens)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)

    else: #vary npbs
        gs = gridspec.GridSpec(len(nbps),4)
        for i in range(len(nbps)):
            axs.append([])
            for j in range(4):
                axs[i].append(plt.subplot(gs[i,j]))

        ngen = '200g'
        scal = 'noscale'
        for i, nbp in enumerate(nbps): 
            axs[i][0].set_ylabel(nbp)
            for j in range(4):
                if i == 0:
                    axs[0][j].set_title(categories[j])

                astral_temp = astral_data.loc[(astral_data['NGEN'] == ngen) & (astral_data['SCAL'] == scal) & (astral_data['NBPS'] == nbp) & (astral_data['category'] == str(j))]
                error_astral = astral_temp['error']

                mpest_temp = mpest_data.loc[(mpest_data['NGEN'] == ngen) & (mpest_data['SCAL'] == scal) & (mpest_data['NBPS'] == nbp) & (mpest_data['category'] == str(j))]
                error_mpest = mpest_temp['error']
                error_mpest = error_mpest[~np.isnan(error_mpest)] #mpest has missing data            

                trips_temp = trips_data.loc[(trips_data['NGEN'] == ngen) & (trips_data['SCAL'] == scal) & (trips_data['NBPS'] == nbp) & (trips_data['category'] == str(j))]
                error_trips = trips_temp['error']


                if i == len(nbps)-1:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], labels=['Astral','MP-EST','Trips'], sym='.')
                    axs[i][j].tick_params(axis='x', labelsize='7')
                else:
                    axs[i][j].boxplot([error_astral,error_mpest,error_trips], sym='.')
                    axs[i][j].tick_params(bottom=False, labelbottom=False)

                axs[i][j].hlines(0,0,4,colors='red')
                axs[i][j].set_xlim(0,4)
                axs[i][j].tick_params(axis='y', labelsize='8')
                axs[i][j].set_title(letters[i*4+j],
                             loc="left", x=-0.15, y=1, fontsize=10)

    axs = [ax for sub in axs for ax in sub] # flatten the 2D list
    plt.tight_layout()
    plt.show()

#make sure you change figure size appropriately
plot_avian(1)
# plot_mammalian(2)
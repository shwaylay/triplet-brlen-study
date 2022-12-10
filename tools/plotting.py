import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd


def plot_avian(scal,ngen,nbps):
    actual_data = pd.read_csv('48-taxon-avian-simulated-actual.csv')
    summary_stats = pd.read_csv('48-taxon-avian-simulated-summary-stats.csv')

    fig = plt.figure(figsize=(7.5, 6))
    gs = gridspec.GridSpec(3,3)
    ax0 = plt.subplot(gs[0,0])
    ax1 = plt.subplot(gs[0,1])
    ax2 = plt.subplot(gs[0,2])
    ax3 = plt.subplot(gs[1,0])
    ax4 = plt.subplot(gs[1,1])
    ax5 = plt.subplot(gs[1,2])
    ax6 = plt.subplot(gs[2,0])
    ax7 = plt.subplot(gs[2,1])
    ax8 = plt.subplot(gs[2,2])

    axs = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]

    # reps = ['R'+str(x) for x in range(1,21)]
    # methods = ['astral','mpest','trips']

    # different params for the models (more here so i remember them)
    # Avian
    # scals = ['0.5X', '1X', '2X']
    # ngens = ['50', '100', '200', '500', '1000'] # 1000 works with all scales, rest only work for 1X
    # nbps = ['true', '500']

    #Avian dataset

    brlen_actual = dict()
    brlen_astral = dict()
    brlen_mpest = dict()
    brlen_trips = dict()

    for i, row in actual_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb

        brlen_actual[key] = row['DATA_BRLEN']
        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'astral')]

        brlen_astral[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]

        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'mpest')]

        brlen_mpest[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]

        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'trips')]

        brlen_trips[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]


    x = range(0,len(brlen_actual.keys()))

    actual = list(brlen_actual.values())
    astral = [x[0] for x in list(brlen_astral.values())]
    mpest = [x[0] for x in list(brlen_mpest.values())]
    trips = [x[0] for x in list(brlen_trips.values())]


    # plot average lenghs
    ax0.set_title(r'Astral', fontsize=12)
    ax1.set_title(r'MP-EST', fontsize=12)
    ax2.set_title(r'Trips', fontsize=12)
    ax0.plot(actual, actual, label="actual")
    ax1.plot(actual, actual, label="actual")
    ax2.plot(actual, actual, label="actual")
    ax0.scatter(actual, astral,marker='.')
    ax1.scatter(actual, mpest,marker='.')
    ax2.scatter(actual, trips,marker='.')
    ax0.set_ylabel(r'Estimated Length', fontsize=10)

    #plot absolute error
    abs_err_astral = [abs(astral[i] - actual[i]) for i in range(0,len(actual))]
    abs_err_mpest = [abs(mpest[i] - actual[i]) for i in range(0,len(actual))]
    abs_err_trips = [abs(trips[i] - actual[i]) for i in range(0,len(actual))]

    ax3.scatter(actual, abs_err_astral, label="astral", marker='.')
    ax4.scatter(actual, abs_err_mpest, label="mpest", marker= '.')
    ax5.scatter(actual, abs_err_trips, label="trips", marker = '.')
    ax3.set_ylabel(r'Absolute Error', fontsize=10)

    #plot percent error
    per_err_astral = [(abs_err_astral[i]/actual[i]) for i in range(0,len(actual))]
    per_err_mpest = [(abs_err_mpest[i]/actual[i]) for i in range(0,len(actual))]
    per_err_trips = [(abs_err_trips[i]/actual[i]) for i in range(0,len(actual))]

    #remove extreme outliers
    temp_per_err = []
    astral_actual = []
    for i in range(len(per_err_astral)):
        x = per_err_astral[i]
        if x < 100:
            temp_per_err.append(x)
            astral_actual.append(actual[i])

    per_err_astral = temp_per_err

    temp_per_err = []
    mpest_actual = []
    for i in range(len(per_err_mpest)):
        x = per_err_mpest[i]
        if x < 100:
            temp_per_err.append(x)
            mpest_actual.append(actual[i])

    per_err_mpest = temp_per_err

    temp_per_err = []
    trips_actual = []
    for i in range(len(per_err_trips)):
        x = per_err_trips[i]
        if x < 100:
            temp_per_err.append(x)
            trips_actual.append(actual[i])

    per_err_trips = temp_per_err

    ax6.scatter(astral_actual, per_err_astral, label="astral", marker='.')
    ax7.scatter(mpest_actual, per_err_mpest, label="mpest", marker= '.')
    ax8.scatter(trips_actual, per_err_trips, label="trips", marker = '.')
    ax6.set_ylabel(r'Percent Error', fontsize=10)
    ax6.set_xlabel('Actual Branch Length')
    ax7.set_xlabel('Actual Branch Length')
    ax8.set_xlabel('Actual Branch Length')

    plt.tight_layout()
    plt.show()

def plot_mammalian(scal, ngen, nbps):
    actual_data = pd.read_csv('37-taxon-mammalian-simulated-actual.csv')

    summary_stats = pd.read_csv('37-taxon-mammalian-simulated-summary-stats.csv')

    fig = plt.figure(figsize=(7.5, 6))
    gs = gridspec.GridSpec(3,3)
    ax0 = plt.subplot(gs[0,0])
    ax1 = plt.subplot(gs[0,1])
    ax2 = plt.subplot(gs[0,2])
    ax3 = plt.subplot(gs[1,0])
    ax4 = plt.subplot(gs[1,1])
    ax5 = plt.subplot(gs[1,2])
    ax6 = plt.subplot(gs[2,0])
    ax7 = plt.subplot(gs[2,1])
    ax8 = plt.subplot(gs[2,2])

    axs = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]

    # reps = ['R'+str(x) for x in range(1,21)]
    # methods = ['astral','mpest','trips']

    # different params for the models (more here so i remember them)
    # Mammalian
    # scals = ['noscale', 'scaled2d', 'scale2u'] #noscale works for all, rest only work for 200g and 500b
    # ngens = ['25g', '50g', '100g', '200g', '400g', '800g'] #200g works for all, rest only work for no scale and 500b
    # nbps = ['250b', '500b', '1000b', '1500b', 'true'] #500b works for all, rest only work for noscale and 200g

    #Mammalian dataset

    brlen_actual = dict()
    brlen_astral = dict()
    brlen_mpest = dict()
    brlen_trips = dict()

    for i, row in actual_data.iterrows():
        bipa = row['BIPA']
        bipb = row['BIPB']

        key = bipa + "|" + bipb

        brlen_actual[key] = row['DATA_BRLEN']
        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'astral')]
        brlen_astral[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]

        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'mpest')]

        brlen_mpest[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]

        temp_data = summary_stats.loc[(summary_stats['BIPA'] == bipa) &
                                        (summary_stats['BIPB'] == bipb) &
                                        (summary_stats['SCAL'] == scal) &
                                        (summary_stats['NGEN'] == ngen) &
                                        (summary_stats['NBPS'] == nbps) &
                                        (summary_stats['METHOD'] == 'trips')]

        brlen_trips[key] = [temp_data['MEAN_BRLEN'].iloc[0],temp_data['VAR_BRLEN'].iloc[0]]


    x = range(0,len(brlen_actual.keys()))

    actual = list(brlen_actual.values())
    astral = [x[0] for x in list(brlen_astral.values())]
    mpest = [x[0] for x in list(brlen_mpest.values())]
    trips = [x[0] for x in list(brlen_trips.values())]


    # plot average lenghs
    ax0.set_title(r'Astral', fontsize=12)
    ax1.set_title(r'MP-EST', fontsize=12)
    ax2.set_title(r'Trips', fontsize=12)
    ax0.plot(actual, actual, label="actual")
    ax1.plot(actual, actual, label="actual")
    ax2.plot(actual, actual, label="actual")
    ax0.scatter(actual, astral,marker='.')
    ax1.scatter(actual, mpest,marker='.')
    ax2.scatter(actual, trips,marker='.')
    ax0.set_ylabel(r'Estimated Length', fontsize=10)

    #plot absolute error
    abs_err_astral = [abs(astral[i] - actual[i]) for i in range(0,len(actual))]
    abs_err_mpest = [abs(mpest[i] - actual[i]) for i in range(0,len(actual))]
    abs_err_trips = [abs(trips[i] - actual[i]) for i in range(0,len(actual))]

    ax3.scatter(actual, abs_err_astral, label="astral", marker='.')
    ax4.scatter(actual, abs_err_mpest, label="mpest", marker= '.')
    ax5.scatter(actual, abs_err_trips, label="trips", marker = '.')
    ax3.set_ylabel(r'Absolute Error', fontsize=10)

    #plot percent error
    per_err_astral = [(abs_err_astral[i]/actual[i]) for i in range(0,len(actual))]
    per_err_mpest = [(abs_err_mpest[i]/actual[i]) for i in range(0,len(actual))]
    per_err_trips = [(abs_err_trips[i]/actual[i]) for i in range(0,len(actual))]

    ax6.scatter(actual, per_err_astral, label="astral", marker='.')
    ax7.scatter(actual, per_err_mpest, label="mpest", marker= '.')
    ax8.scatter(actual, per_err_trips, label="trips", marker = '.')
    ax6.set_ylabel(r'Percent Error', fontsize=10)
    ax6.set_xlabel('Actual Branch Length')
    ax7.set_xlabel('Actual Branch Length')
    ax8.set_xlabel('Actual Branch Length')

    plt.tight_layout()
    plt.show()

# plot_avian('1X',1000,500)
plot_mammalian('noscale','200g','500b')
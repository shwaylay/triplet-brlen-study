import pandas as pd

study_dir = '/fs/cbcb-lab/ekmolloy/msuehle/triplet-brlen-study/'
data_dir = study_dir+'data/mahbub2021wqfm/'
data_sets = ['37-taxon-mammalian-simulated', '48-taxon-avian-simulated']

reps = [f'R{x}' for x in range(1,21)]

# for avian
scales_a = [['0.5X', '1X', '2X'],['1X']]
ngens_a = [['1000'],['50', '100', '200', '500', '1000']] #note that only 1X has < 1000
nbpss_a = [['true', '500'],['true', '500']]

# for mammalian
#vary ils
scales_m1 = ['noscale', 'scale2d', 'scale2u']
ngens_m1 = ['200g']
nbpss_m1 = ['500b']

#varying sequence length
scales_m2 = ['noscale']
ngens_m2 = ['200g']
nbpss_m2 = ['250b','1000b','1500b','true']

#varying number genes
scales_m3 = ['noscale']
ngens_m3 = ['25g','50g','100g','400g','800g']
nbpss_m3 = ['500b']

scales_m = [scales_m1, scales_m2, scales_m3]
ngens_m = [ngens_m1, ngens_m2, ngens_m3]
nbpss_m = [nbpss_m1, nbpss_m2, nbpss_m3]

# go through avian
astral_results_a = []
mpest_results_a = []
trips_results_a = []

for i in range(2):
    for scal in scales_a[i]:
        for ngen in ngens_a[i]:
            for nbps in nbpss_a[i]:
                for rep in reps:
                    model = f'{scal}-{ngen}-{nbps}/{rep}/'
                    try:
                        astral_results_a.append(pd.read_csv(data_dir+f'{data_sets[1]}/'+model+'astral_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "+f'{data_sets[1]}/'+ model + "astral_branch_info.model_species_tree.csv")
                    try:
                        mpest_results_a.append(pd.read_csv(data_dir+f'{data_sets[1]}/'+model+'mpest_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "+f'{data_sets[1]}/'+model+"mpest_branch_info.model_species_tree.csv")
                    try:
                        trips_results_a.append(pd.read_csv(data_dir+f'{data_sets[1]}/'+model+'trips_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "+f'{data_sets[1]}/'+model+"trips_branch_info.model_species_tree.csv")

pd.concat(astral_results_a).to_csv('astral_results_combined_avian.csv')
pd.concat(mpest_results_a).to_csv('mpest_results_combined_avian.csv')
pd.concat(trips_results_a).to_csv('trips_results_combined_avian.csv')

# go through mammalian
astral_results_m = []
mpest_results_m = []
trips_results_m = []

for i in range(3):
    for scal in scales_m[i]:
        for ngen in ngens_m[i]:
            for nbps in nbpss_m[i]:
                for rep in reps:
                    model = f'{scal}.{ngen}.{nbps}/{rep}/'
                    try:
                        astral_results_m.append(pd.read_csv(data_dir+f'{data_sets[0]}/'+model+'astral_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "+f'{data_sets[0]}/'+model+'astral_branch_info.model_species_tree.csv')
                    try:
                        mpest_results_m.append(pd.read_csv(data_dir+f'{data_sets[0]}/'+model+'mpest_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "+f'{data_sets[0]}/'+model+'mpest_branch_info.model_species_tree.csv')
                    try:
                        trips_results_m.append(pd.read_csv(data_dir+f'{data_sets[0]}/'+model+'trips_branch_info.model_species_tree.csv'))
                    except (FileNotFoundError):
                        print("could not find: "f'{data_sets[0]}/'+model+'trips_branch_info.model_species_tree.csv')

pd.concat(astral_results_m).to_csv('astral_results_combined_mammalian.csv')
pd.concat(mpest_results_m).to_csv('mpest_results_combined_mammalian.csv')
pd.concat(trips_results_m).to_csv('trips_results_combined_mammalian.csv')

import argparse
import numpy as np
import treeswift
from math import comb
import sys


if __name__ == "__main__":
    '''
    This is how we handle loading the input dataset, running your functions, and outputting the results
    '''

    # parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--treefile',
                        required=True, type=str,
                        help="Input nexus file containing trees generated by MPEST")
    parser.add_argument('-o', '--output',
                        required=False, type=str, default='stdout',
                        help="Output file to write pseudo log-likelihood score")
    args = parser.parse_args()

    trees = treeswift.read_tree_nexus(args.treefile)

    max_key = ''
    max_val = -np.inf
    for key in trees['info'].keys():
        val =  float(trees['info'][key])
        if val > max_val:
            max_val = val
            max_key = key    

    #print(trees[max_key].newick())

    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    outfile.write('%s' % trees[max_key].newick())
    outfile.close()

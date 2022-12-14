import argparse
import numpy as np
import treeswift
from math import comb
import sys
from os.path import *

def correct(nexus):
    output = ''
    i = 0
    if isfile(expanduser(nexus)): # plain-text file
        f = open(expanduser(nexus))
        for l in f:
            if 'tree mpest' in l:
                output += l.replace('mpest',str(i))
                i += 1
            elif l.endswith(';\n'):
                output += l[:len(l)-2] + '\n;\n'
            else:
                output += l
    else:
        raise ValueError("could not find file")

    return output

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

    corrected = correct(args.treefile)


    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    outfile.write('%s' % corrected)
    outfile.close()
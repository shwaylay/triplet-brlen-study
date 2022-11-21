import argparse
import numpy as np
from treeswift import read_tree_newick
from math import comb
import sys

class ControlFile():
    def __init__(self, streefile, gtreefile):
        self.gtreefile = gtreefile
        self.stree = read_tree_newick(streefile)
        self.gtrees = []

        with open(gtreefile, 'r') as f:
            for line in f:
                self.gtrees.append(read_tree_newick(line))
        self.ngenes = len(self.gtrees)
    
    def generate_control_file(self):
        filetxt = f"""{self.gtreefile}
0
6950387
5
{self.ngenes} {self.stree.num_nodes(internal=False)}
"""
        for leaf in self.stree.traverse_leaves():
            filetxt += f"{leaf.get_label()} 1 {leaf.get_label()}\n"

        filetxt += "2\n"

        # set internal branch lengths to 0.1
        #for v in self.stree.traverse_internal():
         #   if not v.is_root():
          #      v.set_edge_length(0.1)
        # set external branch lengths to 1
        #for v in self.stree.traverse_leaves():
         #   v.set_edge_length(1)

        filetxt += self.stree.newick() + "\n"

        return filetxt


if __name__ == "__main__":
    '''
    This is how we handle loading the input dataset, running your functions, and outputting the results
    '''

    # parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-g', '--gtreefile',
                        required=True, type=str,
                        help="Input file containing gene trees (one newick string per line)")
    parser.add_argument('-s', '--streefile',
                        required=True, type=str,
                        help="Input file containing species tree (one newick string)")
    # parser.add_argument('-l', '--leaffile',
    #                     required=True, type=str,
    #                     help="Input file containing leaf labels, one per line")
    parser.add_argument('-o', '--output',
                        required=False, type=str, default='stdout',
                        help="Output file to write pseudo log-likelihood score")
    args = parser.parse_args()

    cfile = ControlFile(args.streefile, args.gtreefile)

    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    outfile.write('%s' % cfile.generate_control_file())
    outfile.close()

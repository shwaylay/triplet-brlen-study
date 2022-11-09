import argparse
import os
import treeswift
import sys


def main(args):
    cfile = args.output + ".control"
    gfile = args.output + ".trees"
    tfile = args.output + ".tre"

    labelset = set()

    # Rename gene trees
    with open(args.input, 'r') as fi, \
         open(gfile, 'w'):
        for line in fi:
            tree = treeswift.Tree(line)
 
            # Rename leaves
            for leaf in tree.traverse_leaves():
                leaf.label = "S" + leaf.label
                labelset.add(leaf.label)

            fo.write(tree)

    # Write MP-EST control file

    # Run MP-EST

    # Save best scoring tree



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mpest", type=str,
                        help="Path to MP-EST",
                        required=True)

    parser.add_argument("-i", "--input", type=str,
                        help="Input file containing gene trees "
                             "(one newick string per line)",
                        required=True)

    parser.add_argument("-o", "--output", type=str,
                        help="Output file containing species tree "
                             "(newick string)",
                        required=True)

    main(parser.parse_args())


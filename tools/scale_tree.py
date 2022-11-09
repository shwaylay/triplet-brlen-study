"""
Scale tree
Written by Erin K. Molloy (github: ekmolloy)
"""
import argparse
import dendropy
import sys


def main(args):
    taxa = dendropy.TaxonNamespace()
    tree = dendropy.Tree.get(path=args.input,
                             schema='newick',
                             taxon_namespace=taxa)

    for node in tree.preorder_node_iter():
        if node.edge.length is not None:
            elen = node.edge.length
            node.edge.length = args.scale * elen

    sys.stdout.write(tree.as_string(schema="newick")) #[5:]) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        help="Input newick string",
                        required=True)

    parser.add_argument("-s", "--scale", type=float,
                        help="Scale factor",
                        required=True)

    main(parser.parse_args())


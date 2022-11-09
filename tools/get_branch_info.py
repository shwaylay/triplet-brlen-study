"""
Grab branch info
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

    taxa = set([x.label for x in taxa])

    temp = args.header.split(',')
    head = temp[0:-1]
    mthd = temp[-1]
    cols = ["BIPA", "BIPB", mthd + "_BRLEN"]
    header = ','.join(head) + ',' + ','.join(cols) + '\n'
    sys.stdout.write(header)

    for node in tree.preorder_node_iter():
        bipA = set([x.taxon.label for x in node.leaf_nodes()])
        bipB = taxa.difference(bipA)

        if (len(bipA) > 1) and (len(bipB) > 1):
            bipA = ','.join(sorted(list(bipA)))
            bipB = ','.join(sorted(list(bipB)))
            tmp = sorted([bipA, bipB])

            if node.edge.length is not None:
                brln = str("%f" % float(node.edge.length))
            else:
                brln = "NA"

            sys.stdout.write("%s,\"%s\",\"%s\",%s\n" %
                             (args.prefix, tmp[0], tmp[1], brln))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        help="Input newick string",
                        required=True)

    parser.add_argument("-p", "--prefix", type=str,
                        help="Prefix",
                        required=True)

    parser.add_argument("-e", "--header", type=str,
                        help="Header",
                        required=True)

    main(parser.parse_args())


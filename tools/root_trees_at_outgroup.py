import argparse
import dendropy
import sys

def remove_branch_lengths(tree):
    for node in tree.preorder_node_iter():
        node.edge.length = None
        if node.is_leaf() == False:
            node.label = None

def unroot(tree):
    tree.is_rooted = False
    tree.collapse_basal_bifurcation(set_as_unrooted_tree=True)

def find_outgroup_node(tree, outgroup):
    if len(outgroup) == 1:
        og = outgroup[0]
        x = tree.find_node_with_taxon_label(og)
        if x is None:
            sys.exit("Outgroup %s does not exist in tree!" % og)
    else:
        sys.exit("TO DO: Need to implement the multi-taxon outgroup case!")

    return x


def root_at_outgroup(tree, outgroup):
    remove_branch_lengths(tree)

    unroot(tree)

    tree.is_rooted = True

    x = find_outgroup_node(tree, outgroup)
    tree.reroot_at_edge(x.edge,
                        update_bipartitions=False)
        

def main(args):
    outgroup = args.outgroup.split(',')

    if args.output is None:
        fo = sys.stdout
    else:
        fo = open(args.output, 'w')

    with open(args.input, 'r') as fi:

        for line in fi:
            taxa = dendropy.TaxonNamespace()
            tree = dendropy.Tree.get(string=line,
                                     schema='newick',
                                     taxon_namespace=taxa)

            root_at_outgroup(tree, outgroup)

            fo.write(tree.as_string(schema="newick")[5:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        help="Input file with one newick string per line",
                        required=True)

    parser.add_argument("-x", "--outgroup", type=str,
                        help="Comma separated list of outgroups",
                        required=True)

    parser.add_argument("-o", "--output", type=str,
                        help="Output file with one newick string per line",
                        required=False)

    main(parser.parse_args())


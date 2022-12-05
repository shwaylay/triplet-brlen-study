import argparse
import numpy as np
from treeswift import read_tree_newick
from math import comb
import sys

# I commented out all code that uses a leaf list since I don't think it's necessary
class EST():
    def __init__(self, streefile, gtreefile):
        self.stree = read_tree_newick(streefile)
        self.gtrees = []

        with open(gtreefile, 'r') as f:
            for line in f:
                self.gtrees.append(read_tree_newick(line))
        self.ngenes = len(self.gtrees)

        # Read leaf names (i.e., species) into a list
        # self.leaf_list = []
        # with open(lflatfile,'r') as f:
        #     for line in f.readlines():
        #         self.leaf_list.append(line[:-1])

        #self.nleaves = len(self.leaf_list)
        #self.ntrips = comb(self.nleaves, 3)

        #if self.nleaves != len(list(set(self.leaf_list))):
        #    sys.exit("Multiple leaves have the same label!")

        # self.leaf2indx = {}
        # for i, l in enumerate(self.leaf_list):
        #     self.leaf2indx[l] = i

        # for gtree in self.gtrees:
        #     self.index_tree(gtree, setbrln=True)
        # self.index_tree(self.stree)

        # TO DO: Check all trees are binary

        # Attributes to be computed
        #self.obs_trip = np.zeros(self.ntrips * 3, dtype=int)    # Observed triplets in gene trees
        #self.exp_trip = np.zeros(self.ntrips * 3, dtype=float)  # Branch lengths in model species tree
        self.pllk = 0.0                                            # Pseudolikelihood score


    # def index_tree(self, tree, setbrln=False):
    #     """
    #     This function is to label each node in a tree
    #     with an index so that there is partial order.

    #     Specifically, for two vertices x and y, 
    #     x.index < y.index means that 
    #     x is at the same depth as y or is deeper than y
    #     in the tree.
    #     """
    #     index = self.nleaves
    #     for node in tree.traverse_postorder():
    #         if node.is_leaf():
    #             node.index = self.leaf2indx[node.label]
    #         else:
    #             node.index = index
    #             index += 1
    #         if setbrln:
    #             node.edge_length = 1.0

    # returns A,B,C such that A is set of leaves in u.left, B is set of leaves in u.right, and C is set of leaves in u.sibling
    #might want to do post order traversal instead'
    #maintain list of nodes bellow a node
    #NOTE: right now just handling branches between two nodes (not branches that span multiple)
    def get_tripart(self, u):
        #u is root
        if u.is_root():
            return None
        
        children = u.child_nodes()
        #u does not have two children
        #u does not have any children
        if len(children) < 2:
            return None
        
        A = [x.get_label() for x in children[0].traverse_leaves()]
        B = [x.get_label() for x in children[1].traverse_leaves()]
        parent = u.get_parent()

        #u does not have any siblings
        if len(parent.child_nodes()) < 2:
            return None

        sibling = parent.child_nodes()[0] if parent.child_nodes()[0] != u else parent.child_nodes()[1]
        C = [x.get_label() for x in sibling.traverse_leaves()]

        return A,B,C

    # t-> gene tree
    # A,B,C-> set of all leaves in A,B,C in species tree around branch Q respectively
    def count_trips(self, t, A, B, C):
        Vmap = dict() #probs could change to more efficient data structure

        def V(u):
            if u == None:
                return np.array([0,0,0])
            else:
                return Vmap[u]
    
        trips = dict()
        for u in t.traverse_postorder():
            if u.is_leaf():
                s = u.get_label()
                Vmap[u] = np.array([1 if s in A else 0,
                        1 if s in B else 0,
                        1 if s in C else 0])
                trips[u] = 0
            else:
                #assign left and right children and grandchildren
                #if child does not exist, assign None
                children = u.child_nodes()
                l = None if len(children) < 1 else children[0]
                r = None if len(children) < 2 else children[1]
                lchildren = l.child_nodes()
                ll = None if len(lchildren) < 1 else lchildren[0]
                lr = None if len(lchildren) < 2 else lchildren[1]
                rchildren = r.child_nodes()
                rl = None if len(rchildren) < 1 else rchildren[0]
                rr = None if len(rchildren) < 2 else rchildren[1]
                Vmap[u] = V(l) + V(r)
                #enumerate all possible triplet cases
                trips[u] = trips[l] + trips[r] + \
                           V(ll)[0]*V(lr)[1]*V(r)[2] + \
                           V(lr)[0]*V(ll)[1]*V(r)[2] + \
                           V(ll)[0]*V(ll)[1]*V(r)[2] + \
                           V(lr)[0]*V(lr)[1]*V(r)[2] + \
                           V(rl)[0]*V(rr)[1]*V(l)[2] + \
                           V(rr)[0]*V(rl)[1]*V(l)[2] + \
                           V(rl)[0]*V(rl)[1]*V(l)[2] + \
                           V(rr)[0]*V(rr)[1]*V(l)[2]
        return trips[t.root]
                


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
    # estimator = EST(args.streefile, args.gtreefile, args.leaffile)
    # score = estimator.pseudolikelihood()

    # # Run code and output score
    # if (not isinstance(score, float) and not isinstance(score, int)) or score > 0:
    #     raise ValueError('ERROR_SCORE')

    # if args.output == 'stdout':
    #     from sys import stdout as outfile
    # else:
    #     outfile = open(args.output,'w')

    # outfile.write('%s\n' % str(score))
    # outfile.close()

    #'Hardcoded' example
    estimator = EST(args.streefile, args.gtreefile)

    for n in estimator.stree.traverse_postorder(leaves=False):
        if not n.is_root():
            f1 = 0
            f2 = 0
            f3 = 0
            for g in estimator.gtrees:
                ABC = estimator.get_tripart(n)
                if ABC != None:
                    A,B,C = ABC
                    f1 = f1 + estimator.count_trips(g,A,B,C)
                    f2 = f2 + estimator.count_trips(g,A,C,B)
                    f3 = f3 + estimator.count_trips(g,B,C,A)

            f_total = f1 + f2 + f3
            if f_total == 0:
                q1,q2,q3,d = 0,0,0,0
            else:
                q1 = f1/f_total
                q2 = f2/f_total
                q3 = f3/f_total
                if q1 == 1: # since ln(0) is not doable
                    q1 = .999
                d = (-1)*np.log(((3/2)*(1-q1))) #note np.log does natural log by default
            label = "\'[q1=" + str(q1) + ";" + \
                    "q2=" + str(q2) + ";" + \
                    "q3=" + str(q3) + ";" + \
                    "f1=" + str(f1) + ";" + \
                    "f2=" + str(f2) + ";" + \
                    "f3=" + str(f3) + "]\'"
            n.set_label(label)
            n.set_edge_length(d)

    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    outfile.write('%s' % estimator.stree.newick())
    outfile.close()

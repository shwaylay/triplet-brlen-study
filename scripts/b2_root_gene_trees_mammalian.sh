#!/bin/bash

SCAL=$1
NGEN=$2
NBPS=$3
REPL=$4

MODL="$SCAL.$NGEN.$NBPS"
MYMODL="$SCAL,$NGEN,$NBPS,$REPL"

# Define directories
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJECTDIR="$GROUPDIR/msuehle/triplet-brlen-study"

# Define software and related tools
REROOT="$PROJECTDIR/tools/root_trees_at_outgroup.py"

# Define input files
INDIR="$GROUPDIR/group/data/mahbub2021wqfm/37-taxon-mammalian-simulated/$MODL/$REPL"
INPUT="$INDIR/all_gt.tre"
if [ ! -e $INPUT ]; then
    exit
fi

# Define output files
OUTDIR="$PROJECTDIR/data/mahbub2021wqfm/37-taxon-mammalian-simulated/$MODL/$REPL"
OUTPUT="$OUTDIR/rooted_gene_trees.tre"

if [ ! -e $OUTPUT ]; then
    if [ $NBPS == "true" ]; then
        cp $INPUT $OUTPUT
    else
        /opt/local/stow/Python3-3.6.0/bin/python3 \
        $REROOT -i $INPUT \
                -x "GAL" \
                -o $OUTPUT
    fi
fi


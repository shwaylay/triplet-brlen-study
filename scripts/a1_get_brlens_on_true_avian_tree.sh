#!/bin/bash

exit

# Define directories
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJECTDIR="$GROUPDIR/msuehle/triplet-brlen-study"

# Define software and related tools
SCALETR="$PROJECTDIR/tools/scale_tree.py"
GETBRLN="$PROJECTDIR/tools/get_branch_info.py"

# Define input / output files
INDIR="$GROUPDIR/group/data/mahbub2021wqfm/48-taxon-avian-simulated"
OUTDIR="$PROJECTDIR/data/mahbub2021wqfm/48-taxon-avian-simulated"

INPUT="$INDIR/true_tree_trimmed"
if [ ! -e $INPUT ]; then
    exit
fi
OUTPUT="$OUTDIR/model_species_tree_none.tre"
if [ ! -e $OUTPUT ]; then
    cp $INPUT $OUTPUT
fi

INPUT="$INDIR/True.tree"
if [ ! -e $INPUT ]; then
    exit
fi

SNAMS=( "0.5X" "1X" "2X" )
SVALS=( "0.5" "1.0" "2.0" )

for i in 0 1 2; do
    SNAM=${SNAMS[$i]}
    SVAL=${SVALS[$i]}

    echo $SNAM
    echo $SVAL

    # Scale model species tree
    OUTPUT="$OUTDIR/model_species_tree_${SNAM}.tre"
    if [ ! -e $OUTPUT ]; then
        /opt/local/stow/Python3-3.6.0/bin/python3 $SCALETR \
            --input $INPUT \
            --scale $SVAL &> $OUTPUT
    fi

    # Get branch lengths
    MYCSV="$OUTDIR/model_branch_info.model_species_tree_${SNAM}.csv"
    if [ ! -e $MYCSV ]; then
        # Extract branch length info
        /opt/local/stow/Python3-3.6.0/bin/python3 $GETBRLN \
            --input $OUTPUT \
            --prefix "TRUE,$SNAM" \
            --header "TREE,SCAL,TRUE" &> $MYCSV
    fi
done


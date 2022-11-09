#!/bin/bash

SCAL=$1
NGEN=$2
NBPS=$3
REPL=$4

MODL="$SCAL-$NGEN-$NBPS"
MYMODL="$SCAL,$NGEN,$NBPS,$REPL"

# Define directories
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJECTDIR="$GROUPDIR/msuehle/triplet-brlen-study"

# Define software and related tools
ASTRAL3DIR="$GROUPDIR/group/software/ASTRAL_v5.7.8/Astral"
ASTRAL3=astral.5.7.8.jar
MPEST="$GROUPDIR/group/software/mp-est_v2.1/src/mpest"
# ToDo: Add paths to other methods

# Define input and output files
DIR="$PROJECTDIR/data/mahbub2021wqfm/48-taxon-avian-simulated/$MODL/$REPL"

GTRE_FILE="$DIR/rooted_gene_trees.tre"
if [ ! -e $GTRE_FILE ]; then
    exit
fi
STRE_FILE="$DIR/../../model_species_tree_none.tre"
if [ ! -e $STRE_FILE ]; then
    exit
fi

# Estimate branch lengths in true species tree

# Run ASTRAL
OUTPUT="$DIR/astral_scored.model_species_tree.tre"
if [ ! -e $OUTPUT ]; then
    java -D"java.library.path=$ASTRAL3DIR/lib" \
         -jar $ASTRAL3DIR/$ASTRAL3 \
         -q $STRE_FILE \
         -t2 \
         -i $GTRE_FILE \
         -o $OUTPUT
fi

#ToDo: Run MP-EST

#ToDo: Run other methods


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
PYTHON="$PROJECTDIR/tools/msuehle/bin/python"

# Define software and related tools
GETBRLN="$PROJECTDIR/tools/get_branch_info.py"
GETBRLN_ASTRAL="$PROJECTDIR/tools/get_astral_t2_branch_info.py"
GETBRLN_TRIPS="$PROJECTDIR/tools/get_trips_branch_info.py"

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

# Run ASTRAL
INPUT="$DIR/astral_scored.model_species_tree.tre"
OUTPUT="$DIR/astral_branch_info.model_species_tree.csv"
if [ -e $INPUT ] && [ ! -e $OUTPUT ]; then
    # Extract branch length info
     $PYTHON $GETBRLN_ASTRAL \
         --input $INPUT \
         --prefix "$MYMODL,TRUE" \
         --header "SCAL,NGEN,NBPS,REPL,TREE" &> $OUTPUT
fi

#similar code for MP-EST
INPUT="$DIR/mpest_scored.model_species_tree.tre"
OUTPUT="$DIR/mpest_branch_info.model_species_tree.csv"
if [ -e $INPUT ] && [ ! -e $OUTPUT ]; then
    # Extract branch length info
     $PYTHON $GETBRLN_TRIPS \
         --input $INPUT \
         --prefix "$MYMODL,TRUE" \
         --header "SCAL,NGEN,NBPS,REPL,TREE" &> $OUTPUT
fi


#ToDo: Add similar code for your methods
#Trips
INPUT="$DIR/trips_scored.model_species_tree.tre"
OUTPUT="$DIR/trips_branch_info.model_species_tree.csv"
if [ -e $INPUT ] && [ ! -e $OUTPUT ]; then
    # Extract branch length info
     $PYTHON $GETBRLN_TRIPS \
         --input $INPUT \
         --prefix "$MYMODL,TRUE" \
         --header "SCAL,NGEN,NBPS,REPL,TREE" &> $OUTPUT
fi


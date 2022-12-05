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
PYTHON="$PROJECTDIR/tools/msuehle/bin/python"
TRIPS="$PROJECTDIR/tools/compute_triplets.py"
# MPEST tools
GETCONTROL="$PROJECTDIR/tools/generate_control_file.py"
CORRECT="$PROJECTDIR/tools/correct_MPEST.py"
REFORMAT="$PROJECTDIR/tools/reformat_MPEST.py"

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

# Run MP-EST
OUTPUT="$DIR/mpest_scored.model_species_tree.tre"
CONTROL_FILE="${OUTPUT}-control"
NEW_GTRE_FILE="rooted_gene_trees.tre"
cp $GTRE_FILE $NEW_GTRE_FILE

if [ ! -e $OUTPUT ]; then
    # Make control file
    $PYTHON $GETCONTROL \
	-g $NEW_GTRE_FILE \
	-s $STRE_FILE \
	-o $CONTROL_FILE

    # Run MPEST
    $MPEST $CONTROL_FILE

    # Correct MPEST output
    MPESTOUT="${DIR}/MPESTout.txt"
    $PYTHON $CORRECT -t ${NEW_GTRE_FILE}_besttree.tre -o $MPESTOUT

    # Reformat the corrected file
    $PYTHON $REFORMAT -t $MPESTOUT -o $OUTPUT

    rm $CONTROL_FILE
    rm $MPESTOUT
    rm ${GTRE_FILE}_besttree.tre
    rm $NEW_GTRE_FILE
fi

# Run Trips
OUTPUT="$DIR/trips_scored.model_species_tree.tre"
if [ ! -e $OUTPUT ]; then
    $PYTHON $TRIPS -g $GTRE_FILE \
	           -s $STRE_FILE \
	           -o $OUTPUT
fi


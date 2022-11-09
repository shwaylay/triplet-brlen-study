#!/bin/bash

exit

# Mammalian simulated data set

for DO in 1 2 3; do

if [ $DO -eq 1 ]; then
    # (a) varying ILS
    SCALS=( "noscale" "scale2d" "scale2u" )
    NGENS=( "200g" )
    NBPSS=( "500b" )
elif [ $DO -eq 2 ]; then
    # (b) varying sequence length
    SCALS=("noscale" )
    NGENS=( "200g" )
    NBPSS=( "250b" "1000b" "1500b" "true" )
elif [ $DO -eq 3 ]; then
    # (c) varying number of genes
    SCALS=( "noscale" )
    NGENS=( "25g" "50g" "100g" "400g" "800g" )
    NBPSS=( "500b" )
else
    exit
fi

REPLS=( $(seq -f "R%g" 1 20) )

for SCAL in ${SCALS[@]}; do
    for NGEN in ${NGENS[@]}; do
        for NBPS in ${NBPSS[@]}; do
            MODL="${SCAL}.${NGEN}.${NBPS}"
            for REPL in ${REPLS[@]}; do

            echo "Submitting $MODL/$REPL..."
            sbatch \
                --job-name="b2.$MODL.$REPL" \
                --output="b2.$MODL.$REPL.%j.out" \
                --error="b2.$MODL.$REPL.%j.err" \
                --export=SCAL="$SCAL",NGEN="$NGEN",NBPS="$NBPS",REPL="$REPL" \
            b2_drive.sbatch
            done
        done
    done
done
done


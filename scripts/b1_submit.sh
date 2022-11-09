#!/bin/bash

exit

# Avian simulated data set

for DO in 1 2; do

if [ $DO -eq 1 ]; then
    # (a) and (d)
    SCALS=( "0.5X" "1X" "2X" )
    NGENS=( 1000 )
    NBPSS=( "true" 500 )
elif [ $DO -eq 2 ]; then
    # (b) and (c)
    SCALS=( "1X" )
    NGENS=( 50 100 200 500 )
    NBPSS=( "true" 500 )
else
    exit
fi

REPLS=( $(seq -f "R%g" 1 20) )

for SCAL in ${SCALS[@]}; do
    for NGEN in ${NGENS[@]}; do
        for NBPS in ${NBPSS[@]}; do
            MODL="${SCAL}-${NGEN}-${NBPS}"
            for REPL in ${REPLS[@]}; do

            echo "Submitting $MODL/$REPL..."
            sbatch \
                --job-name="b1.$MODL.$REPL" \
                --output="b1.$MODL.$REPL.%j.out" \
                --error="b1.$MODL.$REPL.%j.err" \
                --export=SCAL="$SCAL",NGEN="$NGEN",NBPS="$NBPS",REPL="$REPL" \
            b1_drive.sbatch
            done
        done
    done
done
done

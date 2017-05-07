#!/bin/bash

for Ch in {0..7};do

    for Clip_sel in {1..3}; do

	for Att in {0..15}; do

	    python Plot_Vin_Vout.py -Att $Att -Clip_sel $Clip_sel -Ch $Ch

	done
    done
done
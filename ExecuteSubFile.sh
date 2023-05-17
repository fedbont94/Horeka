#!/bin/sh
sbatch -p multiple SubFile.sub
# sbatch --partition=accelerated -A hk-project-pevradio SubFile.sub
# --ntasks-per-node=31 
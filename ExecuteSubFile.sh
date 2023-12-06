#!/bin/sh
sbatch --partition=cpuonly -A hk-project-pevradio SubFile.sub 4.9 6.6
# sbatch --partition=cpuonly -A hk-project-pevradio SubFile.sub 6.5 6.5
sbatch --partition=cpuonly -A hk-project-pevradio SubFile.sub 6.7 6.9

# sbatch --partition=accelerated -A hk-project-pevradio SubFile.sub

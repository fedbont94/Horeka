#!/bin/sh
sbatch -p cpuonly --ntasks-per-node=76 -A hk-project-radiohfi SubFile.sub
# --ntasks-per-node=31 
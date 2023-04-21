#!/bin/sh
sbatch --partition=cpuonly -A hk-project-radiohfi SubFile.sub
# sbatch --partition=accelerated -A hk-project-pevradio SubFile.sub
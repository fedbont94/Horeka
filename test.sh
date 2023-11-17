#!/bin/sh
partition=$(squeue -h -j ${SLURM_JOB_ID} -o "%P")
echo "Slurm partition: $partition"

if [ $partition=cpuonly ]
then
    echo "Running on CPU partition"
fi
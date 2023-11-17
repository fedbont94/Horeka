#!/bin/sh
if [ "$1" = "clsim" ]
then
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub
else
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub
fi

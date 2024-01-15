#!/bin/sh
if [ "$1" = "clsim" ]
then
    echo "Submitting clsim jobs on GPU nodes"
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.0
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.1
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.2
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.3
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.4
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.5
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.6
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.7
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.8
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 5.9
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.0
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.1
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.2
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.3
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.4
    sbatch -A hk-project-pevradio --partition=accelerated --gres=gpu:4 SubFile.sub 6.5
else
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.0
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.1
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.2
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.3
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.4
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.5
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.6
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.7
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.8
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 5.9
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.0
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.1
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.2
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.3
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.4
    sbatch -A hk-project-pevradio --partition=cpuonly SubFile.sub 6.5
fi

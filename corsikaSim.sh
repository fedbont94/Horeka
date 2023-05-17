#!/bin/bash

# source /home/hk-project-pevradio/rn8463/.bashrc
module load compiler/gnu/10.2
module load mpi/openmpi/4.1
PYTHON=/home/kit/ikp/bg5912/virtual_env/bin/python3
SCRIPT=/home/kit/ikp/bg5912/Horeka_Jelena/MakeCorsikaSim.py

#TODO Make sure this is the right corsika path
cd /home/kit/ikp/bg5912/work/soft/corsika-77420/run/

#TODO Make sure to change the parameters correctly. Documentation in the args of MakeCorsikaSim.py
# specifically:
#TODO check paths in dirSimulations and logDirProcesses
#TODO check corsikaExe
$PYTHON $SCRIPT \
                --username bg5912 \
                --primary 14 \
                --dataset 14000.0 \
                --dirSimulations "/home/kit/ikp/bg5912/work/sims/GRAND/mpitest/sim_storage/" \
                --pathCorsika "/home/kit/ikp/bg5912/work/soft/corsika-77420/run/" \
                --corsikaExe "/mpi_corsika77420Linux_SIBYLL_urqmd_thin_coreas_parallel_runner" \
                --startNumber 0 \
                --endNumber 10 \
                --energyStart 8.0 \
                --energyEnd 8.1 \
                --energyStep 0.1 \
                --azimuthStart 0.00000000 \
                --azimuthEnd 0.0000000 \
                --zenithStart 0.00000000 \
                --zenithEnd 0.00000000 \
                --obslev 200 \
                --logDirProcesses "/home/kit/ikp/bg5912/work/sims/GRAND/mpitest/logs/" \
                --parallelSim 1

# "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/" \
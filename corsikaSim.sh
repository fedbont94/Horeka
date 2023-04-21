#!/bin/bash

# source /home/hk-project-pevradio/rn8463/.bashrc

PYTHON=/home/hk-project-radiohfi/bg5912/virtual_env/bin/python3
SCRIPT=/home/hk-project-radiohfi/bg5912/Horeka/MakeCorsikaSim.py

#TODO Make sure this is the right corsika path
cd /home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/

#TODO Make sure to change the parameters correctly. Documentation in the args of MakeCorsikaSim.py
# specifically:
#TODO check paths in dirSimulations and logDirProcesses
#TODO check corsikaExe
$PYTHON $SCRIPT \
                --username bg5912 \
                --primary 14 \
                --dataset 14000.0 \
                --dirSimulations "/home/hk-project-radiohfi/bg5912/work/sims/GRAND/mpitest/sim_storage/" \
                --pathCorsika "/home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/" \
                --corsikaExe "./mpi_corsika77420Linux_SIBYLL_urqmd_thin_coreas_parallel_runner" \
                --startNumber 0 \
                --endNumber 10 \
                --energyStart 10.7 \
                --energyEnd 11.0 \
                --energyStep 0.1 \
                --azimuthStart 0.00000000 \
                --azimuthEnd 359.9900000 \
                --zenithStart 70.00000000 \
                --zenithEnd 70.00000000 \
                --obslev 126400 \
                --logDirProcesses "/home/hk-project-radiohfi/bg5912/work/sims/GRAND/proton_test_gp13+stshp/logs/" \
                --parallelSim 1

# "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/" \
#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

PYTHON=/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeCorsikaSim.py

#TODO Make sure this is the right corsika path
cd /home/hk-project-pevradio/rn8463/corsika/corsika-77420/run/

#TODO Make sure to change the parameters correctly. Documentation in the args of MakeCorsikaSim.py
$PYTHON $SCRIPT \
                --username rn8463 \
                --primary 1 \
                --dataset 14000.0 \
                --dirSimulations "/home/hk-project-pevradio/rn8463/testCorsika/" \
                --pathCorsika "/home/hk-project-pevradio/rn8463/corsika/corsika-77420/run/" \
                --corsikaExe "corsika77420Linux_SIBYLL_flukainfn" \
                --startNumber 0 \
                --endNumber 1000 \
                --energyStart 4.0 \
                --energyEnd 8.0 \
                --energyStep 0.1 \
                --azimuthStart 0.00000000 \
                --azimuthEnd 359.99000000 \
                --zenithStart 0.00000000 \
                --zenithEnd 65.0000000 \
                --logDirProcesses "/home/hk-project-pevradio/rn8463/logCorsikaGamma4/" \
                --parallelSim 1

# "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/" \
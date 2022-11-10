#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc
cd /home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/

PYTHON=/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/corsika_simulations/MakeCorsikaSim.py

$PYTHON $SCRIPT \
                --username rn8463 \
                --primary 1 \
                --dataset 13400.0 \
                --dirSimulations "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/" \
                --pathCorsika "/home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/" \
                --corsikaExe "corsika77401Linux_SIBYLL_fluka" \
                --startNumber 0 \
                --endNumber 1000 \
                --energyStart 5.0 \
                --energyEnd 7.0 \
                --energyStep 0.1 \
                --azimuthStart 0.00000000 \
                --azimuthEnd 359.99000000 \
                --zenithStart 0.00000000 \
                --zenithEnd 65.0000000 \
                --logDirProcesses "/home/hk-project-pevradio/rn8463/logCorsikaGamma/" \
                --parallelSim 100
#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

ENV=/home/hk-project-pevradio/rn8463/icetray/build/env-shell.sh
PYTHON=/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeDetectorResponse.py

$ENV $PYTHON $SCRIPT \
                -inDirectory "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/data/" \
                -outDirectory "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/" \
                -pythonPath "/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3" \
                -detector "IC86" \
                -GCD "/lsdf/kit/ikp/projects/IceCube/sim/GCD/GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz" \
                -year "2012" \
                -MCdataset 13400 \
                -dataset 12012 \
                -seed 1201200000 \
                -doLv3 \
                -doFiltering \
                -energyStart 5.0 \
                -energyEnd 5.1 \
                -energyStep 0.1 \
                -logDirProcesses "/home/hk-project-pevradio/rn8463/logDetResponse/" \
                -parallelSim 1 \
                --photonDirectory "/lsdf/kit/ikp/projects/IceCube/sim/photon-tables/" \
                --NumbSamples 100 \
                --NumbFrames 0 \
                --ITSG_ExtraOptions "" \
                --clsim_ExtraOptions "" \
                --DET_ExtraOptions "" \
                --LV1_ExtraOptions "" \
                --LV2_ExtraOptions "" \
                --LV3_ExtraOptions "" \
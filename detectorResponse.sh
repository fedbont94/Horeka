#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

ENV=/home/hk-project-pevradio/rn8463/icetray/build/env-shell.sh
PYTHON=/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeDetectorResponse.py

$ENV $PYTHON $SCRIPT \
                -inDirectory "/home/hk-project-pevradio/rn8463/gamma_simulations/corsika/data/" \
                -outDirectory "/home/hk-project-pevradio/rn8463/gamma_simulations/detector_response/" \
                -pythonPath "/hkfs/home/project/hk-project-pevradio/rn8463/virtual_env/bin/python3" \
                -detector "IC86" \
                -GCD "/hkfs/home/project/hk-project-pevradio/rn8463/GCDs/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz" \
                -year "2012" \
                -MCdataset 14000 \
                -dataset 12012 \
                -seed 1201200000 \
                -doLv3 \
                -doFiltering \
                -energyStart 6.0 \
                -energyEnd 6.1 \
                -energyStep 0.1 \
                -logDirProcesses "/home/hk-project-pevradio/rn8463/logDetResponse/" \
                -parallelSim 1 \
                --photonDirectory "/home/hk-project-pevradio/rn8463/photon-tables/" \
                --NumbSamples 100 \
                --NumbFrames 0 \
                --ITSG_ExtraOptions "" \
                --clsim_ExtraOptions "" \
                --DET_ExtraOptions "" \
                --LV1_ExtraOptions "" \
                --LV2_ExtraOptions "" \
                --LV3_ExtraOptions "" \

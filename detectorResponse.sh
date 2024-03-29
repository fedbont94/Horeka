#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

# This is used for the generated folders file. So all the detector ones and in-ice
environment1="/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-env /home/hk-project-pevradio/rn8463/icetray/build/"
# This is used for the filtered folders file. So all the lv1, lv2
environment2="/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/icetray-env combo/V01-01-06"
# Lv3 enviroment 
environment3="/home/hk-project-pevradio/rn8463/icetray/build/env-shell.sh"

ENV=/home/hk-project-pevradio/rn8463/icetray/build/env-shell.sh

PYTHON=/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/RHEL_7_x86_64/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeDetectorResponse.py

############### Generated #####################
# $ENV $TRAY $PYTHON $SCRIPT \
# $environment1 $PYTHON $SCRIPT \
#                 -inDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/corsika/data/" \
#                 -outDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/detector_response/" \
#                 -pythonPath $PYTHON \
#                 -detector "IC86" \
#                 -GCD "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz" \
#                 -year "2012" \
#                 -MCdataset 14000 \
#                 -dataset 12012 \
#                 -seed 1201200000 \
#                 -doFiltering \
#                 -energyStart 5.0 \
#                 -energyEnd 6.0 \
#                 -energyStep 0.1 \
#                 -logDirProcesses "/home/hk-project-pevradio/rn8463/log/logDetResponse5060/" \
#                 -parallelSim 100 \
#                 --photonDirectory "/cvmfs/icecube.opensciencegrid.org/data/photon-tables/" \
#                 --NumbSamples 200 \
#                 --NumbFrames 0 \
#                 --doITSG \
#                 --doDET 

                # --doCLSIM \


############### Filtered Lv1 and Lv2 #####################
# $ENV $TRAY $PYTHON $SCRIPT \
$environment2 $PYTHON $SCRIPT \
                -inDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/corsika/data/" \
                -outDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/detector_response/" \
                -pythonPath $PYTHON \
                -detector "IC86" \
                -GCD "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz" \
                -year "2012" \
                -MCdataset 14000 \
                -dataset 12012 \
                -seed 1201200000 \
                -doFiltering \
                -energyStart 5.4 \
                -energyEnd 6.0 \
                -energyStep 0.1 \
                -logDirProcesses "/home/hk-project-pevradio/rn8463/log/logDetResponse5460lv2/" \
                -parallelSim 1 \
                --photonDirectory "/cvmfs/icecube.opensciencegrid.org/data/photon-tables/" \
                --NumbSamples 300 \
                --NumbFrames 0 \
                --doITSG \
                --doDET \
                --doLV1 \
                --doLV2 


# ############### Filtered Lv3 #####################
# # $ENV $TRAY $PYTHON $SCRIPT \
# eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`
# $environment3 $PYTHON $SCRIPT \
#                 -inDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/corsika/data/" \
#                 -outDirectory "/hkfs/work/workspace/scratch/rn8463-gamma_simulations/detector_response/" \
#                 -pythonPath $PYTHON \
#                 -detector "IC86" \
#                 -GCD "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz" \
#                 -year "2012" \
#                 -MCdataset 14000 \
#                 -dataset 12012 \
#                 -seed 1201200000 \
#                 -doFiltering \
#                 -energyStart 5.0 \
#                 -energyEnd 6.0 \
#                 -energyStep 0.1 \
#                 -logDirProcesses "/home/hk-project-pevradio/rn8463/logDetResponseTest/" \
#                 -parallelSim 1 \
#                 --photonDirectory "/cvmfs/icecube.opensciencegrid.org/data/photon-tables/" \
#                 --NumbSamples 100 \
#                 --NumbFrames 0 \
#                 --doITSG \
#                 --doDET \
#                 --doLV1 \
#                 --doLV2 \
#                 --doLV3 

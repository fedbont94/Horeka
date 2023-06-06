#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

# This is used for the generated folders file. So all the detector ones and in-ice
environment1="/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-env /home/hk-project-pevradio/rn8463/icetray/build/"
# This is used for the filtered folders file. So all the lv1, lv2
environment2="/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/icetray-env combo/V01-01-06"
# Lv3 enviroment 
environment3="/home/hk-project-pevradio/rn8463/icetray/surfacearray/build/env-shell.sh"

# Python and script
PYTHON=/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/RHEL_7_x86_64/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeDetectorResponse.py

# Fixed parameters
inDirectory="/hkfs/work/workspace/scratch/rn8463-gammaCorsikaTankScint/data/"
outDirectory="/hkfs/work/workspace/scratch/rn8463-gammaDetectorTankScint"
i3build="/home/hk-project-pevradio/rn8463/icetray/surfacearray/build/"
detector="IC86"
GCD="/home/hk-project-pevradio/rn8463/GCD/GCD_Base2021.Run135903.T00S1.Pass2_V1b_Snow2025_6ScintSTA.i3.bz2"
year="2025"
MCdataset=202500
dataset=12025
seed=1202500000
energyStep=0.1
NumbSamples=100

#################################### TODO ####################################
# Energy range for the detector response
energyStart=4.0
energyEnd=4.1

# Parallelization
parallelSim=1
logDirProcesses="/home/hk-project-pevradio/rn8463/log/logTest/"
#################################### TODO ####################################

############### Generated #####################
$environment3 $PYTHON $SCRIPT \
                -inDirectory $inDirectory \
                -outDirectory $outDirectory \
                -pythonPath $PYTHON \
                -i3build $i3build \
                -detector $detector \
                -GCD $GCD \
                -year $year \
                -MCdataset $MCdataset \
                -dataset $dataset \
                -seed $seed \
                -energyStart $energyStart \
                -energyEnd $energyEnd \
                -energyStep $energyStep \
                -logDirProcesses $logDirProcesses \
                -parallelSim $parallelSim \
                --NumbSamples $NumbSamples \



# eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`
# $environment3 $PYTHON $SCRIPT \
#                 -inDirectory $inDirectory \
#                 -outDirectory $outDirectory \
#                 -pythonPath $PYTHON \
#                 -detector $detector \
#                 -GCD $GCD \
#                 -year $year \
#                 -MCdataset $MCdataset \
#                 -dataset $dataset \
#                 -seed $seed \
#                 -energyStart $energyStart \
#                 -energyEnd $energyEnd \
#                 -energyStep $energyStep \
#                 -logDirProcesses $logDirProcesses \
#                 -parallelSim $parallelSim \
#                 --photonDirectory $photonDirectory \
#                 --NumbSamples $NumbSamples \
#                 --NumbFrames $NumbFrames \
#                 -doFiltering \
#                 --doITSG \
#                 --doDET \
#                 --doLV1 \
#                 --doLV2 \
#                 --doLV3 

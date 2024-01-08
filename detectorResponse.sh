#!/bin/bash

source /home/hk-project-pevradio/rn8463/.bashrc

# This is used for the generated folders file. So all the detector ones and in-ice
environment1="/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-env /home/hk-project-pevradio/rn8463/icetray/build/"
# This is used for the filtered folders file. So all the lv1, lv2
environment2="/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/icetray-env combo/V01-01-06"
# Lv3 enviroment 
environment3="/home/hk-project-pevradio/rn8463/icetray/build/env-shell.sh"

# Python and script
PYTHON=/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/RHEL_7_x86_64/bin/python3
SCRIPT=/home/hk-project-pevradio/rn8463/simulations_scripts/MakeDetectorResponse.py

# Fixed parameters
inDirectory="/hkfs/work/workspace/scratch/rn8463-proton-corsika/data/"
outDirectory="/hkfs/work/workspace/scratch/rn8463-proton_DetectorResponseITonly/2012/"
detector="IC86"
GCD="/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz"
year="2012"
MCdataset=14001
dataset=12012
seed=1201200000
energyStep=0.1
photonDirectory="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/"
NumbSamples=100
NumbFrames=0

#################################### TODO ####################################
# Energy range for the detector response
energyStart=${1}
energyEnd=${1}

# Parallelization
parallelSim=100
logDirProcesses="/home/hk-project-pevradio/rn8463/log/DetProtonExtended/"
#################################### TODO ####################################


################ doITSG #####################
# $environment1 $PYTHON $SCRIPT \
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
#                 --doITSG 

############### doCLSIM #####################
# $environment1 $PYTHON $SCRIPT \
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
#                 -parallelSim 1 \
#                 --photonDirectory $photonDirectory \
#                 --NumbSamples $NumbSamples \
#                 --NumbFrames $NumbFrames \
#                 -doFiltering \
#                 --doCLSIM # --doInIceBg 
                

################ doDET #####################
# $environment1 $PYTHON $SCRIPT \
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
#                 -parallelSim 1 \
#                 --photonDirectory $photonDirectory \
#                 --NumbSamples $NumbSamples \
#                 --NumbFrames $NumbFrames \
#                 -doFiltering \
#                 --doDET 


# # ############### Filtered Lv1 and Lv2 #####################
# $environment2 $PYTHON $SCRIPT \
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
#                 -parallelSim 50 \
#                 --photonDirectory $photonDirectory \
#                 --NumbSamples $NumbSamples \
#                 --NumbFrames $NumbFrames \
#                 -doFiltering \
#                 --doLV1 \
#                 --doLV2 

############### Filtered Lv3 #####################
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`
$environment3 $PYTHON $SCRIPT \
                -inDirectory $inDirectory \
                -outDirectory $outDirectory \
                -pythonPath $PYTHON \
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
                -parallelSim 1 \
                --photonDirectory $photonDirectory \
                --NumbSamples $NumbSamples \
                --NumbFrames $NumbFrames \
                -doFiltering \
                --doLV3 
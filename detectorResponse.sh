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
inDirectory="/hkfs/work/workspace/scratch/mk9399-corsika_sibyll23d/datasets/gamma_14000/data/"
outDirectory="/hkfs/work/workspace/scratch/rn8463-gamma_simulations/detector_response/"
detector="IC86"
GCD="/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.Run120844.T00S1.Pass2_V1b_Snow121021.i3.gz"
year="2012"
MCdataset=14000
dataset=12012
seed=1201200000
energyStep=0.1
photonDirectory="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/"
NumbSamples=100
NumbFrames=0

#################################### TODO ####################################
# Energy range for the detector response
energyStart=4.0
energyEnd=6.4

# Parallelization
parallelSim=100
logDirProcesses="/home/hk-project-pevradio/rn8463/log/logDetResponseGammaExtra/"
#################################### TODO ####################################

############### Generated #####################
$environment1 $PYTHON $SCRIPT \
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
                -parallelSim $parallelSim \
                --photonDirectory $photonDirectory \
                --NumbSamples $NumbSamples \
                --NumbFrames $NumbFrames \
                -doFiltering \
                --doITSG \
                --doDET 

                # --doInIceBg \
                # --doCLSIM \


############### Filtered Lv1 and Lv2 #####################
$environment2 $PYTHON $SCRIPT \
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
                -parallelSim $parallelSim \
                --photonDirectory $photonDirectory \
                --NumbSamples $NumbSamples \
                --NumbFrames $NumbFrames \
                -doFiltering \
                --doLV1 \
                --doLV2 

                # --doITSG \
                # --doDET \


# ############### Filtered Lv3 #####################
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
                -parallelSim $parallelSim \
                --photonDirectory $photonDirectory \
                --NumbSamples $NumbSamples \
                --NumbFrames $NumbFrames \
                -doFiltering \
                --doLV3 
                
                # --doITSG \
                # --doDET \
                # --doLV1 \
                # --doLV2 \

#!/bin/env python3

import os
import numpy as np

from utils.Submitter import Submitter
from utils.MultiProcesses import MultiProcesses
from utils.DetectorSimulator import DetectorSimulator


def make_parser(): 
    """
    Makes all the arguments that are required for the following script
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Inputs for the Detector Response Maker"
    )
    ############################## Directories paths ####################################
    parser.add_argument(
        "-inDirectory",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/data/",
        help="Directory where the simulation are stored. Please give the data folder. \
            This script assumes that in this folder there are subdirectories with energy number",
    )
    parser.add_argument(
        "-outDirectory",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/",
        help="Directory where the detector response  has to be stored. \
            It will create here a new folder: 'detector_response'.\
            Output folder name. The output file(s) will be <output>/generates/(topsimulator|detector)/[TopSimulator|Detector]_DETECTOR_corsika_icetop.MCDATASET.RUN.i3.bz2 \
            for level 0s, <output>/filtered/Level[1|2]_DETECTOR_corsika_icetop.MCDATASET.RUN.i3.bz2, for level 1 and 2, Level3_DETECTOR_DATASET_Run.RUN.i3.bz2 for level3 \
            The condor files will be saved in the realtive condor folders",
    )
    ############################# General Requirement #####################################        
    parser.add_argument(
        "-pythonPath", 
        type=str, 
        default="/usr/bin/python3", 
        help="Python path which runs the simulations of detector response"
    )      
    parser.add_argument(
        "-i3build", 
        type=str, 
        default="/home/hk-project-pevradio/rn8463/icetray/build/", 
        help="The path to the build directory of icetray environment"
    )
    parser.add_argument(
        "-detector", 
        type=str, 
        default="IC86", 
        help="Detector type/geometry (IC79, IC86, IC86.2012...): the full name will be used only for L3 reconstruction,\
            while for the other only the base (i.e. IC86 if declared IC86.2012) [default: IC86]"
    )
    parser.add_argument(
        "-GCD", 
        type=str, 
        default="/lsdf/kit/ikp/projects/IceCube/sim/GCD/GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz", 
        help="path where the GCD lv2 file is located"
    )
    parser.add_argument(
        "-year", 
        type=str, 
        default="2012", 
        help="Detector year it will be used for the full detector name in the L3 reconstruction."
    )
    parser.add_argument(
        "-MCdataset", 
        type=int, 
        default=13400, 
        help="Number of corsika dataset [default: 13410]"
    )
    parser.add_argument(
        "-dataset", 
        type=int, 
        default=12012, 
        help="Number of dataset [default: 12012]"
    )
    parser.add_argument(
        "-seed", 
        type=int, 
        default=120120000, 
        help="The seed is the base seed which is 100_000 times the given dataset number"
    )
    parser.add_argument(
        "-doLv3", 
        action='store_true', # default False
        help="Analysis level, i.e. include level 3 in the production"
    )
    parser.add_argument(
        "-doFiltering", 
        action='store_true', # default False
        help="Cut data with the trigger filtering. Useful for Level 0, 1 and 2"
    )
    ############################## Energy ####################################
    parser.add_argument(
        "-energyStart", 
        type=float, 
        default=5.0, 
        help="Lower limit of energy"
    )
    parser.add_argument(
        "-energyEnd", 
        type=float, 
        default=7.0, 
        help="Upper limit of energy"
    )
    parser.add_argument(
        "-energyStep", 
        type=float, 
        default=0.1, 
        help="Step in energy, 0.1 default (do not change unless you know what you are doing)"
    )
    ############################# Parallelization #####################################
    parser.add_argument(
        "-logDirProcesses",
        type=str,
        default="/home/hk-project-pevradio/rn8463/logDetResponse/",
        help="Directory where log files of the multiple subProcesses are stored",
    )
    parser.add_argument(
        "-parallelSim",
        type=int,
        default=100,
        help="Number of parallel simulation processes",
    )
    ##################################################################
    parser.add_argument(
        "--photonDirectory", 
        type=str, 
        default="/lsdf/kit/ikp/projects/IceCube/sim/photon-tables/", 
        help="The path where the photon library is located. Needed for the simulations"
    )    
    parser.add_argument(
        "--NumbSamples", 
        type=int, 
        default=100, 
        help="How many samples per run will be simulated by icetopshowergenerator.py [default: 100]"
    )
    parser.add_argument(
        "--NumbFrames", 
        type=int, 
        default=0, 
        help="How many frames will be processed (0=unbound) [default: 0] "
    )
    ############################# Scripts Extra Options #####################################
    parser.add_argument(
        "--ITSG_ExtraOptions", 
        type=str, 
        default="", 
        help="  Enquoted other options for icetopsimulator.py; example: -o --raise-observation-level 3"
    )    
    parser.add_argument(
        "--clsim_ExtraOptions", 
        type=str, 
        default="", 
        help="  Enquoted other options for clsim.py; example: -o --raise-observation-level 3"
    )
    parser.add_argument(
        "--DET_ExtraOptions",
        type=str,
        default="",
        help="  Enquoted other options for detector.py (level 0 simulation)",
    )
    parser.add_argument(
        "--LV1_ExtraOptions",
        type=str,
        default="",
        help="  Enquoted other options for SimulationFiltering.py (level 1 simulation)",
    )
    parser.add_argument(
        "--LV2_ExtraOptions",
        type=str,
        default="",
        help="  Enquoted other options for process.py (level 2 simulation)",
    )
    parser.add_argument(
        "--LV3_ExtraOptions", 
        type=str, 
        default="", 
        help="Enquoted other options for level3_iceprod.py (level 3 simulation); available only if -a is declared"
    )
    return parser
    
def generatorFake():
    yield None, None

class ProcessRunner():
    def __init__(self, detectorSim, submitter, energies, inDirectory, doFiltering, extraOptions={}):
        self.detectorSim = detectorSim
        self.submitter = submitter 
        self.energies = energies
        self.inDirectory = inDirectory
        self.doFiltering = doFiltering
        self.extraOptions = extraOptions       

    def generatorKeys(self):
        """
        nproc is the number of input files you give (e.g. I have 667 in each energy bin folder)
        runid is the number of the corsika shower
        runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
        procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667

        some of the scripts (like icetopshowergenerator) take the base seed, nproc and proxcnum and calculate the actual used seed by combining those three numbers
        """
        
        for energy in self.energies:
            inDir = f"{self.inDirectory}/{energy}/"
            # nproc is the number of files simulated per energy bin obtained by listing all files in the direcory and getting the len of it
            nproc = len([f for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir,f)) ])
            for index, corsikaFile in enumerate(os.listdir(inDir)):
                runID=int(corsikaFile.partition("DAT")[-1][-5:])
                runname=str(corsikaFile.partition("DAT")[-1])
                procnum=index+1
                keyArgs = [energy, inDir+corsikaFile, runname, nproc, procnum, runID]
                yield (f"{energy}_{runname}", keyArgs)

    def run_processes(self, energy, corsikaFile, runname, nproc, procnum, runID):
        """
        This functions can be edited and can be used for running all processes needed that can ebe found in DetectorSimulator
        If your function is not available, add it to the class and run it here. 
        """
        ##################################### ITShowerGenerator ##########################################
        exeFile, ITSGFile = self.detectorSim.run_ITShowerGenerator(energy=energy, 
                                                        runname=runname, 
                                                        inputFile=corsikaFile, 
                                                        nproc=nproc, 
                                                        procnum=procnum, 
                                                        runID=runID, 
                                                        extraOptions=self.extraOptions.get("ITSG"))
        if exeFile is not None: 
            print(energy, runname, "run_ITShowerGenerator")
            self.executeFile(key=f"{energy}_{runname}_ITSG", exeFile=exeFile)        
        ####################################### clsim ########################################
        exeFile, clsimFile = self.detectorSim.run_clsim(energy=energy, 
                                            runname=runname, 
                                            inputFile=ITSGFile, 
                                            nproc=nproc, 
                                            procnum=procnum, 
                                            extraOptions=self.extraOptions.get("clsim"), 
                                            oversize=5, 
                                            efficiency=1.0, 
                                            icemodel="spice_3.2.1",)
        if exeFile is not None: 
            print(energy, runname, "run_clsim")
            self.executeFile(key=f"{energy}_{runname}_clsim", exeFile=exeFile) 
        ################################# detector ##############################################
        exeFile, DETFile = self.detectorSim.run_detector(energy=energy, 
                                            runname=runname, 
                                            inputFile=clsimFile, 
                                            nproc=nproc, 
                                            procnum=procnum, 
                                            runID=runID, 
                                            doFiltering=self.doFiltering, 
                                            extraOptions=self.extraOptions.get("Det"), 
                                            mcprescale=1, 
                                            mctype="CORSIKA")
        if exeFile is not None: 
            print(energy, runname, "run_detector")
            self.executeFile(key=f"{energy}_{runname}_detector", exeFile=exeFile) 
        ################################### LV1 ############################################
        exeFile, LV1File = self.detectorSim.run_lv1(energy=energy, 
                                            runname=runname,  
                                        DETFile=DETFile, 
                                        extraOptions=self.extraOptions.get("lv1"),)
        if exeFile is not None: 
            print(energy, runname, "run_lv1")
            self.executeFile(key=f"{energy}_{runname}_lv1", exeFile=exeFile) 
        ################################## LV2 #############################################
        exeFile, LV2File = self.detectorSim.run_lv2(energy=energy, 
                                        runname=runname,  
                                        LV1File=LV1File, 
                                        extraOptions=self.extraOptions.get("lv2"),)
        if exeFile is not None: 
            print(energy, runname, "run_lv2")
            self.executeFile(key=f"{energy}_{runname}_lv2", exeFile=exeFile) 
        #################################### LV3 ###########################################
        exeFile, LV3File = self.detectorSim.run_lv3(energy=energy, 
                                        runname=runname, 
                                        LV2File=LV2File, 
                                        runID=runID, 
                                        extraOptions=self.extraOptions.get("lv3"),
                                        domeff=1.0,)
        if exeFile is not None: 
            print(energy, runname, "run_lv3")
            self.executeFile(key=f"{energy}_{runname}_lv3", exeFile=exeFile) 
        ###############################################################################
        
        return

    def executeFile(self, key, exeFile): 
        self.submitter.startSingleProcess(key, exeFile)
        self.submitter.communicateSingleProcess(key)
        return

 
def mainLoop(args):

    energies = np.around( # Need to round the numpy array otherwise the floating is wrong
                    np.arange(
                        args.energyStart, # energy starting point
                        args.energyEnd + args.energyStep, # energy end point plus one step in order to include last step
                        args.energyStep, # step in energies
                        ),
                decimals=1 # the rounding has to have one single decimal point for the folder. 
    )
    
    detectorSim = DetectorSimulator(
        pythonPath=args.pythonPath,
        dataset=args.dataset,
        MCdataset=args.MCdataset,
        seed=args.seed,
        year=args.year,
        doLv3=args.doLv3,
        NumbSamples=args.NumbSamples,
        NumbFrames=args.NumbFrames,
        i3build=args.i3build,
        outDirectory=args.outDirectory,
        detector=args.detector,#"IC86"
        GCD=args.GCD,
        photonDirectory=args.photonDirectory)
        
    submitter = Submitter(
        MakeKeySubString=generatorFake,
        logDir=args.logDirProcesses,
        parallel_sim=args.parallelSim,
    )
    
    processRun = ProcessRunner(
        detectorSim=detectorSim, 
        submitter=submitter,
        energies=energies,
        inDirectory=args.inDirectory, 
        doFiltering=args.doFiltering,
        extraOptions={
            "ITSG": args.ITSG_ExtraOptions,
            "clsim":args.clsim_ExtraOptions,
            "Det":args.DET_ExtraOptions,
            "lv1":args.LV1_ExtraOptions,
            "lv2":args.LV2_ExtraOptions,
            "lv3":args.LV3_ExtraOptions,
            }
        )
        
    multiProcessor = MultiProcesses(
        keysGenerator=processRun.generatorKeys, 
        functionToRun=processRun.run_processes, 
        parallel_sim=args.parallelSim)
    
    # if args.doLv3:
    #     detectorSim.make_Lv3GCD()
        
    multiProcessor.startProcesses()
    multiProcessor.checkProcesses()
            

if __name__ == "__main__":
    
    parser = make_parser()
    mainLoop(args=parser.parse_args())

    print("------------------- Program finished --------------------")

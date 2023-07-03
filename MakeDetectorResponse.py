#!/bin/env python3

"""
This script is used to make the detector response for a given energy range.
Uses as input the Coriska simulation files and outputs the Lv3 files.

The args values can be used to specify the desired configuration for the simulation.

How to run:
    python3 MakeDetectResponse.py 
 if you want to change any configuration from the default once add the [args] after it
 e.g.:
    python3 MakeDetectResponse.py -inDirectory /path/to/folder -outDirectory /path/to/folder ..... 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""

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
        help="Python path which runs the simulations of detector response",
    )
    parser.add_argument(
        "-i3build",
        type=str,
        default="/home/hk-project-pevradio/rn8463/icetray/build/",
        help="The path to the build directory of icetray environment",
    )
    parser.add_argument(
        "-detector",
        type=str,
        default="IC86",
        help="Detector type/geometry (IC79, IC86, IC86.2012...): the full name will be used only for L3 reconstruction,\
            while for the other only the base (i.e. IC86 if declared IC86.2012) [default: IC86]",
    )
    parser.add_argument(
        "-GCD",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/GCD/GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz",
        help="path where the GCD lv2 file is located",
    )
    parser.add_argument(
        "-year",
        type=str,
        default="2012",
        help="Detector year it will be used for the full detector name in the L3 reconstruction.",
    )
    parser.add_argument(
        "-MCdataset",
        type=int,
        default=13400,
        help="Number of corsika dataset [default: 13410]",
    )
    parser.add_argument(
        "-dataset", type=int, default=12012, help="Number of dataset [default: 12012]"
    )
    parser.add_argument(
        "-seed",
        type=int,
        default=120120000,
        help="The seed is the base seed which is 100_000 times the given dataset number",
    )
    parser.add_argument(
        "-doFiltering",
        action="store_true",  # default False
        help="Cut data with the trigger filtering. Useful for Level 0, 1 and 2",
    )
    ############################## Energy ####################################
    parser.add_argument(
        "-energyStart", type=float, default=5.0, help="Lower limit of energy"
    )
    parser.add_argument(
        "-energyEnd", type=float, default=7.0, help="Upper limit of energy"
    )
    parser.add_argument(
        "-energyStep",
        type=float,
        default=0.1,
        help="Step in energy, 0.1 default (do not change unless you know what you are doing)",
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
        help="The path where the photon library is located. Needed for the simulations",
    )
    parser.add_argument(
        "--NumbSamples",
        type=int,
        default=100,
        help="How many samples per run will be simulated by icetopshowergenerator.py [default: 100]",
    )
    parser.add_argument(
        "--NumbFrames",
        type=int,
        default=0,
        help="How many frames will be processed (0=unbound) [default: 0] ",
    )
    ############################# Scripts Extra Options #####################################
    parser.add_argument(
        "--doITSG",
        action="store_true",
        help="do you want to run ITShowerGenerator.py? deafualt: False",
    )
    parser.add_argument(
        "--doInIceBg",
        action="store_true",
        help="do you want to run In-Ice background with Corsika and polyplopia? deafualt: False",
    )
    parser.add_argument(
        "--doCLSIM",
        action="store_true",
        help="do you want to run clsim.py? deafualt: False",
    )
    parser.add_argument(
        "--doDET",
        action="store_true",
        help="do you want to run detector.py? deafualt: False",
    )
    parser.add_argument(
        "--doLV1",
        action="store_true",
        help="do you want to run SimulationFiltering.py? (level 1 simulation) deafualt: False",
    )
    parser.add_argument(
        "--doLV2",
        action="store_true",
        help="do you want to run the process.py? (level 2 simulation) deafualt: False",
    )
    parser.add_argument(
        "--doLV3",
        action="store_true",
        help="do you want to run level3_iceprod.py? (level 3 simulation) deafualt: False",
    )
    return parser.parse_args()


def generatorFake():
    """
    This is a fake generator that is used to in the submitter class to run the simulation in a single process.
    """
    yield None, None


class ProcessRunner:
    """
    This class is used to run the simulations and call the shell scripts.
    -----------------------------------------------------------------------
    Parameters:
        detectorSim: the detector simulation class
        submitter: the submitter class
        energies: the energy range that will be simulated
        inDirectory: the directory where the data corsika files are located
        doFiltering: if True, the data will be filtered with the lv3 trigger filtering
        extraOptions: a dictionary with the extra options that will be passed to the submitter class # TODO: check if this is needed
    """

    def __init__(
        self,
        detectorSim,
        submitter,
        energies,
        inDirectory,
        doFiltering,
        extraOptions={},
    ):
        self.detectorSim = detectorSim
        self.submitter = submitter
        self.energies = energies
        self.inDirectory = inDirectory
        self.doFiltering = doFiltering
        self.extraOptions = extraOptions

    def generatorKeys(self):
        """
        This generator is used to generate the keys for the submitter class.

        nproc is the number of input files you give (e.g. I have 667 in each energy bin folder)
        runid is the number of the corsika shower
        runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
        procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667

        some of the scripts (like icetopshowergenerator) take the base seed, nproc and proxcnum and calculate the actual used seed by combining those three numbers
        """
        # loop over all energies and yield the key and the arguments for the run_processes function
        for energy in self.energies:
            inDir = f"{self.inDirectory}/{energy}/"
            # list all files in the directory and sort them
            fileList = sorted(
                [f for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir, f))]
            )
            # nproc is the number of files simulated per energy bin obtained by listing all files in the direcory and getting the len of it
            nproc = len(fileList)
            # loop over all files in the directory
            for index, corsikaFile in enumerate(fileList):
                if corsikaFile.endswith(".bz2"):
                    continue
                runID = int(corsikaFile.partition("DAT")[-1][-5:])
                runname = str(corsikaFile.partition("DAT")[-1])
                procnum = index + 1
                keyArgs = [energy, inDir + corsikaFile, runname, nproc, procnum, runID]
                yield (f"{energy}_{runname}", keyArgs)

    def run_processes(self, energy, corsikaFile, runname, nproc, procnum, runID):
        """
        This functions can be edited and can be used for running all processes needed that can ebe found in DetectorSimulator
        If your function is not available, add it to the class and run it here.
        """
        ##################################### ITShowerGenerator ##########################################
        if self.extraOptions.get("doITSG"):
            exeFile, ITSGFile = self.detectorSim.run_ITShowerGenerator(
                energy=energy,
                runname=runname,
                inputFile=corsikaFile,
                nproc=nproc,
                procnum=procnum,
                runID=runID,
            )
            if exeFile is not None:
                print(energy, runname, "run_ITShowerGenerator")
                self.executeFile(key=f"{energy}_{runname}_ITSG", exeFile=exeFile)
            inputFile = ITSGFile
        if self.extraOptions.get("doInIceBg"):
            ####################################### corsika #################################################
            exeFile, corsikaBgFile = self.detectorSim.run_corsikaBg(
                energy=energy,
                runname=runname,
                nproc=nproc,
                procnum=procnum,
                CORSIKA_samples=100,
            )
            if exeFile is not None:
                print(energy, runname, "run_CorsikaBg")
                self.executeFile(key=f"{energy}_{runname}_CorsikaBg", exeFile=exeFile)

            ####################################### polyplopia #############################################
            exeFile, polyplopiaFile = self.detectorSim.run_polyplopia(
                energy=energy,
                runname=runname,
                inputFile=inputFile,
                backgroundfile=corsikaBgFile,  # "corsika_bg.i3.bz2",
                MCTreeName="I3MCTree",
                OutputMCTreeName="I3MCTree",
                mctype="corsika",
                TimeWindow=40,
                log_level="INFO",
                extraOptions="",
            )
            if exeFile is not None:
                print(energy, runname, "run_polyplopia")
                self.executeFile(key=f"{energy}_{runname}_polyplopia", exeFile=exeFile)
            inputFile = polyplopiaFile

        if self.extraOptions.get("doCLSIM"):
            ####################################### clsim ########################################
            exeFile, clsimFile = self.detectorSim.run_clsim(
                energy=energy,
                runname=runname,
                inputFile=inputFile,
                nproc=nproc,
                procnum=procnum,
                oversize=5,
                efficiency=1.0,
                icemodel="spice_3.2.1",
            )
            if exeFile is not None:
                print(energy, runname, "run_clsim")
                self.executeFile(key=f"{energy}_{runname}_clsim", exeFile=exeFile)
            inputFile = clsimFile
        ################################# detector ##############################################
        if self.extraOptions.get("doDET"):
            exeFile, DETFile = self.detectorSim.run_detector(
                energy=energy,
                runname=runname,
                inputFile=inputFile,
                nproc=nproc,
                procnum=procnum,
                runID=runID,
                doFiltering=self.doFiltering,
                mcprescale=1,
                mctype="CORSIKA",
            )
            if exeFile is not None:
                print(energy, runname, "run_detector")
                self.executeFile(key=f"{energy}_{runname}_detector", exeFile=exeFile)
        ################################### LV1 ############################################
        if self.extraOptions.get("doLV1"):
            DETFile = self.detectorSim.run_detector(
                energy=energy,
                runname=runname,
                inputFile="",
                nproc=nproc,
                procnum=procnum,
                runID=runID,
                doFiltering=self.doFiltering,
                mcprescale=1,
                mctype="CORSIKA",
                return_name=True,
            )
            exeFile, LV1File = self.detectorSim.run_lv1(
                energy=energy,
                runname=runname,
                DETFile=DETFile,
            )
            if exeFile is not None:
                print(energy, runname, "run_lv1")
                self.executeFile(key=f"{energy}_{runname}_lv1", exeFile=exeFile)
        ################################## LV2 #############################################
        if self.extraOptions.get("doLV2"):
            exeFile, LV2File = self.detectorSim.run_lv2(
                energy=energy,
                runname=runname,
                LV1File=LV1File,
                extraOptions=self.extraOptions.get("lv2"),
            )
            if exeFile is not None:
                print(energy, runname, "run_lv2")
                self.executeFile(key=f"{energy}_{runname}_lv2", exeFile=exeFile)
        #################################### LV3 ###########################################
        if self.extraOptions.get("doLV3"):
            LV2File = self.detectorSim.run_lv2(
                energy=energy,
                runname=runname,
                LV1File="",
                extraOptions=self.extraOptions.get("lv2"),
                return_name=True,
            )
            exeFile, LV3File = self.detectorSim.run_lv3(
                energy=energy,
                runname=runname,
                LV2File=LV2File,
                runID=runID,
                extraOptions=self.extraOptions.get("lv3"),
                domeff=1.0,
            )
            if exeFile is not None:
                print(energy, runname, "run_lv3")
                self.executeFile(key=f"{energy}_{runname}_lv3", exeFile=exeFile)
        ###############################################################################

        return

    def executeFile(self, key, exeFile):
        """
        This function executes the sh file that was created by the DetectorSimulator class.
        And comminicates with the file has completed so that the log and the err file can be created and the new process can be started.
        """
        self.submitter.startSingleProcess(key, exeFile)
        self.submitter.communicateSingleProcess(key)
        return


def mainLoop(args):
    """
    This is the main loop of the program.
    It defines the energies and some useful classes.

    DetectorSimulator is the class that creates all the sh files with the python scripts that are needed to run the simulation.

    Submitter is the class that spawns the python processes by calling multiple python scipts at the same time.

    ProcessRunner  is the class that runs the simulation. Can be modified to run the simulation in a different way.

    mutliProcessor is the class that runs the processes in parallel by calling all the functions one after the other.
    """

    # Define the energies that are going to be simulated.
    energies = np.around(  # Need to round the numpy array otherwise the floating is wrong
        np.arange(
            args.energyStart,  # energy starting point
            args.energyEnd
            + args.energyStep,  # energy end point plus one step in order to include last step
            args.energyStep,  # step in energies
        ),
        decimals=1,  # the rounding has to have one single decimal point for the folder.
    )

    # The class that creates all the sh files with the python scripts that are needed to run the simulation.
    detectorSim = DetectorSimulator(
        pythonPath=args.pythonPath,
        dataset=args.dataset,
        MCdataset=args.MCdataset,
        seed=args.seed,
        year=args.year,
        NumbSamples=args.NumbSamples,
        NumbFrames=args.NumbFrames,
        i3build=args.i3build,
        outDirectory=args.outDirectory,
        detector=args.detector,  # "IC86"
        GCD=args.GCD,
        photonDirectory=args.photonDirectory,
    )

    # The class that spawns the python processes by calling multiple python scipts at the same time.
    submitter = Submitter(
        MakeKeySubString=generatorFake,
        logDir=args.logDirProcesses,
        parallel_sim=args.parallelSim,
    )

    # The class that runs the simulation. Can be modified to run the simulation in a different way.
    processRun = ProcessRunner(
        detectorSim=detectorSim,
        submitter=submitter,
        energies=energies,
        inDirectory=args.inDirectory,
        doFiltering=args.doFiltering,
        extraOptions={
            "doITSG": args.doITSG,
            "doInIceBg": args.doInIceBg,
            "doCLSIM": args.doCLSIM,
            "doDET": args.doDET,
            "doLV1": args.doLV1,
            "doLV2": args.doLV2,
            "doLV3": args.doLV3,
        },
    )

    # The class that runs the processes in parallel by calling all the functions one after the other.
    multiProcessor = MultiProcesses(
        keysGenerator=processRun.generatorKeys,
        functionToRun=processRun.run_processes,
        parallel_sim=args.parallelSim,
    )

    # Start the processes in the multiProcessor class and check if they are finished.
    # This loops until all the processes are finished.
    multiProcessor.startProcesses()
    multiProcessor.checkProcesses()


if __name__ == "__main__":
    mainLoop(args=make_parser())

    print("------------------- Program finished --------------------")

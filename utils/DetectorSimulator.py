#!/usr/bin/env python3
"""
Some documentation 
"""

import os
import pathlib
import stat


class DetectorSimulator:
    """
    This class is used to create all the shell scripts that need to be executed.
    It also creates the folders and the executable file for the simulation script.
    """

    def __init__(
        self,
        pythonPath,
        dataset,
        MCdataset,
        seed,
        year,
        doLv3,
        NumbSamples=100,
        NumbFrames=0,
        i3build="",
        outDirectory="",
        detector="IC86",
        GCD="",
        photonDirectory="",
    ):
        """
        Parameters:
            pythonPath: the path to the python executable (which python3)
            dataset: the name of the dataset (ask the coordinators)
            MCdataset: the name of the MC dataset (ask the coordinators)
            seed: the seed for the random number generator (ask the coordinators)
            year: the year of the simulation
            doLv3: if True, it will do the Level3 simulation
            NumbSamples: the number of samples to be simulated (default 100)
            NumbFrames: the number of frames to be simulated (default 0)
            i3build: the path to the icetray build directory (github.com/icecube/icetray)
            outDirectory: the path to the output directory where the data will be stored
            detector: the detector to be simulated (default IC86)
            GCD: the path to the GCD file
            photonDirectory: on cobalt medison cluster is /cvmfs/icecube.opensciencegrid.org/data/photon-tables/
        """

        self.pythonPath = pythonPath
        self.dataset = dataset
        self.MCdataset = MCdataset
        self.seed = seed
        self.NumbSamples = NumbSamples
        self.NumbFrames = NumbFrames

        self.i3build = i3build
        self.outDirectory = outDirectory
        self.detector = f"{detector}.{year}"
        self.GCD = GCD
        self.photonDir = photonDirectory
        self.Lv3GCD = ""
        if doLv3:
            self.Lv3GCD = self.GCD

    ########################### Useful functions ############################

    def make_Lv3GCD(self):
        """
        It makes sure that the GCD Lv3 file does not exist.
        If so, creates the new folder and calls the script for making the file.

        WARNING: This is probably outdated. If you do not know hwo to use it ask the coordinators.
        """
        gcdbase = os.path.basename(self.GCD)
        gcdname, i3, GCDend = gcdbase.partition(".i3")
        self.Lv3GCD = f"{self.outDirectory}/gcd/{gcdname}_L3{i3}{GCDend}"

        pathlib.Path(f"{self.outDirectory}/gcd/").mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(self.Lv3GCD):
            print("Making the GCD file")
            os.system(
                f"{self.pythonPath} {self.i3build}/icetop_Level3_scripts/resources/scripts/MakeL3GCD_MC.py --MCgcd {self.GCD} --obslevel 2840. --output {self.Lv3GCD}"
            )

    def checkIfInputExists(self, inputFile):
        """
        Checks if the input file exists, if not a working message is shown
        """
        fileToCheck = pathlib.Path(inputFile)
        if not fileToCheck.is_file():
            import warnings

            warnings.warn(
                f"\nThe program is not stopped, but be aware that: \n{inputFile} \nDOES NOT EXIST!!"
            )
        return

    def writeSHexeFile(
        self, exeFile, cmdPython, cmdOptions, cmdMoveFile, cmdSTART="", cmdEND=""
    ):
        """
        Writes the executable file and makes it executable.
        The exeFile will:
            runs the python script
            move the file from the temp to the data directory
            can remove the exeFile once completed (if the command is given)
        ----------------------------------------------------------------
        Parameters:
            exeFile: the name of the executable
            cmdPython: the python path and the path to the script
            cmdOptions: the options to be passed to the python script
            cmdMoveFile: moves the file from the temp to the data location when the script is over
            cmdSTART: is a command that can be used before executing the python script (default does nothing)
            cmdEND: is a command that can be used at the end.
                    E.G. removing the exeFile once its completed (default does nothing)
                    it could be useful to check if everything runs correctly
        """
        with open(exeFile, "w") as file:
            file.write(r"#!/bin/sh")  # This shows that the file is an executable
            file.write(
                "\n"
                + f"{cmdSTART}\n"
                + f"{cmdPython} {cmdOptions}\n"  # Execute python script with arguments
                + f"{cmdMoveFile}\n"
                + f"{cmdEND}\n"
            )

        # Make the file executable
        st = os.stat(exeFile)
        os.chmod(exeFile, st.st_mode | stat.S_IEXEC)

    def make_folders(self, folder, energy):
        """
        It makes the data, temp, logs and inps folders and the energy subfolders in the path given.
        --------------------------------------------------------------------------------
        Parameters:
            folder: folder where the folders needs to be created
            energy: the energy usually in log10 GeV that needs to be created
        """
        pathlib.Path(f"{folder}/data/{energy}/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{folder}/temp/{energy}/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{folder}/logs/{energy}/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{folder}/inps/{energy}/").mkdir(parents=True, exist_ok=True)

    def get_radius(self, logE):
        """
        According to the IC standard simulations,
        the radius depends on the energy as follows:

        rgen[logE>5.0] = 800
        rgen[logE>6.0] = 1100
        rgen[logE>7.0] = 1700
        rgen[logE>8.0] = 2600
        rgen[logE>9.0] = 3900

        --------------------------------------------
        Parameters:
            logE: log10 of the energy in GeV
        Return:
            radius: the radius which used in the simulations
        """
        logE = int(logE)
        radius = {
            5: 800,
            6: 1100,
            7: 1700,
            8: 2600,
            9: 3900,
        }
        return radius[logE]

    ########################### Main simulation scipts ####################################
    def run_ITShowerGenerator(
        self, energy, runname, inputFile, nproc, procnum, runID, extraOptions=""
    ):
        """
        Runs the icetopshowergenerator.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            inputFile: the name of the input file in this case it is the Corsika output file

            nproc is the number of input files you give (e.g. I have 667 in each energy bin folder)
            runid is the number of the corsika shower
            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667

            extraOptions: the extra Options that can be passed to the python script
        Return:
            exeFile: the file that need to be executed
        """
        self.checkIfInputExists(inputFile)
        outputFolder = f"{self.outDirectory}/generated/topsimulator"
        outputFolder += (
            f"/TopSimulator_{self.detector}_corsika_icetop.{self.MCdataset}/"
        )

        ITSGdataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the input file needs to be written

        # Checks if the file already exist, in case so it returns None
        if os.path.isfile(ITSGdataFile):
            return None, ITSGdataFile

        # this function makes the data, temp, logs, inps directory
        self.make_folders(outputFolder, energy)

        # TODO never checked if the untar of the bz2 file works
        if inputFile.endswith(".bz2"):
            baseName = os.path.basename(inputFile)
            name, _, __ = baseName.partition(".bz2")
            pathTemp = f"{outputFolder}/temp/{energy}/"
            cmdSTART = f"\nbzip2 -dc {inputFile} > {pathTemp}{name} \n"
            inputFile = f"{pathTemp}/{name}"
        else:
            cmdSTART = "\n"

        # The python script that needs to be executed with its arguments
        cmdPython = f"{self.pythonPath} {self.i3build}/simprod-scripts/resources/scripts/icetopshowergenerator.py "
        cmdOptions = f"\
            --UseGSLRNG \
            --gcdfile {self.GCD} \
            --seed {self.seed} \
            --nproc {nproc} \
            --samples {self.NumbSamples} \
            --r {self.get_radius(energy)} \
            --no-PropagateMuons \
            --RunID {runID} \
            --procnum {procnum} \
            --inputfilelist {inputFile} \
            --outputfile {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "
        if extraOptions:
            cmdOptions += extraOptions

        # moves the file to its final location once everything is done
        cmdMoveFile = f"mv {tempFile} {ITSGdataFile}"

        # writes the sh file and makes it executable
        self.writeSHexeFile(
            exeFile, cmdPython, cmdOptions, cmdMoveFile, cmdSTART=cmdSTART
        )

        return exeFile, ITSGdataFile

    def run_polyplopia(
        self,
        energy,
        runname,
        inputFile,
        backgroundfile="corsika_bg.i3.bz2",
        MCTreeName="I3MCTree",
        OutputMCTreeName="I3MCTree",
        mctype="corsika",
        TimeWindow=40,
        log_level="INFO",
        extraOptions="",
    ):
        """
        Runs the polyplopia.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            inputFile: the name of the input file in this case it is the Corsika output file

            backgroundfile: the name of the background file default is corsika_bg.i3.bz2
            MCTreeName: the name of the MCTree in the i3 file default is I3MCTree
            OutputMCTreeName: the name of the output MCTree in the i3 file default is I3MCTree
            mctype: the type of the MC default is corsika
            TimeWindow: the time window in ns default is 40
            log_level: the log level default is INFO
            extraOptions: the extra Options that can be passed to the python script
        Return:
            exeFile: the file that need to be executed
        """
        self.checkIfInputExists(inputFile)
        outputFolder = f"{self.outDirectory}/generated/topsimulator"
        outputFolder += f"/Polyplotpia_{self.detector}_corsika_icetop.{self.MCdataset}/"

        polyplopiaDataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path to File name
        )
        tempFile = f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path to the temp file name
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the input file needs to be written

        # Checks if the file already exist, in case so it returns None
        if os.path.isfile(polyplopiaDataFile):
            return None, polyplopiaDataFile

        # this function makes the data, temp, logs, inps directory
        self.make_folders(outputFolder, energy)

        # The python script that needs to be executed with its arguments
        cmdPython = f"{self.pythonPath} {self.i3build}/simprod-scripts/resources/scripts/SnowSuite/2-Polyplopia.py "
        cmdOptions = f"\
            --seed {self.seed} \
            --backgroundfile {backgroundfile} \
            --MCTreeName {MCTreeName} \
            --OutputMCTreeName {OutputMCTreeName} \
            --mctype {mctype} \
            --TimeWindow {TimeWindow} \
            --log-level {log_level} \
            --infile {inputFile} \
            --outfile {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "
        if extraOptions:
            cmdOptions += extraOptions

        # moves the file to its final location once everything is done
        cmdMoveFile = f"mv {tempFile} {polyplopiaDataFile}"

        # writes the sh file and makes it executable
        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        return exeFile, polyplopiaDataFile

    def run_clsim(
        self,
        energy,
        runname,
        inputFile,
        nproc,
        procnum,
        extraOptions="",
        oversize=5,
        efficiency=1.0,
        icemodel="spice_3.2.1",
    ):
        """
        Runs the clsim.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            inputFile: the name of the input file in this case it is the Corsika output file

            nproc is the number of input files you give (e.g. I have 667 in each energy bin folder)
            runid is the number of the corsika shower
            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667

            extraOptions: the extra Options that can be passed to the python script
        Return:
            exeFile: the file that need to be executed

        """
        self.checkIfInputExists(inputFile)

        icemodellocation = f"{self.i3build}/ice-models/resources/models/ICEMODEL"
        holeiceparametrization = (
            f"{self.i3build}/ice-models/resources/models/ANGSENS/angsens_flasher/as.9"
        )

        outputFolder = f"{self.outDirectory}/generated/clsim"
        outputFolder += f"/CLS_{self.detector}_corsika_icetop.{self.MCdataset}/"

        CLSdataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the input file needs to be written

        # Checks if the file already exist, in case so it returns None
        if os.path.isfile(CLSdataFile):
            return None, CLSdataFile

        self.make_folders(outputFolder, energy)

        cmdPython = f"{self.pythonPath} {self.i3build}/simprod-scripts/resources/scripts/clsim.py "
        cmdOptions = f"\
            --UseGSLRNG \
            --gcdfile {self.GCD} \
            --seed {self.seed} \
            --nproc {nproc} \
            --UseGPUs \
            --oversize {oversize} \
            --IceModel {icemodel} \
            --IceModelLocation {icemodellocation} \
            --holeiceparametrization {holeiceparametrization} \
            --efficiency {efficiency} \
            --procnum {procnum} \
            --inputfilelist {inputFile} \
            --outputfile {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "

        if extraOptions:
            cmdOptions += extraOptions

        cmdMoveFile = f"mv {tempFile} {CLSdataFile}"

        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        return exeFile, inputFile

    def run_detector(
        self,
        energy,
        inputFile,
        runname,
        nproc,
        procnum,
        runID,
        doFiltering,
        extraOptions="",
        mcprescale=1,
        mctype="CORSIKA",
    ):
        """
        Runs the detector.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            inputFile: the name of the input file in this case it is the Corsika output file

            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            nproc is the number of input files you give (e.g. I have 667 in each energy bin folder)
            procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667
            runID is the number of the corsika shower
            doFiltering is a boolean that decides if the filtering is done or not
            extraOptions: the extra Options that can be passed to the python script
            mcPrescale: the prescale factor for the MCPrescale
            mctype: the type of the MC, in this case it is CORSIKA

        Return:
            exeFile: the file that need to be executed

        """

        self.checkIfInputExists(inputFile)

        outputFolder = f"{self.outDirectory}/generated/detector"
        outputFolder += f"/Detector_{self.detector}_corsika_icetop.{self.MCdataset}/"

        DETdataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the input file needs to be written

        # Checks if the file already exist, in case so it returns None
        if os.path.isfile(DETdataFile):
            return None, DETdataFile

        self.make_folders(outputFolder, energy)

        # skipkeys="SignalI3MCPEs,BackgroundI3MCPESeriesMap,I3MCPESeriesMap,I3MCPESeriesMapWithoutNoise"
        cmdPython = f"{self.pythonPath} {self.i3build}/simprod-scripts/resources/scripts/detector.py "
        cmdOptions = f"\
            --UseGSLRNG \
            --gcdfile {self.GCD} \
            --IceTop \
            --UseLinearTree \
            --MCPrescale {mcprescale} \
            --MCType {mctype} \
            --LowMem \
            --seed {self.seed} \
            --nproc {nproc} \
            --DetectorName {self.detector} \
            --RunID {runID} \
            --procnum {procnum} \
            --inputfile {inputFile} \
            --outputfile {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "
        if not doFiltering:
            cmdOptions += "--no-FilterTrigger "

        if self.NumbFrames:
            cmdOptions += f"-n {self.NumbFrames} "

        if extraOptions:
            cmdOptions += extraOptions

        cmdMoveFile = f"mv {tempFile} {DETdataFile}"

        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        # Execute DET via submitter
        return exeFile, DETdataFile

    def run_lv1(
        self,
        energy,
        runname,
        DETFile,
        extraOptions="",
    ):
        """
        Runs the level1.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            DETFile: the name of the input file in this case it is the detector output file
            extraOptions: the extra Options that can be passed to the python script

        Return:
            exeFile: the file that need to be executed

        """

        self.checkIfInputExists(DETFile)
        outputFolder = f"{self.outDirectory}/filtered/level1"
        outputFolder += f"/Level1_{self.detector}_corsika_icetop.{self.MCdataset}/"

        LV1dataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the executable file will to be written

        # Checks if the file already exist, if so it there is no need to redo it.
        # It will return None and the file, which will be used as input for the next process
        if os.path.isfile(LV1dataFile):
            return None, LV1dataFile

        self.make_folders(outputFolder, energy)

        cmdPython = f"{self.pythonPath} {self.i3build}/filterscripts/resources/scripts/SimulationFiltering.py "

        cmdOptions = f"\
            --needs_wavedeform_spe_corr \
            --photonicsdir {self.photonDir} \
            -g {self.GCD} \
            -i {DETFile} \
            -o {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "

        if self.NumbFrames:
            cmdOptions += f"-n {self.NumbFrames} "

        if extraOptions:
            cmdOptions += extraOptions

        cmdMoveFile = f"mv {tempFile} {LV1dataFile}"

        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        # Execute LV1 via submitter
        return exeFile, LV1dataFile

    def run_lv2(
        self,
        energy,
        runname,
        LV1File,
        extraOptions="",
    ):
        """
        Runs the level2.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            LV1File: the name of the input file in this case it is the level1 output file
            extraOptions: the extra Options that can be passed to the python script

        Return:
            exeFile: the file that need to be executed

        """

        self.checkIfInputExists(LV1File)
        outputFolder = f"{self.outDirectory}/filtered/level2"
        outputFolder += f"/Level2_{self.detector}_corsika_icetop.{self.MCdataset}/"

        LV2dataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the executable file will to be written

        # Checks if the file already exist, if so it there is no need to redo it.
        # It will return None and the file, which will be used as input for the next process
        if os.path.isfile(LV2dataFile):
            return None, LV2dataFile

        self.make_folders(outputFolder, energy)
        cmdPython = f"{self.pythonPath} {self.i3build}/filterscripts/resources/scripts/offlineL2/process.py "

        cmdOptions = f"\
            --photonicsdir {self.photonDir} \
            -g {self.GCD} \
            -s \
            -i {LV1File} \
            -o {tempFile} > {logsFile}.out 2> {logsFile}.err \
            "

        if self.NumbFrames:
            cmdOptions += f"-n {self.NumbFrames} "

        if extraOptions:
            cmdOptions += extraOptions

        cmdMoveFile = f"mv {tempFile} {LV2dataFile}"

        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        # Execute LV1 via submitter
        return exeFile, LV2dataFile

    def run_lv3(
        self,
        energy,
        runname,
        LV2File,
        runID,
        extraOptions="",
        domeff=1.0,
    ):
        """
        Runs the level3.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            runname is in principle the same as runid but with leading zeros and as a string which is then used for file naming
            LV2File: the name of the input file in this case it is the level2 output file
            runID: the runID of the simulation
            extraOptions: the extra Options that can be passed to the python script
            domeff: the domefficiency of the simulation (default is 1.0)

        Return:
            exeFile: the file that need to be executed

        """

        self.checkIfInputExists(LV2File)
        # if not os.path.isfile(self.Lv3GCD):
        #     raise SystemExit('The Lv3_GCD file has not been created. \nMake sure to do it before running the lv3 reconstruction')

        outputFolder = f"{self.outDirectory}/filtered/level3"
        outputFolder += f"/Level3_Lv3_{self.detector}_{self.dataset}_Run/"

        LV3dataFile = (
            f"{outputFolder}/data/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        tempFile = (
            f"{outputFolder}/temp/{energy}/{runname}.i3.bz2"  # Path and File name
        )
        logsFile = (
            f"{outputFolder}/logs/{energy}/{runname}"  # ERR and OUT file destination
        )
        exeFile = f"{outputFolder}/inps/{energy}/{runname}.sh"  # Path where the executable file will to be written

        # Checks if the file already exist, if so it there is no need to redo it.
        # It will return None and the file, which will be used as input for the next process
        if os.path.isfile(LV3dataFile):
            return None, LV3dataFile

        self.make_folders(outputFolder, energy)

        cmdPython = f"{self.pythonPath} {self.i3build}/icetop_Level3_scripts/resources/scripts/level3_iceprod.py "
        cmdOptions = f"\
            -d {self.detector} \
            --isMC \
            --waveforms \
            --spe-corr \
            --do-inice \
            --print-usage \
            --dataset {self.dataset} \
            --run {runID} \
            -o {tempFile} > {logsFile}.out 2> {logsFile}.err \
            {self.GCD} {LV2File} \
            "
        # --domeff {domeff} \ #TODO Why no domeff?
        # --L2-gcdfile {self.GCD} \
        # --L3-gcdfile {self.Lv3GCD} \
        # --photonicsdir {self.photonDir} \

        if self.NumbFrames:
            cmdOptions += f"-n {self.NumbFrames} "

        if extraOptions:
            cmdOptions += extraOptions

        cmdMoveFile = f"mv {tempFile} {LV3dataFile}"

        self.writeSHexeFile(exeFile, cmdPython, cmdOptions, cmdMoveFile)

        # Execute LV3 via submitter
        return exeFile, LV3dataFile

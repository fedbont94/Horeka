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
            NumbSamples: the number of samples to be simulated (default 100)
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

        self.i3build = i3build
        self.outDirectory = outDirectory
        self.detector = f"{detector}.{year}"
        self.GCD = GCD

    ########################### Useful functions ############################

    def checkIfInputExists(self, inputFile):
        """
        Checks if the input file exists, if not a working message is shown
        """
        fileToCheck = pathlib.Path(inputFile)
        if not fileToCheck.is_file():
            import warnings

            warnings.warn(
                f"\
                    \nThe program is not stopped, but be aware that: \
                    \n{inputFile} \
                    \n!!!!! DOES NOT EXIST !!!!!\
                    \n",
                stacklevel=2,  # This is to show the line where the warning is raised and not repeated twice
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

        rgen[logE>4.0] = 400
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
            4: 400 - 100,
            5: 800 - 200,
            6: 1100 - 200,
            7: 1700 - 200,
            8: 2600 - 200,
            9: 3900 - 200,
        }
        return radius[logE]

    ########################### Main simulation scipts ####################################
    def run_simITExDefault(self, energy, runname, inputFile, runID, extraOptions=""):
        """
        Runs the build/surface-sim-scripts/resources/scripts/simITExDefault.py scripts with the default options
        --------------------------------------------------------
        Parameters:
            energy: the energy in log10 E/GeV
            inputFile: the name of the input file in this case it is the Corsika output file

            runid is the number of the corsika shower
            procnum is the index of the run in the set of given inputs, so the first run that will be processed has procnum 1, no matter what the runid is, the last is my example would be 667

            extraOptions: the extra Options that can be passed to the python script
        Return:
            exeFile: the file that need to be executed
        """
        self.checkIfInputExists(inputFile)
        outputFolder = f"{self.outDirectory}/generated/"
        outputFolder += f"/ITExDefault_{self.detector}_icetop.{self.MCdataset}/"

        ITExFile = (
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
        if os.path.isfile(ITExFile):
            return None, ITExFile

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
        cmdPython = f"{self.pythonPath} {self.i3build}/surface-sim-scripts/resources/scripts/simITExDefault.py "
        cmdOptions = f"\
            --output {tempFile} > {logsFile}.out 2> {logsFile}.err \
            --gcd {self.GCD} \
            -s {self.NumbSamples} \
            -x -235 \
            -y 140 \
            -r {self.get_radius(energy)} \
            --seed {self.seed} \
            --run_id {runID} \
            {inputFile} \
            "
        # --no_ice_top
        # --arrang
        # --raise-observation-level 0 \

        if extraOptions:
            cmdOptions += extraOptions

        # moves the file to its final location once everything is done
        cmdMoveFile = f"mv {tempFile} {ITExFile}"

        # writes the sh file and makes it executable
        self.writeSHexeFile(
            exeFile, cmdPython, cmdOptions, cmdMoveFile, cmdSTART=cmdSTART
        )

        return exeFile, ITExFile

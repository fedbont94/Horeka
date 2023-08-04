#!/usr/bin/env python3
import os


class ProcessRunner:
    """
    This class is used to run the simulations and call the shell scripts.
    -----------------------------------------------------------------------
    Parameters:
        detectorSim: the detector simulation class
        submitter: the submitter class
        energies: the energy range that will be simulated
        inDirectory: the directory where the data corsika files are located
    """

    def __init__(
        self,
        detectorSim,
        submitter,
        energies,
        inDirectory,
    ):
        self.detectorSim = detectorSim
        self.submitter = submitter
        self.energies = energies
        self.inDirectory = inDirectory

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
                keyArgs = [energy, inDir + corsikaFile, runname, runID]
                yield (f"{energy}_{runname}", keyArgs)

    def run_processes(self, energy, corsikaFile, runname, runID):
        """
        This functions can be edited and can be used for running all processes needed that can ebe found in DetectorSimulator
        If your function is not available, add it to the class and run it here.
        """
        ##################################### ITExDefault ##########################################
        exeFile, ITExFile = self.detectorSim.run_simITExDefault(
            energy=energy,
            runname=runname,
            inputFile=corsikaFile,
            runID=runID,
        )
        if exeFile is not None:
            print(energy, runname, "run_simITExDefault")
            self.executeFile(key=f"{energy}_{runname}_ITEx", exeFile=exeFile)

        return

    def executeFile(self, key, exeFile):
        """
        This function executes the sh file that was created by the DetectorSimulator class.
        And comminicates with the file has completed so that the log and the err file can be created and the new process can be started.
        """
        self.submitter.startSingleProcess(key, exeFile)
        self.submitter.communicateSingleProcess(key)
        return

#!/usr/bin/env python3
"""
This class can be used for generating the submission stings and sh executable files. 
It also has the generator function which yields the keys and string to submit, 
made via the combinations of file and energies 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""
import numpy as np
import os
import stat

class SimulationMaker:
    """
    This class has to useful functions. 
        generator: which yields a key and a string to submit 
        makeStringToSubmit: which writes a temporary file and a string to submit
    
    Parameters:
        startNumber:    the start of the simulation (eg. integer default value 0)
        endNumber:      the end of the simulation (eg. integer default value if startNumber is 0, 
                        it is the total number of simulations.
        energies:       the array binned in energies for the simulation
        fW:             the file writer class. In order to use some of the functions in this class
        pathCorsika:    the path where Corsika is installed
        corsikaExe:     the name of the Corsika executable that needs to be used
    
    """
    def __init__(self, startNumber, endNumber, energies, fW, pathCorsika, corsikaExe):
        self.startNumber = startNumber
        self.endNumber = endNumber
        self.energies = energies
        self.fW = fW
        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe

    def generator(self):
        """
        This function generates all possible configuration of energy and file number. 
        It yields the key and the String to submit
        The yield function returns every time a different value as the for loop proceeds
        """
        # This is a loop over all energies and gives the low and high limit values.
        # Eg. 5.0 and 5.1
        for log10_E1, log10_E2 in zip(self.energies[:-1], self.energies[1:]):
            # Creates "data", "temp", "log", "inp" folders and energy subfolder
            self.fW.makeFolders(log10_E1)

            # It loops over all the unique numbers 
            # for procNumber, runNumber in zip(binArray[:-1], binArray[1:]):
            for runIndex in range(self.startNumber, self.endNumber):
                # Creates the file name for the simulation
                # The runNumber is calculated as follows:
                # EEiiii where EE is the energy in log10/GeV *10 
                # and iiii is the run index number. 
                runNumber = int(log10_E1 * 10_000 * 10 + runIndex) 
                #remove the *10 for energies above 10 - otherwise the filenames are messed up
                
                # Check if this simulation is not in data. Thus, was already created
                # There is thus no need to redo it
                if f"DAT{runNumber}" not in os.listdir(
                    f"{self.fW.directories['data']}/{log10_E1}/"
                ):
                    # It writes the Corsika input file 
                    self.fW.writeFile(runNumber, log10_E1, log10_E2)
                    # The unique key for the the Submitter is created as followed. 
                    # It has not practical use, nut MUST be unique 
                    key = f"{log10_E1}_{runNumber}"
                    # It calls the function to create a sting which will be used for the job execution
                    stringToSubmit = self.makeStringToSubmit(log10_E1, runNumber)
                    yield (key, stringToSubmit)

    def makeStringToSubmit(self, log10_E, runNumber):
        # A few paths to files are defined. 
        inpFile = f"{self.fW.directories['inp']}/{log10_E}/SIM{runNumber}.inp" # input file
        logFile = f"{self.fW.directories['log']}/{log10_E}/DAT{runNumber}.log" # log file 
        # The move command which moves the file from the temporary directory to the data directory 
        # when the simulation is completed
        mvDATfiles = f"mv {self.fW.directories['inp']}/{log10_E}/DAT{runNumber} {self.fW.directories['data']}/{log10_E}/DAT{runNumber}"
        
        # Makes a temp file for the execution of corsika.
        tempFile = f"{self.fW.directories['temp']}/{log10_E}/temp_{runNumber}.sh"
        with open(tempFile, "w") as f:
            f.write(r"#!/bin/sh") # This shows that the file is an executable
            f.write(
                f"\ncd {self.pathCorsika}" # You must execute corsika in its folder. Otherwise returns an error
                # You must delete corsika non completed files. Otherwise returns an error and exits without executing the file 
                + f"\nrm {self.fW.directories['inp']}/{log10_E}/DAT{runNumber}" # Removes the non-completed simulation file if already existing
                + f"\nrm {self.fW.directories['inp']}/{log10_E}/DAT{runNumber}.long" # Removes the non-completed long file if already existing
                + f"\nrm {logFile}" # Removes the non-completed log file if already existing
                # remove old radio files created by corsika
                + f"\nrm -r {self.fW.directories['inp']}/{log10_E}/SIM{runNumber}_coreas"
                + f"\nrm {self.fW.directories['inp']}/{log10_E}/SIM{runNumber}_coreas.bins"
                # TODO check if you use mpi or not - the commands for executing corsika are different
                # + f"\n{self.pathCorsika}/{self.corsikaExe} < {inpFile} > {logFile}" # This is how you execute a corsika file
                + f"module load compiler/gnu/10.2"
                + f"module load mpi/openmpi/4.1"
                + f"\nmpirun --bind-to core:overload-allowed --map-by core -report-bindings {self.pathCorsika}/{self.corsikaExe} {inpFile} > {logFile}" # This is how you execute an mpi corsika file
                + f"\n{mvDATfiles}" # Move the DAT files from inp directory to the data directory
                # + f"\nrm {tempFile}" # It removes this temporary file since it is not needed anymore
                + f"\n "
            )


        # Make the file executable
        st = os.stat(tempFile)
        os.chmod(tempFile, st.st_mode | stat.S_IEXEC)

        # The stringToSubmit is basically the execution of the temporary sh file
        subString = tempFile
        return subString


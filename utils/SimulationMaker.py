#!/usr/bin/env python3
"""
This class can be used for generating the submission stings and sh executable files. 
It also has the generator function which yields the keys and string to submit, 
made via the combinations of file and energies 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022

edited for radio by 
@author: Jelena
@date: June 2023

Submitting the sims with this program takes too long with Corsika :(
It's actually better to do one job per shower - for Coreas at least.
So FOR RADIO: use this whole thing to create the input and sh files 
and then run those separately using submit_jobs.py

"""
import numpy as np
import os
import stat
from utils.runNumberGenerator import runNumberGenerator

class SimulationMaker:
    """
    This class has two useful functions. 
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
    def __init__(self, 
                 startNumber, 
                 endNumber, 
                 energies, 
                 fW, 
                 pathCorsika, 
                 corsikaExe, 
                 zenith, 
                 azimuth, 
                 primary_particle
    ):
        
        self.startNumber = startNumber
        self.endNumber = endNumber
        self.energies = energies
        self.fW = fW
        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe
        self.zenith = zenith
        self.azimuth = azimuth
        self.primary_particle = primary_particle
        self.runNumGen = runNumberGenerator()



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
            for runIndex in range(self.startNumber, self.endNumber):
                # Creates the file name for the simulation
                particleID = self.runNumGen.getPrimaryID(self.primary_particle)
                zenithID = self.runNumGen.getZenithID(self.zenith)
                azimuthID = self.runNumGen.getAzimuthID(self.azimuth)
                # 
                print(particleID, azimuthID, runIndex)
                runNumber = format(int(particleID * 1E5 + zenithID * 1E4 + azimuthID * 1E3 + runIndex), '06d')
                print(runNumber)
                
                # Check if this COREAS (!) simulation is not in inp. 
                # If so, this simulation was already created
                # There is thus no need to redo it
                if f"SIM{runNumber}_coreas" not in os.listdir(
                    f"{self.fW.directories['inp']}/{log10_E1}//"

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
        
        # Makes a temp file for submitting the jobs.
        tempFile = f"{self.fW.directories['temp']}/{log10_E}/temp_{runNumber}.sh"
        with open(tempFile, "w") as f:
            f.write(r"#!/bin/sh") # This shows that the file is an executable
            f.write(
                f"\n"
                # You must delete corsika non completed files. Otherwise returns an error and exits without executing the file 
                # + f"\nrm {self.fW.directories['inp']}/{log10_E}/DAT{runNumber}" # Removes the non-completed simulation file if already existing
                # + f"\nrm {self.fW.directories['inp']}/{log10_E}/DAT{runNumber}.long" # Removes the non-completed long file if already existing
                # + f"\nrm {logFile}" # Removes the non-completed log file if already existing
                # # remove old radio files created by corsika
                # + f"\nrm -r {self.fW.directories['inp']}/{log10_E}/SIM{runNumber}_coreas"
                # + f"\nrm {self.fW.directories['inp']}/{log10_E}/SIM{runNumber}_coreas.bins"
                + f"\nrm -r {self.fW.directories['data']}" # not used in radio
                + f"\n"
            )


        # Make the file executable
        st = os.stat(tempFile)
        os.chmod(tempFile, st.st_mode | stat.S_IEXEC)

        # The stringToSubmit is basically the execution of the temporary sh file
        subString = tempFile
        return subString


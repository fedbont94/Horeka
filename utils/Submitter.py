#!/usr/bin/env python3

"""
This is the master script which spawns subprocesses for multiple instances instead of multiple job submissions.
This takes a single CPU and actually performs a busy wait in Popen.communicate function.
"""
# import os
# import numpy as np
import subprocess
import time

class Submitter:
    """
    Classed used for calling multiple scripts in a single submission (eg. on the Horeka cluster)
    """
    def __init__(self, MakeKeySubString, logDir, parallel_sim=50):
        """
        Parameters:
        key_processString_generator: is a function that yields the key and process string needed for the simulation
        logDir: Directory where log files are stored
        parallelRunningSims: number of parallel processes that wants to be executed
        processDict: Dictionary where all the running processes are stored
        """
        
        self.key_processString_generator = MakeKeySubString()
        self.logDir = logDir
        self.parallelRunningSims = parallel_sim
        self.processDict = {}

    def startProcesses(self):
        """
        It is the first function to be called.
        It starts as many processes as chosen.
        """
        print("Start Process")
        for _ in range(self.parallelRunningSims):
            self.startSingleProcess()        
            
    def startSingleProcess(self):
        """
        It starts a single process.
        It gets the key and the processString returned by the yield
        in the key_processString_generator function.
        The next command gets the value from the generator which yield
        both key and processString. In case there is no more value,
        it will return None. 
        Thus, the if checks if the keys is valid, to avoid a wrong execution.
        It uses then a Popen to spawn a single process and 
        adds it to the processDict.
        In case the key is not valid, it prints a message to the user.
        """       
        key, processString = next(self.key_processString_generator, (None, None))
        if key is not None:
            self.processDict[key] = subprocess.Popen(
                processString.split(),
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ) 
        else:
            print("No more files in yield")        
        return
    
    def checkRunningProcesses(self):
        """
        It is a continuos check over the running simulations.
        As long as there are keys in the processDict it keeps the checking.
        If one process is completed, it calls communicateSingleProcess.
        It then waits a few seconds before performing the checks again.
        This is done to avoid overloading the CPU with useless checks 
        """     
        # Gets all the keys in the processDict which needs to be used in the loop
        keyToLoop = list(self.processDict.keys())

        # If there are processes active it keeps looping in while
        while keyToLoop:
            for key in keyToLoop:
                # Check if the process is completed
                if self.processDict[key].poll() is not None:
                    
                    # Communicates the process that is completed
                    keyToLoop = self.communicateSingleProcess(key)
            
            # Waits before restarting the loop.
            # This is done to avoid overloading the CPU with useless checks 
            sleepTime = 10
            time.sleep(sleepTime)
        return

            
    def communicateSingleProcess(self, key):
        """
        After the check if the process is completed, it communicates the output.
        Writes the process output and errors to che chosen directory
        Pops the process which is completed from the processDict and kills it.
        Starts a new single process
        
        Parameters:
        key: the key of the process to communicate
        
        Returns:
        keyToLoop: The updated list of processes keys which has to be in loop
        """        
        out, err = self.processDict[key].communicate()
        if out is None or err is None:
            return list(self.processDict.keys())
        with open(f"{self.logDir}/output_{key}.out", "w") as f:
            f.write(str(out))
        with open(f"{self.logDir}/output_{key}.err", "w") as f:
            f.write(str(err))

        print("Deleting key")
        self.deleteSingleProcess(key)
        
        print("\n==================== New Process ====================")
        self.startSingleProcess()

        keyToLoop = list(self.processDict.keys())
        return keyToLoop


    def deleteSingleProcess(self, key):
        """
        Pops the process from the processDict and kills it,
        in order to be sure that the memory is freed
        
        Parameters:
        key: the key of the process to kill
        """
        if key in self.processDict.keys():
            self.processDict.pop(key).kill()


# def mainLoop():
#     """
#     This is the main part of the code.
#     It calls the class Submitter where you need to define:

#     prim: name of the primary
#     energies: array or list of energies 
#     numbOfFiles: number of files in the folder per energy per zenith
#     parallelRunningSims: number of parallel detector response simulations that wants to be processed
#     processDict: Directory where all the running detector responses are stored
#     generated_paths: is an that references to the function that yields the variables needed for the simulation
#     """
    
#     submitter = Submitter(
#                 MakeKeySubString=TODO_function(), 
#                 num_files=201, 
#                 logDir="", 
#                 parallel_sim=50)

#     # It starts the submitting by submitting as many processes as chosen
#     submitter.startProcesses()
    
#     # It starts the checks on the running processes
#     submitter.checkRunningProcesses()


# if (__name__ == '__main__'):
    
#     mainLoop()
    
#     print("-------------------- Program finished --------------------")

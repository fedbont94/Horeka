#!/bin/env python3

import time 
import multiprocessing as mp

            
class MultiProcesses:    
    """
    Classed used for calling a function multiple times in a single submission (eg. on the Horeka cluster)
    """
    def __init__(self, keysGenerator, functionToRun, parallel_sim=50) -> None:
        """
        Parameters:
            keysGenerator: is a function that yields the key and process string needed for the simulation
            functionToRun: is a function that holds the processes that need to be run
            parallelRunningSims: number of parallel processes that wants to be executed
            processDict: Dictionary where all the running processes are stored
        """
        self.keysGenerator = keysGenerator()
        self.functionToRun = functionToRun
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
        return
    
    def startSingleProcess(self, key=None, keyArgs=None):
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
        if ((key is None) or (keyArgs is None)):
            key, keyArgs = next(self.keysGenerator, (None, None))
            
        if ((key is not None) and (keyArgs is not None)):            
            print("\n==================== New Process ====================")
            self.processDict[key] = mp.Process(target=self.functionToRun, args=[*keyArgs])
            self.processDict[key].start()
        # else:
        #     print("No more files in yield")        
        return
    
    def checkProcesses(self):
        """
        It is a continuos check over the running simulations.
        As long as there are keys in the processDict it keeps the checking.
        This is done by calling the singleCheck function 
        It then waits a few seconds before performing the checks again.
        This is done to avoid overloading the CPU with useless checks 
        """     
        # Gets all the keys in the processDict which needs to be used in the loop
        keyToLoop = list(self.processDict.keys())

        # If there are processes active it keeps looping in while
        while keyToLoop:
            keyToLoop = self.singleCheck(keyToLoop)            
            # Waits before restarting the loop.
            # This is done to avoid overloading the CPU with useless checks 
            sleepTime = 10
            time.sleep(sleepTime)
        return
    
    
    def singleCheck(self, keyToLoop): 
        """
        Performs a single loop over all running processes and check if one is completed.
        If one process is completed, it pops it out and starts a new one.
        -----------------------------------------------------------------------
        Returns:
            keyToLoop: The updated keys over which the loop has to be performed
        """
        keyToLoop = list(self.processDict.keys())
        for key in keyToLoop:
            if not self.processDict[key].is_alive():
                # Pops out the process that is completed
                self.processDict.pop(key)
                # Starts a new process since one is completed
                self.startSingleProcess()
        # Updates the keys over which the loop has to be performed
        keyToLoop = list(self.processDict.keys())
        return keyToLoop
    
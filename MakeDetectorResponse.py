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


import numpy as np

from utils.Submitter import Submitter
from utils.MultiProcesses import MultiProcesses
from utils.DetectorSimulator import DetectorSimulator
from utils.ProcessRunner import ProcessRunner

from utils.utilsFunctions import generatorFake, make_parser


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
    energies = np.linspace(
        args.energyStart,  # energy starting point
        args.energyEnd,  # energy end point
        int((args.energyEnd - args.energyStart) / args.energyStep)
        + 1,  # number of energies +1 because of the linspace
    ).round(1)

    # The class that creates all the sh files with the python scripts that are needed to run the simulation.
    detectorSim = DetectorSimulator(
        pythonPath=args.pythonPath,
        dataset=args.dataset,
        MCdataset=args.MCdataset,
        seed=args.seed,
        year=args.year,
        NumbSamples=args.NumbSamples,
        i3build=args.i3build,
        outDirectory=args.outDirectory,
        detector=args.detector,  # "IC86"
        GCD=args.GCD,
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

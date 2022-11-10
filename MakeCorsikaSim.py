#!/usr/bin/env python3
"""
This is the main script for the Corsika simulations.
It uses the 3 classes imported from utils

FileWriter class can be used to create and write a Corsika inp file 
    and create "data", "temp", "log", "inp" folders.
    
SimulationMaker class can be used for generating the submission stings and sh executable files. 
    It also has the generator function which yields the keys and string to submit, 
    made via the combinations of file and energies 

Submitter class can be used to spawns subprocesses for multiple instances instead of multiple job submissions.

The args values can be used to specify the desired configuration for the simulation.

How to run:
    python3 MakeCorsikaSim.py 
 if you want to change any configuration from the default once add the [args] after it
 e.g.:
    python3 MakeCorsikaSim.py --user myusername --primary 1 ..... 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""

import numpy as np
from utils.FileWriter import FileWriter
from utils.SimulationMaker import SimulationMaker
from utils.Submitter import Submitter


def mainCorsikaSim(args):
    
    energies = np.linspace(
        args.energyStart, # Start point 
        args.energyEnd, # End point (excluded)
        num=int((args.energyEnd-args.energyStart+args.energyStep)/args.energyStep), # Number of points (end-start+step)/step
        ) 

    fW = FileWriter(
        username=args.username,                 # User name on server
        dirSimulations=args.dirSimulations,
        primary=args.primary,                   # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset=args.dataset,                   # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        azimuth={'start': args.azimuthStart,    # Lower limit of zenith (do not change unless you know what you are doing)
                 'end': args.azimuthEnd},       # Upper limit of zenith (do not change unless you know what you are doing)
        zenith ={'start': args.zenithStart,     # Lower limit of azimuth (do not change unless you know what you are doing)
                 'end': args.zenithEnd},        # Upper limit of azimuth (do not change unless you know what you are doing)
    )

    simMaker = SimulationMaker(
        startNumber=args.startNumber, 
        endNumber=args.endNumber, 
        energies=energies, 
        fW=fW,
        pathCorsika = args.pathCorsika,
        corsikaExe = args.corsikaExe,
    )

    submitter = Submitter(
        MakeKeySubString=simMaker.generator,
        logDir=args.logDirProcesses,
        parallel_sim=args.parallelSim,
    )

    submitter.startProcesses()
    submitter.checkRunningProcesses()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Inputs for the Corsika Simulation Maker"
    )

    parser.add_argument(
        "--username", 
        type=str, 
        default="rn8463", 
        help="your user name on server"
    )
    parser.add_argument(
        "--primary",
        type=int,
        default=1,
        help="primary type: 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe",
    )
    parser.add_argument(
        "--dataset",
        type=float,
        default=13400.0,
        help="dataset number: eg. 13000.0 H, 13100.0 He, 13200.0 Oxygen, 13300.0 Fe, 13400.0 Gamma",
    )
    parser.add_argument(
        "--dirSimulations",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/",
        help="Directory where the simulation are stored",
    )
    parser.add_argument(
        "--pathCorsika",
        type=str,
        default="/home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/",
        help="the /run directory where the executable of corsika is located",
    )
    parser.add_argument(
        "--corsikaExe",
        type=str,
        default="corsika77401Linux_SIBYLL_fluka",
        help="the name of the executable of corsika located in the /run directory",
    )
    parser.add_argument(
        "--startNumber",
        type=int,
        default=0,
        help="start number of simulation (e.g. 0 default)",
    )
    parser.add_argument(
        "--endNumber",
        type=int,
        default=1000,
        help="if you startNumber is 0 then it is equal to the total number of simulation per bin (e.g. 667 default)",
    )

    parser.add_argument(
        "--energyStart", 
        type=float, 
        default=5.0, 
        help="Lower limit of energy"
    )
    parser.add_argument(
        "--energyEnd", 
        type=float, 
        default=7.0, 
        help="Upper limit of energy"
    )
    parser.add_argument(
        "--energyStep", 
        type=float, 
        default=0.1, 
        help="Step in energy, 0.1 default (do not change unless you know what you are doing)"
    )

    parser.add_argument(
        "--azimuthStart", 
        type=float, 
        default=0.00000000, 
        help="Lower limit of zenith (do not change unless you know what you are doing)"
    )
    parser.add_argument(
        "--azimuthEnd", 
        type=float, 
        default=359.99000000, 
        help="Upper limit of zenith (do not change unless you know what you are doing)"
    )
    parser.add_argument(
        "--zenithStart", 
        type=float, 
        default=0.00000000, 
        help="Lower limit of azimuth (do not change unless you know what you are doing)"
    )
    parser.add_argument(
        "--zenithEnd", 
        type=float, 
        default=65.0000000, 
        help="Upper limit of azimuth (do not change unless you know what you are doing)"
    )

    parser.add_argument(
        "--logDirProcesses",
        type=str,
        default="/home/hk-project-pevradio/rn8463/logCorsikaGamma/",
        help="Directory where log files of the multiple subProcesses are stored",
    )
    parser.add_argument(
        "--parallelSim",
        type=int,
        default=100,
        help="Number of parallel simulation processes",
    )

    mainCorsikaSim(args=parser.parse_args())

    print("-------------------- Program finished --------------------")

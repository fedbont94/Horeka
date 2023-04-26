#!/usr/bin/env python3
"""
This is the main script for the Corsika simulations.
It uses the 3 classes imported from utils

FileWriter class can be used to create and write a Corsika inp file 
    and create "data", "temp", "log", "inp" folders.
    
CorsikaSimulator class can be used for generating the submission stings and sh executable files. 
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
import sys
import os
import argparse
import numpy as np

from utils.FileWriter import FileWriter
from utils.CorsikaSimulator import CorsikaSimulator
from utils.Submitter import Submitter


def __checkInputs(args):
    """
    This function should check some basic things before the starting the simulation.
        energyEnd > energyStart
        energyEnd <= 10_000 otherwise the numbering is not unique anymore
        primary is in the keys of the pimIdDict
        check if the corsika given is correct
        maybe a warning if seed value is over 900_000_000

    seedValue = int((runNumber + self.primIdDict[self.primary]*1_000_000) % 900_000_001)
    """
    if not args.energyEnd > args.energyStart:
        sys.exit(
            "The energy End value MUST be greater (nor equal) then the starting one!!"
        )

    if not args.energyEnd <= 10_000:
        sys.exit(
            "The energy End value MUST be less then 10.000!! The seed number is not unique otherwise!"
        )

    if args.primary not in args.primIdDict.keys():
        sys.exit(
            "The primary chosen is not in the primIdDict in the mainCorsikaSim. \nBe sure that the --primary is correct.\
            \nIf so, update the args.primIdDict in the mainCorsikaSim."
        )

    if not os.path.isfile(f"{args.pathCorsika}/{args.corsikaExe}"):
        sys.exit(
            "The corsikaExe does not exist or the pathCorsika is wrong.\
            \nCheck them, please!"
        )

    if args.primIdDict[args.primary] * 1_000_000 > 900_000_001:
        import warnings

        warnings.warn(
            "The program is not stopped, \
            but aware that the Corsika seed number is exceeding 900.000.000 (the max allowed value)"
        )
    return


def get_args():
    parser = argparse.ArgumentParser(
        description="Inputs for the Corsika Simulation Maker"
    )

    parser.add_argument(
        "--username", type=str, default="rn8463", help="your user name on server"
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
        "--energyStart", type=float, default=5.0, help="Lower limit of energy"
    )
    parser.add_argument(
        "--energyEnd", type=float, default=7.0, help="Upper limit of energy"
    )
    parser.add_argument(
        "--energyStep",
        type=float,
        default=0.1,
        help="Step in energy, 0.1 default (do not change unless you know what you are doing)",
    )

    parser.add_argument(
        "--azimuthStart",
        type=float,
        default=0.00000000,
        help="Lower limit of azimuth (do not change unless you know what you are doing)",
    )
    parser.add_argument(
        "--azimuthEnd",
        type=float,
        default=359.99000000,
        help="Upper limit of azimuth (do not change unless you know what you are doing)",
    )
    parser.add_argument(
        "--zenithStart",
        type=float,
        default=0.00000000,
        help="Lower limit of azimuth (do not change unless you know what you are doing)",
    )
    parser.add_argument(
        "--zenithEnd",
        type=float,
        default=65.0000000,
        help="Upper limit of azimuth (do not change unless you know what you are doing)",
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

    return parser.parse_args()


def mainCorsikaSim(args):
    """
    Some Documentation of the main function for the Corsika Simulator

    Defines the indexing of the primaries. This can be updated if needed in the future.
    Checks if the inputs given are consistent with the script
    Defines the energy range
    Calls a bunch of classes
    Finally:
    start spawning and checking multiple simulations.
    """
    # This is a dictionary, with keys the Corsika numbering of primary,
    # and values the arbitrary numbering used in this script for all primary particle.
    # In principle this can be expanded with all primaries that one wants
    args.primIdDict = {
        1: 0,  # Gammas (photons)
        14: 1,  # Protons (H)
        402: 2,  # Helium (He)
        1608: 3,  # Oxygen (O)
        5626: 4,  # Iron (Fe)
        2814: 5,  # Silicon (Si)
    }

    # Checks if the input given are consistent with the structure of the script
    __checkInputs(args)

    # Defines the energy range given the start, end and step
    energies = np.around(  # Need to round the numpy array otherwise the floating is wrong
        np.arange(
            args.energyStart,  # energy starting point
            args.energyEnd
            + args.energyStep,  # energy end point plus one step in order to include last step
            args.energyStep,  # step in energies
        ),
        decimals=1,  # the rounding has to have one single decimal point for the folder.
    )

    fW = FileWriter(
        username=args.username,  # User name on server
        dirSimulations=args.dirSimulations,
        primary=args.primary,  # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset=args.dataset,  # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        primIdDict=args.primIdDict,
        azimuth={
            "start": args.azimuthStart,  # Lower limit of zenith (do not change unless you know what you are doing)
            "end": args.azimuthEnd,
        },  # Upper limit of zenith (do not change unless you know what you are doing)
        zenith={
            "start": args.zenithStart,  # Lower limit of azimuth (do not change unless you know what you are doing)
            "end": args.zenithEnd,
        },  # Upper limit of azimuth (do not change unless you know what you are doing)
    )

    corsikaSim = CorsikaSimulator(
        startNumber=args.startNumber,
        endNumber=args.endNumber,
        energies=energies,
        fW=fW,  # The fileWriter class
        pathCorsika=args.pathCorsika,
        corsikaExe=args.corsikaExe,
    )

    submitter = Submitter(
        MakeKeySubString=corsikaSim.generator,
        logDir=args.logDirProcesses,
        parallel_sim=args.parallelSim,
    )

    # Starts the spawn of the simulations
    submitter.startProcesses()
    # Loops over the running processes and checks if any process is complete.
    # If so, it will spawn the next one
    submitter.checkRunningProcesses()


if __name__ == "__main__":
    args = get_args()

    mainCorsikaSim(args=args)

    print("-------------------- Program finished --------------------")

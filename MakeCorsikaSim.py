#!/usr/bin/env python3

import numpy as np
import os
import stat
from utils.FileWriter import FileWriter
from utils.Submitter import Submitter


class SimulationMaker:
    def __init__(self, startNumber, endNumber, energies, fW):
        self.startNumber = startNumber
        self.endNumber = endNumber
        self.energies = energies
        self.fW = fW

    def generator(self):
        for log10_E1, log10_E2 in zip(self.energies[:-1], self.energies[1:]):
            # we are simulating from 5.0 to 7.9 with 30 bins,
            # each containing 667 showers for a total of 20010

            self.fW.makeFolders(log10_E1)

            binNumber = (log10_E1 - 5) * 10
            binArray = np.arange(
                ((self.startNumber + binNumber) * self.endNumber),
                ((self.startNumber + binNumber + 1) * self.endNumber + 1),
                1,
                np.int,
            )
            for procNumber, runNumber in zip(binArray[:-1], binArray[1:]):
                fileNumber = "4{0:05d}".format(runNumber)
                print(fileNumber)
                if f"DAT{fileNumber}" not in os.listdir(
                    f"{self.fW.directories['data']}/{log10_E1}/"
                ):
                    self.fW.writeFile(procNumber, runNumber, log10_E1, log10_E2)
                    key = f"{log10_E1}_{fileNumber}"
                    stringToSubmit = self.makeStringToSubmit(log10_E1, runNumber)
                    yield (key, stringToSubmit)

    def makeStringToSubmit(self, log10_E, runNumber):
        fileNumber = "4{0:05d}".format(runNumber)
        pathCorsika = "/home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/"
        corsika = f"{pathCorsika}/corsika77401Linux_SIBYLL_fluka"
        inpFile = f"{self.fW.directories['inp']}/{log10_E}/SIM{fileNumber}.inp"
        logFile = f"{self.fW.directories['log']}/{log10_E}/DAT{fileNumber}.log"
        mvCommand = f"mv {self.fW.directories['temp']}/{log10_E}/{fileNumber}DAT{fileNumber} {self.fW.directories['data']}/{log10_E}/DAT{fileNumber}"

        # subString = f"cd {pathCorsika} && {corsika} < {inpFile} > {logFile} && {mvCommand}"

        tempFile = f"{self.fW.directories['temp']}/{log10_E}/temp_{fileNumber}.sh"
        with open(tempFile, "w") as f:
            f.write(r"#!/bin/sh")
            f.write(
                f"\ncd {pathCorsika}"
                + f"\n{corsika} < {inpFile} > {logFile}"
                + f"\n{mvCommand}"
                + f"\nrm {tempFile}"
            )

        # Make the file executable
        st = os.stat(tempFile)
        os.chmod(tempFile, st.st_mode | stat.S_IEXEC)

        # The stringToSubmit is basically the execution of the temporary sh file
        subString = tempFile
        return subString


def mainCorsikaSim(args):
    startNumber = 0  # self.startNumber number of simulation (e.g. 0 default)
    endNumber = 667  # if you startNumber is 0 then it is equal to the total number of simulation per bin (e.g. 667 default)

    energyStart = 5.0  # Lower limit of energy
    energyEnd = 7.0  # Upper limit of energy
    energyStep = 0.1  # Step in energy, 0.1 default
    energies = np.around(
        np.arange(energyStart, energyEnd + energyStep, energyStep), decimals=1
    )

    username = "rn8463"  # User name on server
    dirSimulations = "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/"
    primary = 1  # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
    dataset = 13400.0  # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
    azimuthStart = 0.00000000  # Lower limit of zenith
    azimuthEnd = 359.99000000  # Upper limit of zenith
    zenithStart = 0.00000000  # Lower limit of azimuth
    zenithEnd = 65.0000000  # Upper limit of azimuth

    logDirProcesses = "/home/hk-project-pevradio/rn8463/logCorsikaGamma/"
    parallel_sim = 100

    fW = FileWriter(
        username=username,  # User name on server
        dirSimulations=dirSimulations,
        primary=primary,  # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset=dataset,  # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        azimuthStart=azimuthStart,  # Lower limit of zenith
        azimuthEnd=azimuthEnd,  # Upper limit of zenith
        zenithStart=zenithStart,  # Lower limit of azimuth
        zenithEnd=zenithEnd,  # Upper limit of azimuth
    )

    simMaker = SimulationMaker(
        startNumber=startNumber, endNumber=endNumber, energies=energies, fW=fW
    )

    submitter = Submitter(
        MakeKeySubString=simMaker.generator,
        logDir=logDirProcesses,
        parallel_sim=parallel_sim,
    )

    submitter.startProcesses()
    submitter.checkRunningProcesses()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Inputs for the Corsika Simulation Maker"
    )

    parser.add_argument(
        "--user", type=str, default="rn8463", help="your user name on server"
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
        "--startNumber",
        type=int,
        default=0,
        help="start number of simulation (e.g. 0 default)",
    )
    parser.add_argument(
        "--endNumber",
        type=int,
        default=667,
        help="if you startNumber is 0 then it is equal to the total number of simulation per bin (e.g. 667 default)",
    )

    parser.add_argument(
        "--energyStart", type=float, default=5.0, help="Lower limit of energy"
    )
    parser.add_argument(
        "--energyEnd", type=float, default=7.0, help="Upper limit of energy"
    )
    parser.add_argument(
        "--energyStep", type=float, default=0.1, help="Step in energy, 0.1 default"
    )

    parser.add_argument(
        "--azimuthStart", type=float, default=0.00000000, help="Lower limit of zenith"
    )
    parser.add_argument(
        "--azimuthEnd", type=float, default=359.99000000, help="Upper limit of zenith"
    )
    parser.add_argument(
        "--zenithStart", type=float, default=0.00000000, help="Lower limit of azimuth"
    )
    parser.add_argument(
        "--zenithEnd", type=float, default=65.0000000, help="Upper limit of azimuth"
    )

    parser.add_argument(
        "--logDirProcesses",
        type=str,
        default="/home/hk-project-pevradio/rn8463/logCorsikaGamma/",
        help="Directory where log files of the multiple subProcesses are stored",
    )
    parser.add_argument(
        "--parallel_sim",
        type=int,
        default=100,
        help="Number of parallel simulation processes",
    )

    mainCorsikaSim(args=parser.parse_args())

    print("-------------------- Program finished --------------------")

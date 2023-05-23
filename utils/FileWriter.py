#!/usr/bin/env python3
"""
This class can be used to create and write a Corsika inp file and create "data", "temp", "log", "inp" folders.

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""
import pathlib


class FileWriter:
    """
    This class can be used to create and write a Corsika inp file
    and create "data", "temp", "log", "inp" folders.

    Parameters:
        username,                       # User name on server
        dirSimulations,                 # Simulations directory where the data temp and log folder will be created
        primary,                        # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset,                        # changed on 28 Jan 2020 according to IC std: 13000.0 H, 13100 He, 13200 O, 13300 Fe, 13400 Gamma

        azimuth={'start': 0.00000000,   # Lower limit of azimuth (do not change unless you know what you are doing)
                 'end': 359.99000000},  # Upper limit of azimuth (do not change unless you know what you are doing)
        zenith ={'start': 0.00000000,   # Lower limit of zenith (do not change unless you know what you are doing)
                 'end': 65.0000000},    # Upper limit of zenith (do not change unless you know what you are doing)
    """

    def __init__(
        self,
        username,  # User name on server
        dirSimulations,  # Simulations directory where the data temp and log folder will be created
        primary,  # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset,  # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        primIdDict,  # This is a dictionary, with keys the Corsika numbering of primary,
        # and values the arbitrary numbering used in this script for all primary particle.
        azimuth={
            "start": 0.00000000,  # Lower limit of azimuth (do not change unless you know what you are doing)
            "end": 359.99000000,
        },  # Upper limit of azimuth (do not change unless you know what you are doing)
        zenith={
            "start": 0.00000000,  # Lower limit of zenith (do not change unless you know what you are doing)
            "end": 65.0000000,
        },  # Upper limit of zenith (do not change unless you know what you are doing)
    ):
        self.dataset = dataset
        self.username = username
        self.primary = primary
        self.directories = {"sim": dirSimulations}
        self.primIdDict = primIdDict

        self.azimuth = azimuth
        self.zenith = zenith

    def makeFolders(self, log10_E1):
        """
        Creates "data", "temp", "log", "inp" folders and energy subfolder

        Parameters:
            log10_E1: the log10 of the Energy value for the subfolder creation
        """
        for folder in ["data", "temp", "log", "inp"]:
            self.directories[folder] = f"{self.directories['sim']}/{folder}/"
            # Creates the required directories in case they are not existing
            pathlib.Path(f"{self.directories[folder]}/{log10_E1}").mkdir(
                parents=True, exist_ok=True
            )
        return

    def writeFile(self, runNumber, log10_E1, log10_E2):
        """
        Creates and writes a Corsika inp file that can be used as Corsika input
        """
        en1 = 10**log10_E1  # Lower limit of energy in GeV
        en2 = 10**log10_E2  # Upper limit of energy in GeV

        # The seed value in Corsika is 1 <= seed <= 900_000_000;
        # It was decided to adopt the following seed has the form:
        # pprrrrrr where pp is the primary ID (0, 1, 2...) and rrrrrr is teh 6-digit run number
        # The seedValue is % 900.000.000 so that it does not exceed the max allowed seed value in Corsika
        # Note underscore do not change anything in the python numbers, they just make them easier to read
        seedValue = int(
            (runNumber + self.primIdDict[self.primary] * 1_000_000) % 900_000_001
        )

        sim = f"SIM{runNumber}"
        # This is the inp file, which gets written into the folder
        inp_name = f"{self.directories['inp']}/{log10_E1}/{sim}.inp"

        seed1 = seedValue  # int(np.random.normal(mu, sigma))#random chosen)  #changed on 28 Jan 2020 according to IC std
        seed2 = seed1 + 1
        seed3 = seed1 + 2

        # Opening and writing in the file
        with open(inp_name, "w") as file:
            ######Things that go into the input files for corsika#######
            file.write(
                ""
                + f"RUNNR   {runNumber}\n"  # Unique run number in the file name of corsika
                + f"EVTNR   1\n"
                + f"SEED    {seed1}    0    0\n"  #
                + f"SEED    {seed2}    0    0\n"  #
                + f"SEED    {seed3}    0    0\n"  #
                + f"NSHOW   1\n"
                + f"ERANGE  {en1:.11E}    {en2:.11E}\n"  # in GeV
                + f"ESLOPE  -1.0\n"
                + f"PRMPAR  {self.primary}\n"
                + f"THETAP  {self.zenith['start']}    {self.zenith['end']}\n"  #
                + f"PHIP    {self.azimuth['start']} {self.azimuth['end']}\n"  #
                + f"ECUTS   0.02     0.01    4.0E-04 4.00E-04\n"
                + f"ELMFLG  T    T\n"  # Disable NKG since it gets deactivated anyway when CURVED is selected at corsika setup
                + f"OBSLEV  2840.E2\n"  # changed from 2837 m to 2840 m on 26 Nov 2019
                + f"ECTMAP  100\n"  # It DOES NOT effect sim. example 100 you have all particles with energy > 100 GeV printed in the output file. Also used 1.e11
                + f"SIBYLL  T    0\n"  # Keep this only if we are running sibyll
                + f"SIBSIG  T\n"  # Keep this only if we are running sibyll
                # + f"SIBCHM  T\n"  # Enable charm production with Sibyll
                # + f"ARRANG  -120.7\n"  # Rotates the output from corika to IC coordinates # changed Nov 26 2019
                + f"FIXHEI  0.    0\n"
                + f"HADFLG  0    1    0    1    0    2\n"
                + f"STEPFC  1.0\n"
                # + f"DEBUG   F    6    F    1000000\n"
                + f"MUMULT  T\n"
                + f"MUADDI  T\n"
                + f"MAXPRT  1\n"
                + f"MAGNET  16.75       -51.96\n"  # changed on Nov 26 2019
                + f"LONGI   T   20.     T       T\n"
                + f"RADNKG  2.E5\n"
                + f"ATMOD   33\n"  # real atmosphere (April avg. is used here)
                + f"DIRECT  {self.directories['temp']}/{log10_E1}/\n"
                + f"USER    {self.username}\n"
                + f"EXIT\n"
            )

#!/usr/bin/env python3

import pathlib
import numpy as np
import os

class FileWriter:
    def __init__(self,
        username,                   # User name on server
        dirSimulations,             # Simulations directory where the data temp and log folder will be created
        primary,                    # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset,                    # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        azimuthStart=0.00000000,    # Lower limit of zenith
        azimuthEnd=359.99000000,    # Upper limit of zenith
        zenithStart=0.00000000,     # Lower limit of azimuth
        zenithEnd=65.0000000,       # Upper limit of azimuth
    ):

        self.dataset = dataset
        self.username = username
        self.primary = primary
        self.directories = {"sim":dirSimulations}

        self.azimuthStart = azimuthStart
        self.azimuthEnd = azimuthEnd
        self.zenithStart = zenithStart
        self.zenithEnd = zenithEnd

    def makeFolders(self, log10_E1): 
        self.directories["data"] = f"{self.directories['sim']}/data/"
        self.directories["temp"] = f"{self.directories['sim']}/temp/"
        self.directories["log"] = f"{self.directories['sim']}/log/"
        self.directories["inp"] = f"{self.directories['sim']}/inp/"

        # Creates the required directories in case they are not existing
        for path in self.directories.values():
            pathlib.Path(f"{path}/{log10_E1}").mkdir(parents=True, exist_ok=True)
        return
    
    def writeFile(self, procNumber, runNumber, log10_E1, log10_E2):
        en1 = 10**log10_E1  # Lower limit of energy in GeV
        en2 = 10**log10_E2  # Upper limit of energy in GeV

        seedValue = int(
            (((self.dataset * 100000.0) + (procNumber)) % 100000000.0) + 382710.0
        )  # changed on 28 Jan 2020 according to IC std

        # fileNumber="{0:06d}".format(runNumber) # We need 6 digits for the run number according to corsika format
        # We need 6 digits for the run number according to corsika format
        fileNumber = "4{0:05d}".format(runNumber)  
        sim = "SIM" + fileNumber
        # This is the inp file, which gets written into the folder
        inp_name = (self.directories["inp"] + f"/{log10_E1}/" + sim + ".inp")  
        
        seed1 = seedValue  # int(np.random.normal(mu, sigma))#random chosen)  #changed on 28 Jan 2020 according to IC std
        seed2 = seed1 + 1
        seed3 = seed1 + 2
        
        # Opening and writing in the file 
        with open(inp_name, "w") as file:
            ######Things that go into the input files for corsika#######
            # Unique run number in the file name of corsika
            file.write("RUNNR   {0}\n".format(fileNumber))  
            file.write("EVTNR   1\n")
            file.write("SEED    {0} 0    0\n".format(seed1))  #
            file.write("SEED    {0}    0    0\n".format(seed2))  #
            file.write("SEED    {0}    0    0\n".format(seed3))  #
            file.write("NSHOW   1\n")
            file.write("ERANGE  {0:.11E}    {1:.11E}\n".format(en1, en2))  # in GeV
            file.write("ESLOPE  -1.0\n")
            file.write("PRMPAR  {0}\n".format(self.primary))
            file.write("THETAP  {0}    {1}\n".format(self.zenithStart, self.zenithEnd))  #
            file.write("PHIP    {0} {1}\n".format(self.azimuthStart, self.azimuthEnd))  #
            file.write("ECUTS    0.0500 0.0500 0.0100 0.0020\n")
            # Thinning is not used for low energies
            # file.write('THIN    1.00e-7       {0}     0.0\n'.format(thinningpar))##need to customise thinning par for each energy
            # file.write('THINH   1.000E+00      1.000E+02\n')
            file.write("ELMFLG  T    T\n")
            file.write("OBSLEV  2840.E2\n")  ###changed from 2837 m to 2840 m on 26 Nov 2019
            file.write("ECTMAP  100\n")
            file.write("SIBYLL  T    0\n")  ####Keep this only if we are running sibyll
            file.write("SIBSIG  T\n")  ####Keep this only if we are running sibyll
            #Rotates the output from corika to IC coordinates # changed Nov 26 2019
            file.write("ARRANG  -120.7\n")  ###
            # file.write('FIXHEI  0.    0\n')
            # file.write('FIXCHI  0.\n')
            file.write("HADFLG  0    1    0    1    0    2\n")
            file.write("STEPFC  1.0\n")
            file.write("DEBUG  F    6    F    1000000\n")
            file.write("MUMULT  T\n")
            file.write("MUADDI  T\n")
            file.write("MAXPRT  0\n")
            file.write("MAGNET  16.75       -51.96\n")  ## changed on Nov 26 2019
            # 10 to 20 g/cm2 and last column T to F on 26 Nov 2019
            file.write("LONGI   T   20.     T       F\n")  
            file.write("RADNKG  2.E5\n")
            # real atmosphere changed # updated on 10.10.2022 as Agnieszka suggested
            file.write("ATMOD   33\n")  
            file.write("DIRECT  {0}/{1}/{2}\n".format(self.directories["temp"], log10_E1, fileNumber))
            file.write("USER    {0}\n".format(self.username))
            file.write("EXIT\n")


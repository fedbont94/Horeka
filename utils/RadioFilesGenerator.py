#!/usr/bin/env python3

"""
This class generates the additional input files needed for CoREAS.
The .reas file specifies core position (and other info).
The .list file contains the antenna positions and names of the detector.
In this generator, starshape and detector antennas (e.g. GP13) are combined.
The core position and the center of the starshape array are fixed on 0, while
the detector antennas are moved at random for each run.

@author: Jelena
"""

import numpy as np
import random
from miniradiotools.starshapes import create_stshp_list

class RadioFilesGenerator:

    def __init__(self,
        directory,                  # inp directory
        obslev,                     # Observation level in cm
        runNumber,                  
        log10_E1,
        pathStarshapes,             # the path to the starshapes.list file
        pathAntennas,               # the path to the antennas.list file (the detector antennas)
        zenith,
        azimuth,

    ):
        self.directory = directory
        self.obslev = obslev
        self.runNumber = runNumber
        self.log10_E1 = log10_E1
        self.pathStarshapes = pathStarshapes
        self.pathAntennas = pathAntennas
        self.zenith = zenith
        self.azimuth = azimuth
        self.antennaInfo = {}
        self.starshapeInfo = {}


        """
        For CoREAS it's important that all input files (inp, reas and list) are stored in the same directory.
        CoREAS uses the same directory for input and output (keyword DIRECT in .inp file) and this cannot be 
        changed.

        After the run is complete it is possible to move the files anywhere of course. 
        In SimulationMaker.py I tried to clean things up a bit by moving the DAT files to "data", but for now
        I keep all CoREAS input (inp, reas, list) and output (new .reas file, traces in "SIMxxxxxx_coreas" folder 
        and "SIMxxxxxx_coreas.bins") in "inp".

        Make sure that the value for OBSLEV specified in the .inp file is the same as CoreCoordinateVertical 
        in the .reas file and (approximately) the same for the z component of the antennas in the .list file. 
        Otherwise, CORSIKA will just crash without any explanation.
        """

    def reasWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"

        # This is the .reas file, which gets written into the folder
        reas_name = (f"{self.directory}/{self.log10_E1}/{sim}.reas")  
        
        # Opening and writing in the file 
        with open(reas_name, "w") as file:
            ######Things that go into the reas file for CoREAS#######
            file.write(""
                + f"# CoREAS V1.4 parameter file\n"
                + f"# parameters setting up the spatial observer configuration:\n"
                + f"CoreCoordinateNorth = 0                ; in cm\n"
                + f"CoreCoordinateWest = 0                ; in cm\n"
                + f"CoreCoordinateVertical = {self.obslev}      ; in cm\n"
                + f"# parameters setting up the temporal observer configuration:\n"
                + f"TimeResolution = 2e-10                ; in s\n"
                + f"AutomaticTimeBoundaries = 1e-07            ; 0: off, x: automatic boundaries with width x in s\n"
                + f"TimeLowerBoundary = -1                ; in s, only if AutomaticTimeBoundaries set to 0\n"
                + f"TimeUpperBoundary = 1                ; in s, only if AutomaticTimeBoundaries set to 0\n"
                + f"ResolutionReductionScale = 0            ; 0: off, x: decrease time resolution linearly every x cm in radius\n"
                + f"# parameters setting up the simulation functionality:\n"
                + f"GroundLevelRefractiveIndex = 1.00031200        ; specify refractive index at 0 m asl\n"
                + f"# event information for Offline simulations:\n"
                + f"EventNumber = 1\n"
                + f"RunNumber = {self.runNumber} \n"
                + f"GPSSecs = 0\n"
                + f"GPSNanoSecs = 0\n"
                + f"CoreEastingOffline = 0.0000                ; in meters\n"
                + f"CoreNorthingOffline = 0.0000                ; in meters\n"
                + f"CoreVerticalOffline = 0.0000                ; in meters\n"
                + f"OfflineCoordinateSystem = Reference                ; in meters\n"
                + f"RotationAngleForMagfieldDeclination = 0.12532        ; in degrees\n"
                + f"Comment =\n"
                + f"CorsikaFilePath = ./\n"
                + f"CorsikaParameterFile = {sim}.inp"
            )



    def get_antennaPositions(self):
        """
        Get gp13 positions from gp13.list and move them in x and y.
        .list files are structured like "AntennaPosition = x y z name"
        
        We want to randomly move the antennas, but also not too far from the core.
        Therefore, generate random numbers within a radius of the approximate size of the array.
        """
        # generate random numbers for shifting the antenna positions
        R_GP13 = 2000 # approximate size of GP13 in m
        alpha = 2 * np.pi * random.randint(0,R_GP13) # random angle
        r = R_GP13 * np.sqrt(random.randint(0,R_GP13)) # random radius # the sqrt is supposed to make it a uniform distribution
        
        # calculate the shift in x and y
        dx = r * np.cos(alpha)
        dy = r * np.sin(alpha)

        file = np.genfromtxt(self.pathAntennas, dtype = "str")
        # get antenna positions from file
        # file[:,0] and file[:,1] are useless (they are simply "AntennaPosition" and "=")
        # get the x, y and z positions
        self.antennaInfo["x"] = file[:,2].astype(float) + dx
        self.antennaInfo["y"] = file[:,3].astype(float) + dy
        self.antennaInfo["z"] = file[:,4].astype(float)
        # get the names of the antennas
        self.antennaInfo["name"] = file[:,5]



    def get_starshapes(self):
        """
        get starshape positions from starshapes.list
        .list files are structured like "AntennaPosition = x y z name"

        """

        create_stshp_list(self.zenith, self.azimuth, filename=f"{self.directory}/starshapes/SIM{self.runNumber}.list", 
                        obslevel=int(self.obslev), # for Dunhuang, in cm for corsika
                        obsplane = "sp",
                        inclination=np.deg2rad(61.60523), # for Dunhuang
                        Rmin=0., Rmax=50000., n_rings=20, # for positions in starshape (in cm)
                        arm_orientations=np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]), # for positions in starshape
                        vxB_plot=False
                        )

        file = np.genfromtxt(f"{self.directory}/starshapes/SIM{self.runNumber}.list", dtype = "str")
        
        # get antenna positions from file
        # file[:,0] and file[:,1] are useless (they are simply "AntennaPosition" and "=")
        # get the x and y positions
        self.starshapeInfo["x"] = file[:,2].astype(float)
        self.starshapeInfo["y"] = file[:,3].astype(float)
        self.starshapeInfo["z"] = file[:,4].astype(float)
        # get the names of the antennas
        self.starshapeInfo["name"] = file[:,5]


    def listWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"

        # This is the .list file, which gets written into the folder
        list_name  = (f"{self.directory}/{self.log10_E1}/{sim}.list")  
        
        # Opening and writing in the file
        with open(list_name, 'w') as f:
            # write the positions (x, y, z) and names of the starshape antennas to the .list file
            # for i in range(self.starshapeInfo["x"].shape[0]):
            #     f.write(f"AntennaPosition = {self.starshapeInfo['x'][i]} {self.starshapeInfo['y'][i]} {self.starshapeInfo['z'][i]} {self.starshapeInfo['name'][i]}\n") 
            # write the positions (x, y, z) and names of the detector's antennas to the .list file
            for i in range(self.antennaInfo["x"].shape[0]):
                f.write(f"AntennaPosition = {self.antennaInfo['x'][i]} {self.antennaInfo['y'][i]} {self.antennaInfo['z'][i]} {self.antennaInfo['name'][i]}\n") 
            

    def writeReasList(self):
        # define this to make it easier to call the functions

        self.reasWriter()
        self.get_antennaPositions()
        self.get_starshapes()
        self.listWriter()

#!/usr/bin/env python3
import numpy as np

"""
This class is used to generate runNumbers according to this structure:

RunNumber: <012345>

<0>: proton - 0; iron - 1

<1>: energy: x.0-x.9
   where 0: x.0  (log GeV) - corresponds to E18eV

<2>: zenith: 0-9
   where 0: 65; ...; 8: 85

<3>: azimuth: 0-9
   where 0: 0; ...; 8: 360

<4>: empty (0)

<5>: shower variation

*********

@author: Jelena
@date: June 2023

"""

class RunNumberGenerator:
    """
    This class has functions that are used to create the runNumber in SimulationMaker.py.
        
    Dictionaries:
        energies:       the array binned in energies for the simulation
        zenith:         the zenith angle
        azimuth:        the azimuth angle
        primary:        the primary particle
    
    """
    def __init__(self):

        self.zenithDict = {
                            0: 65,   # 65° get ID 0
                            1: 67.5, # and so forth
                            2: 70,
                            3: 72.5,
                            4: 75,
                            5: 77.5,
                            6: 80,
                            7: 82.5,
                            8: 85,
                                    }
        
        self.azimuthDict = {
                            0: 0,   # 0° get ID 0
                            1: 45,  # and so forth
                            2: 90,
                            3: 135,
                            4: 180,
                            5: 225,
                            6: 270,
                            7: 315,
                            8: 360,
                                    }
        
        # TODO: update for more particles
        self.primaryDict = {
                            14:   0,      # Protons (H) - get ID 0
                            5626: 1,      # Iron (Fe) - get ID 1
                                    }



    def getZenithID(self, zenith_angle):
        zenithID = None
        for key, value in self.zenithDict.items():
            if value == zenith_angle:
                zenithID = key
                break
        return zenithID
    

    
    def getAzimuthID(self, azimuth_angle):
        azimuthID = None
        for key, value in self.azimuthDict.items():
            if value == azimuth_angle:
                azimuthID = key
                break
        return azimuthID
    


    def getPrimaryID(self, primary_particle):
        primaryID = None
        for key, value in self.zenithDict.items():
            if value == primary_particle:
                primaryID = key
                break
        return primaryID
    

    def getEnergyID(self, energy):
        energy = round(energy, 1)  # Truncate energy to one decimal place
        energyID = int(energy*10) # now the energyID has two digits

        return energyID
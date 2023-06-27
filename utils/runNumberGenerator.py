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

class runNumberGenerator:
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
                             65.0 : 0,
                             67.5 : 1,
                             70.0 : 2,
                             72.5 : 3,
                             75.0 : 4,
                             77.5 : 5,
                             80.0 : 6,
                             82.5 : 7,
                             85.0 : 8,
                                    }
        
        self.azimuthDict = {
                             0.0  : 0,
                             45.0 : 1,
                             90.0 : 2,
                             135.0: 3,
                             180.0: 4,
                             225.0: 5,
                             270.0: 6,
                             315.0: 7,
                             360.0: 8,
                                    }
        
        # TODO: update for more particles
        self.primaryDict = {
                            14:   0,      # Protons (H) - get ID 0
                            5626: 1,      # Iron (Fe) - get ID 1
                                    }



    def getZenithID(self, zenith_angle):
        return self.zenithDict[zenith_angle]
    

    
    def getAzimuthID(self, azimuth_angle):
        return self.azimuthDict[azimuth_angle]
    


    def getPrimaryID(self, primary_particle):
        return self.primaryDict[primary_particle]
    
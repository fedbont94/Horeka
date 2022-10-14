#!/usr/bin/env python3

import sys
from sys import argv
import numpy as np
import os

##################
### To run this script :
### python cor_prod_top.py [start] [end]
##################

script = sys.argv[0]
start = sys.argv[1]#####start number of simulation, e.g. 0
end = sys.argv[2]#####end number of simulation, e.g. 100

#primary = int(sys.argv[3]) # = 14 # proton 14 ##  Gamma 1
#zen = float(sys.argv[4]) # = 0.00 # theta in degree

#az1= -299.00000000#####Lower limit of azimuth, corresponds to -299+119=-180 deg in IC coordinates
#az2= 61.00000000#####Upper limit of azimuth, corresponds to 61+119=180 deg in IC coordinates
az1= 0.00000000
az2= 359.99000000

zen1 = 0.00000000#####Lower limit of zenith
zen2 = 65.0000000#####Upper limit of zenith
######In IC, we use decades of 0.1 GeV for running the simulations.
#en1 = 10**7.9#####Lower limit of energy in GeV
#en2 = 10**8.0#####Upper limit of energy in GeV
lge1=5.0
lge2=5.1
en1 = 10**lge1#####Lower limit of energy in GeV
en2 = 10**lge2#####Upper limit of energy in GeV
primary = 1####14 is proton, 5626 is Fe, 1 is gamma, 402 is He, 1608 is O

##username='icecubesim'
#username='kang/7.9'
username='rn8463'

dataset=13400.0 #changed on 28 Jan 2020 according to IC std

bn=((lge1-5.0)*10.0) #changed on 28 Jan 2020        ### we are simulating from 5.0 to 7.9 qith 30 bins, each containing 667 showers
binnum=round(bn,1) #changed on 28 Jan 2020
#print bn,repr(bn),repr(lge1), repr(lge1-5.0), repr(5.1-5.0), binnum
procstart=int(binnum)*(666+1) #changed on 28 Jan 2020
procend=int(binnum)*(666+1)+int(end) #changed on 28 Jan 2020

#for k in np.arange(int(start),int(end)+1):
for k in np.arange(int(procstart),int(procend)+1):

        #changed on 28 Jan 2020 according to IC std
        procnum=k
        runnum=k+1
        seedval=int((((dataset*100000.0) + (procnum)) % 100000000.0) + 382710.0)#changed on 28 Jan 2020 according to IC std

        print(start, end, k, primary, zen1, zen2, az1, az2, en1,en2)

        datadir= "/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/"

        #fileno="{0:06d}".format(runnum)######We need 6 digits for the run number according to corsika format
        fileno="3{0:05d}".format(runnum)######We need 6 digits for the run number according to corsika format
        sim="SIM"+fileno
        inp_name=datadir+sim +".inp"######This is the inp file, which gets written into the folder 
        file= open(inp_name, 'w')

        #####Generating the seeds from a normal distribution with mean = mu and spread = sigma
        #mu, sigma = 100000,10000
        #seed1 = int(np.random.normal(mu, sigma))#random chosen)
        seed1 = seedval#int(np.random.normal(mu, sigma))#random chosen)  #changed on 28 Jan 2020 according to IC std
        seed2 = seed1+1
        seed3 = seed1+2
        ##thinningpar = e1*1.00e-7###energy times wmax

        ######Things that go into the input files for corsika#######
        file.write('RUNNR   {0}\n'.format(fileno))#####Should be the same as run number in the file name of corsika, do not give the same run number for two different runs
        file.write('EVTNR   1\n')
        file.write('SEED    {0} 0    0\n'.format(seed1)) #
        file.write('SEED    {0}    0    0\n'.format(seed2)) #
        file.write('SEED    {0}    0    0\n'.format(seed3)) #
        file.write('NSHOW   1\n')
        file.write('ERANGE  {0:.11E}    {1:.11E}\n'.format(en1,en2)) # in GeV
        file.write('ESLOPE  -1.0\n')
        file.write('PRMPAR  {0}\n'.format(primary))
        file.write('THETAP  {0}    {1}\n'.format(zen1, zen2)) #
        file.write('PHIP    {0} {1}\n'.format(az1, az2)) #
        file.write('ECUTS        0.0500 0.0500 0.0100 0.0020\n')
        #file.write('THIN    1.00e-7       {0}     0.0\n'.format(thinningpar))##need to customise thinning par for each energy
        #file.write('THINH   1.000E+00      1.000E+02\n') 
        file.write('ELMFLG  T    T\n')
        file.write('OBSLEV  2840.E2\n')    ###changed from 2837 m to 2840 m on 26 Nov 2019
        file.write('ECTMAP  100\n')
        file.write('SIBYLL  T    0\n')####Keep this only if we are running sibyll
        file.write('SIBSIG  T\n')####Keep this only if we are running sibyll
        file.write('ARRANG  -120.7\n')####Rotates the output from corika to IC coordinates # changed Nov 26 2019
        #file.write('FIXHEI  0.    0\n')
        #file.write('FIXCHI  0.\n')
        file.write('HADFLG  0    1    0    1    0    2\n')
        file.write('STEPFC  1.0\n')
        file.write('DEBUG  F    6    F    1000000\n')
        file.write('MUMULT  T\n')
        file.write('MUADDI  T\n')
        file.write('MAXPRT  0\n')
        file.write('MAGNET  16.75       -51.96\n') ## changed on Nov 26 2019
        file.write('LONGI   T   20.     T       F\n') ## 10 to 20 g/cm2 and last column T to F on 26 Nov 2019
        file.write('RADNKG  2.E5\n')
        file.write('ATMOD   0\n')    #real atmosphere (April avg. is used here)# changed from 10 to 0 on 26th Nov.2019
        file.write('ATMA    -69.7259        -2.79781        0.262692        -8.41695e-05    0.00207722\n')
        file.write('ATMB    1111.7        1128.64        1413.98        587.688\n')
        file.write('ATMC    766099.0        641716.0        588082.0         693300.0        5.4303203E9\n')
        file.write('ATMLAY  760000.0        2200000.0       4040000.0        10000000.0\n')
        file.write('DIRECT  /lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/temp/{0}/{1}\n'.format(lge1,fileno))
        file.write('USER    {0}\n'.format(username))
        file.write('EXIT\n')

        file.close()

README.md multiple corsika simulations on Horeka

@author: Federico Bontempo <federico.bontempo@kit.edu> \
				 PhD student KIT Germany\
@date: October 2022
-------------------------------------------------------------------------------

This folder contains all the necessary scripts to run a multiple corsika simulations in a single submission.

How to submit a job to the cluster:\
./ExecuteSubFile.sh

How to run the python script:\
python3 MakeCorsikaSim.py [--args] # as shown in SubFile.sub

Summary:\
README.md -         This file

ExecuteSubFile.sh - Is an executable that submits on slurm (Horeka cluster) the SubFile.sub \
SubFile.sub -       Contains all the requests in terms of memory, time, node... for the cluster\
                    It loads .bashrc (can be taken out if not necessary)\
                    It cd in the corsika/run/ folder, you may need to change the path\
                    It calls the python script with all arguments that need to be passed and MUST be adapted to your interests.

MakeCorsikaSim.py - Is the main script that for Corsika air shower simulation (more documentation in the script)


utils/FileWriter.py -       Contains a class that can be used to create and write a Corsika inp file and create "data", "temp", "log", "inp" folders. \
                            (more documentation in the script)
utils/SimulationMaker.py -  Contains a class that can be used for generating the submission stings and sh executable files. \
                            It also has the generator function which yields the keys and string to submit, 
                            made via the combinations of file and energies \
utils/Submitter.py -        Contains a class that can be used to spawns subprocesses for multiple instances instead of multiple job submissions.

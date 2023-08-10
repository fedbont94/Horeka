# author: Jelena

import numpy as np
import os
import stat

class SubFilesGenerator:

    def __init__(self,
        inpdir,
        logdir,
        runNumber,                  
        log10_E1,
        zenith,
        pathCorsika = "/home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/",
        corsikaExe = "/mpi_corsika77420Linux_SIBYLL_urqmd_thin_coreas_parallel_runner",
        
    ):
        self.inpdir = inpdir
        self.logdir = logdir
        self.runNumber = runNumber
        self.log10_E1 = log10_E1

        self.zenith = zenith

        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe


        """
        Generate sub files for Horeka 
        (by Jelena)

        """


    def subWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"
        # create the DATxxxxxx ID
        dat = f"DAT{self.runNumber}"

        # This is the .sub file, which gets written into the folder
        sub_file = (f"{self.inpdir}/{self.log10_E1}/{sim}.sub")
        # and the corsika files
        inpFile = f"{self.inpdir}/{self.log10_E1}/{sim}.inp" # input file
        logFile = f"{self.logdir}/{self.log10_E1}/{dat}.log" # log file


        # directory containing the simulation files (input + output)
        inpdir = f"{self.inpdir}/{self.log10_E1}/"
        # create a directory to move all annoying files to after the sim is completed
        datdir = f"{self.inpdir}/{self.log10_E1}/{dat}/"



        # get theta
        theta = self.zenith

        # specify runtime according to theta
        # larger theta require more runtime
        if theta >= 65:
            runtime = "10:00:00"
        elif theta >= 75:
            runtime = "12:00:00"
        elif theta >= 77.5:
            runtime = "16:00:00"
        elif theta >= 80:
            runtime = "30:00:00"
        else:
            runtime = "08:00:00"


        # Opening and writing in the file 
        with open(sub_file, "w") as file:
            ######Things that go into the sub file for Horeka#######
            file.write(""
                + f"#!/bin/bash\n" 
                + f"#SBATCH --job-name={self.runNumber}\n"
                + f"#SBATCH --output=/home/hk-project-radiohfi/bg5912/work/sims/GRAND/lukas/logs/_log%j.out\n"
                + f"#SBATCH --error=/home/hk-project-radiohfi/bg5912/work/sims/GRAND/lukas/logs/_log%j.err\n"
                + f"#SBATCH --nodes=1\n"
                + f"#SBATCH --ntasks-per-node=76\n"
                + f"#SBATCH --cpus-per-task=1\n"
                + f"#SBATCH --time=2-00:00:00\n" #{self.runtime}
                + f"\n"
                + f"# Load MPI module (if necessary)\n"
                + f"# module load mpi\n"
                + f"# Set the path to your MPI-Corsika executable\n"
                + f"MPI_CORSIKA_EXEC='{self.pathCorsika}/{self.corsikaExe}'\n"
                # CORSIKA_EXEC='{self.pathCorsika}/{self.corsikaExe}'\n"
                + f"\n"
                + f"# Set the path to your input and output files\n"
                + f"INPUT_FILE='{inpFile}'\n"
                + f"LOG_FILE='{logFile}'\n"
                + f"\n"
                + f"# Run the MPI-Corsika executable\n"
                + f"echo starting job number {self.runNumber} complete\n"
                + f"echo time: $(date)\n" # print current time
                + f"mpirun --bind-to core:overload-allowed --map-by core -report-bindings -np $SLURM_NTASKS $MPI_CORSIKA_EXEC $INPUT_FILE > $LOG_FILE\n"
                # $CORSIKA_EXEC < $INPUT_FILE > $LOG_FILE\n d
                + f"rm {inpdir}/starshapes/\n"# remove the starshape files
                + f"mkdir {datdir}\n" # create datdir directory
                + f"echo created {datdir}\n"
                + f"mv {inpdir}/DAT??????-* {datdir}\n" # move all annoying files to datdir
                + f"mv {inpdir}/corsika-timetable-* {datdir}\n"
                + f"echo job number {self.runNumber} complete\n"
                + f"echo time: $(date)\n" # print current time
            )

        # Make the file executable
        st = os.stat(sub_file)
        os.chmod(sub_file, st.st_mode | stat.S_IEXEC)



    def writeSubFiles(self):
        # define this to make it easier to call the functions

        self.subWriter()
        
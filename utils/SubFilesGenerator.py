import numpy as np
import random

class SubFilesGenerator:

    def __init__(self,
        directory,                  # inp directory
        runNumber,                  
        log10_E1,
        zenith ={'start': 65.00000000,  # Lower limit of azimuth (do not change unless you know what you are doing)
                 'end': 85.0000000},    # Upper limit of azimuth (do not change unless you know what you are doing)
        
    ):
        self.directory = directory
        self.runNumber = runNumber
        self.log10_E1 = log10_E1

        self.zenith = zenith


        """
        Generate sub files for Horeka 
        (by Jelena) and it is clear <3

        """

    def subWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"

        # This is the .sub file, which gets written into the folder
        sub_file = (f"{self.directory}/{self.log10_E1}/{sim}.sub")
        # and the .sh file
        sh_file = (f"{self.directory}/{self.log10_E1}/{sim}.sh")
        

        # find theta
        theta = self.zenith['start']

        # specify runtime according to theta
        # larger theta require more runtime
        if theta >= 70:
            runtime = "04:00:00"
        elif theta >= 75:
            runtime = "06:00:00"
        elif theta >= 77.5:
            runtime = "10:00:00"
        elif theta >= 80:
            runtime = "30:00:00"
        else:
            runtime = "03:00:00"


        # Opening and writing in the file 
        with open(sub_file, "w") as file:
            ######Things that go into the sub file for Horeka#######
            file.write(""
                + f"#!/bin/bash"
                + f"#SBATCH --job-name={sim}" # job name is the sim number
                + f"#SBATCH --output=/home/hk-project-radiohfi/bg5912/work/sims/GRAND/june/logs/_log%j.out"
                + f"#SBATCH --error=/home/hk-project-radiohfi/bg5912/work/sims/GRAND/june/logs/_log%j.err"
                + f"#SBATCH --nodes=2"
                + f"#SBATCH --cpus-per-task=12"
                + f"#SBATCH --tasks=2"
                + f"#SBATCH --time={runtime}"
                + f""
                + f"{sh_file}" # run the corresponding sh file, which submits the job to the cluster
            )



    def shWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"

        # This is the .sub file, which gets written into the folder
        sub_file = (f"{self.directory}/{self.log10_E1}/{sim}.sub")
        # and the .sh file
        sh_file = (f"{self.directory}/{self.log10_E1}/{sim}.sh")
        
        # Opening and writing in the file 
        with open(sh_file, "w") as file:
            ######Things that go into the sh file for Horeka#######
            file.write(""
                + f"#!/bin/bash"
                + f"sbatch -p cpuonly -A hk-project-radiohfi {sub_file}"
                # specify the partition you want (e.g. cpuonly)
                # specify the project you've been assigned to (e.g. radiohfi)
            )
            


    def writeSubFiles(self):
        # define this to make it easier to call the functions

        self.subWriter()
        self.shWriter()
        
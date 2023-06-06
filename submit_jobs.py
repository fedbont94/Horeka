"""
This script is based on submit_list.sh by Felix Schlüter, translated to python using chatGPT
and modified by Jelena :)
"""
import os
import subprocess
import time

directory = '/path/to/directory'  # Replace with the desired directory path

sub_files = [file for file in os.listdir(directory) if file.endswith('.sub')]

while True:
    if sub_files:
        nrun = int(subprocess.check_output("squeue | grep 'bg5912  R' | wc -l", shell=True))
        npen = int(subprocess.check_output("squeue | grep 'bg5912 PD' | wc -l", shell=True))
        ava_jobs = 300 - nrun - npen
        print(ava_jobs)

        if ava_jobs == 0:
            time.sleep(300)
        else:
            sub_file = sub_files.pop(0)
            print("Executing ", sub_file)

            subprocess.call(["sbatch", "-p", "cpuonly", "-A", "hk-project-radiohfi", os.path.join(directory, sub_file)])

            print("Remove entry")
            print("Number of jobs left: ", len(sub_files))
            time.sleep(5)
    else:
        break

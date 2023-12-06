import pathlib
import glob
import os
import sys
import numpy as np

path = "/hkfs/work/workspace/scratch/rn8463-gammaDetectorTankScint//generated//ITExDefault_IC86.2025_icetop.202500/"
energy_start = 4.0
energy_end = 6.9
energy_step = 0.1
energy_list = np.linspace(
    energy_start, energy_end, int((energy_end - energy_start) / energy_step) + 1
).round(1)

for energy in energy_list:
    print("Energy: ", energy)
    list_outFiles = glob.glob(f"{path}/logs/{energy}/*.out")
    # open file and read the last line
    for file in list_outFiles:
        with open(file) as f:
            lines = f.readlines()
            if not lines:
                continue
            last_line = lines[-1]
            if not "Air-shower" in last_line:
                fileToRemove = (
                    f"{path}/data/{energy}/{os.path.basename(file)[:-4]}.i3.bz2"
                )
                print(f"Removing: {fileToRemove}")
                # os.remove(fileToRemove)

print("-------------------- Program finished -------------------")

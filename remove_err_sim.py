import glob
import os
import sys

# path = "/home/hk-project-pevradio/rn8463/log/logDetGamma/"
# file_list = glob.glob(path + "output*.err")
# for file in sorted(file_list):
#     basename = os.path.basename(file).replace(".err", "")
#     output, energy, number, lv = basename.split("_")
#     if lv == "clsim":
#         ws = "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/generated/clsim/CLS_IC86.2012_corsika_icetop.14000/data/"
#         if os.path.exists(f"{ws}/{energy}/{number}.i3.bz2"):
#             os.remove(f"{ws}/{energy}/{number}.i3.bz2")
#     elif lv == "detector":
#         ws = "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/generated/detector/Detector_IC86.2012_corsika_icetop.14000/data/"
#         if os.path.exists(f"{ws}/{energy}/{number}.i3.bz2"):
#             os.remove(f"{ws}/{energy}/{number}.i3.bz2")
#     elif lv == "lv1":
#         ws = "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse//filtered/level1/Level1_IC86.2012_corsika_icetop.14000/data/"
#         if os.path.exists(f"{ws}/{energy}/{number}.i3.bz2"):
#             os.remove(f"{ws}/{energy}/{number}.i3.bz2")
#     elif lv == "lv2":
#         ws = "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse//filtered/level2/Level2_IC86.2012_corsika_icetop.14000/data/"
#         if os.path.exists(f"{ws}/{energy}/{number}.i3.bz2"):
#             os.remove(f"{ws}/{energy}/{number}.i3.bz2")
#     elif lv == "lv3":
#         ws = "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse//filtered/level3/Level3_Lv3_IC86.2012_12012_Run/data/"
#         if os.path.exists(f"{ws}/{energy}/{number}.i3.bz2"):
#             os.remove(f"{ws}/{energy}/{number}.i3.bz2")
#         else:
#             print(f"{ws}/{energy}/{number}.i3.bz2 is not defined")
#             sys.exit()
#     else:
#         print(f"{lv} is not defined")
#         sys.exit()

paths_list = [
    "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/generated/clsim/CLS_IC86.2012_corsika_icetop.14000/",
    # "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/generated/detector/Detector_IC86.2012_corsika_icetop.14000/",
    # "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/filtered/level1/Level1_IC86.2012_corsika_icetop.14000/",
    # "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/filtered/level2/Level2_IC86.2012_corsika_icetop.14000/",
    # "/hkfs/work/workspace/scratch/rn8463-gamma-detectorResponse/filtered/level3/Level3_Lv3_IC86.2012_12012_Run/",
]

for path in paths_list:
    en_list = os.listdir(path + "/logs/")
    for en in sorted(en_list):
        print(en)
        file_list = glob.glob(f"{path}/logs/{en}/*.err")
        # Read the last line of the file and if does not start with INFO print the file name
        for file in sorted(file_list):
            with open(file, "r") as f:
                lines = f.readlines()
                last_line = lines[-1]
                # if not last_line.startswith("INFO"):
                if (
                    last_line.startswith("Exception")
                    or last_line.startswith("RuntimeError")
                    or last_line.startswith("json.decoder.JSONDecodeError")
                ):
                    basename = os.path.basename(file).replace(".err", "")
                    if os.path.exists(f"{path}/data/{en}/{basename}.i3.bz2"):
                        print(f"Removing: {path}/data/{en}/{basename}.i3.bz2")
                        os.remove(f"{path}/data/{en}/{basename}.i3.bz2")
                    else:
                        print(f"{path}/data/{en}/{basename}.i3.bz2 not exist")
                        # sys.exit()
                elif last_line.startswith("INFO"):
                    continue
                else:
                    print(f"last_line: {last_line}")
                    sys.exit()


print("-------------------- Program finished --------------------")

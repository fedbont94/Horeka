#! /usr/bin/env python3


def make_parser():
    """
    Makes all the arguments that are required for the following script
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Inputs for the Detector Response Maker"
    )
    ############################## Directories paths ####################################
    parser.add_argument(
        "-inDirectory",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/data/",
        help="Directory where the simulation are stored. Please give the data folder. \
            This script assumes that in this folder there are subdirectories with energy number",
    )
    parser.add_argument(
        "-outDirectory",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/",
        help="Directory where the detector response  has to be stored. \
            It will create here a new folder: 'detector_response'.\
            Output folder name. The output file(s) will be <output>/generates/(topsimulator|detector)/[TopSimulator|Detector]_DETECTOR_corsika_icetop.MCDATASET.RUN.i3.bz2 \
            for level 0s, <output>/filtered/Level[1|2]_DETECTOR_corsika_icetop.MCDATASET.RUN.i3.bz2, for level 1 and 2, Level3_DETECTOR_DATASET_Run.RUN.i3.bz2 for level3 \
            The condor files will be saved in the realtive condor folders",
    )
    ############################# General Requirement #####################################
    parser.add_argument(
        "-pythonPath",
        type=str,
        default="/usr/bin/python3",
        help="Python path which runs the simulations of detector response",
    )
    parser.add_argument(
        "-i3build",
        type=str,
        default="/home/hk-project-pevradio/rn8463/icetray/build/",
        help="The path to the build directory of icetray environment",
    )
    parser.add_argument(
        "-detector",
        type=str,
        default="IC86",
        help="Detector type/geometry (IC79, IC86, IC86.2012...): the full name will be used only for L3 reconstruction,\
            while for the other only the base (i.e. IC86 if declared IC86.2012) [default: IC86]",
    )
    parser.add_argument(
        "-GCD",
        type=str,
        default="/lsdf/kit/ikp/projects/IceCube/sim/GCD/GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz",
        help="path where the GCD lv2 file is located",
    )
    parser.add_argument(
        "-year",
        type=str,
        default="2012",
        help="Detector year it will be used for the full detector name in the L3 reconstruction.",
    )
    parser.add_argument(
        "-MCdataset",
        type=int,
        default=13400,
        help="Number of corsika dataset [default: 13410]",
    )
    parser.add_argument(
        "-dataset", type=int, default=12012, help="Number of dataset [default: 12012]"
    )
    parser.add_argument(
        "-seed",
        type=int,
        default=120120000,
        help="The seed is the base seed which is 100_000 times the given dataset number",
    )
    ############################## Energy ####################################
    parser.add_argument(
        "-energyStart", type=float, default=5.0, help="Lower limit of energy"
    )
    parser.add_argument(
        "-energyEnd", type=float, default=7.0, help="Upper limit of energy"
    )
    parser.add_argument(
        "-energyStep",
        type=float,
        default=0.1,
        help="Step in energy, 0.1 default (do not change unless you know what you are doing)",
    )
    ############################# Parallelization #####################################
    parser.add_argument(
        "-logDirProcesses",
        type=str,
        default="/home/hk-project-pevradio/rn8463/logDetResponse/",
        help="Directory where log files of the multiple subProcesses are stored",
    )
    parser.add_argument(
        "-parallelSim",
        type=int,
        default=100,
        help="Number of parallel simulation processes",
    )
    ##################################################################
    parser.add_argument(
        "--NumbSamples",
        type=int,
        default=100,
        help="How many samples per run will be simulated by icetopshowergenerator.py [default: 100]",
    )
    return parser.parse_args()


def generatorFake():
    """
    This is a fake generator that is used to in the submitter class to run the simulation in a single process.
    """
    yield None, None

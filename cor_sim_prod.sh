#!/bin/bash
#$ -S /bin/bash

# Make sure that the .e and .o file arrive in the
# working directory, which is the outputlog directory
#$ -cwd
# export FLUPRO=/cr/icecube/simu/fluka/ # Not nedded since already in .bashrc
#Merge the standard out and standard error to one file
#$ -j y

#$ -l q=crb.q
#$ -l vf=2G

# define paths
#pathInp=/cr/icecube/simu/SIBYLL-2.3c/iron/Inpfiles/
pathInp="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/"
pathCorsika=/home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/
pathOutput=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/#energy number missing
pathOutputLog=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/log
pathScript=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/temp
##pathTemp=/home/tmp/kang/icecubesim/
pathTemp=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/temp

for num in `seq 1322012 1322012`;do
        fnum=${num:1:6}
	echo $fnum
	
        cp innerscript_cor_prod.sh ${pathScript}/CR$fnum.sh
        ##cp innerscript_particles_thin.sh ${pathScript}/CR$inpnum.sh
        echo $fnum
	for file in ${pathInp}/SIM$fnum.inp;do

		# send job
		qsub -v pC=$pathCorsika -v fl=$file -v pO=$pathOutput -v fn=$fnum -v pT=$pathTemp -o ${pathOutputLog}/outputlogfe/ -e ${pathOutputLog}/outputlogfe/ ${pathScript}/CR$fnum.sh
	done
done

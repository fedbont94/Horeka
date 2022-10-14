#!/bin/bash

pathInp="/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/"
pathCorsika=/home/hk-project-pevradio/rn8463/corsika/corsika-77401/run/
pathOutput=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/#energy number missing
pathOutputLog=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/log
pathScript=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/temp
pathTemp=/lsdf/kit/ikp/projects/IceCube/sim/gamma-sim/temp

for num in `seq 1322012 1322012`;do
        fnum=${num:1:6}
	echo $fnum
	
        cp innerscript_cor_prod.sh ${pathScript}/CR$fnum.sh
        ##cp innerscript_particles_thin.sh ${pathScript}/CR$inpnum.sh
        echo $fnum
	for file in ${pathInp}/SIM$fnum.inp;do

		# send job
		qsub 
        # -v $pathCorsika =$pathCorsika 
        # -v $file =$file 
        # -v $pathOutput =$pathOutput 
        # -v $fnum =$fnum 
        # -v $pathTemp =$pathTemp 
        -o ${pathOutputLog}/outputlogfe/ 
        -e ${pathOutputLog}/outputlogfe/ 
        ${pathScript}/CR$fnum.sh


        mkdir -p ${$pathTemp}/${$fnum}
        echo $pathTemp/$fnum 
        ## copy input-file to the tmp folder on the node
        cp $file  $pathTemp/$fnum 
        ## execute job
        ${$pathCorsika}/corsika77401Linux_SIBYLL_fluka < $pathTemp/$fnum/SIM$fnum.inp > $pathTemp/$fnum/DAT$fnum.log
        #copy the output to the destination
        status=$?
        cp -r ${$pathTemp}/${$fnum}/* $pathOutput ;
    
    
    done
done
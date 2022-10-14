#####!/bin/bash
#$ -S /bin/sh

## Send mail at submission(b) and completion(e) of script
#$ -m be
#$ -M donghwa.kang@kit.edu

## Specifies that all environment variables active within the qsub utility be exported to the context of the job.
#$ -V

#augx.q is Ubuntu 16 and crb.q is Ubuntu 18
#$ -l q=crb.q
#ulimit -c 0


## test if /cr/icecube is mounted
bla=$(ls /cr/icecube/simu/)
while [ $? != 0 ]; do
  echo $fnum": not mounted, wait for 5 minutes"
  sleep 5m
done

## create tmp directory on cluster machine 
##mkdir -p /home/tmp/kang/icecubesim/$fn/
##echo /home/tmp/kang/icecubesim/$fn/
#mkdir -p /home/tmp/kang/7.9/$fn/
#echo /home/tmp/kang/7.9/$fn/
mkdir -p ${pT}/${fn}
echo $pT/$fn

## copy input-file to the tmp folder on the node
cp $fl $pT/$fn


## execute job
${pC}/corsika77401Linux_SIBYLL_fluka < $pT/$fn/SIM$fn.inp > $pT/$fn/DAT$fn.log

#copy the output to the destination
status=$?
cp -r ${pT}/${fn}/* $pO;

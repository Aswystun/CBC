#!/bin/bash

########## Load Modules
source /apps/profiles/modules_asax.sh.dyn
module load sra
module load fastqc/0.10.1


MyID=aubats001

  ## Make variable that represents YOUR working directory(WD) in scratch, your Raw data directory (DD) and the pre or postcleaned status (CS).
DD=/scratch/${MyID}/butterfly/RawData
WD=/scratch/${MyID}/butterfly
RDQ=RawDataQuality
 
##  make the directories in SCRATCH for holding the raw data 
mkdir -p ${DD}
## move to the Data Directory
cd ${DD}

vdb-config --interactive
fastq-dump -F --split-files SRR25297534


############## FASTQC to assess quality of the sequence data
## The output from this analysis is a folder of results and a zipped file of results and a .html file.
mkdir ${WD}/${RDQ}
fastqc *.fastq --outdir=${WD}/${RDQ}

#######  Tarball the directory containing the FASTQC results so we can easily bring it back to our computer to evaluate.
cd ${WD}/${RDQ}
tar cvzf ${RDQ}.tar.gz  ${WD}/${RDQ}/*
## when finished use scp or rsync to bring the tarballed .gz results file to your computer and open the .html file to evaluate the quality of your raw data.




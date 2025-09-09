#! /bin/bash


DD=Felis_catus/RawData
WD=Felis_catus
RDQ=RawDataQuality

## move to the Data Directory
cd ${DD}


mkdir ${WD}/${RDQ}
fastqc *.fastq --outdir=${WD}/${RDQ}


cd ${WD}/${RDQ}
tar cvzf ${RDQ}.tar.gz  ${WD}/${RDQ}/*

#! /bin/bash

########## Load Modules
source /apps/profiles/modules_asax.sh.dyn
module load sra


#Change to your Supercomputer ID
MyID=aubats001

DD=/scratch/${MyID}/Felis_catus/RawData
WD=/scratch/${MyID}/Felis_catus
RDQ=RawDataQuality


mkdir -p ${DD}

cd ${DD}

vdb-config --interactive

fastq-dump -F --split-files SRR3218716




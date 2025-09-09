########## Load Modules

source /apps/profiles/modules_asax.sh.dyn
module load fastqc/0.10.1

#Change to your Supercomputer ID
MyID=aubats001

DD=/scratch/${MyID}/Felis_catus/RawData
WD=/scratch/${MyID}/Felis_catus
RDQ=RawDataQuality


#make RDQ directory
mkdir -p ${WD}/${RDQ}
## move to the Data Directory
cd ${DD}


fastqc *.fastq --outdir=../${RDQ}


cd ../${RDQ}
tar cvzf ${RDQ}.tar.gz *

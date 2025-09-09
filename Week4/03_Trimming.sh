#! /bin/bash


#  load the module
source /apps/profiles/modules_asax.sh.dyn
module load trimmomatic/0.39
module load fastqc/0.10.1
MyID=aubats001


WD=/scratch/${MyID}/Felis_catus
DD=/scratch/${MyID}/Felis_catus/RawData
CD=/scratch/${MyID}/Felis_catus/CleanData
PCQ=PostCleanQuality

#adapters= NEED ADAPTERS


mkdir ${CD}
mkdir ${WD}/${PCQ}

## Move to Raw Data Directory
cd ${DD}

### Make list of file names to Trim

ls | grep ".fastq" |cut -d "_" -f 1 | sort | uniq > list


# Need to relative path the adapters
#cp /home/${MyID}/class_shared/AdaptersToTrim_All.fa .


while read i
do


   java -jar /apps/x86-64/apps/spack_0.19.1/spack/opt/spack/linux-rocky8-zen3/gcc-11.3.0/trimmomatic-0.39-iu723m2xenra563gozbob6ansjnxmnfp/bin/trimmomatic-0.39.jar   \
PE -threads 6 -phred33 \
    "$i"_1.fastq "$i"_2.fastq  \
    ${CD}/"$i"_1_paired.fastq ${CD}/"$i"_1_unpaired.fastq  ${CD}/"$i"_2_paired.fastq ${CD}/"$i"_2_unpaired.fastq \
    ILLUMINACLIP:AdaptersToTrim_All.fa:2:35:10 HEADCROP:10 LEADING:30 TRAILING:30 SLIDINGWINDOW:6:30 MINLEN:36



fastqc ${CD}/"$i"_1_paired.fastq --outdir=${WD}/${PCQ}
fastqc ${CD}/"$i"_2_paired.fastq --outdir=${WD}/${PCQ}

done<list			# This is the end of the loop

#########################  Now compress your results files from the Quality Assessment by FastQC 
## move to the directory with the cleaned data
cd ${WD}/${PCQ}

#######  Tarball the directory containing the FASTQC results so we can easily bring it back to our computer to evaluate.
tar cvzf ${PCQ}.tar.gz ${WD}/${PCQ}/*

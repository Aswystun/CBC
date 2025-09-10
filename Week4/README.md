# Week 4 Homework
#### This Directory is my record of using the tool [TERRACE](https://github.com/Shao-Group/TERRACE) on total paired-end RNAseq data of *Felis catus*






## [ASC](https://www.asc.edu/)

Scripts will be tailored to usage on the Alabama Supercomputer, which can make reproducibility difficult:



## 1. [Downloading Data](https://github.com/Aswystun/CBC/blob/main/Week4/01_Download_Data.sh)

RNA-seq of Felis catus: spleen
[SRR3218716](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR3218716&display=metadata)

(Still need adapters and reference genome)

```bash
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
```


## 2. [Raw Data Quality Assessment](https://github.com/Aswystun/CBC/blob/main/Week4/02_SRA_Quality_Check.sh)

```bash
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
```
## 3. [Trimming](https://github.com/Aswystun/CBC/blob/main/Week4/03_Trimming.sh)

```bash
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


```


## 4. [Assembly](https://github.com/Aswystun/CBC/blob/main/Week4/04_Assembly.sh)

```bash
#!/bin/bash

# ============================================================================
# Purpose: Assemble genome from SRR25297534 trimmed paired-end FASTQ data, By Samira S.
# Recommended ASC parameters:
#   - Cores: 12
#   - Time limit: 08:00:00
#   - Memory: 64GB+
########This script is still running with 6 cores, 12 hrs, and 64 GB! Needs some refinement in the future!########
# ============================================================================

# Load SPAdes module
source /apps/profiles/modules_asax.sh.dyn
module load spades

# Define user and project variables
MyID=aubats001
ProjectName=Felis_catus
SRR_ID=SRR3218716

# Define directories
WD=/scratch/$MyID/$ProjectName
CD=$WD/CleanData             # trimmed FASTQ files location
AD=$WD/results/assembly       # assembly output

# Create assembly output directory
mkdir -p $AD

# Run SPAdes genome assembler with gzipped paired-end reads
echo "Starting genome assembly for $SRR_ID..."
spades.py \
  --pe1-1 $CD/${SRR_ID}_1_paired.fastq.gz \
  --pe1-2 $CD/${SRR_ID}_2_paired.fastq.gz \
  -o $AD \
  -t 6 -m 64

# Rename output contigs file for convenience
cp $AD/contigs.fasta $AD/${SRR_ID}_assembly.fasta

echo "Assembly complete. Output saved to $AD/${SRR_ID}_assembly.fasta"
```



# Moving Data from ASC to PC:

```bash


```


## 5. TERRACE [Installation](https://bioconda.github.io/recipes/terrace/README.html)

#### 5a. Option 1 

You will need a conda-compatible package manager, like mamba:

```bash

conda config --add channels conda-forge
conda config --add channels bioconda
conda install -c conda-forge mamba

```
Now Install TERRACE:

```bash
mamba install terrace
```

confirm installation:

```bash
conda list terrace
```
This should return something like:
```bash
# Name                     Version          Build            Channel
terrace                    1.1.2            he153687_0       bioconda
```

Make sure it is up-to-date:
```bash
mamba update terrace
```

To create a new environment, run:
```bash
mamba create --name myenvname terrace
```



#### 5b. Option 2
Installation with Docker container:
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/terrace/README.html)






## [Usage](https://github.com/Shao-Group/TERRACE?tab=readme-ov-file#usage)



The usage of TERRACE is:
```bash
terrace -i <input.bam> -o <output.gtf> -fa <reference-genome.fa> --read_length <length-of-paired-end-reads> -r [reference_annotation.gtf] -fe [feature_file] [options]
```
The input.bam is the read alignment file generated by some RNA-seq aligner, (for example, STAR or HISAT2). Make sure that it is sorted; otherwise run samtools to sort it:
```bash
samtools sort input.bam > input.sort.bam
```
















# Project Overview

This project explores the genome of a butterfly sample (SRR25297534) using a comparative genomics approach. It includes quality control, trimming, assembly, and downstream analyses such as gene family evolution and synteny conservation.



## Downloading Data and Checking Quality

To download directly to the ASC, you can call on the [sra-toolkits](https://github.com/ncbi/sra-tools) module. Then [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) is used to inspect the quality of the data.



```bash
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



```






## Trimming 

We utilize [This bash script](https://github.com/Aswystun/CBC/blob/main/Week2/trimmingCBC.sh) to trim low quality regions from the reads using [Trimmomatic v0.39](http://www.usadellab.org/cms/?page=trimmomatic).


```bash
#!/bin/bash

# loading required modules for script
module load trimmomatic/0.39
module load fastqc

# naming directories as variables for ease of use later on
# change paths as needed for project, using temporary scratch for storage purposes
RAWDATA=/home/aubscb001/CBC/RawData
CLEAN=$PBS_O_WORKDIR/CBC/CleanData
QC=$PBS_O_WORKDIR/CBC/PostCleanQC

# making the required directories if they do not already exist
mkdir -p $CLEAN
mkdir -p $QC

# progress checks on status of script running
echo "Starting trimming in $PBS_O_WORKDIR"
echo "RAWDATA dir: $RAWDATA"
echo "CLEAN dir:   $CLEAN"
echo "QC dir:      $QC"

# this file has the adaptors that will be looped over and trimmed in each of the SRR files
# the file was downloaded from GitHub
ADAPTERS=/home/aubscb001/adapters/TruSeq3-PE.fa


# loop through all R1 FASTQ files (works for .fastq and .fastq.gz) with safety checks. Parameters chosen based on general recommendations 
# from the trimmomatic manual
for R1 in $RAWDATA/*_1.fastq*; do
    # Skip if no files matched
    [ -e "$R1" ] || { echo "No input FASTQ files found in $RAWDATA"; exit 1; }

    # Infer R2 filename
    R2=${R1/_1.fastq/_2.fastq}
    base=$(basename "$R1" | sed 's/_1\.fastq.*//')

    echo "Processing sample: $base"
    echo "  R1: $R1"
    echo "  R2: $R2"

    trimmomatic PE -threads 8 -phred33 \
        "$R1" "$R2" \
        "$CLEAN/${base}_1_paired.fastq.gz" "$CLEAN/${base}_1_unpaired.fastq.gz" \
        "$CLEAN/${base}_2_paired.fastq.gz" "$CLEAN/${base}_2_unpaired.fastq.gz" \
        ILLUMINACLIP:$ADAPTERS:2:30:10 \
        LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

    fastqc -t 8 -o "$QC" \
        "$CLEAN/${base}_1_paired.fastq.gz" \
        "$CLEAN/${base}_2_paired.fastq.gz"
done

# return that the script is completed
echo "✅ Trimming + QC finished. Results in:"
echo "   $CLEAN"
echo "   $QC"
```

The output for this script are trimmed [R1](https://github.com/Aswystun/CBC/blob/main/Week2/SRR25297534_1_paired_fastqc.zip) and [R2](https://github.com/Aswystun/CBC/blob/main/Week2/SRR25297534_2_paired_fastqc.zip) paired reads. 


## Assembly
The genome for SRR25297534 was assembled using [SPAdes](https://github.com/ablab/spades)

```bash
#!/bin/bash

# ============================================================================
# Butterfly Genomics Project: Genome Assembly with SPAdes
# ============================================================================
# Purpose: Assemble genome from SRR25297534 trimmed paired-end FASTQ data, By Samira S.
# Recommended ASC parameters:
#   - Cores: 6+
#   - Time limit: 08:00:00
#   - Memory: 64GB+
########This script is still running with 6 cores, 12 hrs, and 64 GB! Needs some refinement in the future!########
# ============================================================================

# Load SPAdes module
source /apps/profiles/modules_asax.sh.dyn
module load spades

# Define user and project variables
MyID=aubsxs003
ProjectName=ButterflyGenomics
SRR_ID=SRR25297534

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
the output of this scrip


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


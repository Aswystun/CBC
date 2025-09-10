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
RAWDATA=/scratch/${MyID}/Felis_catus/RawData
CLEAN=/scratch/${MyID}/Felis_catus/CleanData
QC=PostCleanQuality
ADAPTERS=/scratch/${MyID}/Felis_catus/Adapters


mkdir -p ${CLEAN}
mkdir -p ${QC}
mkdir -p $ADAPTERS



# Download adapters from Trimmomatic GitHub
cd ${ADAPTERS}
wget https://raw.githubusercontent.com/usadellab/Trimmomatic/main/adapters/TruSeq3-PE.fa
cd ${WD}
ADAPTER3=/scratch/${MyID}/Felis_catus/Adapters/TruSeq3-PE.fa

## Move to Raw Data Directory
cd ${RAWDATA}

### Make list of file names to Trim
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

## 4. [Alignment and Indexing](https://github.com/Aswystun/CBC/blob/main/Week4/04_STAR_Aligner.sh)
```bash
#!/bin/bash

source /apps/profiles/modules_asax.sh.dyn
module load star/2.7.6a
which STAR


MyID=aubats001
WD=/scratch/${MyID}/Felis_catus
CLEAN=${WD}/CleanData
REFERENCE=${WD}/Reference_Genome
REFGENOME=${REFERENCE}/genome.fa
GTFD=${WD}/genes
GTF=${GTFD}/genes.gtf
STAR=${WD}/aligned #Output DIR

mkdir -p ${REFERENCE} ${GTFD} ${STAR}
mkdir -p ${STAR}/STAR_index

cd ${REFERENCE}
wget ftp://ftp.ensembl.org/pub/release-109/fasta/felis_catus/dna/Felis_catus.Felis_catus_9.0.dna.toplevel.fa.gz
gunzip Felis_catus.Felis_catus_9.0.dna.toplevel.fa.gz
mv Felis_catus.Felis_catus_9.0.dna.toplevel.fa genome.fa

cd ${GTFD}

wget ftp://ftp.ensembl.org/pub/release-109/gtf/felis_catus/Felis_catus.Felis_catus_9.0.109.gtf.gz
gunzip Felis_catus.Felis_catus_9.0.109.gtf.gz
mv Felis_catus.Felis_catus_9.0.109.gtf genes.gtf


READ1_FASTQ=${CLEAN}/SRR3218716_1_paired.fastq.gz

read_length=$(zcat ${READ1_FASTQ} | sed -n '2p' | wc -m)
sjdbOverhang=$((read_length - 2))
echo "Calculated sjdbOverhang: ${sjdbOverhang}"

cd ${STAR}

# Generating Genome Index
STAR --runThreadN 8 \
     --runMode genomeGenerate \
     --genomeDir ${STAR}/STAR_index \
     --genomeFastaFiles ${REFGENOME} \
     --sjdbGTFfile ${GTF} \
     --sjdbOverhang ${sjdbOverhang}


# 5. Align reads with STAR
FORWARD=${CLEAN}/SRR3218716_1_paired.fastq.gz
REVERSE=${CLEAN}/SRR3218716_2_paired.fastq.gz

# Align reads
STAR --runThreadN 8 \
     --genomeDir ${STAR}/STAR_index \
     --readFilesIn ${FORWARD} ${REVERSE} \
     --readFilesCommand zcat \
     --outSAMtype BAM SortedByCoordinate \
     --outFileNamePrefix ${STAR}/SRR3218716_

#output should be:
#sample_Aligned.sortedByCoord.out.bam


# Index BAM file for TERRACE
module load samtools/1.18
samtools index ${STAR}/SRR3218716_Aligned.sortedByCoord.out.bam

```

## 4b. [Assembly](https://github.com/Aswystun/CBC/blob/main/Week4/04_Assembly.sh) **OPTIONAL** 
#### This step is not needed, but could be useful for further downstream analysis 

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

## Install miniforge

```bash
cd ~
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh

```
After install:
```bash
source ~/miniforge3/bin/activate
conda init bash
```
This modifies your ~/.bashrc to make conda available automatically.

source your .bashrc

```bash
source ~/.bashrc
```

Now you can create TERRACE environment:
```bash
conda install -y mamba -n base -c conda-forge
mamba create -y -n terrace_env -c conda-forge -c bioconda terrace
conda activate terrace_env
```
You should now see (terrace_env), instead of (Base) 
## 5. [TERRACE](https://github.com/Aswystun/CBC/blob/main/Week4/05_TERRACE.sh)


#### 5a. Option 1 - **What we will be doing** - Using TERRACE on the ASC

```bash
#!/bin/bash


source /apps/profiles/modules_asax.sh.dyn
module load star/2.7.6a
module load samtools/1.18


# Use personal Conda
source ~/miniforge3/bin/activate
conda activate terrace_env

# Set Variables
MyID=aubats001
WD=/scratch/${MyID}/Felis_catus
CLEAN=${WD}/CleanData
REFERENCE=${WD}/Reference_Genome
REFGENOME=${REFERENCE}/genome.fa
STAR_ALIGN=${WD}/aligned
BAM_OUTPUT=${STAR_ALIGN}/SRR3218716_Aligned.sortedByCoord.out.bam
TERRACE_OUTPUT=${STAR_ALIGN}/SRR3218716_terrace_output.gtf
FORWARD=${CLEAN}/SRR3218716_1_paired.fastq.gz

read_length=$(zcat ${FORWARD} | sed -n '2p' | wc -m)
echo "Detected read length: ${read_length}"




terrace -i ${BAM_OUTPUT} \
        -o ${TERRACE_OUTPUT} \
        -fa ${REFGENOME} \
        --read_length ${read_length}
```


[Usage](https://github.com/Shao-Group/TERRACE?tab=readme-ov-file#usage)

The usage of TERRACE is:
```bash
terrace -i <input.bam> -o <output.gtf> -fa <reference-genome.fa> --read_length <length-of-paired-end-reads> -r [reference_annotation.gtf] -fe [feature_file] [options]
```
The input.bam is the read alignment file generated by some RNA-seq aligner, (for example, STAR or HISAT2). Make sure that it is sorted; otherwise run samtools to sort it:
```bash
samtools sort input.bam > input.sort.bam
```






#### 5b. Option 2 - move files from ASC to PC and: [Installation](https://bioconda.github.io/recipes/terrace/README.html)


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



#### 5c. Option 3 - move files from ASC to PC and:
Installation with Docker container:
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/terrace/README.html)












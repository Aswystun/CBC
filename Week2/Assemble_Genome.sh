#!/bin/bash

# ============================================================================
# Butterfly Genomics Project: Genome Assembly with SPAdes
# ============================================================================
# Purpose: Assemble genome from SRR25297534 trimmed paired-end FASTQ data
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

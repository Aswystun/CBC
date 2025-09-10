#!/bin/bash


set -e
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

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

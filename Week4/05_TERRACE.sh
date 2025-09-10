
source /apps/profiles/modules_asax.sh.dyn
module load star/2.7.6a
module load samtools/1.18
module load miniforge3

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

# Activate Conda and install environment
eval "$(conda shell.bash hook)"
if ! conda env list | grep -q terrace_env; then
    conda install -y mamba -n base -c conda-forge
    mamba create -y -n terrace_env -c conda-forge -c bioconda terrace
fi
conda activate terrace_env


terrace -i ${BAM_OUTPUT} \
        -o ${TERRACE_OUTPUT} \
        -fa ${REFGENOME} \
        --read_length ${read_length}

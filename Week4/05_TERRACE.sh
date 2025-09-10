#!/bin/bash

cd /scratch/aubats001/Felis_catus


module load miniforge3   # or anaconda3, if available
eval "$(conda shell.bash hook)"  # may be needed on some clusters
conda install mamba -n base -c conda-forge
conda create -n terrace_env -c conda-forge -c bioconda terrace
conda activate terrace_env

terrace -i input.bam -o output.gtf -fa reference.fa --read_length 150

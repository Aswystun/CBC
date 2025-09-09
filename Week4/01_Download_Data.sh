#! /bin/bash


DD=Felis_catus/Raw_Data
WD=Felis_catus
RDQ=RawDataQuality


mkdir -p ${DD}

cd ${DD}

vdb-config --interactive

fastq-dump -F --split-files SRR3218716




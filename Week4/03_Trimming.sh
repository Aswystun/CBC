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


mkdir -p $CLEAN
mkdir -p $QC
mkdir -p $ADAPTERS



# Download adapters from Trimmomatic GitHub
cd ${ADAPTERS}
wget https://raw.githubusercontent.com/usadellab/Trimmomatic/main/adapters/TruSeq3-PE.fa
cd ${WD}
ADAPTER3=/scratch/${MyID}/Felis_catus/Adapters/TruSeq3-PE.fa

## Move to Raw Data Directory
cd ${DD}

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

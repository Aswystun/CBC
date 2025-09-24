# Week 6 Homework

This week, I will be using the tool [PARAS/PARASECT](https://paras.bioinformatics.nl/submit).
Usually, this tool can be used with the web browser (linked above), but this will be a protocol on how to install from source / use the tool via command line.
Everything will be installed and used on the [Alabama Supercomputer](https://asc.edu/).

## [Installation](https://github.com/BTheDragonMaster/parasect/wiki/Installation#installing-paras-and-parasect-from-source)


```bash
MYID=${aubats001} #chang this to your ID 
conda create --prefix /scratch/${MYID}/conda-envs/parasect-env python=3.11 -y
conda activate /scratch/${MYID}/conda-envs/parasect-env
```

## Dependencies

```bash
conda create -n paras python==3.9
conda install -c bioconda muscle==3.8.1551
conda install -c bioconda hmmer2
pip install pikachu-chem
pip install joblib
pip install scikit-learn==1.2.0
pip install biopython==1.80
pip install numpy==1.25.2
```



**move to sratch folder**

```bash
git clone https://github.com/BTheDragonMaster/parasect.git
```

## [Download Models](https://zenodo.org/records/13165500)
Next, we need to download models for the tool to function:
Travel to the link and download the three files. 
move them into this pathway:

```
scratch/
    <username>/
        parasect/
            paras/
              models/
                  random_forest/
                    __init__.py
                    all_substrates_model.paras
                    model.paras
                    model.parasect


```


## Installation


```bash
cd /scratch/<username>/parasect
pip install .
```


## Usage



```bash
Standard PARAS run:

paras -i paras/data/sequence_data/sequences/reference_sequence.fasta -o ../test
```

**Download genome of choice, make sequences dir in data, and scp genome into directory**

```bash
mkdir paras/data/sequences
mkdir ../results
```

```bash

paras -i paras/data/sequences/AB01_genome.fasta -o ../results

```


<<<<<<< HEAD
[results]()
=======
[results](https://github.com/Aswystun/CBC/blob/main/Week6/run_paras_results.txt)
>>>>>>> e233058c698185b4d757cde9d8c213cf73cb83e0

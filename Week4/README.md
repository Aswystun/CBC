# Week 4 Homework
#### This Directory is my record of using the tool [TERRACE](https://github.com/Shao-Group/TERRACE) on RNAseq data of _____ __________. 

## [Installation](https://bioconda.github.io/recipes/terrace/README.html)
### Option 1 

You will need a conda-compatible package manager, like mamba

```bash

conda config --add channels conda-forge
conda config --add channels bioconda
conda install -c conda-forge mamba

```
Now Install TERRACE

```bash
mamba install terrace
```

confirm installation 

```bash
conda list terrace
```
This should return something like:
```bash
# Name                     Version          Build            Channel
terrace                    1.1.2            he153687_0       bioconda
```

## Make sure it is up-to-date
```bash
mamba update terrace
```

To create a new environment, run:
```bash
mamba create --name myenvname terrace
```



### Option 2
Installation with Docker container:
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/terrace/README.html)











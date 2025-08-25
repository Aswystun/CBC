# Downloading SRA
[You will need to install sra-toolkits](https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit)

Then download the data from [SRR25297534](https://www.ncbi.nlm.nih.gov/sra/?term=SRR25297534) using:
```bash
fastq-dump SRR25297534
```
# Moving Data to SuperComputer Environment
This project will use the [Alabama Supercomputer](https://www.asc.edu/).
To push data to the supercomputer, use:
```bash
rsync --partial -arv <local path and file> <ID:remote path to target folder>
#For Example
rsync --partial -arv SRR25297534.fastq <username>@asax.asc.edu:<path>
```

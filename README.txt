OS: Linux
Dependencies:
1. Perl
2. Python3 (Required libraries:: numpy, scipy, scikit-learn, pandas, setuptools, iced, pastis, config, configparser)
Conflicts between libraries may happen, and here is a list of libraries that works on ubuntu 16.04 for reference:
config          0.5.0.post0
configparser    5.0.1
iced            0.5.7
joblib          0.17.0
numpy           1.19.2
pandas          1.1.3
pastis          0.4.0
pip             20.2.3
python-dateutil 2.8.1
pytz            2020.1
scikit-learn    0.23.2
scipy           1.5.3
setuptools      50.3.0.post20201006
six             1.15.0
threadpoolctl   2.1.0
wheel           0.35.1
3. R (Required package: preprocessCore)

Prepare these files as input in seperate directories:
1. Hi-C contact matrices as individual .tsv file for each chromosome, and rename each Hi-C contact matrix file as "celltype_chromosome", where the "celltype" part should be set as the "-celltype" parameter when running the script with user's own data. For example, when the -celltype parameter is set to "GM12878", Hi-C contact matrix files should be named as "GM12878_chr1", "GM12878_chr2",....
2. a bed file containing chromosomes, starts and ends of all TADs
3. a bed file containing chromosomes, starts and ends of open chromatin regions, can be peak-calling result of DNase-seq or ATAC-seq data by MACS2, HOMER, etc.

Example input files are in "example_data" directory. To test SDOC calculation scripts with example data, run the "get_SDOC.py" python script with no parameters:
"python ./get_SDOC.py"

To calculate SDOC values of TADs with your own data, all parameters are required to be specified:
python ./get_SDOC.py -celltype -TAD_dir -Hi-C_dir -resolution -out_dir -DHS_dir

Description of each parameter:
-celltype: A job name. The script uses this parameter to find Hi-C contact matrix file in -Hi-C_dir, and to create a specific directory for temp files. 
-TAD_dir: The directory containing the TAD bed file (no requirement for the name of the TAD bed file).
-Hi-C_dir: The directory containing Hi-C contact matrix files.
-resolution: The binning size of Hi-C contact matrix files.
-out_dir: The parent directory of all output files.
-DHS_dir: The directory containing the open chromatin regions/peaks file.
# EMP-Benchmark

Benchmark for active module identification (AMI) algorithms.

For more information see [EMP repository][0] and this [paper][1] 

This repository contains an implementation of the criteria used in the benchmark  
  
Score files used in the evaluation are available under data/emp_test/original_datasets.  
RNA files from which GE scores were produced are available at data/ge_datasets.         
## Outline


- [Set your environment](#set-your-environment)
- [Set your directory structure](#integrate-your-nbmd-algorithm-with-emp)
- [Main output files](#main-output-files)
- [EMP-benchmark container](#emp-benchmark container)

## Set your environment

Download the sources and install according to the following:

Clone the repo from github:
```
git clone https://github.com/Shamir-Lab/EMP-benchmark.git
cd EMP-benchmark
```

EMP is written in Python 3.6. We recommend using a virtual environment. in Linux:
```
python -m venv emp-benchmark-env
source emp-benchmark-env/bin/activate
```

To install EMP dependencies type:
```
pip install -r  config/dependencies.txt
```


## Set your directory structure

First, make a directory for your benchmark (e.g. /path/to/benchmark).

Next, specify the data root directory in the config file (under config/conf.json) by setting the `root_dir` field

Then, create the benchmark directory structure by running the lines below: 

```
cd /path/to/root_dir/ 
mkdir ./cache_global/         
mkdir ./go/              
mkdir ./permuted_datasets/    
mkdir ./report/
mkdir ./report/evaluation
mkdir ./report/robustness_cache
mkdir ./report/module_cache_files
mkdir ./report/mehr_cache_files
mkdir ./report/bg
mkdir ./report/md
mkdir ./report/oob
mkdir ./robustness_solutions/ 
mkdir ./true_solutions/       
mkdir ./dictionaries/
mkdir ./original_datasets/    
mkdir ./permuted_solutions/
```


Last, move your output files from EMP to the directories as follows:
1. "*_oob.tsv" files under  ./report/oob
2. "*_md.tsv" files under  ./report/md
3. Content of EMP's robustness solutions folder under robustness_solutions
4. Content of EMP's true solutions folder under ./true_solutions
5. Content of EMP's go folder under ./go
6. Content of EMP's dictionaries folder under ./dictionaries

## Run crieria

Our benchmark contains 6 main criteria: EHR, mEHR, Richness, Intra-module homogeneity, Robustness (F1) and Robustness (AUPR).  

The criteria main files reside in `src/evaluation` directory. Running the criteria is done as follows:

* To run EHR execute: `ehr_counts.py`: with the following parameters:
parameters:  
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").  
  
* To run Richness execute: `richness.py` with the following parameters:
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").
`--pf`: a string to concat to the evaluation output files (default is "GE").  
`--base_folder`: oob folder (default is os.path.join(constants.OUTPUT_GLOBAL_DIR,"oob")).  
`--file_format`: oob files format (default is "emp_diff_modules_{}_{}_passed_oob.tsv")
`--sim_method`: Similarity method as implemented in Fastsemsim (default is "Resnik").  
`--cutoffs`: comma-separated cutoffs of similarity to test (default is "1.0,2.0,3.0,4.0").

* To run Intra-module homogeneity execute `homogeneity.py` with the following parameters:
parameters:  
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").
`--pf`: a string to concat to the evaluation output files (default is "GE").  
`--base_folder`: oob folder (default is os.path.join(constants.OUTPUT_GLOBAL_DIR,"oob")).  
`--file_format`: oob files format (default is "emp_diff_modules_{}_{}_passed_oob.tsv")
`--sim_method`: Similarity method as implemented in Fastsemsim (default is "Resnik").  
`--cutoffs`: comma-separated cutoffs of similarity to test (default is "1.0,2.0,3.0,4.0").
  
* To run mEHR homogeneity execute `mEHR.py` with the following parameters:  
parameters:  
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").

  
* To run robustness (F1) execute `robustness_f1.py` with the following parameters:  
parameters:  
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").
`--pf`: a string to concat to the evaluation output files (default is "GE").  
`--hg_th`: the hypergeomtric threshold of Go terms (default is "0.05").
`--n_start`: first positional index of robustness solutions.  
`--n_end`: last positional index of robustness solutions
`--ss_ratios`: comma-separated downsampling ratios (i.e proportion of activity scores to be remove) from true datasets (default is "0.4,0.3,0.2,0.1").  
`--cutoffs`: comma-separated cutoffs of similarity to test (default is "1.0,2.0,3.0,4.0").

* To run robustness (AUPR) execute, first execute robustness_f1.py as described above. Then run `robustness_aupr.py` with the following parameters:  
`--datasets`: datasets to be test.  
`--algos`: algos to be tested.  
`--prefix`: a string to concat to the evaluation output files (default is "GE").
`--n_start`: first positional index of robustness solutions.  
`--n_end`: last positional index of robustness solutions
`--ss_ratios`: comma-separated dropping ratios from true datasets (default is "0.4,0.3,0.2,0.1"). 


## Main output files

* EHR: `./report/evaluation/count_matrix_{prefix}.tsv`, `./report/evaluation/ehr_matrix_{prefix}.tsv` - term counts and ehr scores per solution, respectively   
* mEHR: `./report/evaluation/mEHR_mean_{}.tsv` - mEHR scores per algorithm and # of top ranked modules 
* Richness: `./report/evaluation/richness_matrix_{cutoff}_{prefix}.tsv` - Richness score per algorithm, one file for each similarity cutoff   
* Intra-module homogeneity: `./report/evaluation/homogeneity_avg_matrix_{cutoff}_{prefix}.tsv` - Richness score per algorithm, one file for each similarity cutoff
* Robustness (f1): `./report/evaluation/robustness_f1_{prefix}_{n_end}_{ss_ratio}.tsv` - robustness f1 score per algorithm, one file for each downsampling ratio 
* Robustness (AUPR): `./report/evaluation/robustness_aupr_{prefix}_{n_end}_{ss_ratio}.tsv` - robustness aupr score per algorithm, one file for each downsampling ratio


## EMP-benchmark container
EMP-benchmark is also available as ready-to-use tool in a container (alongside EMP[0]).
The container was generated and tested using udocker.It can also be loaded using Docker.
To load the container using udocker, do the following steps:
* Install [udocker](https://github.com/indigo-dc/udocker)
* Download the container from [here](https://drive.google.com/file/d/1rq5HIa7G97U9O3XAMrYEYma-XiqPB7zP/view?usp=sharing)
* Extract the tar file from the tar.gz file
* Load the tar file as a container by running `udocker import --tocontainer --clone --name=emp emp-ubuntu-18.tar`
* Go inside the container by running `udocker run emp`
* the EMP-benchmark project resides under /sandbox/
* EMP-benchmark can be executed as described above in this README.


[0]: https://github.com/Shamir-Lab/EMP
[1]:  https://www.embopress.org/doi/full/10.15252/msb.20209593

import sys
sys.path.insert(0, '../')

import constants
import os
import argparse
import pandas as pd
import numpy as np

def ehr_for_solution(algo_sample = None, dataset_sample = None,tsv_file_name=None, filtered_go_ids_file=None, hg_th=0.05):

    try:
        output_oob = pd.read_csv(
            tsv_file_name.format(dataset_sample, algo_sample),
            sep='\t', index_col=0).dropna()
    except Exception as e:
        print(e)
        return 0, 0
    
    sig_hg_genes=output_oob.shape[0]
    sig_emp_genes=output_oob.loc[output_oob.loc[:,'is_emp_pval_max_significant'].values].shape[0]
   
   
    return sig_hg_genes, sig_emp_genes


def main(datasets, algos, prefix):

    hg_th=0.05
    df_matrix = pd.DataFrame()
    df_count_matrix = pd.DataFrame()
    for cur_ds in datasets:
        df_ds=pd.DataFrame()
        for cur_alg in algos:
            sig_hg_genes, sig_emp_genes=ehr_for_solution(cur_alg, cur_ds,tsv_file_name=os.path.join(constants.OUTPUT_GLOBAL_DIR,"oob", "emp_diff_modules_{}_{}_passed_oob.tsv"), filtered_go_ids_file=os.path.join(constants.GO_DIR,"filtered_go_terms.txt"), hg_th=hg_th) # _gwas

            df_ds.loc["{}_{}".format(cur_ds,cur_alg), "algo"]=cur_alg
            df_ds.loc["{}_{}".format(cur_ds,cur_alg), "dataset"]=cur_ds
            if type(sig_emp_genes)==int and type(sig_hg_genes)==int:
                df_ds.loc["{}_{}".format(cur_ds, cur_alg), "n_emp"] = sig_emp_genes
                df_ds.loc["{}_{}".format(cur_ds, cur_alg), "n_hg"] = sig_hg_genes
            else:
                df_ds.loc["{}_{}".format(cur_ds,cur_alg),"n_emp"]=np.sum(sig_emp_genes["passed_oob_permutation_test"].apply(lambda x: np.any(np.array(x[1:-1].split(', '),dtype=np.bool))).values)
                df_ds.loc["{}_{}".format(cur_ds,cur_alg), "n_hg"] = len(sig_hg_genes.index)
            df_ds.loc["{}_{}".format(cur_ds,cur_alg), "ratio"] = round(float(df_ds.loc["{}_{}".format(cur_ds,cur_alg), "n_emp"])/max(df_ds.loc["{}_{}".format(cur_ds,cur_alg), "n_hg"],1),3)
            df_count_matrix.loc[cur_alg, cur_ds] = df_ds.loc["{}_{}".format(cur_ds, cur_alg), "n_emp"]
            df_matrix.loc[cur_alg, cur_ds] = df_ds.loc["{}_{}".format(cur_ds, cur_alg), "ratio"]

    df_matrix.to_csv(os.path.join(constants.OUTPUT_GLOBAL_DIR, "evaluation", "ehr_matrix_{}.tsv".format(prefix)), sep='\t')
    df_count_matrix.to_csv(os.path.join(constants.OUTPUT_GLOBAL_DIR, "evaluation", "count_matrix_{}.tsv".format(prefix)), sep='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('--datasets', dest='datasets')
    parser.add_argument('--prefix', dest='prefix', default="GE")
    parser.add_argument('--algos', dest='algos')

    args = parser.parse_args()
    datasets = args.datasets.split(",")
    algos = args.algos.split(",")
    prefix = args.prefix

    main(datasets,algos,prefix)


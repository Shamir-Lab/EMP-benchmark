import matplotlib

matplotlib.use('Agg')

import sys

sys.path.insert(0, '../')

import argparse

import os
import constants
import pandas as pd
import numpy as np
import scipy
from evaluation.modules_report import modules_ehr_for_solution

MAX_N_MODULES_TH = 20
SCATTER_FACTOR = 40


def calc_emp_pval(cur_rv, cur_dist):
    pos = np.size(cur_dist) - np.searchsorted(np.sort(cur_dist), cur_rv, side='left')

    return pos / float(np.size(cur_dist))


def plot_modules_ehr_summary(prefix, datasets, algos):
    df_statistics = pd.DataFrame()
    for cur_ds in datasets:
        for cur_alg in algos:
            try:
                print("{} {}".format(cur_alg, cur_ds))
                res = modules_ehr_for_solution(cur_alg, cur_ds, prefix=prefix,
                                               terms_file_name=os.path.join(constants.OUTPUT_GLOBAL_DIR, "oob",
                                                                            "emp_diff_modules_{}_{}_passed_oob.tsv"),
                                               modules_file_name=os.path.join(constants.TRUE_SOLUTIONS_DIR,
                                                                              "{}_{}/report/modules_summary.tsv"),
                                               emp_ratio_th=0.5)
            except Exception as e:
                print("error: {}".format(e))
                continue

            if res is None:
                continue
            tps, fps, sig_hg_genes, sig_emp_genes, statistics, full_data = res

            statistics["algo"] = cur_alg
            statistics["dataset"] = cur_ds
            statistics["id"] = "{}_{}".format(cur_alg, cur_ds)

            df_statistics = df_statistics.append(statistics, ignore_index=True)

    df_statistics = df_statistics.set_index("id")
    df_statistics.to_csv(
        os.path.join(constants.OUTPUT_GLOBAL_DIR, "modules_statistics_{}.tsv".format(prefix)),
        sep='\t')

    for i_a, cur_alg in enumerate(set(constants.ALGOS).intersection(algos)):
        for i_d, cur_ds in enumerate(datasets):

            solution_id = "{}_{}".format(cur_alg, cur_ds)

            cur_series = df_statistics.loc[solution_id, :]
            l_modules = []
            for cur_modules in range(int(cur_series["n_modules"])):
                l_modules.append((cur_series['module_{}_emp_ratio'.format(cur_modules)],
                                  cur_series['module_{}_tp'.format(cur_modules)],
                                  cur_series['module_{}_fp'.format(cur_modules)],
                                  cur_series['module_{}_total'.format(cur_modules)],
                                  cur_series['module_{}_size'.format(cur_modules)]))
            l_modules = sorted(l_modules, key=lambda x: (x[0], x[3]), reverse=True)
            for cur in range(min(10, len(l_modules))):

                if l_modules[cur][4] < 1: continue



    summary_m_ehr_mean = pd.DataFrame()
    for n_modules_th in range(1, MAX_N_MODULES_TH + 1):

        l_n_modules = []
        EHRs = pd.DataFrame()
        for cur_ds in datasets:
            for cur_alg in algos:
                solution_id = "{}_{}".format(cur_alg, cur_ds)
                if solution_id not in list(df_statistics.index):
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "ehr"] = 0
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "algo"] = cur_alg
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "dataset"] = cur_ds
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "rank"] = 0
                    continue
                cur_series = df_statistics.loc[solution_id, :]
                l_modules = []
                for cur_modules in range(int(cur_series["n_modules"])):
                    l_modules.append((cur_series['module_{}_emp_ratio'.format(cur_modules)],
                                      cur_series['module_{}_tp'.format(cur_modules)],
                                      cur_series['module_{}_fp'.format(cur_modules)],
                                      cur_series['module_{}_total'.format(cur_modules)],
                                      cur_series['module_{}_size'.format(cur_modules)]))
                l_modules = sorted(l_modules, key=lambda x: (x[0], x[3]), reverse=True)
                l_n_modules.append(len(l_modules))
                for cur in range(min(n_modules_th, len(l_modules))):
                    if l_modules[cur][4] < 1: continue
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "ehr"] = l_modules[cur][0]
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "algo"] = cur_alg
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "dataset"] = cur_ds
                    EHRs.loc["{}_{}_{}".format(cur_ds, cur_alg, cur), "rank"] = cur + 1
        pvals = []
        for cur_ds in datasets:
            for cur_alg in algos:
                try:
                    pvals.append(scipy.stats.mannwhitneyu(
                        EHRs[(EHRs["dataset"] == cur_ds) & (EHRs["algo"] == cur_alg)]["ehr"].values,
                        EHRs[(EHRs["dataset"] == cur_ds) & (EHRs["algo"] != cur_alg)]["ehr"].values)[1])
                except Exception as  e:
                    print(e)
                    pvals.append(1)

        summary_m_ehr_mean[n_modules_th] = EHRs.groupby(by=['dataset', 'algo'])['ehr'].mean().groupby(
            by=['algo']).mean()

    summary_m_ehr_mean = summary_m_ehr_mean[np.sort(summary_m_ehr_mean.columns.values)]

    summary_m_ehr_mean.to_csv(
        os.path.join(constants.OUTPUT_GLOBAL_DIR, "evaluation", "mEHR_mean_{}.tsv".format(prefix)), sep='\t')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('--datasets', dest='datasets')  # TNFa_2,HC12,SHERA,SHEZH_1,ROR_1,ERS_1,IEM Breast_Cancer.G50,Crohns_Disease.G50,Schizophrenia.G50,Triglycerides.G50,Type_2_Diabetes.G50
    parser.add_argument('--prefix', dest='prefix', default="GE")  # PASCAL_SUM   GE
    parser.add_argument('--base_folder_format', dest='base_folder_format',
                        default=os.path.join(constants.OUTPUT_GLOBAL_DIR, "oob"))
    parser.add_argument('--file_format', dest='terms_file_name_format',
                        default="emp_diff_modules_{}_{}_passed_oob.tsv")
    parser.add_argument('--algos', dest='algos',
                        default="jactivemodules_greedy,jactivemodules_sa,netbox,bionet,dcem")  # ,keypathwayminer_INES_GREEDY,hotnet2,my_netbox_td

    args = parser.parse_args()

    datasets = args.datasets.split(",")
    algos = args.algos.split(",")
    prefix = args.prefix
    plot_modules_ehr_summary(prefix, datasets, algos)



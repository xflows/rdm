### plot result data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import numpy as np
from py3plex.algorithms.statistics import critical_distances

def plot_basic(dfx):

    
    dfx.recall = pd.to_numeric(dfx.recall)
    dfx.accuracy = pd.to_numeric(dfx.accuracy)
    dfx.sc = pd.to_numeric(dfx.sc)
    dfx.precision = pd.to_numeric(dfx.precision)
    dfx.time = pd.to_numeric(dfx.time)
    
    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=dfx.recall,hue=dfx.learner)
    f.savefig("../results/recall_bar.pdf", bbox_inches='tight')

    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=pd.to_numeric(dfx.precision),hue=dfx.learner)
    f.savefig("../results/precision_bar.pdf", bbox_inches='tight')

    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=pd.to_numeric(dfx.accuracy),hue=dfx.learner)
    f.savefig("../results/accuracy_bar.pdf", bbox_inches='tight')

    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=pd.to_numeric(dfx.time),hue=dfx.learner)
    f.savefig("../results/time_bar.pdf", bbox_inches='tight')

    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=pd.to_numeric(dfx.sc),hue=dfx.learner)
    f.savefig("../results/AUC_bar.pdf", bbox_inches='tight')

    f = plt.figure()
    sns.barplot(x=dfx.algorithm,y=pd.to_numeric(dfx.internal_time),hue=dfx.learner)
    f.savefig("../results/internal_bar.pdf", bbox_inches='tight')

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'algorithm'],groupby_target='accuracy',outfile="../results/acc.pdf")
    
    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'algorithm'],groupby_target='precision',outfile="../results/prec.pdf")    
    
    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'algorithm'],groupby_target='recall',outfile="../results/rec.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'learner'],groupby_target='recall',outfile="../results/rec_learners.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'learner'],groupby_target='precision',outfile="../results/prec_learners.pdf")

    dfx['prop_learner'] = dfx['learner']+"_"+dfx['algorithm']
    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'prop_learner',],groupby_target='accuracy',outfile="../results/acc_algo_learners.pdf",fontsize=20)

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'prop_learner',],groupby_target='sc',outfile="../results/auc_algo_learners.pdf",fontsize=20)
        
    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'learner',],groupby_target='accuracy',outfile="../results/acc_learners.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'learner'],groupby_target='time',outfile="../results/time_learners.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'algorithm'],groupby_target='time',outfile="../results/time_algorithms.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'algorithm'],groupby_target='internal_time',outfile="../results/internal_time_peop.pdf")

    critical_distances.plot_critical_distance(dfx,groupby=['dataset', 'learner'],groupby_target='sc',outfile="../results/AUC_algorithms.pdf")

def load_data(dfx_file):

    pdf = pd.read_csv(dfx_file,sep=" ")
    return pdf

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--filen",default="../results/dump2.txt")
    args = parser.parse_args()
    rname = args.filen
    # with open(rname) as tn:
    #     for line in tn:
    #         line = line.strip().split()
    #         if len(line) == 10:
    #             print(line)
#    ("RESULT_LINE",str(cnts),learner, cname, dataset, target_label, acc,time_overall,target_label,r[0],p[0],internal_time,sc)
    cnames = ['PH','fold','algorithm','learner','dataset','table','accuracy','time','target','precision','recall','internal_time','sc']
    dfx = load_data(rname)
    dfx.columns = cnames
    print(dfx.dataset.unique())
    
    dfx = dfx.groupby(['algorithm','learner','dataset','target','fold']).max().reset_index()
    print(dfx.head())
    dfx = dfx.dropna()
    dfx = dfx.loc[(dfx.learner != "DT")]
    dfx = dfx.loc[(dfx.dataset == "mutagenesis") | (dfx.dataset == " mutagenesis188")  | (dfx.dataset == "Carcinogenesis") ]
    
#    dfx = dfx[dfx.learner != "MF"]
#    dfx = dfx[dfx.dataset != "Facebook"]
#    dfx = dfx[dfx.dataset != "cs"]
#    dfx = dfx.loc[dfx['dataset'] == 'mutagenesis42']
#    print(dfx)

    plot_basic(dfx)

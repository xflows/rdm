## A simple python job generator

learners = ['aleph','RSD','treeliker']#,'wordification']
dbtuples = [('trains','trains','direction'),
            ('cs','target_churn','target_churn'),
            ('imdb_ijs','actors','gender'),
            ('financial','load','status'),
            ('Carcinogenesis','canc','class'),
            ('mutagenesis','molecule','mutagenic'),
            ('Dunur','target','is_dunur'),
            ('Facebook','feat','gender1'),
            ('NBA','game','ResultOfTeam1')
            
]

classifiers = ["DT","SVM","GBM","MLP","CEN"]

result_file = "./tmp_results_new_v2.txt"
for dtuple in dbtuples:
    for learner in learners:
        for classifier in classifiers:
            print ('python3','benchmark_algorithms.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2],'--learner',learner,"--classifier",classifier,'>>',result_file)

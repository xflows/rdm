## A simple python job generator

learners = ['aleph','RSD','treeliker','wordification']
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

result_file = "./tmp_results_new.txt"
for dtuple in dbtuples:
    for learner in learners:
        print ('python3','benchmark_algorithms.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2],'--learner',learner,'>>',result_file)

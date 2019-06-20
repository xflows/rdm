## A simple python job generator

import benchmark_algorithms

dbtuples = [#('trains','trains','direction'),
            #('ilp','trains','direction'),
            #('cs','target_churn','target_churn'),
            ('mutagenesis','molecule','mutagenic'),
#            ('imdb_top','movies','quality'),
#            ('financial','loans','status'),
            #('Carcinogenesis','canc','class'),
            # ('Dunur','target','is_dunur'),
            # ('Facebook','feat','gender1'),
#            ('imdb_top','movies','quality'),
            # ('mutagenesis42','drugs','active'),
#            ('mutagenesis188','drugs','active'),
            # ('NBA','game','ResultOfTeam1'),
            # ('Bupa','bupa','arg2'),
#            ('medical','Examination','Thrombosis'),
            # ('world','Country','Continent'),
            # ('imdb_MovieLens','users','u_gender'),
            # ('Hepatitis_std','dispat','Type'),
            # ('cs','target_churn','target_churn')
]

dbtuples = [
("airline", "On_Time_On_Time_Performance_2016_1", "ArrDel15"),
("facebook", "feat", "gender1"),
("cacn", "canc", "class"),
("CORA", "paper", "class_label"),
("employee", "salaries", "salary"),
("financial", "loan", "status"),
("FNHK", "pripady", "Delka_hospitalizace"),
("imdb", "actors", "gender"),
("imdb_top", "actors", "gender"),
("muskLarge", "molecule", "class"),
("studentLoan", "no_payment_due", "bool")
]

result_file = "../results/REAL_RUNS.txt"
for dtuple in dbtuples:
    print ('python3','benchmark_algorithms.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2],'>>',result_file+dtuple[0]+".txt")

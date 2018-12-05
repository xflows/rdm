## A simple python job generator

learners = ['aleph','RSD','treeliker','wordification']
dbtuples = [('trains','trains','direction'), ## trains data set
            ('Carcinogenesis','canc','class'), ## cancer data set
            ('Facebook','feat','gender1'),
            ('NCAA','target','team_id1_wins'),            
            ('CORA','paper','class_label'),
            ('imdb_ijs','actors','gender'),
            ('Atherosclerosis','Death','PRICUMR'),
            ('Hepatitis_std','dispat','Type')
]

result_file = "./tmp_results.txt"
for dtuple in dbtuples:
    for learner in learners:
        print ('python3','benchmark_algorithms.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2],'--learner',learner,'>>',result_file)

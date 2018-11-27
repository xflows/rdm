## A simple python job generator

learners = ['aleph','RSD','treeliker','wordification']
dbtuples = [('trains','trains','direction'), ## trains data set
            ('Carcinogenesis','canc','class'), ## cancer data set
            ('Biodegradability','molecule','logp'),
            ('genes','Classification','Localization'),
            ('Facebook','feat','gender1'),
            ('NCAA','target','team_id1_wins'),            
            ('Pyrimidine','molecule','activity'),
            ('CORA','paper','class_label')
]

result_file = "./tmp_results.txt"
for dtuple in dbtuples:
    for learner in learners:
        print ('python','benchmark_algorithms.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2],'>',result_file)

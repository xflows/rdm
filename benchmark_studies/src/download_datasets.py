learners = ['aleph','RSD','treeliker','wordification']
dbtuples = [
    ('imdb_top','movies','quality')
#    ('medical','Examination','Thrombosis'),
#    ('world','Country','Continent'),
#    ('Hepatitis_std','dispat','Type'),
#    ('cs','target_churn','target_churn')
#    ('imdb_MovieLens','users','u_gender')
#    ('Bupa','bupa','arg2'),
    ('financial','load','status'),
#    ('Carcinogenesis','canc','class'),
#    ('mutagenesis','molecule','mutagenic')
]

for dtuple in dbtuples:
    print ('python3','get_datasets.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2])

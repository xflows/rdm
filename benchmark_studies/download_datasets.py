learners = ['aleph','RSD','treeliker','wordification']
dbtuples = [('financial','load','status'),('Carcinogenesis','canc','class'),('mutagenesis','molecule','mutagenic')]

result_file = "./tmp_results_new.txt"
for dtuple in dbtuples:
    print ('python3','get_datasets.py','--dataset',dtuple[0],'--target_table',dtuple[1],'--target_label',dtuple[2])

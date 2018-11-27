## A simple python job generator

learners = ['aleph','RSD','treeliker','wordification']
dbtuples = [('trains','trains','direction','east'), ## trains data set
            ('Carcinogenesis','canc','class','TODO'), ## cancer data set
]
result_file = "./tmp_results.txt"

for dtuple in dbtuples:
    for learner in learners:
        print ('python','benchmark_algorithms.py','--dataset',dtuple[0],'--target_label',dtuple[1],'--target_attribute',dtuple[2],'>',result_file)

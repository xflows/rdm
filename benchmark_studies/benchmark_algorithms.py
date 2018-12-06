import sys

#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('ascii')

#import orange
import numpy as np
from timeit import default_timer as timer
import arff
import argparse
from rdm.db import DBVendor, DBConnection, DBContext, RSDConverter, mapper, AlephConverter,TreeLikerConverter,OrangeConverter
from sklearn import preprocessing
from sklearn.metrics import accuracy_score,f1_score
from rdm.wrappers import RSD
from rdm.wrappers import Aleph
from rdm.wrappers import TreeLiker
from rdm.wrappers import Wordification
from rdm.wrappers import Tertius
from rdm.wrappers import Proper
from rdm.validation import cv_split
from io import StringIO
from scipy.io import arff as sarf
from sklearn import tree
import pandas as pd

def arff_parser(arff):

    """
    Extract instances and test cases.
    """
    
    entries = []
    targets = []    
    
    wtag = False

    for entry in train_arff.split("\n"):
        if wtag:
            en = entry.split(",")
            if len(en)>1:
                en = [x.replace(" ","") for x in en]
                targets.append(en[-1])
                entries.append([float(x) for x  in en[0:len(en)-1]])
        if "@DATA" in entry:
            wtag=True
            
    return (entries,targets)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Benchmark setup')
    parser.add_argument('--learner',type=str,default="aleph")
    parser.add_argument('--dataset',type=str,default="trains")
    parser.add_argument('--target_table',type=str,default="trains")
    parser.add_argument('--target_label',type=str,default="direction")

    args = parser.parse_args()    
    learner = args.learner
    dataset = args.dataset
    target_label = args.target_label
    target_table = args.target_table

    # connection = DBConnection(
    #     'ilp',  # User
    #     'ilp123',  # Password
    #     'workflow.ijs.si',  # Host
    #     dataset,  # Database
    #     vendor=DBVendor.MySQL
    # )    
    
    # Provide connection information
    connection = DBConnection(
        'guest',  # User
        'relational',  # Password
        'relational.fit.cvut.cz',  # Host
        dataset,  # Database
        vendor=DBVendor.MySQL
    )

    # Define learning context
    context = DBContext(connection, target_table=target_table, target_att=target_label)
    print ("Got context..")

    # Cross-validation loop
    predictions = []
    predictions_f1 = []
    times = []
    folds = 5
    target_attr_value = None
    
    for train_context, test_context in cv_split(context, folds=folds, random_seed=0):

        # Find features on the train set
        start = timer()
        if learner == "RSD":
            conv = RSDConverter(train_context)
            rsd = RSD()

            features, train_arff, _ = rsd.induce(
                conv.background_knowledge(),   # Background knowledge
                examples=conv.all_examples(),  # Training examples
                cn2sd=False                    # Disable built-in subgroup discovery
            )

        if learner == "aleph":
            
            tbl = train_context.orng_tables[target_table]
            target_attr_value = tbl[1][target_label].value
            conv = AlephConverter(train_context, target_att_val=target_attr_value)
            aleph = Aleph()
            train_arff, features = aleph.induce('induce_features',conv.positive_examples(),
                                                conv.negative_examples(),
                                                conv.background_knowledge(),printOutput=False)
            
        if learner == "treeliker":
            conv = TreeLikerConverter(train_context)
            conv2 = TreeLikerConverter(test_context)
            treeliker = TreeLiker(conv.dataset(), conv.default_template(),conv2.dataset())   # Runs RelF by default
            train_arff, test_arff = treeliker.run()

            wtag=False
            entries = []
            targets = []
            entries_test = []
            targets_test = []

            for entry in train_arff.split("\n"):
                if wtag:
                    en = entry.split(",")
                    if len(en)>1:
                        en = [x.replace(" ","") for x in en]
                        targets.append(en[-1])
                        en = [1 if "+" in x else 0 for x in en]
                        entries.append(en[0:len(en)-1])
                if "@data" in entry:
                    wtag=True

            wtag=False
            for entry in test_arff.split("\n"):
                if wtag:
                    en = entry.split(",")
                    if len(en) > 1:
                        en = [x.replace(" ","") for x in en]
                        targets_test.append(en[-1])
                        en = [1 if "+" in x else 0 for x in en]
                        entries_test.append(en[0:len(en)-1])

                if "@data" in entry:
                    wtag=True

            print (entries_test,targets_test)
                    
        elif learner == "wordification":
            corange = OrangeConverter(train_context)
            torange = OrangeConverter(test_context)
            wordification = Wordification(corange.target_Orange_table(), corange.other_Orange_tables(), train_context)
            wordification.run(1)
            wordification.calculate_weights()
            wordification.prune(minimum_word_frequency_percentage=10)
            train_arff = wordification.to_arff()

            wordification_test = Wordification(torange.target_Orange_table(), torange.other_Orange_tables(), test_context)
            wordification_test.run(1)
            idfs = wordification.idf
            docs  = wordification_test.resulting_documents
            classes = [str(a) for a in wordification_test.resulting_classes]
            feature_names = wordification.word_features
            feature_vectors = []
            for doc in docs:
                doc_vec = []
                for feature in feature_names:
                    cnt = 0
                    for x in doc:
                        if x  == feature:
                            cnt+=1
                    idf = cnt * idfs[feature]
                    doc_vec.append(idf)
                feature_vectors.append(doc_vec)
            test_arff = wordification_test.to_arff()

            entries = []
            targets = []
            entries_test = []
            targets_test = []
            wtag = False

            for entry in train_arff.split("\n"):
                if wtag:
                    en = entry.split(",")
                    if len(en)>1:
                        en = [x.replace(" ","") for x in en]

                        targets.append(en[-1])
                        entries.append([float(x) for x  in en[0:len(en)-1]])
                if "@DATA" in entry:
                    wtag=True

            wtag=False

            targets_test = classes
            entries_test = feature_vectors


        else:
            ## aleph and RSD parsing
            data = arff.loads(str(train_arff))
            entries = []
            targets = []

            for entry in data:
                en = list(entry)
                features_target = en[-1]
                features_train = en[0:len(en)-1]
                features_train = [1 if x == "+" else 0 for x in features_train]
                entries.append(features_train)
                targets.append(features_target)

            # Map the *test set* using the features from the train set
            if learner == 'aleph':
                tmp_learner = learner
                test_arff = mapper.domain_map(features, tmp_learner, train_context, test_context,format="csv")
                test_ins = test_arff.split("\n")

            elif learner == "RSD":
                tmp_learner = 'rsd'
                test_arff = mapper.domain_map(features, tmp_learner, train_context, test_context,format="csv")
                test_ins = test_arff.split("\n")

            entries_test = []
            targets_test = []
            
            for entry in test_ins:
                en = entry.strip().split(",")
                if en[-1] != '':
                    features_target = en[-1]
                    features_train = en[0:len(en)-1]
                    features_train = [1 if x == "+" else 0 for x in features_train]
                    entries_test.append(features_train)
                    targets_test.append(features_target)

            if learner == "aleph":
                targets_test = ['positive' if x == target_attr_value else 'negative' for x in targets_test]

        train_features = pd.DataFrame(entries)
        train_targets = pd.DataFrame(targets)
        test_features = pd.DataFrame(entries_test)
        test_targets = pd.DataFrame(targets_test)

        le = preprocessing.LabelEncoder()
        le.fit(train_targets)

        targets_train_encoded = le.transform(train_targets)
        targets_test_encoded = le.transform(test_targets)

        clf = tree.DecisionTreeClassifier()
        clf.fit(train_features,targets_train_encoded)
        preds = clf.predict(test_features)

        acc = accuracy_score(preds,targets_test_encoded)
        f1 = f1_score(preds,targets_test_encoded)
        predictions.append(acc)
        predictions_f1.append(f1)
        end = timer()
        times.append(end-start)
        print(acc,f1)

    print ("RESULT_LINE",learner, dataset, target_label, np.mean(predictions), np.mean(predictions_f1),np.mean(times),target_label)

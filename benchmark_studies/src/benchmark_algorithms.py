import sys

#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('ascii')

#import orange
import numpy as np
from timeit import default_timer as timer
import arff
import argparse
from rdm.db import DBVendor, DBConnection, DBContext, RSDConverter, mapper, AlephConverter,TreeLikerConverter,OrangeConverter, SQLparser
from sklearn import preprocessing
from sklearn.metrics import accuracy_score,f1_score
# from rdm.wrappers import RSD
# from rdm.wrappers import Aleph
# from rdm.wrappers import TreeLiker
# from rdm.wrappers import wordification
# from rdm.wrappers import wordification2
# from rdm.wrappers import Tertius
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from rdm.wrappers import *
from rdm.validation import cv_split
from io import StringIO
from scipy.io import arff as sarf
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support
import pickle
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
    parser.add_argument('--dataset',type=str,default="cacn")
    parser.add_argument('--explain',type=bool,default=False)
    parser.add_argument('--target_table',type=str,default="canc")
    parser.add_argument('--target_label',type=str,default="class")

    args = parser.parse_args()
    dataset = args.dataset
    target_label = args.target_label
    target_table = args.target_table

    connection = SQLparser(
        '../../datasets/sql/'+dataset+'.sql'
    )

    # Define learning context
    context = DBContext(connection, target_table=target_table, target_att=target_label)

    # Cross-validation loop
    predictions = []
    predictions_f1 = []
    predictions_recall = []
    predictions_precision = []
    times = []
    folds = 10

    target_attr_value = None
    aucs = []
    cnts = 0
    internal_times = []
    learners = ['sql2vec']#["RSD","aleph","treeliker"ime2]
    estimators = [10,20]
    for estimator_number in estimators:
        for train_cx, test_cx in cv_split(context, folds=folds, random_seed=65413224):
            cnts+=1
            print("Starting CV")
            for learner in learners:
                train_context = train_cx.copy()
                test_context = test_cx.copy()
                try:
                    internal_start = timer()
                    start = timer()
                    if learner == "RSD":
                        conv = RSDConverter(train_context)
                        rsd = RSD()

                        features, train_arff, _ = rsd.induce(
                            conv.background_knowledge(),   # Background knowledge
                            examples=conv.all_examples(),  # Training examples
                            cn2sd=False                    # Disable built-in subgroup discovery
                        )

                    elif learner == "aleph":
                        print("Starting Aleph")
                        tbl = train_context.orng_tables[target_table]
                        #print(tbl)
                        target_attr_value = tbl[1][target_label].value
                        #print(target_attr_value)
                        conv = AlephConverter(train_context, target_att_val=target_attr_value)
                        aleph = Aleph()
                        train_arff, features = aleph.induce('induce_features',conv.positive_examples(),
                                                            conv.negative_examples(),
                                                            conv.background_knowledge(),printOutput=False)
                        print("Getting features")
                        fx = features.split("\n")
                        feature_set = [x for x in fx if "feature(" in x]

                    elif learner == "treeliker":
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

                    elif learner == "wordification2":

                        w2o = Wordification2(verbose=True,target_table_name=target_table)
                        entries,targets = w2o.fit_transform(train_context)
                        entries_test,targets_test = w2o.transform(test_context)
                        entries = entries.todense()
                        entries_test = entries_test.todense()

                    elif learner == "wordification":

                        corange = OrangeConverter(train_context)
                        torange = OrangeConverter(test_context)

            #            other_tables = [train_context.orng_tables[x] for x,y in train_context.orng_tables.items() if x != train_context.target_table]

            #            target__table = train_context.target_table

                        target_table = corange.target_Orange_table()
                        other_tables = corange.other_Orange_tables()

                        wordification = Wordification(target_table, other_tables, train_context)
                        wordification.run(1)
                        wordification.calculate_weights()
                        wordification.prune(minimum_word_frequency_percentage=1)
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

                    elif learner == "sql2vec":
                        sql2vec_alg = sql2vec(train_context.orng_tables,test_context.orng_tables,context.connected, target_table, target_label)
                        entries, targets, entries_test, targets_test, vectorizer = sql2vec_alg.run()                        
                        entries = entries.todense()
                        entries_test = entries_test.todense()
                        features = vectorizer.get_feature_names()
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

                    train_features.columns = features
                    test_features.columns = features


                    #features = pd.concat([train_features,test_features])
                    #targets = pd.concat([train_targets,test_targets])
                    
                 #   features[features.columns] = features[features.columns].apply(pd.to_numeric, errors='coerce')

                 #   train_features[train_features.columns] = train_features[train_features.columns].apply(pd.to_numeric, errors='coerce')

                 #   test_features[test_features.columns] = test_features[test_features.columns].apply(pd.to_numeric, errors='coerce')


                    #features.to_csv("../../folds/features_"+learner+"_"+args.dataset+"_"+str(cnts)+".tsv",sep="\t")
                    #targets.to_csv("../../folds/targets_"+learner+"_"+args.dataset+"_"+str(cnts)+".tsv",sep="\t")


                    le = preprocessing.LabelEncoder()
                    le.fit(train_targets)

                    targets_train_encoded = le.transform(train_targets)
                    targets_test_encoded = le.transform(test_targets)
                    internal_end = timer()
                    internal_time = internal_end-internal_start

                    classifier_obj = []
                    clf1 = tree.DecisionTreeClassifier()
                    clf1.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("DT",clf1))

                    # import autosklearn.classification
                    # clfx = autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=600)
                    # clfx.fit(train_features,targets_train_encoded)
                    # classifier_obj.append(("autoML",clfx))
                    print("Classification commenced.")
                    from sklearn import svm
                    clf2 = svm.SVC(gamma=0.001,probability=True,C=20)
                    clf2.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("SVM",clf2))

                    from sklearn.ensemble import GradientBoostingClassifier
                    clf3 = GradientBoostingClassifier(n_estimators=estimator_number)
                    clf3.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("GBM",clf3))

                    from sklearn.linear_model import LogisticRegression
                    clf4 = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
                    clf4.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("LR",clf4))

                    from sklearn.neighbors.nearest_centroid import NearestCentroid
                    clf = NearestCentroid()
                    clf.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("CEN",clf))

                    from sklearn.ensemble import ExtraTreesClassifier
                    clf5 = ExtraTreesClassifier(n_estimators=estimator_number, max_depth=None,min_samples_split=2, random_state=0)
                    clf5.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("XT",clf5))

                    from sklearn.dummy import DummyClassifier
                    clf6 = DummyClassifier(strategy="most_frequent")
                    clf6.fit(train_features,targets_train_encoded)
                    classifier_obj.append(("MF",clf6))

                    try:
                        import xgboost as xgb
                        clf = xgb.XGBClassifier(n_estimators=estimator_number)
                        clf.fit(train_features,targets_train_encoded)
                        classifier_obj.append(("XGB",clf))
                    except:
                        pass

                    if args.explain:
                        import shap
                        import xgboost
                        X = pd.concat([train_features,test_features],axis=0)
                        Y = np.concatenate((targets_train_encoded,targets_test_encoded))
                        if feature_set !=None:
                            X.columns = feature_set
                            ## natreniramo
                            model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=Y), 100)

                            ## razlozimo celi dataset
                            explainer = shap.TreeExplainer(model)
                            shap_values = explainer.shap_values(X)

                            # visualize the first prediction's explanation
                            shap.summary_plot(shap_values, X)

                    end = timer()
                    for cname, clf in classifier_obj:
                        preds = clf.predict(test_features)
                        acc = accuracy_score(preds,targets_test_encoded)
                        f1 = f1_score(preds,targets_test_encoded)
                        p,r,f1,sup = precision_recall_fscore_support(preds,targets_test_encoded)
                        time_overall = end-start
                        sc = roc_auc_score(targets_test_encoded, clf.predict_proba(test_features)[:,1])
                        print ("RESULT_LINE",str(cnts),learner, cname, dataset, target_label, acc,time_overall,target_label,r[0],p[0],internal_time,sc)

                except Exception as es:
                    print(es)

    #    print ("RESULT_LINE",learner, classifier, dataset, target_label, np.mean(predictions),np.mean(times),target_label,np.mean(predictions_recall),np.mean(predictions_precision),np.mean(internal_times),np.mean(aucs))

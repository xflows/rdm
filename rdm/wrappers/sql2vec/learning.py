## misc methods for learning
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
import xgboost

def svm_learner(train_features,train_classes):
    clf = svm.SVC(kernel='rbf',C=10)
    clf.fit(train_features,train_classes)
    return clf

def gbm_learner(train_features,train_classes):
    clf = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(train_features, label=train_classes), 100)
    return clf

def lr_learner (train_features,train_classes):
    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(train_features,train_classes)
    return clf

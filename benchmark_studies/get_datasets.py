### save all datasets
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
import pickle
import pandas as pd

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
    
    connection = DBConnection(
        'guest',  # User
        'relational',  # Password
        'relational.fit.cvut.cz',  # Host
        dataset,  # Database
        vendor=DBVendor.MySQL
    )

    # Define learning context
    context = DBContext(connection, target_table=target_table, target_att=target_label)
    ## save context to csv
    with open("../datasets/"+args.dataset+'.pickle', 'wb') as handle:
        pickle.dump(context, handle, protocol=pickle.HIGHEST_PROTOCOL)

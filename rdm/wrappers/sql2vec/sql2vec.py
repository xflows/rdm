## sql2vec. Given a simple sql file a target table_attribute with respect to which to propositionalize, this generates a sparse matrix.

import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from .learning import *
#from arcs import *

def cleanp(stx):
    return stx.replace("(","").replace(")","").replace(",","")

def clear(stx):
    return stx.replace("`","").replace("`","")

def get_table_keys(quadruplet):
    tk = defaultdict(set)
    for entry in quadruplet:
        tk[entry[0]].add(entry[1])
        tk[entry[2]].add(entry[3])
    return tk

def relational_words_to_matrix(fw,relation_order):
    docs = []
    vectorizer = TfidfVectorizer(ngram_range=relation_order)
    for k,v in fw.items():
        docs.append(" ".join(v))
    mtx = vectorizer.fit_transform(docs) # mtx = vectorizer.transform(docs)
    return mtx, vectorizer

def relational_words_to_matrix_with_vec(fw,vectorizer):
    docs = []
    for k,v in fw.items():
        docs.append(" ".join(v))
    try:
        mtx = vectorizer.transform(docs)
    except:
        print("NE DELA")
    return mtx

def generate_relational_words(tables,fkg,level=1,target_table=None,target_attribute=None,relation_order=(2,4), vectorizer=None):

    feature_vectors = defaultdict(list)
    core_table = tables[target_table]
    core_foreign = None

    fkg = {k:v for k,v in fkg.items() if k[0] == target_table}

    col_names = [x.name for x in core_table.domain.metas]+[x.name for x in core_table.domain.class_vars]
    target_classes = [x[target_attribute].value for x in core_table]
    for index in range(len(core_table)):

        row = core_table[index]

        for column_name in col_names:
            if column_name != target_attribute:
                feature_vectors[index].append("_".join([str(row[column_name]),column_name,target_table]))

        for fkg_key,fkg_vals in fkg.items():
            for fkg_val in fkg_vals:
                core_keys = [x[fkg_val[0]].value for x in core_table]
                core_foreign = fkg_val[0]
                mapping_table = tables[fkg_key[1]]
                mapping_table_name = fkg_key[1]
                mapping_table_key = fkg_val[1]

                row_core_foreign = row[core_foreign]

                if row_core_foreign == "NULL":
                    feature_vectors[index].append("")
                else:
                    trow_columns = [x.name for x in mapping_table.domain.metas]+[x.name for x in mapping_table.domain.class_vars]
                    vx = [[row[col].value for col in trow_columns] for row in mapping_table if row[mapping_table_key] == row_core_foreign]
                    vx = [x for x in vx if x != []]

                    if vx != []:

                        trow = pd.DataFrame(vx)
                        trow.columns = trow_columns

                        local_tabu = ["id"]

                        trow = trow[[x for x in trow.columns if x not in local_tabu]]


                        try:
                            for x in trow.columns:
                                if x != mapping_table_key:
                                    for value in trow[x]:
                                        feature_vectors[index].append("_".join([str(value),x,mapping_table_name]))
                        except Exception as ex:
                            print(ex)
                            print(trow[x],x,mapping_table_name)
                            print(mapping_table,row_core_foreign)
                            print("ERROR for: "+str(row[core_foreign]))
                            feature_vectors[index].append("")

    if vectorizer:
        matrix = relational_words_to_matrix_with_vec(feature_vectors,vectorizer)
        return matrix, target_classes
    else:
        matrix, vectorizer = relational_words_to_matrix(feature_vectors,relation_order)
        return matrix, target_classes, vectorizer



class sql2vec(object):
    def __init__(self, train_tables, test_tables, fkg, target__table, target_attribute):

        self.train_tables = train_tables
        self.test_tables = test_tables
        self.fkg = fkg
        self.target_table = target__table
        self.target_attribute = target_attribute

    def run(self):

        entries, targets, train_vectorizer = generate_relational_words(self.train_tables,self.fkg,1,self.target_table,self.target_attribute, relation_order=(1,3))
        entries_test, targets_test = generate_relational_words(self.test_tables,self.fkg,1,self.target_table,self.target_attribute, relation_order=(1,3), vectorizer = train_vectorizer)

        return entries,targets,entries_test,targets_test,train_vectorizer

        ##  start from table-class pair
        ## first crawl the internal table structure
        ## parameterize this
        ## for each foreign key from this table, crawl next
        ## get words, do tfidf.

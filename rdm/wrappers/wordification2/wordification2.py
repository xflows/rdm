### the updated wordification algorithm - Blaz Skrlj, 2019
import pickle
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

class Wordification2():
    def __init__(self,max_features=1000, ngram_range=(2,8),verbose=True,target_table_name="trains"):

        self.target_table_name = target_table_name
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.verbose = verbose
        if self.verbose:
            print("Beginning to read the inputs..")
        self.database = None
        
    def load_stored_data(self,datafile,format_d="context"):

        """
        Load stored data - local instance
        """
        
        if format_d == "pickle":
            with open(datafile,"rb") as handle:
                context = pickle.load(handle)        
            self.database = context
            
        else:
            self.database = datafile
        
        if self.verbose:
            print("Loaded the data..")

    def traverse(self,train_data=True):

        connections = self.database.connected
        orange_tables = self.database.orng_tables
        private_keys = self.database.pkeys
        target_table = self.database.target_table        
            
        ## for each instance, get docs
        target_table = orange_tables[target_table]
        target_table_name = self.target_table_name
        target_words = defaultdict(list)
        
        for k,v in connections.items():
            if k[0] == target_table_name:
                link_table = orange_tables[k[1]]
                for initial_row in target_table:
                    target_value = initial_row[self.database.target_att]
                    for row in link_table:
                        for edge in v:
                            foreign_key = initial_row[edge[0]]
                            if row[edge[1]] == foreign_key:
                                words = []
                                for x in row.table:
                                    for j in range(len(x)):
                                        val = x[j]
                                        words.append(x[j].value)
                                target_words[str(target_value)].append(words)
        if train_data:
            self.train_corpus = []
            self.train_labels = []
            for k,v in target_words.items():
                for doc in v:
                    doc = " ".join([str(x) for x in doc])
                    self.train_labels.append(k)
                    self.train_corpus.append(doc)
        else:
            self.test_corpus = []
            self.test_labels = []
            for k,v in target_words.items():
                for doc in v:
                    doc = " ".join([str(x) for x in doc])
                    self.test_labels.append(k)
                    self.test_corpus.append(doc)                    

    def fit_transform(self,datafile):
        self.load_stored_data(datafile)        
        self.traverse(train_data=True)
        self.vectorizer = TfidfVectorizer(max_features=self.max_features,ngram_range=self.ngram_range)
        vectorized_data = self.vectorizer.fit_transform(self.train_corpus)
        del self.database
        return (vectorized_data,self.train_labels)

    def transform(self,datafile):
        self.load_stored_data(datafile)
        self.traverse(train_data=False)
        return(self.vectorizer.transform(self.test_corpus),self.test_labels)

if __name__ == "__main__":

    data_example = "../../../datasets/trains.pickle"
    efc = Wordification2(data_example)
    train_vectors,target_labels = efc.fit_transform()

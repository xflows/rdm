import unittest
import os
import sys
sys.path.append('..')


from rdm.db import DBConnection, DBContext, OrangeConverter, RSDConverter, AlephConverter, TreeLikerConverter, MySQLDataSource
from rdm.wrappers import Wordification, RSD, Aleph, TreeLiker
from conf import TEST_DB, RESULTS_FOLDER


class TestWrappers(unittest.TestCase):

    def setUp(self):
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database']
        )
        self.context = DBContext(MySQLDataSource(self.connection))
        self.context.target_table = 'trains'
        self.context.target_att = 'direction'


    def test_wordification(self):
        conv = OrangeConverter(self.context)
        wordification = Wordification(
            conv.target_Orange_table(),
            conv.other_Orange_tables(),
            self.context
        )
        wordification.run(1)
        wordification.calculate_weights()

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'wordification', 'trains.arff')) as f:
            self.assertMultiLineEqual(wordification.to_arff(), f.read())


    def test_rsd(self):
        conv = RSDConverter(self.context)
        rsd = RSD()
        features, arff, _ = rsd.induce(conv.background_knowledge(),
                                       examples=conv.all_examples())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'rsd', 'trains.arff')) as f:
            self.assertMultiLineEqual(arff, f.read())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'rsd', 'trains.frs')) as f:
            self.assertMultiLineEqual(features, f.read())


    def test_aleph(self):
        conv = AlephConverter(self.context, target_att_val = 'east')
        aleph = Aleph()
        theory, features = aleph.induce('induce_features', conv.positive_examples(), 
                                        conv.negative_examples(),
                                        conv.background_knowledge())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'aleph', 'trains.arff')) as f:
            self.assertMultiLineEqual(theory, f.read())


    def test_treeliker(self):
        conv = TreeLikerConverter(self.context)
        treeliker = TreeLiker(conv.dataset(), conv.default_template())
        arff, _ = treeliker.run()
        
        # This just tests execution for the moment
        # TreeLiker seems to use some random factors
        self.assertTrue(True)

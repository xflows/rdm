import unittest
import os
import sys

sys.path.append('..')

from rdm.db import DBConnection, DBContext, OrangeConverter, RSDConverter, AlephConverter, TreeLikerConverter
from rdm.wrappers import Wordification, RSD, Aleph, TreeLiker
from tests.conf import TEST_DB, TEST_DB_POSTGRES, RESULTS_FOLDER


class TestWrappers(unittest.TestCase):
    def setUp(self):
        # MySQL test db
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database'],
            vendor=TEST_DB['vendor']
        )
        self.context = DBContext(self.connection,
                                 target_table='trains',
                                 target_att='direction')
        # Postgres test db
        self.connection_pg = DBConnection(
            TEST_DB_POSTGRES['user'],
            TEST_DB_POSTGRES['pass'],
            TEST_DB_POSTGRES['host'],
            TEST_DB_POSTGRES['database'],
            vendor=TEST_DB_POSTGRES['vendor']
        )
        self.context_pg = DBContext(self.connection_pg)
        self.context_pg.target_table = 'urbanblock'
        self.context_pg.target_att = 'class'

    def test_wordification_mysql(self):
        conv = OrangeConverter(self.context)
        wordification = Wordification(
            conv.target_Orange_table(),
            conv.other_Orange_tables(),
            self.context
        )
        wordification.run(1)
        wordification.calculate_weights()
        arff = wordification.to_arff()

        with open('wordification_mysql.txt', 'w') as f:
            f.write(arff)

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'wordification', 'trains.arff')) as f:
            self.assertMultiLineEqual(arff, f.read())

    def test_rsd_mysql(self):
        conv = RSDConverter(self.context)
        rsd = RSD()
        features, arff, _ = rsd.induce(conv.background_knowledge(),
                                       examples=conv.all_examples())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'rsd', 'trains.arff')) as f:
            self.assertMultiLineEqual(arff, f.read())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'rsd', 'trains.frs')) as f:
            self.assertMultiLineEqual(features, f.read())

    def test_aleph_pgsql(self):
        conv = AlephConverter(self.context_pg, target_att_val='h_indiv')
        aleph = Aleph()
        theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                        conv.negative_examples(),
                                        conv.background_knowledge())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'aleph', 'geographical.arff')) as f:
            self.assertMultiLineEqual(theory, f.read())


    def test_aleph_mysql(self):
        conv = AlephConverter(self.context, target_att_val='east')
        aleph = Aleph()
        theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                        conv.negative_examples(),
                                        conv.background_knowledge())

        with open(os.path.join(RESULTS_FOLDER, 'wrappers', 'aleph', 'trains.arff')) as f:
            self.assertMultiLineEqual(theory, f.read())

    def test_treeliker_mysql(self):
        conv = TreeLikerConverter(self.context)
        treeliker = TreeLiker(conv.dataset(), conv.default_template())
        arff, _ = treeliker.run()

        # This just tests execution for the moment
        # TreeLiker seems to use some random factors
        self.assertTrue(True)

import os


TEST_DB = {
    'user': 'ilp',
    'pass': 'ilp123',
    'host': 'workflow.ijs.si',
    'database': 'ilp',
    'vendor': 'mysql'
}

TEST_DB_POSTGRES = {
    'user': 'ilp',
    'pass': 'ilp123',
    'host': '10.0.2.2',
    'database': 'ilp',
    'vendor': 'postgresql'
}

RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')

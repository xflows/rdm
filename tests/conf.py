import os


TEST_DB = {
    'user': 'ilp',
    'pass': 'ilp123',
    'host': 'workflow.ijs.si',
    'database': 'ilp',
    'vendor': 'mysql'
}

TEST_DB_POSTGRES = {
    # TODO: Setup test postresql db
    # 'user': 'ilp',
    # 'pass': 'ilp123',
    # 'host': 'workflow.ijs.si',
    # 'database': 'ilp',
    'vendor': 'postgresql'
}

RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')

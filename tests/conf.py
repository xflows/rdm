import os
from rdm.db.context import DBVendor


TEST_DB = {
    'user': 'ilp',
    'pass': 'ilp123',
    'host': 'workflow.ijs.si',
    'database': 'ilp',
    'vendor': DBVendor.MySQL
}

TEST_DB_POSTGRES = {
    'user': 'ilp',
    'pass': 'ilp123',
    'host': 'localhost',
    'database': 'ilp',
    'vendor': DBVendor.PostgreSQL
}

RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')

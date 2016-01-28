'''
MySQL connectivity library.

@author: Anze Vavpetic <anze.vavpetic@ijs.si>
'''
import os
import tempfile
import time
from django import forms
import mysql.connector as sql
from datasource import MySQLDataSource, PgSQLDataSource
from context import DBConnection, DBContext
from converters import RSDConverter, AlephConverter, OrangeConverter, TreeLikerConverter, PrdFctConverter
from mapper import domain_map


def database_connect(input_dict):
    user = str(input_dict['user'])
    password = str(input_dict['password'])
    host = str(input_dict['host'])
    db = str(input_dict['database'])
    vendor = str(input_dict['vendor'])
    dbcon = DBConnection(user, password, host, db, vendor=vendor)
    return {'connection' : dbcon}


def database_db_context(input_dict):
    return {'context' : None}


def database_db_context_finished(postdata, input_dict, output_dict):
    con = input_dict['connection']
    find_con = input_dict['find_connections'] == 'true'
    context = DBContext(con, find_connections=find_con)
    _update_context(context, postdata)
    return {'context' : context}


def _update_context(context, postdata):
    '''
    Updates the default selections with user's selections.
    '''
    widget_id = postdata.get('widget_id')[0]
    context.target_table = postdata.get('target_table%s' % widget_id)[0]
    context.target_att = postdata.get('target_att%s' % widget_id)[0]
    context.tables = postdata.get('tables%s' % widget_id, [])
    if context.target_table not in context.tables:
        raise Exception('The selected target table "%s" is not among the selected tables.' % context.target_table)
    # Propagate the selected tables
    for table in context.cols.keys():
        if table not in context.tables:
            del context.cols[table]
    for pair in context.connected.keys():
        if pair[0] in context.tables and pair[1] in context.tables:
            continue
        del context.connected[pair]
    for table in context.tables:
        context.cols[table] = postdata.get('%s_columns%s' % (table, widget_id), [])
        if table == context.target_table and context.target_att not in context.cols[table]:
            raise Exception('The selected target attribute ("%s") is not among the columns selected for the target table ("%s").' % (context.target_att, context.target_table))
    if context.in_memory:
        context.orng_tables = context.read_into_orange()


def database_rsd_converter(input_dict):
    dump = input_dict['dump'] == 'true'
    rsd = RSDConverter(input_dict['context'], discr_intervals=input_dict['discr_intervals'] or {})
    return {'examples' : rsd.all_examples(), 'bk' : rsd.background_knowledge()}


def database_aleph_converter(input_dict):
    dump = input_dict['dump'] == 'true'
    target_att_val = input_dict['target_att_val']
    if not target_att_val:
        raise Exception('Please specify a target attribute value.')
    aleph = AlephConverter(input_dict['context'], target_att_val=target_att_val, discr_intervals=input_dict['discr_intervals'] or {})
    return {'pos_examples' : aleph.positive_examples(), 'neg_examples' : aleph.negative_examples(), 'bk' : aleph.background_knowledge()}


def database_treeliker_converter(input_dict):
    treeliker = TreeLikerConverter(input_dict['context'], 
                                   discr_intervals=input_dict['discr_intervals'] or {})
    return {'dataset': treeliker.dataset(), 
            'template': treeliker.default_template()}


def database_query_to_odt(input_dict):
    return {'dataset' : None}


def database_orange_converter(input_dict):
    context = input_dict['context']
    orange = OrangeConverter(context)
    return {'target_table_dataset' : orange.target_Orange_table(),'other_table_datasets': orange.other_Orange_tables()}


def database_prd_fct_converter(input_dict):   
    context = input_dict['context']
    prd_fct = PrdFctConverter(context)
    
    url = tempfile.mkdtemp()
    timenow = int(round(time.time() * 1000))
    prd_file_url=os.path.join(url,"prdFctTemp%s.prd"%str(timenow))
    with open(prd_file_url, "w") as prd:
        prd.write( prd_fct.create_prd_file());   

    fct_file_url=os.path.join(url,"prdFctTemp%s.fct"%str(timenow))
    with open(fct_file_url, "w") as fct:
        fct.write( prd_fct.create_fct_file());      
       
    return {'prd_file' : prd_file_url,'fct_file': fct_file_url}

def ilp_map_rsd(input_dict):
    return do_map(input_dict, 'rsd')


def ilp_map_treeliker(input_dict):
    return do_map(input_dict, 'treeliker')


def ilp_map_aleph(input_dict):
    positive_class = input_dict['positive_class']
    return do_map(input_dict, 'aleph', positive_class=positive_class)


def do_map(input_dict, feature_format, positive_class=None):
    '''
    Maps a new example to a set of features.
    '''
    # Context of the unseen example(s)
    train_context = input_dict['train_ctx']
    test_context = input_dict['test_ctx']

    # Currently known examples & background knowledge
    features = input_dict['features']
    format = input_dict['output_format']

    evaluations = domain_map(features, feature_format, train_context,
                             test_context, format=format,
                             positive_class=positive_class)
    return {'evaluations' : evaluations}

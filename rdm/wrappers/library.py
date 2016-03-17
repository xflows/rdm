import re
import json
from string import ascii_lowercase as chars
from random import choice

from aleph import Aleph
from rsd import RSD
from wordification import Wordification
from treeliker import TreeLiker
from security import check_input
from proper import Proper
from tertius import Tertius, OneBC
from caraf import Caraf

from services.webservice import WebService

def ilp_aleph(input_dict):
    aleph = Aleph()
    settings = input_dict['settings']
    mode = input_dict['mode']
    pos = input_dict['pos']
    neg = input_dict['neg']
    b = input_dict['b']
    # Parse settings provided via file
    if settings:
        aleph.settingsAsFacts(settings)
    # Parse settings provided as parameters (these have higher priority)
    for setting, def_val in Aleph.ESSENTIAL_PARAMS.items():
        aleph.set(setting, input_dict.get(setting, def_val))
    # Check for illegal predicates
    for pl_script in [b, pos, neg]:
        check_input(pl_script)
    # Run aleph
    results = aleph.induce(mode, pos, neg, b)
    return {'theory': results[0], 'features': results[1]}


def ilp_rsd(input_dict):
    rsd = RSD()
    settings = input_dict.get('settings',None)
    pos = input_dict.get('pos', None)
    neg = input_dict.get('neg', None)
    examples = input_dict.get('examples', None)
    b = input_dict['b']
    subgroups = input_dict['subgroups'] == 'true'
    # Parse settings
    if settings:
        rsd.settingsAsFacts(settings)
    # Parse settings provided as parameters (these have higher priority)
    for setting, def_val in RSD.ESSENTIAL_PARAMS.items():
        rsd.set(setting, input_dict.get(setting, def_val))
    # Check for illegal predicates
    for pl_script in [b, pos, neg, examples]:
        check_input(pl_script)
    # Run rsd
    features, arff, rules = rsd.induce(b, examples=examples, pos=pos, neg=neg, cn2sd=subgroups)
    return {'features' : features, 'arff' : arff, 'rules' : rules}



def ilp_sdmsegs_rule_viewer(input_dict):
    return {}


def ilp_sdmaleph(input_dict):
    import orange
    ws = WebService('http://vihar.ijs.si:8097', 3600)
    data = input_dict.get('examples')
    if isinstance(data, orange.ExampleTable):
        with tempfile.NamedTemporaryFile(suffix='.tab', delete=True) as f:
            data.save(f.name)
            examples = f.read()
    elif isinstance(data, list):
        examples = json.dumps(data)
    elif isinstance(data, str):
        examples = data
    else:
        raise Exception('Illegal examples format. \
                         Supported formats: str, list or Orange')
    response = ws.client.sdmaleph(
        examples=examples,
        mapping=input_dict.get('mapping'),
        ontologies=[{'ontology' : ontology} for ontology in input_dict.get('ontology')],
        relations=[{'relation' : relation} for relation in input_dict.get('relation')],
        posClassVal=input_dict.get('posClassVal') if input_dict.get('posClassVal') != '' else None,
        cutoff=input_dict.get('cutoff') if input_dict.get('cutoff') != '' else None,
        minPos=input_dict.get('minPos') if input_dict.get('minPos') != '' else None,
        noise=input_dict.get('noise') if input_dict.get('noise') != '' else None,
        clauseLen=input_dict.get('clauseLen') if input_dict.get('clauseLen') != '' else None,
        dataFormat=input_dict.get('dataFormat') if input_dict.get('dataFormat') != '' else None
    )
    return {'theory' : response['theory']}


def ilp_wordification(input_dict):
    target_table = input_dict.get('target_table',None)
    other_tables = input_dict.get('other_tables', None)
    weighting_measure = input_dict.get('weighting_measure', 'tfidf')
    context = input_dict.get('context', None)
    word_att_length = int(input_dict.get('f_ngram_size', 1))
    idf=input_dict.get('idf', None)

    for _ in range(1):
        wordification = Wordification(target_table,other_tables,context,word_att_length,idf)
        wordification.run(1)
        wordification.calculate_weights(weighting_measure)
        #wordification.prune(50)
        #wordification.to_arff()

    return {'arff' : wordification.to_arff(),'corpus': wordification.wordify(),'idf':wordification.idf}


def ilp_treeliker(input_dict):
    template = input_dict['template']
    dataset = input_dict['dataset']
    settings = {
        'algorithm': input_dict.get('algorithm'),
        'minimum_frequency': input_dict.get('minimum_frequency'),
        'covered_class': input_dict.get('covered_class'),
        'maximum_size': input_dict.get('maximum_size'),
        'use_sampling': input_dict.get('use_sampling'),
        'sample_size': input_dict.get('sample_size'),
        'max_degree': input_dict.get('max_degree')
    }
    treeliker = TreeLiker(dataset, template, settings=settings)
    arff_train, arff_test = treeliker.run()
    return {'arff': arff_train, 'treeliker': treeliker}


def ilp_hedwig(input_dict):
    import hedwig

    format = input_dict['format']
    ont_format = '.tsv' if format == 'csv' else '.' + format

    examples_file = tempfile.NamedTemporaryFile(suffix='.' + format, delete=False)
    examples_file.write(input_dict['examples'])
    examples_file.close()

    bk_dir = tempfile.mkdtemp()
    for bk in input_dict['bk']:
        f = tempfile.NamedTemporaryFile(suffix=ont_format, delete=False, dir=bk_dir)
        f.write(bk)
        f.close()

    result = hedwig.run({
        'data': examples_file.name,
        'bk_dir': bk_dir,
        'adjust': input_dict['adjust'],
        'FDR': float(input_dict['fdr']),
        'format': format,
        'support': float(input_dict['sup']),
        'learner': input_dict['learner'],
        'depth': int(input_dict['depth']),
        'optimalsubclass': input_dict['optimal'] == "true",
        'beam': int(input_dict['beam']),
        'alpha': float(input_dict['alpha']),
        'score': input_dict['score_fun'],
        'uris': input_dict['uris'],
        'negations': input_dict['negations'] == "true",
        
        # Presets
        'leaves': True,
        'covered': None,
        'target': None,
        'mode': 'subgroups',
        'output': 'foo.txt',
        'verbose': False,
        'nocache': True
    })

    return {'rules': result}


def ilp_cardinalization(input_dict):
    proper = Proper(input_dict,False)
    output_dict = proper.run()
    return output_dict

def ilp_quantiles(input_dict):
    proper = Proper(input_dict,False)
    output_dict = proper.run()
    return output_dict

def ilp_relaggs(input_dict):
    proper = Proper(input_dict,True)
    output_dict = proper.run()
    return output_dict

def ilp_1bc(input_dict):
    onebc = OneBC(input_dict,False)
    output_dict = onebc.run()
    return output_dict

def ilp_1bc2(input_dict):
    onebc = OneBC(input_dict,True)
    output_dict = onebc.run()
    return output_dict

def ilp_tertius(input_dict):
    tertiusInst = Tertius(input_dict)
    output_dict = tertiusInst.run()
    return output_dict

def ilp_multiple_classes_to_one_binary_score(input_dict):
    output_dict = {}
    pos_col = input_dict['pos_col']
    neg_col = input_dict['neg_col']

    
    output_dict['binary_score'] = to_binary_score(input_dict['multiple_classes'],input_dict['pos_col'],input_dict['neg_col'])
    return output_dict

def ilp_caraf(input_dict):
    caraf = Caraf(input_dict)
    output_dict = caraf.run()    
    return output_dict

def to_binary_score(multiple_score,pos_col,neg_col):
    score_lines = multiple_score.strip().split('\n')
    score_arr = [line.split(',') for line in score_lines]
    pos_idx = -1
    neg_idx = -1
    actual = []
    predicted = []
    isLabels = True
    for line in score_arr:
        if isLabels:
            for i, word in enumerate(line):
                if word == pos_col:
                    pos_idx = i
                elif word == neg_col:
                    neg_idx = i
            isLabels = False
        else:
            if pos_idx == -1 or neg_idx == -1:
                raise Exception('Column names not found.')
            if line[1] == pos_col:
                actual.append(1)
                predicted.append(float(line[pos_idx]) - float(line[neg_idx]))
            elif line[1] == neg_col:
                actual.append(0)
                predicted.append(float(line[pos_idx]) - float(line[neg_idx]))

    res = {"name":"Curve", "actual":actual, "predicted":predicted}
    return res

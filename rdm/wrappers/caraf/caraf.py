'''
Created on 15 mars 2016

@author: alain
'''

import tempfile
import os
from subprocess import Popen, PIPE

class Caraf(object):
    def __init__(self,input_dict):
        fct_file = input_dict['fct_file']
        prd_file = input_dict['prd_file']
        tst_file = input_dict['tst_file']    
        cross_validation_folds = input_dict['cross_validation_folds']
        heuristic = input_dict['heuristic']
        forest_size = input_dict['forest_size']
        random_seed = input_dict['random_seed']
        leaf_size = input_dict['leaf_size']
        target_pred = input_dict['target_pred']
        cnt = input_dict['cnt']
        min = input_dict['min']
        max = input_dict['max']
        sum = input_dict['sum']
        mean = input_dict['mean']
        ratio = input_dict['ratio']
        std = input_dict['std']
        median = input_dict['median']
        first_quartile = input_dict['first_quartile']
        third_quartile = input_dict['third_quartile']
        interquartile_range = input_dict['interquartile_range']
        first_decile = input_dict['first_decile']
        ninth_decile = input_dict['ninth_decile']
        self.has_cross_validation = False # Because results files have different names if cross validation is enabled
        
        # Parameters verification        
        try:
            int(input_dict['leaf_size'])
        except ValueError:
            raise Exception('Leaf size should be an integer')
            
        try:
            int(input_dict['forest_size'])
        except ValueError:
            raise Exception('Forest size should be an integer')
        
        self.args_list = ['java', '-Xmx512m', '-jar', 'bin/caraf.jar']
        self.args_list += [fct_file,'-p',prd_file,'-ta',target_pred,'-h',heuristic,'-l',leaf_size,'-f',forest_size]

        try:
            random_seed = int(input_dict['random_seed'])
        except ValueError:
            pass
        else:
            self.args_list += ['-s', random_seed]
    
        # Do cross validation if it exists, else test file, else nothing
        if cross_validation_folds.strip():
            try:
                cross_folds = int(cross_validation_folds)
            except ValueError:
                raise Exception('Cross validation folds should be an integer')
            else:
                if cross_folds >= 2:
                    self.args_list += ['-e','cv',cross_validation_folds]
                    self.has_cross_validation = True
                else:
                    raise Exception('Cross validation folds should be >= 2')
        elif tst_file.strip():
            self.args_list += ['-e','test',tst_file]
        
        # Aggregation functions
        aggs = []
        if cnt == 'true':
            aggs += ['count']
        if min == 'true':
            aggs += ['min']
        if max == 'true':
            aggs += ['max']
        if mean == 'true':
            aggs += ['mean']
        if sum == 'true':
            aggs += ['sum']
        if ratio == 'true':
            aggs += ['ratio']
        if std == 'true':
            aggs += ['std']
        if median == 'true':
            aggs += ['median']
        if first_quartile == 'true':
            aggs += ['quartile1']
        if third_quartile == 'true':
            aggs += ['quartile3']
        if interquartile_range == 'true':
            aggs += ['interquartile']
        if first_decile == 'true':
            aggs += ['decile1']
        if ninth_decile == 'true':
            aggs += ['decile9']
    
        self.args_list += ['-a',','.join(aggs)]
        self.folder_url = '%s/caraf/' % os.path.dirname(fct_file)
        
    def run(self):
        p = Popen(self.args_list,cwd=os.path.dirname(os.path.abspath(__file__)), stdout=PIPE)
        stdout_str, stderr_str = p.communicate()
        output_dict = {}
        
        # Create url of results files
        if self.has_cross_validation:
            eval_url = '%smodel_cv_eval' % self.folder_url
        else:
            eval_url = '%smodel_eval' % self.folder_url
    
        if self.has_cross_validation:
            predictions_url = '%smodel_cv_predictions' % self.folder_url
        else:
            predictions_url = '%smodel_predictions' % self.folder_url
    
        model_url = '%smodel.xml' % self.folder_url

        # Read the results files
        with open(eval_url) as f:
            eval_file = f.read()
        
        with open(predictions_url) as f:
            predictions_file = f.read()
    
        if not self.has_cross_validation:
            with open(model_url) as f:
                model_file = f.read()
        else:
            model_file = None
    
        output_dict['eval_file'] = eval_file
        output_dict['predictions_file'] = predictions_file
        output_dict['model_file'] = model_file
        
        return output_dict

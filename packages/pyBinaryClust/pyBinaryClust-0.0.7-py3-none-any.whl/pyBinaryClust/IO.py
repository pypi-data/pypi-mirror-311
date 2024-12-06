import re
import math
import fcsparser
import numpy as np
import pandas as pd
import seaborn as sns



def examine_data(input_file = None, transform = 'arcsinh', cofactor = 5):
    if input_file is None:
        return 'Please provide a FCS file.'
    
    meta, raw_data = fcsparser.parse(input_file, reformat_meta = True)
    desc = [x for x in raw_data.columns.tolist() if '_' in x]
    markers = [x for x in desc if not re.compile('[Ee]vent_[Ll]ength|[Bb]ead|DNA|[Ll]ive|[Dd]ead|[Vv]iability').search(x)]
    data = raw_data[markers]
    data.columns = [re.sub('[0-9]*[A-z]{1,2}_', '', x) for x in markers]
    
    if transform == 'arcsinh':
        t_data = np.arcsinh(data / 5)
    elif transform == 'none':
        t_data = data
    else:
        print('Custom transformation currently unsupported. Transforming using default method.')
        t_data = np.arcsinh(data / 5)
    
    t_data['Cell'] = t_data.index + 1
    t_data_melt = t_data.melt(id_vars = 'Cell', var_name = 'Marker', value_name = 'Expression')
    g = sns.FacetGrid(t_data_melt, col = 'Marker', col_wrap = math.ceil(math.sqrt(t_data.shape[1])), sharex = False, sharey = False)
    g.map(sns.kdeplot, 'Expression', fill = True)
    g.set_xlabels('Transformed Read Count')
    



def load_data(input_file = None, channels = None, transform = 'arcsinh', cofactor = 5):
    if input_file is None:
        return 'Please provide a FCS file.'
    
    meta, raw_data = fcsparser.parse(input_file, reformat_meta = True)

    desc = [x for x in raw_data.columns.tolist() if '_' in x]
        
    if channels is not None:
        markers = channels
    else:
        markers = [x for x in desc if not re.compile('[Ee]vent_[Ll]ength|[Bb]ead|DNA|[Ll]ive|[Dd]ead|[Vv]iability').search(x)]
        
    data = raw_data[markers]
    data.columns = [re.sub('[0-9]*[A-z]{1,2}_', '', x) for x in markers]

    if transform == 'arcsinh':
        t_data = np.arcsinh(data / 5)
    elif transform == 'none':
        t_data = data
    else:
        print('Custom transformation currently unsupported. Transforming using default method.')
        t_data = np.arcsinh(data / 5)
        
    return t_data
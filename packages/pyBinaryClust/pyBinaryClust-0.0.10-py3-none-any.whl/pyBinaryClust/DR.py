import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.manifold import TSNE
import umap



def run_TSNE(data = None, scale = True, per = 30):
    
    if data is None:
        return 'Please provide data. Use load_data'
    
    np.random.seed(1)
    
    if scale is True:
        to_run = preprocessing.StandardScaler().fit_transform(data)
    elif scale is False:
        to_run = data
    else:
        return 'Please enter True or False for scale'
    
    tsne_results = TSNE(n_components = 2, perplexity = per).fit_transform(to_run)
    tsne_results = pd.DataFrame(tsne_results)
    tsne_results.columns = ['tsne1', 'tsne2']
    
    return tsne_results
    
    

def run_UMAP(data = None, scale = True):
    
    if data is None:
        return 'Please provide data. Use load_data'
    
    np.random.seed(1)
    
    if scale is True:
        to_run = preprocessing.StandardScaler().fit_transform(data)
    elif scale is False:
        to_run = data
    else:
        return 'Please enter True or False for scale'
    
    umap_results = umap.UMAP().fit_transform(to_run)
    umap_results = pd.DataFrame(umap_results)
    umap_results.columns = ['umap1', 'umap2']
    
    return umap_results    


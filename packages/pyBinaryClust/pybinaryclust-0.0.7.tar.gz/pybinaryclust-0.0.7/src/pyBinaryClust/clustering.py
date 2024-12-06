import re
import numpy as np
import pandas as pd
from sklearn import preprocessing as slpreprocessing
from sklearn.cluster import KMeans
import flowsom as fs



def run_kmeans(to_analyse, cutoff_limit = 2.0):
    to_analyse = pd.DataFrame(to_analyse)
    kmeans_results = KMeans(n_clusters = 2).fit(to_analyse)
    pos = str(np.where(kmeans_results.cluster_centers_ == max(kmeans_results.cluster_centers_)[0])[0][0])
    neg = str(np.where(kmeans_results.cluster_centers_ == min(kmeans_results.cluster_centers_)[0])[0][0])
    to_return = pd.DataFrame(kmeans_results.labels_.astype(str))
    
    if min(kmeans_results.cluster_centers_)[0] > cutoff_limit or max(kmeans_results.cluster_centers_)[0] < cutoff_limit or abs(max(kmeans_results.cluster_centers_)[0] - min(kmeans_results.cluster_centers_)[0]) < 1.0 or abs(max(to_analyse.iloc[:,0]) - max(kmeans_results.cluster_centers_)[0]) > cutoff_limit :
        to_return.loc[(to_analyse > cutoff_limit).iloc[:,0].tolist(), 0] = '+'
        to_return.loc[(to_analyse <= cutoff_limit).iloc[:,0].tolist(), 0] = '-'
    else:
        to_return.loc[to_return.iloc[:,0] == pos, 0] = '+'
        to_return.loc[to_return.iloc[:,0] == neg, 0] = '-'
        
    to_return.columns = to_analyse.columns
    return to_return
    


def binary_class(to_analyse, class_file, scale = False):
    binary_matrix = pd.DataFrame(index = range(to_analyse.shape[0]))
    for column in to_analyse.columns:
        binary_matrix = binary_matrix.merge(run_kmeans(to_analyse[column]), left_index = True, right_index = True)

    kmeans_limits = pd.DataFrame(columns = range(3))
    kmeans_limits.columns = ['pos_min', 'Q1', 'Q3']

    for column in binary_matrix.columns:
        if len(binary_matrix[column].unique()) == 1 and binary_matrix[column].unique()[0] == '-':
            pos_min = 999
            Q1 = 0
            Q3 = 0
        else:
            pos_min = to_analyse.loc[binary_matrix[column] == '+',column].min()
            Q1 = to_analyse.loc[binary_matrix[column] == '+',column].quantile(0.25)
            Q3 = to_analyse.loc[binary_matrix[column] == '+',column].quantile(0.75)
        binary_matrix.loc[list(set(to_analyse.index[to_analyse[column] <= Q1]).intersection(binary_matrix.index[binary_matrix[column] == '+'])), column] = 'L'
        binary_matrix.loc[list(set(to_analyse.index[to_analyse[column] > Q1]).intersection(to_analyse.index[to_analyse[column] <= Q3])), column] = 'I'
        binary_matrix.loc[to_analyse[column] > Q3, column] = 'H'
    
    class_results = pd.DataFrame(index = range(to_analyse.shape[0]), columns = range(1))
    class_results.columns = ['Cell Type']
    class_cat = pd.read_csv(class_file, sep = ',', index_col = 0)
    ##### Clean empty spaces from class file
    ##### class.cat <- apply(class.cat, c(1,2), function (x) { gsub(' ', '', x) })
    ##### class.cat[class.cat == ''] <- 'A'
    
    for cell_type in class_cat.index.tolist():
        temp_row = class_cat.loc[cell_type,:][class_cat.loc[cell_type,:] != 'A']
        marker_neg = temp_row.loc[temp_row != '+'].index.tolist()
        marker_pos = temp_row.loc[temp_row == '+'].index.tolist()
        if len(marker_neg) > 0:
            rows_required_neg = binary_matrix[(binary_matrix[marker_neg] == '-').sum(axis = 1) == len(marker_neg)].index
        else:
            rows_required_neg = binary_matrix.index
        if len(marker_pos) > 0:
            rows_required_pos = binary_matrix[(binary_matrix[marker_pos].isin(['L', 'I', 'H'])).sum(axis = 1) == len(marker_pos)].index
        else:
            rows_required_pos = binary_matrix.index
        rows_required = rows_required_pos.intersection(rows_required_neg)
        if len(rows_required) > 0:
            class_results.loc[rows_required, 'Cell Type'] = cell_type
            
    class_results.loc[class_results['Cell Type'].isna(),'Cell Type'] = 'Unclassified'
    
    return class_results



def binary_summary(data = None, binary_results = None):
    if data is None:
        return 'Please provide data. Use load_data'
    if binary_results is None:
        return 'Please provide binary classification results. Use binary_class'
    
    frequencies = pd.DataFrame(binary_results.value_counts())
    frequencies.columns = ['Frequency']
    frequencies['Percentage'] = frequencies['Frequency'] * 100 / frequencies['Frequency'].sum()
    
    to_analyse = data.merge(binary_results, left_index = True, right_index = True)
    medians = to_analyse.groupby('Cell Type').median()
    
    to_return = medians.merge(frequencies, left_on = 'Cell Type', right_on = 'Cell Type')
    to_return = to_return.index.to_frame().merge(to_return, left_index = True, right_index = True).reset_index(drop = True)
    
    return to_return

    

def cluster_subsets(data = None, binary_results = None, method = 'kmeans', n_cluster = 40):
    if data is None:
        return 'Please provide data. Use load_data'
    if binary_results is None:
        return 'Please provide binary classification results. Use binary_class'

    binary_results['Cluster'] = None
    s_data = slpreprocessing.StandardScaler().fit_transform(data)
    
    for cell_type in binary_results.iloc[:,0].unique():
        if method == 'kmeans':
            binary_results = run_kmeans_cluster(s_data, binary_results, cell_type, n_cluster)
        elif method == 'flowsom':
            binary_results = run_FlowSOM_cluster(s_data, binary_results, cell_type, n_cluster)
        else:
            return 'Please choose a valid clustering method - kmeans or FlowSOM'
    
    cluster_results = binary_results
    
    return cluster_results



def run_kmeans_cluster(data, binary_results, cell_type, n_cluster):
    
    data = pd.DataFrame(data)
    data_subset = data.iloc[binary_results[binary_results.iloc[:,0] == cell_type].index,:]
    row_numbers = data_subset.index
    kmeans_nClus = n_cluster
    
    if data_subset.shape[0] == 0:
        return 'There are no cells in the subset ' + cell_type
    elif data_subset.shape[0] < kmeans_nClus:
        dummy_number = 0
        for temp_number in row_numbers:
            binary_results.loc[temp_number, 'Cluster'] = dummy_number
            dummy_number += 1
        print('There are less than ' + kmeans_nClus + ' cells in the subset ' + cell_type + '. No clustering is performed.')
    else:
        kmeans_results = KMeans(n_clusters = kmeans_nClus).fit(data_subset)
        binary_results.loc[row_numbers, 'Cluster'] = kmeans_results.labels_
        
    return binary_results


def run_FlowSOM_cluster(data, binary_results, cell_type, n_cluster):
    
    data = pd.DataFrame(data)
    data_subset = data.iloc[binary_results[binary_results.iloc[:,0] == cell_type].index,:]
    row_numbers = data_subset.index
    fSOM_xdim = 10
    fSOM_ydim = 10
    fSOM_nClus = n_cluster

    if data_subset.shape[0] == 0:
        return 'There are no cells in the subset ' + cell_type
    elif data_subset.shape[0] < 100:
        print('Population is too small: ' + data_subset.shape[0] + ', FlowSOM cannot be run for ' + cell_type + '. K-means is run instead.')
        binary_results = run_kmeans_cluster(s_data, binary_results, cell_type, n_cluster)
    else:
        fsom = fs.FlowSOM(data_subset, xdim = fSOM_xdim, ydim = fSOM_ydim, n_clusters = fSOM_nClus, seed = 1)
        meta = np.array(fsom.get_cell_data().obs['metaclustering'])
        binary_results.loc[row_numbers, 'Cluster'] = meta

    return binary_results



def cluster_summary(data = None, cluster_results = None):
    if data is None:
        return 'Please provide data. Use load_data'
    if cluster_results is None:
        return 'Please provide cluster results. Use cluster_subset'

    combined = data.merge(cluster_results, left_index = True, right_index = True)
    medians = combined.groupby(['Cell Type', 'Cluster']).median()
    
    frequencies = pd.DataFrame(combined[['Cell Type', 'Cluster']].groupby('Cell Type').value_counts())
    frequencies.columns = ['Frequency']
    frequencies['Percentage'] = frequencies['Frequency'] * 100 / frequencies['Frequency'].sum()
    
    to_return = medians.merge(frequencies, left_index = True, right_index = True)
    to_return['Cell Subtype'] = ''
    to_return = to_return.index.to_frame().merge(to_return, left_index = True, right_index = True).reset_index(drop = True)
    
    return to_return


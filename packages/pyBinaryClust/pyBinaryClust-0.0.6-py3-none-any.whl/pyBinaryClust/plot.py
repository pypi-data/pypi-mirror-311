import math
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


def plot_NRS(data = None, xdim = 7, ydim = 5):
    
    if data is None:
        return 'Please provide data (use load_data).'
    
    def calc_NRS(data):
        if data.shape[0] < 3:
            NRS = pd.DataFrame(index = range(data.shape[1]), columns = range(1))
            return NRS
        else:
            pc = PCA().fit(data)
            components = pd.DataFrame(abs(pc.components_))
            components.columns = pc.feature_names_in_
            variance = pd.Series(pc.explained_variance_)
            NRS = pd.DataFrame(components.mul(variance, axis = 0).sum(axis = 0).sort_values(ascending = False))
            return NRS
            
    NRS = calc_NRS(data)
        
    fig, ax = plt.subplots(figsize = (xdim, ydim))
    ax.bar(NRS.index, NRS.loc[:,0])
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 270, ha = 'center')
    ax.set_ylabel('NRS')
    ax.set_title('Non-Redundancy Score')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    
    
    
def plot_binary_abundances(binary_summary = None, remove_unclass = False, xlabel = 'Percentage Abundance', ylabel = '', title = 'Cell Abundances', xdim = 7, ydim = 5):
    if binary_summary is None:
        return 'Please provide binary classification summary (use binary_summary).'
    
    if remove_unclass is False:
        to_plot = binary_summary
    elif remove_unclass is True:
        to_plot = binary_summary[binary_summary['Cell Type'] != 'Unclassified']
    else:
        return 'Please choose True or False for remove_unclass'
    
    fig, ax = plt.subplots(figsize = (xdim, ydim))
    ax.barh(to_plot['Cell Type'], to_plot['Percentage'])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    


def plot_binary_median(binary_summary = None, remove_unclass = False, xlabel = '', ylabel = '', title = 'Median Expressions', xdim = 12, ydim = 4):
    if binary_summary is None:
        return 'Please provide binary classification summary (use binary_summary).'

    if remove_unclass is False:
        to_plot = binary_summary
    elif remove_unclass is True:
        to_plot = binary_summary[binary_summary['Cell Type'] != 'Unclassified']
    else:
        return 'Please choose True or False for remove_unclass'

    to_plot.index = to_plot['Cell Type']
    fig, ax = plt.subplots(figsize = (xdim, ydim))
    sns.heatmap(to_plot.drop(['Frequency', 'Percentage'], axis = 1), square = True, cmap = sns.cubehelix_palette(as_cmap = True))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 270, ha = 'center')
    fig.tight_layout()



def plot_DR(binary_results = None, DR_results = None, title = '', col = 'Cell Type', facet = False, xdim = 5, ydim = 5, remove_unclass = False):
    
    if DR_results.columns[0] == 'tsne1':
        x = 'tsne1'
        y = 'tsne2'
        x_label = 't-SNE 1'
        y_label = 't-SNE 2'
    elif DR_results.columns[0] == 'umap1':
        x = 'umap1'
        y = 'umap2'
        x_label = 'UMAP 1'
        y_label = 'UMAP 2'
    else:
        return 'Please enter valid input'
        
    to_plot = binary_results.merge(DR_results, left_index = True, right_index = True)
    to_plot = to_plot.sort_values(by = col)
    
    if remove_unclass is True:
        to_plot = to_plot[to_plot[col] != 'Unclassified']
    elif remove_unclass is False:
        to_plot = to_plot
    else:
        return 'Please choose True or False for remove_unclass'
    
    
    sns.set_theme(rc={'figure.figsize': (xdim, ydim)})
    sns.set_style("ticks")
    
    if facet == False:
        ax = sns.scatterplot(data = to_plot, x = x, y = y, s = 2, hue = col, palette = 'Spectral')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        sns.despine()
        plt.legend(markerscale = 5)
        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    elif facet == True:
        g = sns.FacetGrid(to_plot, col = col, col_wrap = math.ceil(math.sqrt(len(to_plot[col].unique()))),  hue = col, palette = 'Spectral', sharex = True, sharey = True)
        g.map(sns.scatterplot, x, y, s = 2)
        for ax in g.axes.flatten():
            ax.tick_params(labelbottom = True, labelleft = True)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)



def plot_DR_marker(data = None, DR_results = None, marker = None, title = None, lower = None, upper = None, xdim = 5.5, ydim = 5, palette = 'Purples'):
    
    if data is None:
        return 'Please provide data (use load_data).'
    if DR_results is None:
        return 'Please provide dimensionality reduction results (use run_TSNE or run_UMAP).'
    if title is None:
        plot_title = marker
    if marker is None:
        return 'Please specify a marker to plot.'
    if lower is None:
        lower_limit = math.floor(data[marker].min())
    else:
        lower_limit = lower
    if upper is None:
        upper_limit = math.ceil(data[marker].max())
    else:
        upper_limit = upper  
  
    if DR_results.columns[0] == 'tsne1':
        x = 'tsne1'
        y = 'tsne2'
        x_label = 't-SNE 1'
        y_label = 't-SNE 2'
    elif DR_results.columns[0] == 'umap1':
        x = 'umap1'
        y = 'umap2'
        x_label = 'UMAP 1'
        y_label = 'UMAP 2'
    else:
        return 'Please enter valid input'
    
    to_plot = data.merge(DR_results, left_index = True, right_index = True)
    
    fig, ax = plt.subplots(figsize = (xdim, ydim))
    plot = ax.scatter(to_plot[x], to_plot[y] , s = 1.5, c = to_plot[marker], cmap = palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(plot_title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.colorbar(plot)
    fig.tight_layout()
    
    

def plot_cluster_heatmap(data = None, cluster_results = None, cell_type = None, xdim = 14, ydim = 13):
    
    if data is None:
        return 'Please provide data. Use load_data'
    if cluster_results is None:
        return 'Please provide cluster results. Use cluster_subset'
    if cell_type is None:
        return 'Please choose the cell type to plot.'
    
    combined = data.merge(cluster_results, left_index = True, right_index = True)
    medians = combined.groupby(['Cell Type', 'Cluster']).median()
    
    frequencies = pd.DataFrame(combined[['Cell Type', 'Cluster']].groupby('Cell Type').value_counts())
    frequencies.columns = ['Frequency']
    frequencies['Percentage'] = frequencies['Frequency'] * 100 / frequencies['Frequency'].sum()
    
    to_plot = medians.merge(frequencies, left_index = True, right_index = True)
    to_plot = to_plot.index.to_frame().merge(to_plot, left_index = True, right_index = True).reset_index(drop = True)
    to_plot = to_plot[to_plot['Cell Type'] == cell_type].drop(['Cell Type', 'Frequency'], axis = 1).reset_index(drop = True)
    
    to_clust = to_plot.drop(['Cluster', 'Percentage'], axis = 1)
    Z1 = hierarchy.linkage(to_clust, 'ward')
    Z2 = hierarchy.linkage(to_clust.T, 'ward')
        
    for_barplot = to_plot[['Cluster', 'Percentage']]
    for_barplot.index = for_barplot['Cluster']
    for_barplot = for_barplot.iloc[hierarchy.leaves_list(Z1),:]
    for_heatmap = to_clust.iloc[hierarchy.leaves_list(Z1), hierarchy.leaves_list(Z2)].T
    
    plt.style.use('default')
    fig, axs = plt.subplots(4, 2, figsize = (xdim, ydim), sharex = False, sharey = False, gridspec_kw = dict(height_ratios = [1, 1, 7.9, 0.1], width_ratios = [1, 9]))
    
    plot01 = hierarchy.dendrogram(Z1, orientation= 'top', labels = to_clust.index, color_threshold = 0, above_threshold_color = '#000000', ax = axs[0, 1])
    axs[0,1].spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    axs[0,1].xaxis.set_visible(False)
    axs[0,1].yaxis.set_visible(False)
    
    plot11 = sns.barplot(for_barplot, x = 'Cluster', y = 'Percentage', order = for_barplot['Cluster'], ax = axs[1, 1])
    axs[1,1].spines[['top', 'right']].set_visible(False)
    axs[1,1].set_xlabel('Cluster')
    axs[1,1].set_ylabel('Percentage\nAbundance (%)')
    
    plot20 = hierarchy.dendrogram(Z2, orientation= 'left', labels = to_clust.columns, distance_sort = 'descending', color_threshold = 0, above_threshold_color = '#000000', ax = axs[2, 0])
    axs[2,0].spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    axs[2,0].xaxis.set_visible(False)
    axs[2,0].yaxis.set_visible(False)
    
    plot21 = sns.heatmap(for_heatmap, square = False, xticklabels = True, yticklabels = True, cmap = 'vlag', cbar = True, cbar_ax = axs[3, 1], cbar_kws = dict(orientation = "horizontal", label = 'Median Expression'), ax = axs[2, 1])
    axs[0,0].set_visible(False)
    axs[1,0].set_visible(False)
    axs[3,0].set_visible(False)
    
    fig.tight_layout()
    
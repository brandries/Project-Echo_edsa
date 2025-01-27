# Clustering of timeseries data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import RobustScaler, StandardScaler
import hdbscan
from src.models.dynamic_time_warping import *

class DataPreprocess(object):
    def __init__(self):
        pass

    def read_data(self, sku_labels, features):
        print('Reading in the data...')
        self.labels = pd.read_csv(sku_labels)
        self.features = pd.read_csv(features)
        self.features.dropna(axis=1, inplace=True)
        return self.labels, self.features

    def scale_data(self, df, scaler):
        scale = scaler
        skus = df['id']
        df.set_index('id', inplace=True)
        X = scale.fit_transform(df)
        return X


class DimensionalityReduction(object):
    def __init__(self):
        pass

    def run_dimred(self, features, dimred):
        print('Running Dimentionality Reduction...')
        projection = dimred.fit_transform(features)
        return projection


class Clustering(object):
    def __init__(self):
        pass

    def cluster(self, dimred, clustering_algo):
        print('Clustering...')
        clusters_fit = clustering_algo.fit_predict(dimred[[0,1]])
        return clusters_fit


def main():
    dp = DataPreprocess()
    subset = 'none'
    df = pd.read_csv('extracted_features.csv')
    df.set_index('id', inplace=True)
    df.dropna(axis=1, inplace=True)
    pp = Preprocessing()
    feat = pd.read_csv('aggregate_products.csv')
    pivot = pp.pivot_table(feat)
    sorted = pp.sort_nas(pivot)
    pivot_nans, nans, pivot_no_nans, no_nans = pp.split_nans(sorted, df)
    scaler = StandardScaler()
    if subset == 'nan':
        use_df = nans
    elif subset == 'no_nans':
        use_df = no_nans
    elif subset == 'none':
        use_df = df
    print('There are {} samples'.format(len(use_df)))
    X = scaler.fit_transform(use_df)
    dr = DimensionalityReduction()
    tsne = umap.UMAP(n_neighbors = 2, min_dist=0.0, n_components=10)
    tsne = dr.run_dimred(X, tsne)
    plot_df = pd.DataFrame(tsne).join(df.reset_index())
    cl = Clustering()
    clus_algo = hdbscan.HDBSCAN(min_cluster_size=50)
    clusters_fit = cl.cluster(plot_df, clus_algo)
    tsne_cluster = plot_df.join(pd.DataFrame(clusters_fit), rsuffix='clus')
    tsne_cluster.rename(columns={'0':'tsne1', 1:'tsne2', '0clus':'cluster'},
                        inplace=True)

    print('Outputting...')
    out_df = tsne_cluster[['id', 'cluster']]
    out_df.to_csv('tsne_clusters.csv', index=False)

if __name__ == '__main__':
    main()

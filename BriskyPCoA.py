import pandas as pd
import numpy as np
import os
from skbio.stats.ordination import pcoa
from scipy.spatial.distance import pdist, squareform
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--abundance', type=str, default='./data/abundance.csv', help='Abundance data, entries represent taxas and columns represent samples')
    parser.add_argument('-l', '--lables', type=str, default='./data/metadata.csv', help='Labels of samples, first column represent SampleID and second column represent labels')
    parser.add_argument('-d', '--distance', type=str, default='jensenshannon', help='Optional distance')
    parser.add_argument('-o', '--output', type=str, default='./visulizing_result', help='Output path of visulizing result')
    args = parser.parse_args()
    
    print('Loading data...')
    abundanceData = pd.read_csv(args.abundance, index_col=0)
    metaData = pd.read_csv(args.lables, index_col=0)
    abundanceData = abundanceData[metaData.index.values.tolist()].T
    
    print('Calculating...')
    distanceMatrix = squareform(pdist(abundanceData, args.distance))
    distancePCoA = pd.DataFrame(pcoa(distanceMatrix, number_of_dimensions=2).samples.values.tolist(), index=metaData.index, columns=['PC1', 'PC2'])
    distancePCoA['labels'] = metaData
    
    print('Visilizing result using seaborn')
    plotPCoA = sns.displot(data=distancePCoA, x='PC1', y='PC2', hue='labels')
    plt.legend(title='')
    
    print(f'Done, saving result into {args.output}')
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    
    plt.savefig(f'{args.output}/scatter_plot.jpg')
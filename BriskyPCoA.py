import pandas as pd
import numpy as np
import os
from skbio.stats.ordination import pcoa
from scipy.spatial.distance import pdist, squareform
import argparse
from plotnine import*
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--abundance', type=str, default='./data/abundance.csv', help='Abundance data, entries represent taxas and columns represent samples')
    parser.add_argument('-l', '--lables', type=str, default='./data/metadata.csv', help='Labels of samples, first column represent SampleID and second column represent labels')
    parser.add_argument('-m', '--mode', type=str, default='PCA', help='Choose the analyse mode, PCA & PCoA are available')
    parser.add_argument('-d', '--distance', type=str, default='jensenshannon', help='Optional distance metric for pcoa')
    parser.add_argument('-o', '--output', type=str, default='./visulizing_result', help='Output path of visulizing result')
    args = parser.parse_args()
    
    print('Loading data...')
    abundanceData = pd.read_csv(args.abundance, index_col=0)
    metaData = pd.read_csv(args.lables, index_col=0)
    abundanceData = abundanceData[metaData.index.values.tolist()].T
    
    print('Calculating...')
    if args.mode == 'PCoA':
        distanceMatrix = squareform(pdist(abundanceData, args.distance))
        distancePlt = pd.DataFrame(pcoa(distanceMatrix, number_of_dimensions=2).samples.values.tolist(), index=metaData.index, columns=['PC1', 'PC2'])
    else:
        pca = PCA(n_components=2)
        distancePlt = pd.DataFrame(data = pca.fit_transform(abundanceData), columns=['PC1', 'PC2'])
    distancePlt['labels'] = metaData.values
    
    print('Visilizing result using plotnine')
    # Customize your plot below.
    plotPCoA = (ggplot(distancePlt, aes('PC1', 'PC2', color='labels', fill='labels'))+
                    geom_point(size=2)+
                    stat_ellipse(geom = "polygon", alpha = 0.1)+
                    theme_bw()+
                    theme(axis_line = element_line(color="gray", size = 2))+
                    theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())+
                    theme(figure_size=(10, 10))+
                    theme(legend_position = (0.8,0.8))+
                    theme(text=element_text(size=20)))
    
    print(f'Done, saving result into {args.output}')
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    
    plotPCoA.save(f'{args.output}/plot_result.jpg')
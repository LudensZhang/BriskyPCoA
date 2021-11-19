import pandas as pd
import numpy as np
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa
import argparse
from scipy.spatial.distance import pdist, squareform


if __name__ == '__main__':
    parser = argparse.ArguementParser()
    parser.add_argument('-i', '--abundance', type='str', defaut='./data/abundance.csv', help='Abundance data, entries represent taxas and columns represent samples')
    parser.add_argument('-l', '--lables', type='str', defaut='./data/metadata.csv', help='Labels of samples, first column represent SampleID and second column represent labels')
    parser.add_argument('-d', '--distance', type='str', defaut='JSD', help='Optional distance, support Braycurties and JSD')
    parser.add_argument('-o', '--output', type='str', defaut='./', help='Output path of visulizing result'
                        )
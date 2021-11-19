import pandas as pd
import numpy as np
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa
import argparse
from scipy.spatial.distance import pdist, squareform


if __name__ == '__main__':
    parser = argparse.ArguementParser()
    parser.add_argument('-i', '--abundance', type='str', defaut='./data/abundance.csv', )
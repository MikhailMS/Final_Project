# Import packages
import time, re, collections, ebooklib, pickle, multiprocessing
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import numpy as np

# Import modules
from utils import *
from text_analysis_module import plot_features

# Main class
text_module_name = 'text_analysis_module'
module_name = 'mapping_module'

def loadTextFeatures():
    """Loads extracted text features"""
    text_features_files = [f for f in listdir("./{}/".format(text_module_name)) if (isfile(join("./{}".format(text_module_name), f)) and ("extracted_features" in f))]

    if text_features_files:
        print '\n===' + turquoise + ' TEXT FEATURES FOUND... ' + "./{}/{}".format(text_module_name, text_features_files[0]) + '==='
        print '\n===' + turquoise + ' LOADING FEATURES... ' + normal + '==='
        features = pickle.load(open("./{}/{}".format(text_module_name, text_features_files[0]), 'rb'))
        features = [x for sublist in features for x in sublist]  # Flat into 1D List
        print '\n===' + turquoise + ' FEATURES DATA SET LENGTH: {} '.format(len(features)) + normal + '==='
        print '\n===' + turquoise + ' LOAD IS COMPLETED! ' + normal + '==='
        return features
    else:
        print '\n===' + red + ' TEXT FEATURES NOT FOUND! ' + normal + '==='
        return None

def median(data):
    """Returns a medians for given data set"""
    if data:
        median = list()
        for entry in data:
            temp = np.asarray(entry)
            median.append(np.median(temp))
        return median
    else:
        print '\n===' + red + ' NO DATA GIVEN! ' + normal + '==='

def split_list(data_list, N):
    """Splits data_list into groups of size N"""
    return [data_list[i:i + N] for i in xrange(0, len(data_list), N)]

def map_sentiment(entry):
    """Takes a data entry of sentiment scores and produces a value:
    1 - for positive, -1 -  for negative. Output value is used for music composition"""
    if entry>0:
        return 1
    else:
        return -1

def map_readability(entry):
    """Takes a data entry of readability scores and produces a value:
    from 1 to 7, where 1 - low complexity and 7 - greatest. Output value is used for music composition"""
    if entry>=13:
        return 7
    if entry>=11:
        return 6
    if entry>=9:
        return 5
    if entry>=7:
        return 4
    if entry>=5:
        return 3
    if entry>=3:
        return 2
    if entry>=1:
        return 1
    else:
        return -1

def map_lex_density(entry):
    """Takes a data entry of lexical density scores and produces a value:
    from 1 to 4, where 1 - low density and 7 - greatest. Output value is used for music composition"""
    if entry>=75:
        return 4
    if entry>=50:
        return 3
    if entry>=25:
        return 2
    if entry>=0:
        return 1
    else:
        return -1

def map_text_parameters(group_size=5, visual=False):
    """Maps text features with music parameters, so later would be sent to
    music composition function in order to generate music pieces, that represent
    text features.
    'group_size' defines the sample for which median is computed (smoothing results)
    If 'visual'=True, than it would show graphs for computed features
    """
    N = group_size # number of elements in groups
    features = loadTextFeatures()

    # Extract features from saved data set
    sent_score = list([x[0] for x in features])  # List of all sentiment scores
    lex_score = list([x[1][0] for x in features])  # List of all lexical density scores
    read_score = list([x[1][1] for x in features]) # List of all readability scores

    # Split initial lists in lists with groups of size N, to calculate medians
    sent_score = split_list(sent_score, N)
    lex_score = split_list(lex_score, N)
    read_score = split_list(read_score, N)

    # Calculate medians
    sent_score_median = median(sent_score)
    lex_score_median = median(lex_score)
    read_score_median = median(read_score)


    # Map features
    sent_score_mapped = map(map_sentiment, sent_score_median)
    lex_score_mapped = map(map_lex_density, lex_score_median)
    read_score_mapped = map(map_readability, read_score_median)

    # Save results into files
    pickle.dump(sent_score_mapped, open('./{}/{}'.format(module_name, 'sentiment_mapped.p'), "wb"))
    pickle.dump(lex_score_mapped, open('./{}/{}'.format(module_name, 'lexical_mapped.p'), "wb"))
    pickle.dump(read_score_mapped, open('./{}/{}'.format(module_name, 'readability_mapped.p'), "wb"))

    # Plot graphs for computed features if requested
    if visual:
        plot_features(sent_score_median, lex_score_median, read_score_median, label='median value') # medians visualisation
        plot_features(sent_score_mapped, lex_score_mapped, read_score_mapped, label='mapped value') # mapped features visualisation

    return sent_score_mapped, lex_score_mapped, read_score_mapped

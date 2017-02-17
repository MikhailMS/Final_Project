# Import packages
import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

# Import modules
from utils import *
from text_analysis import module_name

# Main class
def plot_graphs(sent_score, lex_score, read_score, length, label=''):
    """Helper function to avoid repeated code"""
    plt.rcParams["figure.figsize"] = 30, 8

    plt.scatter(xrange(length), sent_score, s=10, c='c')
    plt.plot(xrange(length), sent_score, c='c')
    plt.grid()
    plt.xlabel('Sample index')
    plt.ylabel('Sentiment score {}'.format(label))
    plt.show()

    plt.scatter(xrange(length), lex_score, s=10, c='r')
    plt.plot(xrange(length), lex_score, c='r')
    plt.grid()
    plt.xlabel('Sample index')
    plt.ylabel('Lexical density score {}'.format(label))
    plt.show()

    plt.scatter(xrange(length), read_score, s=10, c='r')
    plt.plot(xrange(length), read_score, c='r')
    plt.grid()
    plt.xlabel('Sample index')
    plt.ylabel('Readability score {}'.format(label))
    plt.show()

def plot_features(sent_score=None, lex_score=None, read_score=None, label=''):
    """Visualisation function - plots graphs for sentiment, lexical density and
    readability scores"""

    # Find file that holds extracted features
    dump_results = [f for f in listdir("./{}/".format(module_name)) if (isfile(join("./{}/".format(module_name), f)) and ("extracted_features" in f))]

    # If data was passed to function then use it, otherwise
    if (sent_score is not None) and (lex_score is not None) and (read_score is not None):
        length = len(sent_score) # It doesn't matter which list's length to take
        plot_graphs(sent_score, lex_score, read_score, length, label)

    # If file with extracted features exists, then load file and plot features
    elif dump_results:
        print '\n===' + turquoise + ' PREVIOUS RESULTS FOUND... ' + normal + dump_results[0] + '==='
        print '\n===' + turquoise + ' LOADING RESULTS...' + normal + '==='
        results = pickle.load(open('./{}/{}'.format(module_name, dump_results[0]), 'rb'))
        print '\n===' + turquoise + ' LOAD IS COMPLETED!' + normal + '==='
        results = [x for sublist in results for x in sublist]  # Flat results into 1D List

        print 'Results length: ', len(results)

        y_sent = list([x[0] for x in results])  # List of all sentiment scores
        y_lex = list([x[1][0] for x in results])  # List of all lexical density scores
        y_read = list([x[1][1] for x in results])  # List of all readability scores

        length = len(results)
        plot_graphs(y_sent, y_lex, y_read, length, label)

    # Otherwise
    else:
        print '\n===' + red + 'NO DATA FOUND' + normal + '==='

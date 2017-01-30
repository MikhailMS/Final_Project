import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

# Font effects for console/terminal output
red = "\x1b[1;31m"
turquoise = "\x1b[1;36m"
normal = "\x1b[0m"


def plot_features():
    # Find file that holds extracted features
    dump_results = [f for f in listdir(".") if (isfile(join(".", f)) and ("extracted_features" in f))]

    # If such file exists, then load file and return features
    if dump_results:
        print '\n===' + turquoise + ' PREVIOUS RESULTS FOUND... ' + normal + dump_results[0] + '==='
        print '\n===' + turquoise + ' LOADING RESULTS...' + normal + '==='
        results = pickle.load(open(dump_results[0], 'rb'))
        print '\n===' + turquoise + ' LOAD IS COMPLETED!' + normal + '==='
        results = [x for sublist in results for x in sublist]  # Flat results into 1D List

        print 'Results length: ', len(results)

        y_sent = list([x[0] for x in results])  # List of all sentiment scores
        y_lex = list([x[1][0] for x in results])  # List of all lexical density scores
        y_read = list([x[1][1] for x in results])  # List of all readability scores

        plt.rcParams["figure.figsize"] = 30, 8

        plt.scatter(xrange(len(results)), y_sent, s=10, c='c')
        plt.plot(xrange(len(results)), y_sent, c='c')
        plt.grid()
        plt.xlabel('Sample index')
        plt.ylabel('Sentiment score')
        plt.show()

        plt.scatter(xrange(len(results)), y_lex, s=10, c='r')
        plt.plot(xrange(len(results)), y_lex, c='r')
        plt.grid()
        plt.xlabel('Sample index')
        plt.ylabel('Lexical density score')
        plt.show()

        plt.scatter(xrange(len(results)), y_read, s=10, c='r')
        plt.plot(xrange(len(results)), y_read, c='r')
        plt.grid()
        plt.xlabel('Sample index')
        plt.ylabel('Readability score')
        plt.show()

    # Otherwise
    else:
        print '\n===' + red + 'NO DATA FOUND' + normal + '==='


plot_features()

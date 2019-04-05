# Import packages
import cPickle as pickle
import music21
# import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

# Import modules
from utils import *
from constants import *

# Main class
def compute_complexity_stats(folders):
    """Computes stats which may help to identify complexity of music piece
    Hypothesis is that simplier music would have more single notes and fewer chords
    and more complex music would have less single notes and more complex chords (3 and more notes)
    """
    if folders:
        folders = set(folders) # This is redundant, but nice to see analysis being done in order
        for iter,folder in enumerate(folders):
            results = list()
            print '[+]' + green + ' Analysing {} files '.format(folder) + normal + '[+]'
            available_files = [f for f in listdir("./{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder)) if (isfile(join("./{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder), f)) and (".mid" in f))]
            for music in available_files:
                name = music[:-4]
                print 'Computing stats for {}'.format(music)
                try:
                    score = music21.converter.parse("./{}/{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder, music))

                    single_notes   = 0
                    total_notes    = 0
                    simple_chords  = 0
                    complex_chords = 0

                    for note in score.recurse().getElementsByClass('Note'):
                        single_notes += 1
                        total_notes  += 1
                    for chord in score.recurse().getElementsByClass('Chord'):
                        if len(chord.pitches) < 3:
                            simple_chords += 1
                            total_notes   += len(chord.pitches)
                        if len(chord.pitches) >= 3:
                            complex_chords += 1
                            total_notes    += len(chord.pitches)
                    total_elem_played = single_notes + simple_chords + complex_chords
                    n_bars            = total_elem_played/4.0 # Redundant - 4.0 is a number of elements played in a single bar, since music size is 4/4
                    notes_p_bar       = total_notes/n_bars    # Redundant

                    results.append([single_notes, total_notes, simple_chords, complex_chords, notes_p_bar, total_elem_played])
                except:
                    print '{} has been ignored'.format(music)
            print '[!!]' + green + ' Saving results to ./{}/{}/complexity_stats_{}.p '.format(MODULE_NAME, RESULTS_DIR, int(folder[-1])) + normal + '[!!]'
            pickle.dump(results,open('./{}/{}/complexity_stats_{}.p'.format(MODULE_NAME, RESULTS_DIR, int(folder[-1])), 'wb'))
    else:
        print '[!!]'+ red + 'No subfolders found!' + normal + '[!!]'
    print '[+]' + green + ' Complexity analysis is completed ' + normal + '[+]'

def get_complexity_stats():
    """Higher level function that runs complexity stats computation"""
    stats_saved = [f for f in listdir("./{}/{}/".format(MODULE_NAME, RESULTS_DIR)) if isfile(join("./{}/{}".format(MODULE_NAME, RESULTS_DIR), f)) and ("complexity_stats" in f)]
    music_folders = [f for f in listdir("./{}/{}/".format(MODULE_NAME, MUSIC_DIR)) if not isfile(join("./{}/{}".format(MODULE_NAME, MUSIC_DIR), f)) and ("level" in f)]

    if stats_saved:
        folders_to_analyse = music_folders[:]
        folders_been_analysed = [f for f in music_folders for stats in stats_saved if f[-1] in stats[-3]]
        for item in folders_been_analysed:
            folders_to_analyse.remove(item)

        if len(music_folders)==len(folders_been_analysed):
            print '[+]' + green + ' All data has been analysed. Loading results... ' + normal + '[+]\n'
        else:
            print '[+]' + green + ' Previous results found. Analysing from stop point... {} '.format(folders_to_analyse[0]) + normal + '[+]\n'
            compute_complexity_stats(folders_to_analyse)

    else:
        print '[+]' + green + ' No previous results found. Starting from beggining... ' + normal + '[+]\n'
        compute_complexity_stats(music_folders)
        print '[+]' + green + ' Getting results ready... ' + normal + '[+]\n'

def get_n_plot_complexity_stats(visual):
    """Plots graphs for complexity stats"""
    complexity_stats_files = [f for f in listdir("./{}/{}/".format(MODULE_NAME, RESULTS_DIR)) if isfile(join("./{}/{}".format(MODULE_NAME, RESULTS_DIR), f)) and ("complexity_stats" in f)]

    simple_stats = list()
    print '\n[+]' + green + ' Computing simple stats ' + normal + '[+]'
    for iter,f in enumerate(complexity_stats_files):

        all_stats = pickle.load(open('./{}/{}/{}'.format(MODULE_NAME, RESULTS_DIR, f), 'rb'))
        all_stats = np.asarray(all_stats)
        print '\nLength of Level {} is {}'.format(iter+1, len(all_stats))

        mins  = all_stats[:,[0,2,3,5]].min(0)  # Get minimum values
        maxes = all_stats[:,[0,2,3,5]].max(0)  # Get maximum values
        means = all_stats[:,[0,2,3,5]].mean(0) # Get mean values
        std   = all_stats[:,[0,2,3,5]].std(0)  # Get standard deviation values
        print 'Level {}, means {}'.format(iter+1, means)
        simple_stats.append(means)

        if visual:
            plt.subplot(3,2,iter+1)
            plt.title('Level {} stats'.format(iter+1))
            # Initialize stacked errorbars:
            plt.errorbar(np.arange(4), means, std, fmt='ok', lw=3, markersize='5')
            plt.errorbar(np.arange(4), means, [means - mins, maxes - means], fmt='.k',
                         ecolor='blue', lw=1, markersize='5')
            plt.xlim(-1, 4)
            plt.grid()

    if visual:
        plt.show()

    complex_stats = list()
    print '\n[+]' + green + ' Computing complex stats ' + normal + '[+]\n'
    for iter,f in enumerate(complexity_stats_files):
        results = list()

        all_stats = pickle.load(open('./{}/{}/{}'.format(MODULE_NAME, RESULTS_DIR, f), 'rb'))
        all_stats = np.asarray(all_stats)

        single_notes_per_total_elem   = list(map(dist_helper, all_stats[:,0], all_stats[:,5]))
        simple_chords_per_total_elem  = list(map(dist_helper, all_stats[:,2], all_stats[:,5]))
        complex_chords_per_total_elem = list(map(dist_helper, all_stats[:,3], all_stats[:,5]))

        results.append(single_notes_per_total_elem)
        results.append(simple_chords_per_total_elem)
        results.append(complex_chords_per_total_elem)
        results = np.asarray(results)
        results = results.T

        mins  = results.min(0)  # Get minimum values
        maxes = results.max(0)  # Get maximum values
        means = results.mean(0) # Get mean values
        std   = results.std(0)  # Get standard deviation values
        print 'Level {}, means {}'.format(iter+1, means, mins)
        complex_stats.append(means) # Save means for identification of complexity of generated music

        if visual:
            plt.subplot(3,2,iter+1)
            plt.title('Level {} complex stats'.format(iter+1))
            # Initialize stacked errorbars:
            plt.errorbar(np.arange(3), means, std, fmt='ok', lw=3, markersize='5')
            plt.errorbar(np.arange(3), means, [means - mins, maxes - means], fmt='.k',
                         ecolor='gray', lw=1, markersize='5')
            plt.xlim(-1, 3)
            plt.grid()

    if visual:
        plt.show()

    stats = np.hstack((simple_stats, complex_stats))
    return stats

def dist_helper(x,y):
    """Returns percentage"""
    return x/float(y)*100

def run_complexity_analysis(visual=True):
    """Runs computation of music complexity stats and then plot distribution graphs for each complexity level (enabled by default)
    First set of graphs is simple:
      First column:  distribution of single notes played at given level (naive)
      Second column: distribution of simple chords played at given level (naive)
      Third column:  distribution of complex chords played at given level (naive)
      Fourth column: distribution of total played elements at given level (naive)

    Second set of graphs is a bit more complicated:
      First column:  distribution of (single_notes/total_played_elements) at given level
      Second column: distribution of (simple_chords/total_played_elements) at given level
      Third column:  distribution of (complex_chords/total_played_elements) at given level
    """
    get_complexity_stats()
    stats = get_n_plot_complexity_stats(visual)
    print np.shape(stats)
    return stats

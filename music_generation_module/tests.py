# Import packages
import music21
import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# Import modules
from utils import *
from constants import *

# Tests go here
def compare_composed_key_n_requested(sent_score_mapped):
    """Compares requested tonic key with composed tonic key to ensure that
    LSTM model generates correct output.
    sent_score_mapped - sentiment score received after if was mapped onto tonic key value range
    """
    given_scores = sent_score_mapped
    counter = 0
    print '[+]' + green + ' Analysing tonic key of {} files '.format(RESULTS_DIR) + normal + '[+]'

    for iter, _ in enumerate(sent_score_mapped):
        music = '{}.mid'.format(iter)
        try:
            score = music21.converter.parse("./{}/{}/{}".format(MODULE_NAME, RESULTS_DIR, music))
            key = score.analyze('key')
            print '{} is in {} key'.format(music, key.mode)
            result = 1 if key.mode=='major' else 0
            #print "Key, that's required by mapped sentiment: {}; Key, that's been composed by LSTM model: {}".format(given_scores[iter], result)

            if result==given_scores[iter]:
                counter += 1
        except:
            print '{} has been ignored'.format(music)
    print 'Percentage of correctly composed music pieces (Tonic key) : {}\n'.format((counter/float(len(given_scores)))*100)

def compare_composed_complexity_n_requested(read_score_mapped, complexity_stats):
    """Compares requested music complexity with composed complexity to ensure that
    LSTM model generates correct output.
    read_score_mapped - readability score received after if was mapped onto music complexity value range
    """
    given_scores = read_score_mapped
    counter = 0
    print '\n[+]' + green + ' Analysing complexity of {} files '.format(RESULTS_DIR) + normal + '[+]'

    for iter, _ in enumerate(read_score_mapped):
        # Compute complexity of generated music piece
        music = '{}.mid'.format(iter)
        print 'Computing stats for {}'.format(music)
        try:
            score = music21.converter.parse("./{}/{}/{}".format(MODULE_NAME, RESULTS_DIR, music))

            single_notes = 0
            total_notes = 0
            simple_chords = 0
            complex_chords = 0

            for note in score.recurse().getElementsByClass('Note'):
                single_notes += 1
                total_notes += 1
            for chord in score.recurse().getElementsByClass('Chord'):
                if len(chord.pitches) < 3:
                    simple_chords += 1
                    total_notes += len(chord.pitches)
                if len(chord.pitches) >= 3:
                    complex_chords += 1
                    total_notes += len(chord.pitches)
            total_elem_played = single_notes + simple_chords + complex_chords

            s_notes_per_total_elem = single_notes/float(total_elem_played)*100
            s_chords_per_total_elem = simple_chords/float(total_elem_played)*100
            c_chords_per_total_elem = complex_chords/float(total_elem_played)*100

            piece_complexity = np.array([single_notes, simple_chords, complex_chords, total_elem_played,
                                         s_notes_per_total_elem, s_chords_per_total_elem, c_chords_per_total_elem])
            complexity_mask = complexity_stats # Complexity computed from initialy given labels

            pred_cosine_complexity_mixed = np.argmax(cosine_similarity(piece_complexity.reshape(1, -1), complexity_mask))+1 # Calculate the closest complexity group for generated piece
            pred_euc_complexity_mixed    = np.argmax(euclidean_distances(piece_complexity.reshape(1, -1), complexity_mask))+1 # Calculate the closest complexity group for generated piece
            pred_cosine_complexity_compl = np.argmax(cosine_similarity(piece_complexity[-3:].reshape(1, -1), complexity_mask[:,-3:]))+1 # Calculate the closest complexity group for generated piece
            pred_euc_complexity_compl    = np.argmax(euclidean_distances(piece_complexity[-3:].reshape(1, -1), complexity_mask[:,-3:]))+1 # Calculate the closest complexity group for generated piece

            #print "Initial complexity label {}; Complexity, that's been predicted by computed complexity mask {}".format(int(folder[-1]), pred_cosine_complexity, pred_euc_complexity)

            if (pred_cosine_complexity_mixed==given_scores[iter]) or (pred_euc_complexity_mixed==given_scores[iter]) or (pred_cosine_complexity_compl==given_scores[iter]) or (pred_euc_complexity_compl==given_scores[iter]):
                counter += 1
        except:
            print '{} has been ignored'.format(music)
    print 'Percentage of correctly composed music pieces (Complexity) : {}'.format((counter/float(len(given_scores)))*100)

def compare_init_labels_n_complexity_mask(complexity_stats):
    """Checks how well complexity mask preforms on initial music complexity lables"""
    music_folders = [f for f in listdir("./{}/{}/".format(MODULE_NAME, MUSIC_DIR)) if not isfile(join("./{}/{}".format(MODULE_NAME, MUSIC_DIR), f)) and ("level" in f)]

    for iter, folder in enumerate(music_folders):
        available_files = [f for f in listdir("./{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder)) if (isfile(join("./{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder), f)) and (".mid" in f))]
        counter = 0
        print '\n[+]' + green + ' Analysing {} files '.format(folder) + normal + '[+]\n'
        for music in available_files:
            name = music[:-4]
            print 'Computing stats for {}'.format(music)
            try:
                score = music21.converter.parse("./{}/{}/{}/{}".format(MODULE_NAME, MUSIC_DIR, folder, music))

                single_notes = 0
                total_notes = 0
                simple_chords = 0
                complex_chords = 0

                for note in score.recurse().getElementsByClass('Note'):
                    single_notes += 1
                    total_notes += 1
                for chord in score.recurse().getElementsByClass('Chord'):
                    if len(chord.pitches) < 3:
                        simple_chords += 1
                        total_notes += len(chord.pitches)
                    if len(chord.pitches) >= 3:
                        complex_chords += 1
                        total_notes += len(chord.pitches)
                total_elem_played = single_notes + simple_chords + complex_chords

                s_notes_per_total_elem = single_notes/float(total_elem_played)*100
                s_chords_per_total_elem = simple_chords/float(total_elem_played)*100
                c_chords_per_total_elem = complex_chords/float(total_elem_played)*100

                piece_complexity = np.array([single_notes, simple_chords, complex_chords, total_elem_played,
                                             s_notes_per_total_elem, s_chords_per_total_elem, c_chords_per_total_elem])
                complexity_mask = complexity_stats # Complexity computed from initialy given labels

                pred_cosine_complexity_mixed = np.argmax(cosine_similarity(piece_complexity.reshape(1, -1), complexity_mask))+1 # Calculate the closest complexity group for generated piece
                pred_euc_complexity_mixed = np.argmax(euclidean_distances(piece_complexity.reshape(1, -1), complexity_mask))+1 # Calculate the closest complexity group for generated piece
                pred_cosine_complexity_compl = np.argmax(cosine_similarity(piece_complexity[-3:].reshape(1, -1), complexity_mask[:,-3:]))+1 # Calculate the closest complexity group for generated piece
                pred_euc_complexity_compl = np.argmax(euclidean_distances(piece_complexity[-3:].reshape(1, -1), complexity_mask[:,-3:]))+1 # Calculate the closest complexity group for generated piece

                #mean_pred = (pred_cosine_complexity_mixed + pred_euc_complexity_mixed + pred_cosine_complexity_compl + pred_euc_complexity_compl)/4.0
                #print "Initial complexity label {}; Complexity, that's been predicted by computed complexity mask {}".format(int(folder[-1]), mean_pred)

                if (pred_cosine_complexity_mixed==int(folder[-1])) or (pred_euc_complexity_mixed==int(folder[-1])) or (pred_cosine_complexity_compl==int(folder[-1])) or (pred_euc_complexity_compl==int(folder[-1])):
                    counter += 1
            except:
                print '{} has been ignored'.format(music)

        print '[+]' + green + ' Correct predictions for {} is {}% '.format(folder, counter/float(len(available_files))*100) + normal + '[+]\n'


def run_tests(complexity_stats, sent_score_mapped=None, read_score_mapped=None):
    #compare_composed_key_n_requested(sent_score_mapped)
    #compare_composed_complexity_n_requested(read_score_mapped, complexity_stats)
    compare_init_labels_n_complexity_mask(complexity_stats)

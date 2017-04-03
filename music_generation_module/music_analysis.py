# Import packages
import os, random, re, time
import cPickle as pickle
import shelve
import signal
import music21
from os import listdir
from os.path import isfile, join

# Import modules
from midi_to_statematrix import *
from model_training import batch_len
from model_data import *
from utils import *

# Main class
module_name = 'music_generation_module'
music_dir = 'music'

def process_music():
    """Function deletes files that cannot be used in training and
    returns a dictionary of the form -> {'name': MIDI_statematrix}
    """
    saved_result = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if (isfile(join("./{}/{}/".format(module_name, music_dir), f)) and ("music_trans" in f))]

    if saved_result:
        print '[+]' + green + ' All music files has been analysed. Loading results... ' + normal + '[+]\n'
    else:
        print '[+]' + green + ' No previous results found. Starting from the beginning... ' + normal + '[+]\n'
        skipped = dict()
        pieces = shelve.open('./{}/{}/music_trans'.format(module_name, music_dir))

        music_folders = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if not(isfile(join("./{}/{}/".format(module_name, music_dir), f))) and ("level" in f)]

        for iter,folder in enumerate(music_folders):
            available_files = [f for f in listdir("./{}/{}/{}".format(module_name, music_dir, folder)) if (isfile(join("./{}/{}/{}".format(module_name, music_dir, folder), f)) and (".mid" in f))]

            for music in available_files:

                name = music[:-4]
                try:
                    outMatrix = midiToNoteStateMatrix(join("./{}/{}/{}".format(module_name, music_dir, folder), music))
                    if len(outMatrix) <= batch_len:
                        print "Skipped {}".format(music)
                        skipped[music] = folder
                        continue

                    complexity_score = iter+1

                    score = music21.converter.parse("./{}/{}/{}/{}".format(module_name, music_dir, folder, music))
                    key = score.analyze('key')
                    key_score = 1 if key.mode=='major' else 0

                    pieces[name] = [outMatrix, complexity_score, key_score]
                    print "Loaded {}: {}_{} and has complexity {}".format(name, key.mode, key_score, complexity_score)
                except TypeError, e:
                    print "Error: {} skipped {}".format(e, music)
                    skipped[music] = folder

        if skipped:
            for k,v in skipped.iteritems():
                try:
                    os.remove('./{}/{}/{}/{}'.format(module_name, music_dir, v, k))
                except OSError, e:
                    print '{} could not be deleted by script: {}'.format(item, e)
        else:
            pass

        print '\n===' + turquoise + ' {} MIDI files has been processed & saved... '.format(len(pieces)) + normal + '===\n'
        pieces.close()

def load_trans_music():
    """Once all music has been converted into statematrix form,
    load them into one dict and return it
    """
    results = dict()
    trans_music = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if isfile(join("./{}/{}".format(module_name, music_dir), f)) and ("music_" in f)]

    for music in trans_music:
        results.update(pickle.load(open('./{}/{}/{}'.format(module_name, music_dir, music), 'rb')))

    return results

def get_complexity_dict():
    """Returns a dictionary of complexity of music pieces
    key - music name,
    value - complexity score
    """
    complexity_scores = dict()
    music_folders = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if not(isfile(join("./{}/{}/".format(module_name, music_dir), f))) and ("level" in f)]

    if music_folders:
        for iter,folder in enumerate(music_folders):
            available_files = [f for f in listdir("./{}/{}/{}".format(module_name, music_dir, folder)) if (isfile(join("./{}/{}/{}".format(module_name, music_dir, folder), f)) and (".mid" in f))]
            complexity_scores.update({music[:-4]:(iter+1) for music in available_files})
    else:
        print '[!!]'+ red + ' No subfolders found! ' + normal + '[!!]'

    pickle.dump(complexity_scores,open('./{}/{}/{}.p'.format(module_name, music_dir, 'complexity_scores'), 'wb'))
    print '[+]' + green + ' Complexity analysis is completed ' + normal + '[+]'

    return complexity_scores

def music_key_helper(folders):
    """Helper subfunction for get_music_key_dict() function, to follow DRY paradigm"""
    results = dict()
    if folders:
        for folder in folders:
            print '[+]' + green + ' Analysing {} files '.format(folder) + normal + '[+]'
            available_files = [f for f in listdir("./{}/{}/{}".format(module_name, music_dir, folder)) if (isfile(join("./{}/{}/{}".format(module_name, music_dir, folder), f)) and (".mid" in f))]
            for music in available_files:
                name = music[:-4]
                score = music21.converter.parse("./{}/{}/{}/{}".format(module_name, music_dir, folder, music))
                key = score.analyze('key')
                print '{} is in {} key'.format(music, key.mode)
                results[name] = 1 if key.mode=='major' else 0
                results.update({name: 1 if key.mode=='major' else 0})
            #results.update({music[:-4]: (1 if music21.converter.parse("./{}/{}/{}/{}".format(module_name, music_dir, folder, music)).analyze('key').mode=='major' else 0) for music in available_files})
            print '[!!]' + green + ' Saving results to ./{}/{}/keys_{}.p '.format(module_name, music_dir, folder) + normal + '[!!]'
            pickle.dump(results,open('./{}/{}/keys_{}.p'.format(module_name, music_dir, folder), 'wb'))
    else:
        print '[!!]'+ red + 'No subfolders found!' + normal + '[!!]'
    print '[+]' + green + ' Key analysis is completed ' + normal + '[+]'

def load_music_key():
    """Once all keys are available, load them into one dict and return it"""
    results = dict()
    keys_saved = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if isfile(join("./{}/{}".format(module_name, music_dir), f)) and ("keys_" in f)]

    for key in keys_saved:
        results.update(pickle.load(open('./{}/{}/{}'.format(module_name, music_dir, key), 'rb')))

    return results

def get_music_key_dict():
    """Returns a dictionary of music piece's key
    key - music name,
    value - key (0 - minor, 1 - major)
    """
    keys_saved = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if isfile(join("./{}/{}".format(module_name, music_dir), f)) and ("keys_" in f)]
    music_folders = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if not isfile(join("./{}/{}".format(module_name, music_dir), f)) and ("level" in f)]

    if keys_saved:
        folders_to_analyse = music_folders[:]
        folders_been_analysed = [f for f in music_folders for keys in keys_saved if f[-1] in keys[-3]]
        for item in folders_been_analysed:
            folders_to_analyse.remove(item)

        if len(music_folders)==len(folders_been_analysed):
            print '[+]' + green + ' All data has been analysed. Loading results... ' + normal + '[+]\n'
        else:
            print '[+]' + green + ' Previous results found. Analysing from stop point... {} '.format(folders_to_analyse[0]) + normal + '[+]\n'
            music_key_helper(folders_to_analyse)

    else:
        print '[+]' + green + ' No previous results found. Starting from beginning... ' + normal + '[+]\n'
        music_key_helper(music_folders)
        print '[+]' + green + ' Getting results ready... ' + normal + '[+]\n'

def music_analysis():
    """Main function that calls helper functions to perform music analysis"""

    print '\n===' + turquoise + ' MIDI files are being cleaned & transformed... ' + normal + '===\n'
    process_music()

    #print '\n===' + turquoise + ' Getting complexity scores for MIDI files... ' + normal + '===\n'
    #complexity = get_complexity_dict()

    #print '\n===' + turquoise + ' Getting keys for MIDI files... ' + normal + '===\n'
    #get_music_key_dict()

    pcs = shelve.open('./{}/{}/music_trans'.format(module_name, music_dir))
    #keys = load_music_key()
    return pcs

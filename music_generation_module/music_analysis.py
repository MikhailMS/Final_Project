# Import packages
import os, random, re, time
import cPickle as pickle
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
    """Function deletes files that cannot be used in training to reduce running time on next try"""
    skipped = dict()
    pieces = {}
    music_keys = load_music_key()

    music_folders = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if not(isfile(join("./{}/{}/".format(module_name, music_dir), f))) and ("level" in f)]

    for iter, folder in enumerate(music_folders):
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
                key = music_keys.get(name)

                outMatrix.append(complexity_score)
                outMatrix.append(key)
                pieces[name] = outMatrix
                print "Loaded {}:  has complexity: {}, key: {} and length: {}".format(name, complexity_score, key, len(outMatrix))

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

    print 'Application can load {} music files for training'.format(len(pieces))
    return pieces

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
                #results.update({name: 1 if key.mode=='major' else 0})
            #results.update({music[:-4]: (1 if music21.converter.parse("./{}/{}/{}/{}".format(module_name, music_dir, folder, music)).analyze('key').mode=='major' else 0) for music in available_files})
            print '[!!]' + green + ' Saving results to ./{}/{}/keys_{}.p '.format(module_name, music_dir, folder) + normal + '[!!]'
            pickle.dump(results,open('./{}/{}/keys_{}.p'.format(module_name, music_dir, folder), 'wb'))
    else:
        print '[!!]'+ red + 'No subfolders found!' + normal + '[!!]'
    print '[+]' + green + ' Key analysis is completed ' + normal + '[+]'

def load_music_key():
    """Once all keys are available, load them into one dict and return it"""
    results = dict()
    keys_saved = [f for f in listdir("./{}/{}/".format(module_name, music_dir)) if ("keys_" in f)]

    for key in keys_saved:
        results.update(pickle.load(open('./{}/{}/{}'.format(module_name, music_dir, key), 'rb')))
    print len(results)
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
        print '[+]' + green + ' No previous results found. Starting from beggining... ' + normal + '[+]\n'
        music_key_helper(music_folders)
        print '[+]' + green + ' Getting results ready... ' + normal + '[+]\n'

def music_analysis():
    """Main function that calls helper functions to perform music analysis"""
    get_music_key_dict() # Takes ages to complete
    pcs = process_music()

    return pcs

# Import packages
import os, random, re
import cPickle as pickle
import signal
import sys
import music21
from os import listdir
from os.path import isfile, join

# Import modules
from midi_to_statematrix import *
from model_data import *
from utils import *
from constants import *

# Main class
def getMidiSegment(midi):
    """Gets random midi file from the dictionary of loaded files,
    initialises random starting point and then returns 2 segments:
    output and input.
    """
    piece_output = random.choice(midi.values())
    start = random.randrange(0,len(piece_output[:-2])-batch_len,division_len)
    #print "Range is {} {} {} -> {}".format(0,len(piece_output)-batch_len,division_len, start)

    compl_score = piece_output[-2] # Retrieve the complexity of according music piece
    key_score = piece_output[-1] # Retrieve the tonic of according music piece
    #print 'getMidiSegment - complexity: {}, key: {}'.format(compl_score, key_score)

    seg_out = piece_output[start:start+batch_len]
    seg_in = noteStateMatrixToInputForm(seg_out+[compl_score]+[key_score])

    return seg_in, seg_out

def getMidiSegmentInitialStep(midi, compl, key):
    """Similar to getMidiSegment function, but returns music piece with specific
    complexity and key
    """
    piece_output = random.choice(midi.values())

    while (piece_output[-2]!=compl or piece_output[-1]!=key): # Make sure that we pick correct initial music file
        piece_output = random.choice(midi.values())
        print 'Requested compl&key: {}, {}; Retrieved compl&key: {},{} -> gives {}'.format(compl, key, piece_output[-2], piece_output[-1], (piece_output[-2]!=compl or piece_output[-1]!=key))

    compl_score = piece_output[-2] # Retrieve the complexity of according music piece
    key_score = piece_output[-1] # Retrieve the tonic of according music piece

    start = random.randrange(0,len(piece_output[:-2])-batch_len,division_len)

    #print "Range is {} {} {} -> {}".format(0,len(piece_output)-batch_len,division_len, start)

    seg_out = piece_output[start:start+batch_len]
    seg_in = noteStateMatrixToInputForm(seg_out+[compl_score]+[key_score])

    return seg_in, seg_out

def getMidiSegmentTextFeatures(midi, compl, key):
    """Similar to getMidiSegment function, but uses initial midi file for future
    music composition with given complexity and key
    """
    piece_output = midi

    compl_score = compl # Set the complexity of according music piece
    key_score = key # Set the tonic of according music piece

    start = len(piece_output)-batch_len # Take the last part of the generated piece for more consistent music composition

    #print "Range is {} {} {} -> {}".format(0,len(piece_output)-batch_len,division_len, start)

    seg_out = piece_output[start:start+batch_len]
    seg_in = noteStateMatrixToInputForm(seg_out+[compl_score]+[key_score])

    return seg_in, seg_out

def getMidiBatch(midi):
    """Returns input and output arrays, where each contains specific number of
    sequences (batch_width)"""
    inp,out = zip(*[getMidiSegment(midi) for _ in range(batch_width)])
    return numpy.array(inp), numpy.array(out)

def trainModel(model, midi, epochs, start=0):
    """Trains LSTM model on loaded midi files at given number of epochs
    Saves model configuration into file (.p) along with respective generated music (.mid)
    for that configuration.
    """
    stopflag = [False]
    def signal_handler(signame, sf):
        stopflag[0] = True
    old_handler = signal.signal(signal.SIGINT, signal_handler)

    available_configs = [f for f in listdir("./{}/{}/".format(module_name, output_dir)) if (isfile(join("./{}/{}/".format(module_name, output_dir), f)) and ("params" in f))]
    if available_configs:
        print '\n===' + green + ' PREVIOUS CONFIGURATIONS FOUND... ' + normal + '==='
        available_configs = [re.findall(r'\d+', x) for x in available_configs]
        available_configs = [x for sublist in available_configs for x in sublist]
        available_configs = map(int,available_configs)
        available_configs.sort()
        best_conf = available_configs[-1]

        if best_conf < epochs:
            print '\n===' + green + ' LOADING CONFIGURATION FROM ' + './{}/{}/params{}.p '.format(module_name, output_dir, best_conf) + normal + '==='
            model.learned_config = pickle.load(open('./{}/{}/params{}.p'.format(module_name, output_dir, best_conf), 'rb'))
            print '\n===' + green + ' LOAD IS COMPLETED! STARTING TRAINING... ' + normal + '==='

            for i in range(best_conf,epochs+1):
                if stopflag[0]:
                    break
                error = model.update_fun(*getMidiBatch(midi))
                if i % 100 == 0:
                    print '\n[+]' + yellow + " Epoch {}, error={} ".format(i,error) + normal + '==='
                    pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
                if i % 500 == 0 or (i % 100 == 0 and i < 1000):
                    xIpt, xOpt = map(numpy.array, getMidiSegment(midi))
                    noteStateMatrixToMidi(numpy.concatenate((numpy.expand_dims(xOpt[0], 0), model.predict_fun(batch_len, 1, xIpt[0])), axis=0),'./{}/{}/sample{}'.format(module_name, output_dir, i))
                    pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
            signal.signal(signal.SIGINT, old_handler)
        else:
            print '\n===' + red + ' BEST FOUND CONFIGURATION ({}) IS FINAL. EXITING... '.format(best_conf) + normal + '==='
            model.learned_config = pickle.load(open('./{}/{}/params{}.p'.format(module_name, output_dir, best_conf), 'rb'))
            signal.signal(signal.SIGINT, old_handler)
    else:
        print '\n===' + red + ' NO PREVIOUS CONFIGURATIONS FOUND. ' + normal + '==='
        print '\n===' + green + ' STARTING TRAINING FROM SCRATCH... ' + normal + '==='
        for i in range(start,start+epochs+1):
            if stopflag[0]:
                break
            error = model.update_fun(*getMidiBatch(midi))
            if i % 100 == 0:
                print '\n[+]' + yellow + " Epoch {}, error={} ".format(i,error) + normal + '==='
                pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
            if i % 500 == 0 or (i % 100 == 0 and i < 1000):
                xIpt, xOpt = map(numpy.array, getMidiSegment(midi))
                noteStateMatrixToMidi(numpy.concatenate((numpy.expand_dims(xOpt[0], 0), model.predict_fun(batch_len, 1, xIpt[0])), axis=0),'./{}/{}/sample{}'.format(module_name, output_dir, i))
                pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
        signal.signal(signal.SIGINT, old_handler)

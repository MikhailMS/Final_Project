# Import packages
import random, re
from os import listdir
from os.path import isfile, join
import cPickle as pickle
import signal

# Import modules
from midi_to_statematrix import *
from model_data import *
from utils import *


# Main class
batch_width = 12 # number of sequences in a batch
batch_len = 16*8 # length of each sequence
division_len = 16 # interval between possible start locations
module_name = 'music_generation_module'
output_dir = 'output'

def loadMusic(dirpath):
    """Loads MIDI files into a dictionary
    Returns a dictionary of the form -> {'name': MIDI_statematrix}
    """
    pieces = {}

    for fname in listdir(dirpath):
        if fname[-4:] not in ('.mid','.MID'):
            continue

        name = fname[:-4]

        outMatrix = midiToNoteStateMatrix(join(dirpath, fname))
        if len(outMatrix) < batch_len:
            continue

        pieces[name] = outMatrix
        print "Loaded {}".format(name)

    return pieces

def getMidiSegment(midi):
    """Gets random midi file from the dictionary of loaded files,
    initialises random starting point and then returns 2 segments:
    output and input.
    """
    piece_output = random.choice(midi.values())
    start = random.randrange(0,len(piece_output)-batch_len,division_len)
    # print "Range is {} {} {} -> {}".format(0,len(piece_output)-batch_len,division_len, start)

    seg_out = piece_output[start:start+batch_len]
    seg_in = noteStateMatrixToInputForm(seg_out)

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
        print '\n===' + green + ' PREVIOUS RESULTS FOUND... ' + normal + '==='
        available_configs = [re.findall(r'\d+', x) for x in available_configs]
        available_configs = [x for sublist in available_configs for x in sublist]
        available_configs = map(int,available_configs)
        available_configs.sort()
        best_conf = available_configs[-1]

        #"./{}/music".format(module_name)
        print '\n===' + green + ' LOADING ' + './{}/{}/params{}.p'.format(module_name, output_dir, best_conf) + normal + '==='
        model.learned_config = pickle.load(open('./{}/{}/params{}.p'.format(module_name, output_dir, best_conf), 'rb'))
        print '\n===' + green + ' LOAD IS COMPLETED! STARTING TRAINING... ' + normal + '==='

        for i in range(best_conf,epochs):
            if stopflag[0]:
                break
            error = model.update_fun(*getMidiBatch(midi))
            if i % 100 == 0:
                print '\n[+]' + yellow + " Epoch {}, error={} ".format(i,error) + normal + '==='
            if i % 500 == 0 or (i % 100 == 0 and i < 1000):
                xIpt, xOpt = map(numpy.array, getMidiSegment(midi))
                noteStateMatrixToMidi(numpy.concatenate((numpy.expand_dims(xOpt[0], 0), model.predict_fun(batch_len, 1, xIpt[0])), axis=0),'./{}/{}/sample{}'.format(module_name, output_dir, i))
                pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
        signal.signal(signal.SIGINT, old_handler)

    else:
        for i in range(start,start+epochs):
            if stopflag[0]:
                break
            error = model.update_fun(*getMidiBatch(midi))
            if i % 100 == 0:
                print '\n[+]' + yellow + " Epoch {}, error={} ".format(i,error) + normal + '==='
            if i % 500 == 0 or (i % 100 == 0 and i < 1000):
                xIpt, xOpt = map(numpy.array, getMidiSegment(midi))
                noteStateMatrixToMidi(numpy.concatenate((numpy.expand_dims(xOpt[0], 0), model.predict_fun(batch_len, 1, xIpt[0])), axis=0),'./{}/{}/sample{}'.format(module_name, output_dir, i))
                pickle.dump(model.learned_config,open('./{}/{}/params{}.p'.format(module_name, output_dir, i), 'wb'))
        signal.signal(signal.SIGINT, old_handler)

# Import packages
import cPickle as pickle
import time, gzip, numpy, os
from midi_to_statematrix import *

# Import modules
import model_training
import lstm_model
from utils import *

# Main class
module_name = 'music_generation_module'
output_dir = 'output'

def music_composition_helper(m, pcs, times, keep_thoughts=False, name="final"):
    """Function composes music according to trained LSTM models
    and stores them into 'output' folder
    """
    xIpt, xOpt = map(lambda x: numpy.array(x, dtype='int8'), model_training.getMidiSegment(pcs))
    all_outputs = [xOpt[0]]
    if keep_thoughts:
        all_thoughts = []
    m.start_slow_walk(xIpt[0])
    cons = 1
    for time in range(model_training.batch_len*times):
        resdata = m.slow_walk_fun( cons )
        nnotes = numpy.sum(resdata[-1][:,0])
    	if nnotes < 2:
    		if cons > 1:
    			cons = 1
    		cons -= 0.02
    	else:
    		cons += (1 - cons)*0.3
    	all_outputs.append(resdata[-1])
    	if keep_thoughts:
    		all_thoughts.append(resdata)
    noteStateMatrixToMidi(numpy.array(all_outputs),'./{}/{}/{}'.format(module_name, output_dir, name))
    if keep_thoughts:
    	pickle.dump(all_thoughts, open('./{}/{}/{}.p'.format(module_name, output_dir, name),'wb'))

def run_music_composition(music_length= 30, epochs=5500):
    start = time.time()

    try:
        os.mkdir('./{}/{}'.format(module_name, output_dir))
        print '\n===' + green + ' {} folder been created '.format(output_dir) + normal + '==='
    except:
        print '\n===' + red + ' {} folder already exists '.format(output_dir) + normal + '==='
        pass
    print '\n===' + turquoise + ' MIDI files are being loaded... ' + normal + '==='
    pcs = model_training.loadMusic("./{}/music".format(module_name)) # Load all available MIDI files

    print '\n===' + turquoise + ' LSTM model is being created... ' + normal + '==='
    m = lstm_model.Model([300,300],[100,50], dropout=0.5) # Create LSTM model

    print '\n===' + turquoise + ' LSTM model is being trained... ' + normal + '==='
    model_training.trainModel(m, pcs, epochs) # Train LSTM model

    # Save LSTM model configuration
    print '\n===' + turquoise + ' LSTM model is being saved... ' + normal + '==='
    pickle.dump( m.learned_config, open( "./{}/{}/final_learned_config.p".format(module_name, output_dir), "wb" ) )

    print '\n===' + turquoise + ' Music is being generated... ' + normal + '==='
    music_composition_helper(m, pcs, music_length, name="composition") # Generate music

    finish = time.time() - start
    print '\n===' + turquoise + ' Application has finished in ' + normal + str(finish) + 'seconds' + '==='

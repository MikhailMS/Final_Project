# Import packages
import cPickle as pickle
import time, gzip, numpy, os
from midi_to_statematrix import *

# Import modules
import model_training
import lstm_model
from utils import *

# Main class
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
    noteStateMatrixToMidi(numpy.array(all_outputs),'output/'+name)
    if keep_thoughts:
    	pickle.dump(all_thoughts, open('output/'+name+'.p','wb'))

def run_music_composition(epochs=5500):
    start = time.time()
    output_dir = 'output'
    try:
        os.mkdir(output_dir)
        print output_dir + ' been created.'
    except:
        print output_dir + ' already exists.'
        pass
    print '\n===' + turquoise + ' MIDI files are being loaded... ' + normal + '==='
    pcs = model_training.loadMusic("music") # Load all available MIDI files

    print '\n===' + turquoise + ' LSTM model is being created... ' + normal + '==='
    m = lstm_model.Model([300,300],[100,50], dropout=0.5) # Create LSTM model

    print '\n===' + turquoise + ' LSTM model is being trained... ' + normal + '==='
    model_training.trainModel(m, pcs, epochs) # Train LSTM model

    # Save LSTM model configuration
    print '\n===' + turquoise + ' LSTM model is being saved... ' + normal + '==='
    pickle.dump( m.learned_config, open( "output/final_learned_config.p", "wb" ) )

    print '\n===' + turquoise + ' Music is being generated... ' + normal + '==='
    music_composition_helper(m, pcs, 30, name="composition") # Generate music

    finish = time.time() - start
    print '\n===' + turquoise + ' Application has finished in ' + normal + str(finish) + 'seconds' + '==='

import cPickle as pickle
import gzip, numpy, os
from midi_to_statematrix import *

import model_training
import lstm_model

def gen_adaptive(m, pcs, times, keep_thoughts=False, output_dir='output', name="final"):
	"""Function generates music according to trained LSTM models
	and stores them into 'output' folder
	"""
	try:
    	os.makedirs(output_dir)
    except:
    	pass
	xIpt, xOpt = map(lambda x: numpy.array(x, dtype='int8'), model_training.getPieceSegment(pcs))
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

pcs = multi_training.loadMidiSamples("music") # Load all available MIDI files

m = model.Model([300,300],[100,50], dropout=0.5) # Create LSTM model

model_training.trainModel(m, pcs, 10000) # Train LSTM model

# Save LSTM model configuration
pickle.dump( m.learned_config, open( "output/final_learned_config.p", "wb" ) )

gen_adaptive(m, pcs, 10, name="composition") # Generate music

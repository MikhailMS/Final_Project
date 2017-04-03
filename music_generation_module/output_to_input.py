# Import packages
import theano, theano.tensor as T
import numpy as np

# Import modules
from model_data import noteStateSingleToInputForm

# Main class
class OutputFormToInputFormOp(theano.Op):
    # Properties attribute
    __props__ = ()

    def make_node(self, state, time):
        state = T.as_tensor_variable(state)
        time = T.as_tensor_variable(time)
        #complexity_score = T.as_tensor_variable(complexity_score)
        #key_score = T.as_tensor_variable(key_score)

        return theano.Apply(self, [state, time], [T.bmatrix()])


    # Python implementation:
    def perform(self, node, inputs_storage, output_storage):
        state, time, = inputs_storage
        output_storage[0][0] = np.array(noteStateSingleToInputForm(state, time), dtype='int8')

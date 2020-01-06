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
        time  = T.as_tensor_variable(time)
        """Assumably there should be third variable that holds extra params
        extra = T.as_tensor_variable(extra)
        return theano.Apply(self, [state, time, extra], [T.bmatrix()])
        """
        return theano.Apply(self, [state, time], [T.bmatrix()])


    # Python implementation:
    def perform(self, node, inputs_storage, output_storage):
        state, time          = inputs_storage
        output_storage[0][0] = np.array(noteStateSingleToInputForm(state, time), dtype='int8')
        """Taking third parameter into account:
        state, time, extra = inputs_storage
        output_storage[0][0][0] = np.array(noteStateSingleToInputForm(state, time, extra), dtype='int8')
        """

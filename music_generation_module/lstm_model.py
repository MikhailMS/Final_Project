# Import packages
import theano, theano_lstm, theano.tensor as T
import numpy as np
from theano_lstm import Embedding, LSTM, RNN, StackedCells, Layer, create_optimization_updates, masked_loss, MultiDropout

# Import modules

# Main class
def has_hidden(layer):
    """
    Returns True, if layer has a trainable
    initial hidden state.
    """
    return hasattr(layer, 'initial_hidden_state')

def matrixify(vector, n):

    # Cast n to int32 if necessary to prevent error on 32 bit systems
    return T.repeat(T.shape_padleft(vector),
                    n if (theano.configdefaults.local_bitwidth() == 64) else T.cast(n,'int32'),
                    axis=0)

def initial_state(layer, dimensions = None):
    """
    Initalizes the recurrence relation with an initial hidden state
    if needed, else replaces with a "None" to tell Theano that
    the network **will** return something, but it doesn't need
    to send it to the next step of the recurrence
    """
    if dimensions is None:
        return layer.initial_hidden_state if has_hidden(layer) else None
    else:
        return matrixify(layer.initial_hidden_state, dimensions) if has_hidden(layer) else None

def initial_state_with_taps(layer, dimensions = None):
    """Optionally wrap tensor variable into a dictionary
    with taps=[-1]
    """
    state = initial_state(layer, dimensions)
    if state is not None:
        return dict(initial=state, taps=[-1])
    else:
        return None

class PassthroughLayer(Layer):
    """
    Empty "layer" that would return the final output of the LSTM model
    """

    def __init__(self):
        self.is_recursive = False

    def create_variables(self):
        pass

    def activate(self, x):
        return x

    @property
    def params(self):
        return []

    @params.setter
    def params(self, param_list):
        pass

def get_last_layer(result):
    """Returns last layer of the model"""
    if isinstance(result, list):
        return result[-1]
    else:
        return result

def ensure_list(result):
    """Returns a list of result(-s)
    If result is not of type 'list', then translate it into list and return it
    """
    if isinstance(result, list):
        return result
    else:
        return [result]

class Model(object):

    def __init__(self, t_layer_sizes, p_layer_sizes, extra_layer_sizes=None, dropout=0):

        # Initialise number of layers (neural network layers)
        self.t_layer_sizes = t_layer_sizes # time_model layers
        self.p_layer_sizes = p_layer_sizes # pitch_model layers
        """extra_layer_sizes represents a layers to handle
        extra features (music key, complexity, notes density(notes/segment) )
        """
        # self.extra_layer_sizes = extra_layer_sizes

        """From architecture definition, size of the notewise input
        Maybe worth changing to 88 (to include all piano notes)
        Definition - **Number of recurrent layers (suitable for storing information for long
        periods of time**
        """
        self.t_input_size = 80

        # Time network maps from notewise input size to various hidden sizes
        self.time_model = StackedCells(self.t_input_size, celltype=LSTM, layers = t_layer_sizes)
        # Add output layer to time_model
        self.time_model.layers.append(PassthroughLayer())

        """Pitch network takes last layer of time_model and state of last note, moving upward
        and eventually ends with a two-element sigmoid layer (time, pitch [??])
        """
        p_input_size = t_layer_sizes[-1] + 2
        self.pitch_model = StackedCells(p_input_size, celltype=LSTM, layers = p_layer_sizes)
        self.pitch_model.layers.append(Layer(p_layer_sizes[-1], 2, activation = T.nnet.sigmoid))

        """Assumably here I need to place model/models that would take care
        of extra features, such as: key, complexity, note density"""
        # self.extra_input_size = 3
        # self.extra_model = StackedCells(self.extra_input_size, celltype=LSTM, layers=extra_layer_sizes)
        # Add output layer to extra_model
        # self.extra_model.layers.append(PassthroughLayer())

        self.dropout = dropout

        self.conservativity = T.fscalar()
        self.srng = T.shared_randomstreams.RandomStreams(np.random.randint(0, 1024))

        self.setup_train()
        self.setup_predict()
        self.setup_slow_walk()

    @property
    def params(self):
        return self.time_model.params + self.pitch_model.params # + self.extra_model.params

    @params.setter
    def params(self, param_list):
        ntimeparams = len(self.time_model.params)
        self.time_model.params = param_list[:ntimeparams]
        self.pitch_model.params = param_list[ntimeparams:] # param_list[ntimeparams:-1]
        # self.extra_model.params = param_list[-1]

    @property
    def learned_config(self):
        return [self.time_model.params, self.pitch_model.params,
                [l.initial_hidden_state for mod in (self.time_model, self.pitch_model) for l in mod.layers if has_hidden(l)]]
        # return [self.time_model.params, self.pitch_model.params, self.extra_model.params,
        # [l.initial_hidden_state for mod in (self.time_model, self.pitch_model, self.extra_model) for l in mod.layers if has_hidden(l)]]

    @learned_config.setter
    def learned_config(self, learned_list):
        self.time_model.params = learned_list[0]
        self.pitch_model.params = learned_list[1]
        # self.extra_model.params = learned_list[2]
        for l, val in zip((l for mod in (self.time_model, self.pitch_model) for l in mod.layers if has_hidden(l)), learned_list[2]):
            l.initial_hidden_state.set_value(val.get_value())
        # for l, val in zip((l for mod in (self.time_model, self.pitch_model, self.extra_model) for l in mod.layers if has_hidden(l)), learned_list[3]):
            # l.initial_hidden_state.set_value(val.get_value())

    def setup_train(self):
"""========================= Initialization ========================="""
        # dimensions: (batch, time, notes, input_data) with input_data as in architecture
        self.input_mat = T.btensor4()
        """Assumably we need an array of btensor4 variables to hold extra params input
        self.input_mat = [T.btensor4(), T.btensor4()]
        """
        # dimensions: (batch, time, notes, onOrArtic) with 0:on, 1:artic
        self.output_mat = T.btensor4()
        """Therefore we need array of btensor4 variables to hold extra params output
        self.output_mat = [T.btensor4(), T.btensor4()]
        """

        self.epsilon = np.spacing(np.float32(1.0))

"""======== Functions that represent steps(forward learning) ========"""
        def step_time(in_data, *other):
            """Returns new state for time_model"""
            other = list(other)
            split = -len(self.t_layer_sizes) if self.dropout else len(other)
            hiddens = other[:split]
            masks = [None] + other[split:] if self.dropout else []
            new_states = self.time_model.forward(in_data, prev_hiddens=hiddens, dropout=masks)
            return new_states

        def step_note(in_data, *other):
            """Returns new state for pitch_model"""
            other = list(other)
            split = -len(self.p_layer_sizes) if self.dropout else len(other)
            hiddens = other[:split]
            masks = [None] + other[split:] if self.dropout else []
            new_states = self.pitch_model.forward(in_data, prev_hiddens=hiddens, dropout=masks)
            return new_states

        def step_extra(in_data, *other):
            """Returns new state of extra_model [NEED FIXING]"""
            other = list(other)
            split = -len(self.extra_layer_sizes) if self.dropout else len(other)
            hiddens = other[:split]
            masks = [None] + other[split:] if self.dropout else []
            new_states = self.extra_model.forward(in_data, prev_hiddens=hiddens, dropout=masks)
            return new_states

"""=================== STAGE 0 - data preparation ==================="""
        # We generate an output for each input, so it doesn't make sense to use the last output as an input.
        # Note that we assume the sentinel start value is already present
        # TEMP CHANGE: NO SENTINEL
        input_slice = self.input_mat[:,0:-1]
        n_batch, n_time, n_note, n_ipn = input_slice.shape
        # time_inputs is a matrix (time, batch/note, input_per_note)
        time_inputs = input_slice.transpose((1,0,2,3)).reshape((n_time,n_batch*n_note,n_ipn))
        num_time_parallel = time_inputs.shape[1]
        """If we apply above changes [161-163, 166-168] we need to make different input_slice
        input_slice = self.input_mat[0][:,0:-1]
        n_batch, n_time, n_note, n_ipn = input_slice.shape
        # time_inputs is a matrix (time, batch/note, input_per_note)
        time_inputs = input_slice.transpose((1,0,2,3)).reshape((n_time,n_batch*n_note,n_ipn))
        num_time_parallel = time_inputs.shape[1]

        input_slice = self.input_mat[1][:,0:-1]
        n_sent, n_lex, n_read, n_ipn = input_slice.shape
        Make similar num_time_parallel as above
        """

"""====================== STAGE 1 - time_model ======================"""
        # Apply dropout to time_model
        if self.dropout > 0:
            time_masks = theano_lstm.MultiDropout( [(num_time_parallel, shape) for shape in self.t_layer_sizes], self.dropout)
        else:
            time_masks = []
        time_outputs_info = [initial_state_with_taps(layer, num_time_parallel) for layer in self.time_model.layers]
        time_result, _ = theano.scan(fn=step_time, sequences=[time_inputs], non_sequences=time_masks, outputs_info=time_outputs_info)
        self.time_thoughts = time_result

        """Now time_result is a list of matrix [layer](time, batch/note, hidden_states)
        for each layer but we only care about the hidden state of the last layer.
        Transpose to be (note, batch/time, hidden_states)
        """
        last_layer = get_last_layer(time_result)
        n_hidden = last_layer.shape[2]
        time_final = get_last_layer(time_result).reshape((n_time,n_batch,n_note,n_hidden)).transpose((2,1,0,3)).reshape((n_note,n_batch*n_time,n_hidden))

        """note_choices_inputs represents the last chosen note.
        Starts with [0,0], doesn't include last note. In (note, batch/time, 2) format
        Shape of start is thus (1, N, 2), concatenated with all but last element of output_mat transformed to (x, N, 2)
        """
        start_note_values = T.alloc(np.array(0,dtype=np.int8), 1, time_final.shape[1], 2 )
        correct_choices = self.output_mat[:,1:,0:-1,:].transpose((2,0,1,3)).reshape((n_note-1,n_batch*n_time,2))
        note_choices_inputs = T.concatenate([start_note_values, correct_choices], axis=0)
        """Together, this and the output from the last LSTM (time_model[?]) goes to the new LSTM (pitch_model[?]),
        but rotated, so that the batches in one direction are the steps in the other, and vice versa.
        """
        note_inputs = T.concatenate( [time_final, note_choices_inputs], axis=2 )
        num_timebatch = note_inputs.shape[1]

"""===================== STAGE 2 - pitch_model ======================"""
        # Apply dropout to pitch_model
        if self.dropout > 0:
            pitch_masks = theano_lstm.MultiDropout( [(num_timebatch, shape) for shape in self.p_layer_sizes], self.dropout)
        else:
            pitch_masks = []

        note_outputs_info = [initial_state_with_taps(layer, num_timebatch) for layer in self.pitch_model.layers]
        note_result, _ = theano.scan(fn=step_note, sequences=[note_inputs], non_sequences=pitch_masks, outputs_info=note_outputs_info)

        self.note_thoughts = note_result

        """Now note_result is a list of matrix [layer](note, batch/time, onOrArticProb)
        for each layer but we only care about the hidden state of the last layer.
        Transpose to be (batch, time, note, onOrArticProb)
        """
        note_final = get_last_layer(note_result).reshape((n_note,n_batch,n_time,2)).transpose(1,2,0,3)
        # In order to pass this results to STAGE 3, we need to follow similar pattern to STAGE 1
        # However, it may not be needed, and STAGE 3 would require data directly from STAGE 1

"""===================== STAGE 3 - extra_model ======================"""
        # Apply dropout to extra_model
        # Then carry on as for STAGE 2

"""=================== Finish train(update stage) ==================="""
        """The cost of the entire procedure is the negative log likelihood of the events all happening.
        For the purposes of training, if the ouputted probability is P, then the likelihood of seeing a 1 is P, and
        the likelihood of seeing 0 is (1-P). So the likelihood is (1-P)(1-x) + Px = 2Px - P - x + 1
        Since they are all binary decisions, and are all probabilities given all previous decisions, we can just
        multiply the likelihoods, or, since we are logging them, add the logs.

        Note that we mask out the articulations for those notes that aren't played,
        because it doesn't matter whether or not those are articulated.
        The padright is there because self.output_mat[:,:,:,0] -> 3D matrix with (b,x,y), but we need 3d tensor with
        (b,x,y,1) instead
        """
        active_notes = T.shape_padright(self.output_mat[:,1:,:,0])
        mask = T.concatenate([T.ones_like(active_notes),active_notes], axis=3)
        loglikelihoods = mask * T.log( 2*note_final*self.output_mat[:,1:] - note_final - self.output_mat[:,1:] + 1 + self.epsilon )
        self.cost = T.neg(T.sum(loglikelihoods))

        # Maybe worth changing optimization method [default = adadelta]
        updates, _, _, _, _ = create_optimization_updates(self.cost, self.params, method="adadelta")

        # Create custom theano update functions
        self.update_fun = theano.function(
            inputs=[self.input_mat, self.output_mat],
            outputs=self.cost,
            updates=updates,
            allow_input_downcast=True)
        self.update_thought_fun = theano.function(
            inputs=[self.input_mat, self.output_mat],
            outputs= ensure_list(self.time_thoughts) + ensure_list(self.note_thoughts) + [self.cost],
            allow_input_downcast=True)


    def _predict_step_note(self, in_data_from_time, *states):
        """Takes data and layers' states and returns new states + chosen notes"""
        # States are [ *hiddens, last_note_choice ]
        hiddens = list(states[:-1])
        in_data_from_prev = states[-1]
        in_data = T.concatenate([in_data_from_time, in_data_from_prev])

        # correct for dropout
        if self.dropout > 0:
            masks = [1 - self.dropout for layer in self.pitch_model.layers]
            masks[0] = None
        else:
            masks = []

        # Now new_states is a per-layer set of activations.
        new_states = self.pitch_model.forward(in_data, prev_hiddens=hiddens, dropout=masks)

        # Thus, probabilities is a vector of two probabilities, P(play), and P(artic | play)
        probabilities = get_last_layer(new_states)

        shouldPlay = self.srng.uniform() < (probabilities[0] ** self.conservativity)
        shouldArtic = shouldPlay * (self.srng.uniform() < probabilities[1])

        chosen = T.cast(T.stack(shouldPlay, shouldArtic), "int8")

        return ensure_list(new_states) + [chosen]

    def _predict_step_extra(self, in_data_from_time, *states):
        """If extra data should be predicted, then this function should be
        created in the same manner as _predict_step_note()
        Takes data and layers's states and returns new states + chosen extra params
        """

    def setup_predict(self):
        

    def setup_slow_walk(self):


    def start_slow_walk(self, seed):
# Import packages
import itertools
import numpy as np

# Import modules
from midi_to_statematrix import upperBound, lowerBound

# Main class
def getOrDefault(datalist, index, default):
    """If index is out of scope, then returns default value,
    otherwise returns value from the 'datalist' at index 'index'
    """
    try:
        return datalist[index]
    except IndexError:
        return default

def buildContext(state):
    """Returns a list of notes that a played at the given state:
    0 - not played, other values - played
    """
    context = [0]*12
    for note, notestate in enumerate(state):
        if notestate[0] == 1:
            pitchclass = (note + lowerBound) % 12
            context[pitchclass] += 1
    return context

def buildBeat(time):
    """Returns a beat:
    possible variations are whole note(1), half note (1/2), quarter(1/4) and eighth
    """
    return [2*x-1 for x in [time%2, (time//2)%2, (time//4)%2, (time//8)%2]]

def noteInputForm(note, state, context, beat, complexity_score, key_score):
    """Converts given state into input form (data list),
    that is used to train model
    """
    position = note # Redundant
    part_position = [position]

    pitchclass = (note + lowerBound) % 12 # Identify pitch class (range [0,11])
    part_pitchclass = [int(i == pitchclass) for i in range(12)] # Builds an array of length 12, where index represent pitch class

    # Concatenate the note states for the previous vicinity
    part_prev_vicinity = list(itertools.chain.from_iterable((getOrDefault(state, note+i, [0,0]) for i in range(-12, 13))))
    part_context = context[pitchclass:] + context[:pitchclass] # Why we change a context order here?

    # Bring complexity_score and key_score to similar form (list)
    part_complexity = [complexity_score]
    part_key = [key_score]

    return part_position + part_pitchclass + part_prev_vicinity + part_context + beat + part_key + part_complexity # Adds up into 81

def noteStateSingleToInputForm(state, time, complexity_score, key_score):
    """Converts state from statematrix into input form (data list),
    that is used to train model
    """
    beat = buildBeat(time)
    context = buildContext(state)
    #print 'Time step: {}, state length: {}, beat: {}, context: {}\n\t'.format(time, len(state), beat, context)
    return [noteInputForm(note, state, context, beat, complexity_score, key_score) for note in range(len(state))]

def noteStateMatrixToInputForm(statematrix, complexity_score=0, key_score=0):
    """Converts statematrix(representation of MIDI file) into list of data
    that is used to train model. Returns a list of input forms (data list)
    """
    input_form = [ noteStateSingleToInputForm(state,time, complexity_score, key_score) for time,state in enumerate(statematrix) ]
    return input_form

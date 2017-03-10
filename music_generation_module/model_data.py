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

def noteInputForm(note, state, context, beat):
    """Converts given state into input form (data list),
    that is used to train model
    """
    position = note
    part_position = [position]

    pitchclass = (note + lowerBound) % 12
    part_pitchclass = [int(i == pitchclass) for i in range(12)]

    # Concatenate the note states for the previous vicinity
    part_prev_vicinity = list(itertools.chain.from_iterable((getOrDefault(state, note+i, [0,0]) for i in range(-12, 13))))
    part_context = context[pitchclass:] + context[:pitchclass] # Why we change a context order here?

    return part_position + part_pitchclass + part_prev_vicinity + part_context + beat + [1] + [3] # Adds up into 81

def noteStateSingleToInputForm(state,time):
    """Converts state from statematrix into input form (data list),
    that is used to train model
    """
    beat = buildBeat(time)
    context = buildContext(state)
    return [noteInputForm(note, state, context, beat) for note in range(len(state))]

def noteStateMatrixToInputForm(statematrix):
    """Converts statematrix(representation of MIDI file) into list of data
    that is used to train model. Returns a list of input forms (data list)
    """
    input_form = [ noteStateSingleToInputForm(state,time) for time,state in enumerate(statematrix) ]
    return input_form

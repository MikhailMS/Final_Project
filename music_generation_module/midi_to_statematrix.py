# Import packages
import midi, numpy

# Main class

# Need to add description to what is lower/upper boundaries
lowerBound = 24
upperBound = 102

def midiToNoteStateMatrix(midifile):
    """
    Converts given MIDI file to state matrix (model readable form)
    and return the latter
    """
    pattern = midi.read_midifile(midifile) # midi.containers.Pattern

    timeleft    = [track[0].tick for track in pattern]
    print(timeleft)
    print(len(timeleft))
    posns       = [0 for track in pattern]
    print(posns)
    statematrix = []
    span        = upperBound - lowerBound
    time        = 0

    state = [[0,0] for x in range(span)]
    statematrix.append(state)
    while True:
        if time % (pattern.resolution / 4) == (pattern.resolution / 8):
            # Create a new state, defaulting to holding notes
            oldstate = state
            state    = [[oldstate[x][0],0] for x in range(span)]

            statematrix.append(state)

        for i in range(len(timeleft)):
            while timeleft[i] == 0:
                track = pattern[i]
                pos   = posns[i]

                evt = track[pos]
                if isinstance(evt, midi.NoteEvent):
                    print(evt.pitch)
                    if (evt.pitch < lowerBound) or (evt.pitch >= upperBound):
                        pass
                        # print "Note {} at time {} out of bounds (ignoring)".format(evt.pitch, time)
                    else:
                        if isinstance(evt, midi.NoteOffEvent) or evt.velocity == 0:
                            state[evt.pitch-lowerBound] = [0, 0]
                        else:
                            state[evt.pitch-lowerBound] = [1, 1]
                elif isinstance(evt, midi.TimeSignatureEvent):
                    if evt.numerator not in (2, 4):
                        # Don't need to worry about non-4 time signatures
                        # print "Found time signature event {}. Escape!".format(evt)
                        return statematrix

                try:
                    timeleft[i] = track[pos + 1].tick
                    posns[i] += 1
                except IndexError:
                    timeleft[i] = None

            if timeleft[i] is not None:
                timeleft[i] -= 1

        if all(t is None for t in timeleft):
            break

        time += 1

    return statematrix

def noteStateMatrixToMidi(statematrix, name="result",  velocity=0.5):
    """
    Converts given state matrix to MIDI file
    and return the latter, so it could be passed to software to play it out
    """
    vel         = velocity
    statematrix = numpy.asarray(statematrix) # Make sure we work with an array
    pattern     = midi.Pattern()
    track       = midi.Track()

    print 'Velocity multiplier: {}'.format(vel)
    pattern.append(track)

    span      = upperBound - lowerBound
    tickscale = 55 # Why 55?

    lastcmdtime = 0
    prevstate = [[0,0] for x in range(span)]
    for time, state in enumerate(statematrix + [prevstate[:]]):
        offNotes = []
        onNotes = []
        for i in range(span):
            n = state[i]
            p = prevstate[i]
            if p[0] == 1:
                if n[0] == 0:
                    offNotes.append(i)
                elif n[1] == 1:
                    offNotes.append(i)
                    onNotes.append(i)
            elif n[0] == 1:
                onNotes.append(i)
        for note in offNotes:
            track.append(midi.NoteOffEvent(tick=(time-lastcmdtime)*tickscale, pitch=note+lowerBound))
            lastcmdtime = time
        for note in onNotes:
            track.append(midi.NoteOnEvent(tick=(time-lastcmdtime)*tickscale, velocity=int(126*vel), pitch=note+lowerBound))
            lastcmdtime = time

        prevstate = state

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    midi.write_midifile("{}.mid".format(name), pattern)


state = midiToNoteStateMatrix('/Users/mikhailmolotkov/Desktop/COM3600 - Research Project/Application_code/music_generation_module/music/level_1/ea_me61_9.mid')
print(len(state))
print(state)

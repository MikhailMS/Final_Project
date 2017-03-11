# Import packages
import midi, numpy

# Main class
lowerBound = 24
upperBound = 102
velocity_scale = 127.0

def midiToNoteStateMatrix(midifile):
    """Converts given MIDI file to state matrix (model readable form)
    and return the latter
    """
    pattern = midi.read_midifile(midifile)

    timeleft = [track[0].tick for track in pattern]
    posns = [0 for track in pattern]

    statematrix = []
    span = upperBound-lowerBound
    time = 0

    state = [[0,0] for x in range(span)]
    statematrix.append(state)
    while True:
        if time % (pattern.resolution / 4) == (pattern.resolution / 8):
            # Create a new state, defaulting to holding notes
            oldstate = state
            state = [[oldstate[x][0],0] for x in range(span)]
            statematrix.append(state)

        for i in range(len(timeleft)):
            while timeleft[i] == 0:
                track = pattern[i]
                pos = posns[i]

                evt = track[pos]
                if isinstance(evt, midi.NoteEvent):
                    if (evt.pitch < lowerBound) or (evt.pitch >= upperBound):
                        #print "Note {} at time {} out of bounds (ignoring)".format(evt.pitch, time)
                        pass
                    else:
                        if isinstance(evt, midi.NoteOffEvent) or evt.velocity == 0:
                            state[evt.pitch-lowerBound] = [0, 0]
                        else:
                            scaled = evt.velocity/velocity_scale
                            state[evt.pitch-lowerBound] = [1, scaled]
                elif isinstance(evt, midi.TimeSignatureEvent):
                    """Need to test if this bit makes output better or worse"""
                    if evt.numerator not in (2, 4):
                        # Don't need to worry about non-4 time signatures
                        # print "Found time signature event {}. Escape!".format(evt)
                        #return statematrix
                        pass

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

def noteStateMatrixToMidi(statematrix, name="result"):
    """Converts given state matrix to MIDI file
    and return the latter, so it could be passed to software to play it out
    """
    statematrix = numpy.asarray(statematrix) # Make sure we work with an array
    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)

    span = upperBound-lowerBound
    tickscale = 55 # Why 55?

    lastcmdtime = 0
    prevstate = [[0,0] for x in range(span)]
    for time, state in enumerate(statematrix + [prevstate[:]]):
        offNotes = []
        onNotes = []
        velocity = []
        for i in range(span):
            n = state[i]
            p = prevstate[i]
            if p[0] == 1:
                if n[0] == 0:
                    offNotes.append(i)
                elif n[1] > 1:
                    offNotes.append(i)
                    onNotes.append(i)
                    velocity.append(n[1])
            elif n[0] == 1:
                onNotes.append(i)
                velocity.append(n[1])
        for note in offNotes:
            track.append(midi.NoteOffEvent(tick=(time-lastcmdtime)*tickscale, pitch=note+lowerBound))
            lastcmdtime = time
        for iter,note in enumerate(onNotes):
            track.append(midi.NoteOnEvent(tick=(time-lastcmdtime)*tickscale, velocity=int(velocity[iter]*velocity_scale), pitch=note+lowerBound))
            lastcmdtime = time

        prevstate = state

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    midi.write_midifile("{}.mid".format(name), pattern)

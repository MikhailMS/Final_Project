# Import packages
import music21
from os import listdir
from os.path import isfile, join

# Import modules
#from utils import *

#== Main class ==#

# Main tonics for key shifting
c_tonic = dict([("G#", 4),("A-", 4),("A", 3),("A#", 2),("B-", 2),("B", 1),("C", 0),("C#", -1),("D-", -1),("D", -2),("D#", -3),
               ("E-", -3),("E", -4),("F", -5),("F#", 6),("G-", 6),("G", 5)])
c_s_tonic = dict([("G#", 5),("A-", 5),("A", 4),("A#", 3),("B-", 3),("B", 2),("C", 1),("C#", 0),("D-", 0),("D", -1),("D#", -2),
               ("E-", -2),("E", -3),("F", -4),("F#", -5),("G-", -5),("G", 6)])

d_f_tonic = dict([("G#", 5),("A-", 5),("A", 4),("A#", 3),("B-", 3),("B", 2),("C", 1),("C#", 0),("D-", 0),("D", -1),("D#", -2),
               ("E-", -2),("E", -3),("F", -4),("F#", -5),("G-", -5),("G", 6)])
d_tonic = dict([("G#", 6),("A-", 6),("A", 5),("A#", 4),("B-", 4),("B", 3),("C", 2),("C#", 1),("D-", 1),("D", 0),("D#", -1),
               ("E-", -1),("E", -2),("F", -3),("F#", -4),("G-", -4),("G", -5)])
d_s_tonic = dict([("G#", -5),("A-", -5),("A", 6),("A#", 5),("B-", 5),("B", 4),("C", 3),("C#", 2),("D-", 2),("D", 1),("D#", 0),
               ("E-", 0),("E", -1),("F", -2),("F#", -3),("G-", -3),("G", -4)])

e_f_tonic = dict([("G#", -5),("A-", -5),("A", 6),("A#", 5),("B-", 5),("B", 4),("C", 3),("C#", 2),("D-", 2),("D", 1),("D#", 0),
               ("E-", 0),("E", -1),("F", -2),("F#", -3),("G-", -3),("G", -4)])
e_tonic = dict([("G#", -4),("A-", -4),("A", -5),("A#", 6),("B-", 6),("B", 5),("C", 4),("C#", 3),("D-", 3),("D", 2),("D#", 1),
               ("E-", 1),("E", 0),("F", -1),("F#", -2),("G-", -2),("G", -3)])

f_tonic = dict([("G#", -3),("A-", -3),("A", -4),("A#", -5),("B-", -5),("B", 6),("C", 5),("C#", 4),("D-", 4),("D", 3),("D#", 2),
               ("E-", 2),("E", 1),("F", 0),("F#", -1),("G-", -1),("G", -2)])
f_s_tonic = dict([("G#", -2),("A-", -2),("A", -3),("A#", -4),("B-", -4),("B", -4),("C", 6),("C#", 5),("D-", 5),("D", 4),("D#", 3),
               ("E-", 3),("E", 2),("F", 1),("F#", 0),("G-", 0),("G", -1)])

g_f_tonic = dict([("G#", -2),("A-", -2),("A", -3),("A#", -4),("B-", -4),("B", -4),("C", 6),("C#", 5),("D-", 5),("D", 4),("D#", 3),
               ("E-", 3),("E", 2),("F", 1),("F#", 0),("G-", 0),("G", -1)])
g_tonic = dict([("G#", -1),("A-", -1),("A", -2),("A#", -3),("B-", -3),("B", -4),("C", -5),("C#", 6),("D-", 6),("D", 5),("D#", 4),
               ("E-", 4),("E", 3),("F", 2),("F#", 1),("G-", 1),("G", 0)])
g_s_tonic = dict([("G#", 0),("A-", 0),("A", -1),("A#", -2),("B-", -2),("B", -3),("C", -4),("C#", -5),("D-", -5),("D", 6),("D#", 5),
               ("E-", 5),("E", 4),("F", 3),("F#", 2),("G-", 2),("G", 1)])

a_f_tonic = dict([("G#", 0),("A-", 0),("A", -1),("A#", -2),("B-", -2),("B", -3),("C", -4),("C#", -5),("D-", -5),("D", 6),("D#", 5),
               ("E-", 5),("E", 4),("F", 3),("F#", 2),("G-", 2),("G", 1)])
a_tonic = dict([("G#", 1),("A-", 1),("A", 0),("A#", -1),("B-", -1),("B", -2),("C", -3),("C#", -4),("D-", -4),("D", -5),("D#", 6),
               ("E-", 6),("E", 5),("F", 4),("F#", 3),("G-", 3),("G", 2)]) # same as A minor scale
a_s_tonic = dict([("G#", 2),("A-", 2),("A", 1),("A#", 0),("B-", 0),("B", -1),("C", -2),("C#", -3),("D-", -3),("D", -4),("D#", -5),
               ("E-", -5),("E", 6),("F", 5),("F#", 4),("G-", 4),("G", 3)])

b_f_tonic = dict([("G#", 2),("A-", 2),("A", 1),("A#", 0),("B-", 0),("B", -1),("C", -2),("C#", -3),("D-", -3),("D", -4),("D#", -5),
               ("E-", -5),("E", 6),("F", 5),("F#", 4),("G-", 4),("G", 3)])
b_tonic = dict([("G#", 3),("A-", 3),("A", 2),("A#", 1),("B-", 1),("B", 0),("C", -1),("C#", -2),("D-", -2),("D", -3),("D#", -4),
               ("E-", -4),("E", -5),("F", 6),("F#", 5),("G-", 5),("G", 4)])

def shift_key():
    """Shifts music key by parallel key rules"""

    # Get midi files
    music_files = [f for f in listdir("./output") if (isfile(join("./output", f)) and (".mid" in f))]

    for fname in music_files:

        name = fname[:-4]
        print "Loaded {}".format(name)
        score = music21.converter.parse('./output/{}'.format(fname))
        key = score.analyze('key')
        print 'Before change: {}, {}'.format(key.tonic.name, key.mode)

        # Check if should be done major -> minor shift
        if '{} {}'.format(key.tonic.name,key.mode) == "C major":
            halfSteps = a_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "C# major":
            halfSteps = a_s_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "D- major":
            halfSteps = b_f_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "D major":
            halfSteps = b_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "E- major":
            halfSteps = c_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "E major":
            halfSteps = c_s_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "F major":
            halfSteps = d_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "F# major":
            halfSteps = d_s_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "G major":
            halfSteps = e_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "A- major":
            halfSteps = f_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "A major":
            halfSteps = f_s_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "B- major":
            halfSteps = g_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "B major":
            halfSteps = g_s_tonic[key.tonic.name]
            print 'Minors: {}'.format(halfSteps)

        # Check if should be done minor -> major shift
        elif '{} {}'.format(key.tonic.name,key.mode) == "C minor":
            halfSteps = e_f_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "C# minor":
            halfSteps = e_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "D minor":
            halfSteps = f_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "D# minor":
            halfSteps = f_s_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "E minor":
            halfSteps = g_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "F minor":
            halfSteps = a_f_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "F# minor":
            halfSteps = a_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "G minor":
            halfSteps = b_f_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "G# minor":
            halfSteps = b_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "A minor":
            halfSteps = c_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "A# minor":
            halfSteps = c_s_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "B- minor":
            halfSteps = d_f_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        elif '{} {}'.format(key.tonic.name,key.mode) == "B minor":
            halfSteps = d_tonic[key.tonic.name]
            print 'Majors: {}'.format(halfSteps)

        newscore = score.transpose(halfSteps)
        key = newscore.analyze('key')
        print 'After change: {}, {}'.format(key.tonic.name, key.mode)

        if name == 'composition':
            newFileName = "Clean_{}.mid".format(name)
            print '{} is saved!'.format(newFileName)
            newscore.write('midi',newFileName)

shift_key()

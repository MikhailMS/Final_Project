# Import packages
import os, re, collections, pickle, multiprocessing, urllib2
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from operator import itemgetter

# Import modules
#from utils import *

# Main class
scores_website = 'http://www.music-scores.com'
composers_page = 'composer.php'

midi_website = 'http://www.piano-midi.de'
midi_page = 'midi_files.htm'

midi_website_2 = 'http://www.midiworld.com'
midi_page_2 = 'classic.htm'

midi_website_3 = 'https://www.8notes.com/school/midi/piano/'

output_module = 'music_generation_module'

def get_composers():
    """Function parses website and returns a list of all composers available
    on website
    """
    composers = list()
    # Initialize parser
    html_page = urllib2.urlopen('{}/{}'.format(scores_website, composers_page))
    soup = BeautifulSoup(html_page, 'lxml')

    # Start parser
    for link in soup.findAll('a'):
        url = '{}'.format(link.get('href'))
        if url.endswith('/composer.php'):
            url = str(url)
            url = url.split('/')
            composers.append(url[0])

    # Remove those who aren't composers
    try:
        composers.remove('christmas').remove('theory').remove('traditional')
    except:
        pass

    return composers

def get_music_name_n_score():
    """Function parses website and extracts music name and according complexity score.
    Returns a dictionary of the form {'complexity_level':[music name]}
    """
    instrument = 'piano'
    midi_url = midi_website_3 + '{}.mid'.format(music_name) # To be used to load midi
    results = dict()
    # Initialize parser

    # Start parser

    # Find name and score

    # Store values in dictionary

    return resutls

def get_midi_files():
    """Function parses website and extracts midi files for music, that been returned
    by get_music_name_n_score() function. Saves midi files in appropriate folders
    according to their complexity score
    """
    # Create folders to store midi files
    for i in xrange(1,8):
        try:
            os.mkdir('./{}/level_{}'.format(output_module, i))
            print '\n===' + green + ' level_{} folder been created '.format(i) + normal + '==='
        except:
            print '\n===' + red + ' level_{} folder already exists '.format(i) + normal + '==='
            pass

    # Initialize parser

    # Get names of music files
    names = get_music_name_n_score()

    # Start parser

    # Find midi file

    # Save midi in suitable folders

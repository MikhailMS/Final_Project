# Import packages
import os, re, collections, pickle, multiprocessing, urllib2, time
from bs4 import BeautifulSoup
from random import randint
from os import listdir
from os.path import isfile, join
from operator import itemgetter

# Import modules
#from utils import *

# Main class
dict = set()

def download_midi_recursive(website, page, folder):
    """Recursively downloads midi files from specified website
    and stores it under 'music' folder
    """
    if page in dict:
        return

    dict.add(page)
    print "Downloading page " + page

    html_page = urllib2.urlopen(website + '/' + page)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        url = '{}'.format(link.get('href'))

        if url.endswith('.mid'):
            try:
                filename = os.path.basename(url)
                midiurl = urllib2.urlopen(website + '/' + url)
                fullpath = './{}/{}'.format(folder,filename)

                if os.path.exists(fullpath):
                    print "Skipping " + filename
                else:
                    print "Downloading " +  filename
                    with open(fullpath, "wb") as local_file:
                        content = midiurl.read()
                        local_file.write(content)

            except urllib2.HTTPError, e:
                print "Http error" + e.code + url
            except urllib2.URLError, e:
                print "Url error" + e.reason + url
        if url.endswith('.htm'):
            try:
                relativeurl = os.path.basename(url)
                download_midi_recursive(website, relativeurl, folder)
            except Exception, e:
                print e.message

def download_midi_files():
    """Function parses website and extracts midi files for requested music pieces
    and saves midi files into folder
    """
    # Initialize main parser
    counter_pages = urllib2.urlopen(target_url.format(1))
    soup = BeautifulSoup(counter_pages, 'lxml')
    n_pages = soup.find('div', {'class':'pagination'})
    last_page = int(n_pages.text[32:34])+1

    for i in xrange(1, last_page):
        html_page = urllib2.urlopen(target_url.format(i))
        soup = BeautifulSoup(html_page, 'lxml')
        print '|=== Parent URL: {} ===|'.format(target_url.format(i))

        for link in soup.findAll('a'):
            url = '{}'.format(link.get('href'))
            if url.endswith(page_suffix) and 'scores' in url:
                midi_url = '{}{}{}'.format(base_url, url, ftype_suffix)
                print '/== Target url: {} ==\\'.format(midi_url)

                # Open target url
                midi_page = urllib2.urlopen(midi_url)
                soup = BeautifulSoup(midi_page, 'lxml')

                # Find link that ends with target_suffix
                for l in soup.findAll('a'):
                    try:
                        midi_url = '{}'.format(l.get('href'))
                    except UnicodeEncodeError, e:
                        print "Unicode Encode Error: {}".format(e.reason)

                    if midi_url.endswith(target_suffix):
                        load_midi_url = '{}{}'.format(base_url, midi_url)
                        print '[+] Load midi url: {}'.format(load_midi_url)

                        # Try to load midi file
                        try:
                            filename = os.path.basename(load_midi_url)
                            midi_file = urllib2.urlopen(load_midi_url)
                            fullpath = './{}/{}'.format(folder,filename)
                            if os.path.exists(fullpath):
                                print "Skipping {}".format(filename)
                            else:
                                print "Downloading {}".format(filename)
                                with open(fullpath, "wb") as local_file:
                                    content = midi_file.read()
                                    local_file.write(content)

                        except urllib2.HTTPError, e:
                            print "Http error: {}, {}".format(e.reason, url)
                            pass
                        except urllib2.URLError, e:
                            print "Url error: {}, {}".format(e.reason, url)
                            pass
                        break
                # Reduce number of request to avoid blocking
                time.sleep(randint(1,5))

def clean_directory():
    folder = 'music'
    file_names = [f for f in listdir("./{}/".format(folder)) if (isfile(join("./{}/".format(folder), f)) and ("format0" in f))]
    print len(file_names)
    if file_names:
        for item in file_names:
            os.remove('./{}/{}'.format(folder,item))
    else:
        print 'No bad files were found!'

def run_midi_load():
    # Create folder for midi files
    try:
        os.mkdir('./{}'.format(folder))
    except:
        pass

    # Define download_midi_files() URLs
    base_url = 'https://www.8notes.com'
    target_url = 'https://www.8notes.com/piano/classical/sheet_music/default.asp?page={}&orderby=6u'
    ftype_suffix = '?ftype=midi'
    page_suffix = '.asp'
    target_suffix = '.mid'

    # Define download_midi_recursive() URLs
    #website = "http://www.midiworld.com"
    #page = "classic.htm"
    website = "http://www.piano-midi.de"
    page = "midi_files.htm"

    # Define an output directories
    output_module = 'music_generation_module'
    folder = 'music'

    # Run download functions
    start = time.time()
    download_midi_recursive(website, page, folder)
    download_midi_files()

    # Delete broken files
    clean_directory()
    print 'Download finished in {} secs'.format(time.time() - start)

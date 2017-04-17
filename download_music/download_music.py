# Import packages
import os, urllib2, time
from random import randint
from os.path import isfile, join
from os import listdir
from bs4 import BeautifulSoup

# Main class
# To avoid loading similar URL's, initialise a dictionary that holds all used URL's
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
                fullpath = './{}/{}'.format(folder, filename)

                if os.path.exists(fullpath):
                    print "Skipping " + filename
                else:
                    print "Downloading " + filename
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
    n_pages = soup.find('div', {'class': 'pagination'})
    last_page = int(n_pages.text[32:34]) + 1

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
                            fullpath = './{}/{}'.format(folder, filename)
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
                time.sleep(randint(1, 5))


def download_music_n_scores():
    """Function parses music-score.com website and extracts midi files for requested music pieces
    and saves midi files into folder according to music complexity score
    """
    folder = 'level_'
    access_code = ''
    empty_url = 'http://www.music-scores.com'
    base_url = 'http://www.music-scores.com/skill/composer2.php?skill={}&name=Piano'
    full_url = 'http://www.music-scores.com/skill/composer2.php?pageNum_composer={}&totalRows_composer={}&skill={}&name=Piano'
    midi_load_url = 'http://www.music-scores.com//cgi-bin/midirubatomid.cgi?filename={}&accesscode={}&Submit2=Go'

    for comp in xrange(1, 10):
        # Create folder for midi files
        try:
            os.mkdir('./{}'.format(folder + str(comp)))
        except:
            pass
        print '|====| START PARSING COMPLEXITY {} |====| \n'.format(comp)
        level = comp
        n_files = 0
        pages = 0

        counter_pages = urllib2.urlopen(base_url.format(level))
        soup = BeautifulSoup(counter_pages, 'lxml')
        n_pages = soup.find('p', {'class': 'justify'}).text

        for item in n_pages.split(' '):
            try:
                n_files = int(item)
            except ValueError, e:
                pass

        pages = n_files / 20
        print '/=== Skill level: {}. Number of files to download: {} \\=== \n'.format(
            level, n_files)

        for i in xrange(pages + 1):
            # Open page with list of all available music files
            html_page = urllib2.urlopen(full_url.format(i, n_files, level))
            soup = BeautifulSoup(html_page, 'lxml')
            print '|=== Parent URL: {} ===|'.format(
                full_url.format(i, n_files, level))

            for link in soup.findAll('a'):
                url = '{}'.format(link.get('href'))
                if ('sheetmusic=' in url) and ('midi.' in url) and (
                        'Theory' not in url) and (url not in dict):
                    dict.add(url)
                    midi_url = '{}{}'.format(empty_url, url)
                    print '/== Target url: {} ==\\'.format(midi_url)

                    # Open page with particular midi file
                    midi_page = urllib2.urlopen(midi_url)
                    soup = BeautifulSoup(midi_page, 'lxml')

                    # Find link that contains name of music file
                    for l in soup.findAll('source'):
                        url = '{}'.format(l.get('src'))
                        if '.mp3' in url:
                            file_name = url.split('/')[2].split('.')[0]
                            load_midi_url = midi_load_url.format(
                                file_name, access_code)
                            file_name = '{}{}'.format(file_name, '.mid')
                            print '[+] Load midi url: {}'.format(load_midi_url)

                            # Try to load midi file
                            try:
                                filename = os.path.basename(file_name)
                                midi_file = urllib2.urlopen(load_midi_url)
                                fullpath = './{}/{}'.format(
                                    folder + str(comp), filename)
                                if os.path.exists(fullpath):
                                    print "Skipping {}".format(filename)
                                else:
                                    print "Downloading {}".format(filename)
                                    with open(fullpath, "wb") as local_file:
                                        content = midi_file.read()
                                        local_file.write(content)

                            except urllib2.HTTPError, e:
                                print "Http error: {}, {}".format(
                                    e.reason, url)
                                pass
                            except urllib2.URLError, e:
                                print "Url error: {}, {}".format(e.reason, url)
                                pass
                            break
                    # Reduce number of request to avoid blocking
                    time.sleep(randint(1, 5))


def clean_directory():
    folder = 'music'
    try:
        file_names = [
            f for f in listdir("./{}/".format(folder))
            if (isfile(join("./{}/".format(folder), f)) and ("format0" in f))
        ]
        print len(file_names)
        if file_names:
            for item in file_names:
                os.remove('./{}/{}'.format(folder, item))
        else:
            print 'No bad files were found!'
    except OSError, e:
        print "No folder '{}'".format(folder)
        pass


def run_midi_load():
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

    # Run download functions
    start = time.time()
    #download_midi_recursive(website, page, folder)
    #download_midi_files()
    download_music_n_scores()

    # Delete broken files
    clean_directory()
    print 'Download finished in {} secs'.format(time.time() - start)


run_midi_load()

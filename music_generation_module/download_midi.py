# Import packages
from bs4 import BeautifulSoup
import os, re, urllib2


# Main class
def download_midi_recursive(website, page, folder):
    """Recursively downloads midi files from specified website
    and stores it under 'music' folder
    """
    dict = set()
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
                fullpath = folder + '/' + filename

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

# website = "http://www.midiworld.com"
# page = "classic.htm"

website = "http://www.piano-midi.de"
page = "midi_files.htm"

folder = './music'
download_midi_recursive(website, page, folder)

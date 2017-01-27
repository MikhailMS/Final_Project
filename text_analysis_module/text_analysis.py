# Import packages
import ebooklib
from ebooklib import epub

from bs4 import BeautifulSoup

import time
from os import listdir
from os.path import isfile, join
# Import modules


# Main class
def build_sentiment_model():
    """Trains the sentiment model that is used for determining
    sentiment of the text
    Returns a sentiment model
    """

def sentiment_analysis(text, model):
    """Takes 'text' and 'model' variables: representation of the text to be analysed
    and sentiment model respectively.
    Returns a sentiment score for given text
    """

def read_in_epub(book_name):
    """Function reads in specific ePub book and
    outputs set of files that are believed to be different chapters.
    """
    book = epub.read_epub(book_name)

    #for item in book.get_items():
    #    print item
    i = 1
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        #print item.content # html format
        file_name = 'output_'+str(i)+'.txt'
        if item.is_chapter():
            with open(file_name, 'a') as output:
                output.write(item.get_body_content())
        #print item.get_body_content() # returns content inside tags with 'body' class
        i = i+1
        #print item.get_content() same to content attribute
        #print item.is_chapter() # returns True if object is a chapter

def extract_text():
    """Reads in an output of 'read_in_epub()' function
    and extracts only textual(important) data from those files
    and outputs files with clean text, that would be used for analysis
    """
    def clean_string(x):
        """Returns clean str, without 'p' tag and leftovers of convertion html-> str"""
        return x.replace('<p>','').replace('</p>','').replace("'",'`').replace('\xe2\x80\x94',' ').replace("\"",'')

    files = [f for f in listdir(".") if (isfile(join(".", f)) and ("output_" in f))]
    for file_name in files:
        page = open(file_name, 'r')
        soup = soup = BeautifulSoup(page, "lxml")
        page = soup.find_all('p')
        strings = list()

        for sub_str in page:
            strings.append(clean_string(str(sub_str)))

        file_name = "clean_"+file_name
        with open(file_name, 'a') as output:
            for string in strings:
                output.write("%s\n" % string)

start = time.time()
print extract_text()
print time.time() - start

# Import packages
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import time
from os import listdir
from os.path import isfile, join
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from operator import itemgetter
# Import modules

# Main class
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

def sentiment_analysis(text):
    """'text' variable: representation of the text to be analysed.
    Returns a sentiment score for given text piece.
    To access values, use following keys:
    'neg' - negative score
    'pos' - positive score
    'neu' - neural score
    """
    sentences = []
    scores = []
    list_sentences = tokenize.sent_tokenize(text)
    sentences.extend(list_sentences)

    sentiment_analyser = SentimentIntensityAnalyzer()
    for sentence in sentences:
        score = sentiment_analyser.polarity_scores(sentence)
        scores.insert(0,score)

    total_score = {key:sum(map(itemgetter(key), scores)) for key in scores[0]}
    if total_score['neg']>total_score['pos']:
        return -abs(total_score['neg']/len(scores))
    else:
        return total_score['pos']/len(scores)

def main():
    # Process text and clean it
    book_name = "o-henry.epub"
    read_in_epub(book_name)
    extract_text()

    # Start sliding window to get text features
    sentiment_analysis()

start = time.time()
#main()
print time.time() - start

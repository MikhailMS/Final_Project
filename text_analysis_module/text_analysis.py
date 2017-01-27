# Import packages
import time, re, collections, ebooklib, nltk
from ebooklib import epub
from bs4 import BeautifulSoup
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

def lexical_density_and_readability_analysis(text, allow_digits=False):
    """'text' variable: representation of the text to be analysed.
    Returns a pair of values:
        lexical density score
        readability score
    """
    print "[+] Tokenizing text..."
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tokens = tokenizer.tokenize(text)

    print "[+] Tagging tokens..."
    tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())
    tagged_tokens = tagger.tag(tokens)

    print "[+] Tallying tags..."
    lexical_counter = collections.Counter()
    personal_pronoun_counter = collections.Counter()
    adjective_counter = collections.Counter()
    adverb_counter = collections.Counter()
    noun_counter = collections.Counter()
    verb_counter = collections.Counter()

    for token in tagged_tokens:

        if token[1] == None:
            continue

        # Adjectives
        elif 'JJ' in token[1]:
            lexical_counter[token[0]] += 1
            adjective_counter[token[0]] += 1

        elif 'JJR' in token[1]:
            lexical_counter[token[0]] += 1
            adjective_counter[token[0]] += 1

        elif 'JJS' in token[1]:
            lexical_counter[token[0]] += 1
            adjective_counter[token[0]] += 1

        # Nouns
        elif 'NN' in token[1]:
            lexical_counter[token[0]] += 1
            noun_counter[token[0]] += 1

        elif 'NNP' in token[1]:
            lexical_counter[token[0]] += 1
            noun_counter[token[0]] += 1

        elif 'NNPS' in token[1]:
            lexical_counter[token[0]] += 1
            noun_counter[token[0]] += 1

        elif 'NNS' in token[1]:
            lexical_counter[token[0]] += 1
            noun_counter[token[0]] += 1

        # Adverbs
        elif 'RB' in token[1]:
            lexical_counter[token[0]] += 1
            adverb_counter[token[0]] += 1

        elif 'RBR' in token[1]:
            lexical_counter[token[0]] += 1
            adverb_counter[token[0]] += 1

        elif 'RBS' in token[1]:
            lexical_counter[token[0]] += 1
            adverb_counter[token[0]] += 1

        # Verbs
        elif 'VB' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        elif 'VBD' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        elif 'VBG' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        elif 'VBN' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        elif 'VBP' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        elif 'VBZ' in token[1]:
            lexical_counter[token[0]] += 1
            verb_counter[token[0]] += 1

        # Personal pronouns
        elif 'PPS' in token[1]:
            lexical_counter[token[0]] += 1
            personal_pronoun_counter[token[0]] += 1

    print "[+] Counting sentences..."
    total_sentences = len(nltk.sent_tokenize(text.decode('utf-8')))

    print "[+] Split text into words..."
    if allow_digits:
        words = re.findall(r"['\-\w]+", text)
    else:
        words = re.findall(r"['\-A-Za-z]+", text)

    total_words = 0.0
    total_chars = 0
    for word in words:

        word = word.strip(r"&^%$#@!")

        # Allow hyphenated words, but not hyphens as words on their own.
        if word == '-':
            continue

        # Record lengths of every word
        length = len(word)

        # Record total number of words and chars
        total_words += 1
        total_chars += length

    # Calculate the lexical density of the text.
    #total_unique_words = len(counters[0])
    total_meaningful_words = sum(lexical_counter.values())
    lexical_density = 100.0 * total_meaningful_words / float(total_words)

    # Calculate the ARI (readability) score
    ASL = total_words / float(total_sentences)
    ALW = total_chars / float(total_words)
    ARI_score = (0.5 * ASL) + (4.71 * ALW) - 21.43

    return round(lexical_density, 2), round(ARI_score, 2)

def main():
    # Process text and clean it
    book_name = "o-henry.epub"
    read_in_epub(book_name)
    extract_text()

    # Start sliding window to get text features
    sentiment_analysis()
    lexical_density_and_readability_analysis()

start = time.time()
#main()
input_file = 'clean_output_15.txt'
print "[+] Reading text from '" + input_file + "'..."
text = open(input_file).read().lower()
print lexical_density_and_readability_analysis(text)
print time.time() - start

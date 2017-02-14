# Import packages
import time, re, collections, ebooklib, pickle, multiprocessing, nltk
from ebooklib import epub
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from operator import itemgetter
from utils import *

# Main class
def read_in_epub(book_name):
    """Function reads in specific ePub book and
    outputs set of files that are believed to be different chapters.
    """
    book = epub.read_epub(book_name)

    i = 1
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        file_name = 'output_' + str(i) + '.txt'
        if item.is_chapter():
            with open(file_name, 'a') as output:
                output.write(item.get_body_content())  # write content inside tags with 'body' class
        i += 1


def extract_text():
    """Reads in an output of 'read_in_epub()' function
    and extracts only textual(important) data from those files
    and outputs files with clean text, that would be used for analysis
    """

    def clean_string(x):
        """Returns clean str, without 'p' tag and leftovers of conversion html-> str"""
        return x.replace('<p>', '').replace('</p>', '').replace("'", '`').replace('\xe2\x80\x94', ' ').replace("\"", '')

    files = [f for f in listdir(".") if (isfile(join(".", f)) and ("output_" in f))]
    for file_name in files:
        page = open(file_name, 'r')
        soup = BeautifulSoup(page, "lxml")
        page = soup.find_all('p')
        strings = list()

        for sub_str in page:
            strings.append(clean_string(str(sub_str)))

        file_name = "clean_" + file_name
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
    sentences.extend(tokenize.sent_tokenize(text))

    # Use NLTK built-in sentiment analyzer
    sentiment_analyser = SentimentIntensityAnalyzer()
    for sentence in sentences:
        score = sentiment_analyser.polarity_scores(sentence)
        scores.insert(0, score)  # Record polarity score

    # Sum up all scores within the key
    total_score = {key: sum(map(itemgetter(key), scores)) for key in scores[0]}

    if total_score['neg'] > total_score['pos']:
        sc = -abs(total_score['neg'] / len(scores))
        print ('\n' + yellow + '[+] Sentiment score... ' + normal + str(sc))
        return round(sc, 2)
    else:
        sc = total_score['pos'] / len(scores)
        print ('\n' + yellow + '[+] Sentiment score... ' + normal + str(sc))
        return round(sc, 2)


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

        if token[1] is None:  # if token[1] == None: (from stable version)
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
    print ('|#|' + yellow + '[+] Total number of sentences... ' + normal + str(total_sentences))

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
    print ('|##|' + yellow + ' Total words... ' + normal + str(total_words))
    print ('|###|' + yellow + ' Total chars... ' + normal + str(total_chars))

    # Calculate the lexical density of the text.
    total_meaningful_words = sum(lexical_counter.values())
    lexical_density = 100.0 * total_meaningful_words / float(total_words)

    # Calculate the ARI (readability) score
    asl = total_words / float(total_sentences)
    alw = total_chars / float(total_words)
    ari_score = (0.5 * asl) + (4.71 * alw) - 21.43

    print ('|####|' + yellow + ' Lexical density score... ' + normal + str(round(lexical_density, 2)) + '%')
    print ('|#####|' + yellow + ' Readability score... ' + normal + str(round(ari_score, 2)))

    return round(lexical_density, 2), round(ari_score, 2)


def sliding_window(text):
    """Function slides through given text with fixed window_size and fixed
    slide_step, applyind sentiment_analysis() and lexical_density_and_readability_analysis()
    functions to every piece of text, that falls into window.
    Returns a set of data that is a representation of
    extraxted features from given text
    """
    window_size = 200  # Assumably average amount of words that could be read out load per minute
    slide_size = 50  # For efficiency purpose, slid_size should be 1/4 of window_size
    extracted_features = []  # Stores features extracted from text piece
    text_words = []

    for word in text.split():  # Get a list of all words in the teext sample
        text_words.append(word)

    if (len(text_words) <= window_size) or (len(text_words) - window_size <= slide_size):
        sample = ' '.join(text_words)  # Join words into set of sentence, that would be analysed
        print '\n===' + blue + ' Analysing new sentence...' + normal + '==='
        print ('\n' + green + '[+] Start sentiment analysis...' + normal)
        sentiment = sentiment_analysis(sample)
        print ('\n' + green + 'Sentiment analysis is done!' + normal)

        print ('\n' + green + '[+] Start lexical density & \n readability analysis...' + normal)
        lexical, readability = lexical_density_and_readability_analysis(sample)
        print ('\n' + green + 'Lexical density & readability analysis is done!' + normal)
        extracted_features.append((sentiment, (lexical, readability)))
    else:
        for i in xrange(0, len(text_words) - window_size, slide_size):
            sample = ' '.join(text_words[i:i + 200])
            print '\n===' + blue + ' Analysing new sentence...' + normal + '==='
            print ('\n' + green + '[+] Start sentiment analysis...' + normal)
            sentiment = sentiment_analysis(sample)
            print ('\n' + green + 'Sentiment analysis is done!' + normal)

            print ('\n' + green + '[+] Start lexical density & \n readability analysis...' + normal)
            lexical, readability = lexical_density_and_readability_analysis(sample)
            print ('\n' + green + 'Lexical density & readability analysis is done!' + normal)
            extracted_features.append((sentiment, (lexical, readability)))

    return extracted_features


def identify_number_cores(file_names):
    """ Takes a list of files that would be analysed
    and returns the number of cores, that should be used for the task
    """
    available_cores = multiprocessing.cpu_count()
    files_for_analys = len(file_names)

    if available_cores > files_for_analys:
        return files_for_analys  # Number of files in the list
    else:
        return available_cores  # Number of available cores


def worker(file_names, send_end):
    """Represents a single worker that completes sliding_window() function
    and returns results back to main (parent) process
    """
    result = []
    # Start sliding window to get text features
    for item in file_names:
        print "\n [+] Reading text from '" + item + "'..."
        text_sample = open(item).read().lower()
        result.append(sliding_window(text_sample))
    send_end.send(result)


def split_tasks(file_names, cores_available):
    """Splits files across all available cores"""
    k, m = divmod(len(file_names), cores_available)
    return list((file_names[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(cores_available)))


def text_analysis_helper(file_names):
    """Helper function to make code more readable:
    Runs sliding_window() function on all clean text files ->
    Gets results into one variable ->
    Saves and returns results (unless no data found)
    """
    if len(file_names) != 0:  # Check if text data exists, if so
        results = []
        print '\n===' + blue + ' STARTING ANALYSIS ' + normal + '==='
        for file_name in file_names:
            print "\n [+] Reading text from '" + file_name + "'..."
            text = open(file_name).read().lower()
            results.append(sliding_window(text))

        print '\n===' + blue + ' RESULTS ' + normal + '==='

        # Save results to save time on next run
        pickle.dump(results, open("extracted_features.p", "wb"))

        return results
    else:  # Otherwise
        print '\n===' + red + ' NO TEXT DATA FOUND. EXITING... ' + normal + '==='
        return None


def text_analysis_helper_parallel(file_names):
    """Helper function to make code more readable:
    Assigns tasks to available cores -> Receives results from cores ->
    Puts results into one variable ->
    Saves and returns results (unless no data found)
    """
    if len(file_names) != 0:  # Check if text data exists, if so
        jobs = []
        available_cores = identify_number_cores(file_names)  # Identify required number of cores
        file_names = split_tasks(file_names, available_cores)  # Split tasks between cores

        pipe_list = []
        print '\n===' + blue + ' STARTING ANALYSIS ' + normal + '==='
        # Run workers (one worker per core)
        for i in xrange(available_cores):
            recv_end, send_end = multiprocessing.Pipe(False)
            p = multiprocessing.Process(target=worker, args=(file_names[i], send_end))
            jobs.append(p)
            pipe_list.append(recv_end)
            p.start()

        for proc in jobs:
            proc.join()

        results = [x.recv() for x in pipe_list]  # Combine all results
        results = [x for sublist in results for x in sublist]  # Flat results into 1D List

        output_file = "extracted_features.p"
        print '\n===' + blue + ' SAVE RESULTS TO: ' + normal + output_file + '==='
        # Save results to save time on next run
        pickle.dump(results, open(output_file, "wb"))

        print '\n===' + blue + ' RESULTS ' + normal + '==='
        return results
    else:  # Otherwise
        print '\n===' + red + ' NO TEXT DATA FOUND. EXITING... ' + normal + '==='
        return None


def run_text_analysis(book_name):
    """Methods runs sliding_window() function over all text files and
    returns a set of extracted features as an array
    in the form -> (sentiment, (lexical_score, readability_score))
    """
    # Find file that holds extracted features
    dump_results = [f for f in listdir(".") if (isfile(join(".", f)) and ("extracted_features" in f))]

    # If such file exists, then load file and return features
    if dump_results:
        print '\n===' + turquoise + ' PREVIOUS RESULTS FOUND... ' + normal + dump_results[0] + '==='
        print '\n===' + turquoise + ' LOADING RESULTS...' + normal + '==='
        results = pickle.load(open(dump_results[0], 'rb'))
        print '\n===' + turquoise + ' LOAD IS COMPLETED!' + normal + '==='
        return results
    # Otherwise initiate feature extraction process
    else:
        file_names = [f for f in listdir(".") if (isfile(join(".", f)) and ("clean_output_" in f))]
        if file_names:  # If clean_output files already exist, skip load & clean stages
            print '\n===' + turquoise + ' CLEAN DATA FOUND... ' + normal + '==='
            return text_analysis_helper(file_names)  # Complete analysis
        else:
            # Otherwise load text and clean it
            book_names = [f for f in listdir(".") if (isfile(join(".", f)) and (".epub" in f))]
            print '\n===' + blue + ' READ IN THE BOOK... ' + normal + book_names[0] + '==='
            read_in_epub(book_names[0])
            print '\n===' + blue + ' CLEAN UP THE TEXT...' + normal + '==='
            extract_text()

            # Give user a chance to manually clean(check) output files to improve results
            while True:
                user_input = raw_input(
                    "\n You are given option to do manual cleaning.\n Type in [Done]/[done] or [d], when finished, otherwise press any key to skip: ")
                if user_input == 'Done' or user_input == 'done' or user_input == 'd':
                    print '\n===' + blue + ' MANUAL CLEANING IS DONE... ' + normal + '==='
                    break
                else:
                    print '\n===' + red + ' MANUAL CLEANING HAS BEEN SKIPPED... ' + normal + '==='
                    break

            file_names = [f for f in listdir(".") if (isfile(join(".", f)) and ("clean_output_" in f))]
            return text_analysis_helper(file_names)  # Complete analysis


def run_text_analysis_in_parallel():
    """Methods runs sliding_window() function over all text files on all
    available cpu_cores and returns a set of extracted features as an array
    in the form -> (sentiment, (lexical_score, readability_score))
    """
    # Find file that holds extracted features
    dump_results = [f for f in listdir(".") if (isfile(join(".", f)) and ("extracted_features" in f))]

    # If such file exists, then load file and return features
    if dump_results:
        print '\n===' + turquoise + ' PREVIOUS RESULTS FOUND... ' + normal + dump_results[0] + '==='
        print '\n===' + turquoise + ' LOADING RESULTS...' + normal + '==='
        results = pickle.load(open(dump_results[0], 'rb'))
        print '\n===' + turquoise + ' LOAD IS COMPLETED!' + normal + '==='
        return results
    # Otherwise initiate feature extraction process
    else:

        file_names = [f for f in listdir(".") if (isfile(join(".", f)) and ("clean_output_" in f))]

        if file_names:  # If clean_output files exist, skip load & clean stages
            print '\n===' + turquoise + ' CLEAN DATA FOUND... ' + normal + '==='
            return text_analysis_helper_parallel(file_names)  # Complete analysis
        else:
            # Find books in root directory
            book_names = [f for f in listdir(".") if (isfile(join(".", f)) and (".epub" in f))]
            # Otherwise load text and clean it
            print '\n===' + blue + ' READ IN THE BOOK... ' + normal + book_names[0] + ' ==='
            read_in_epub(book_names[0])
            print '\n===' + blue + ' CLEAN UP THE TEXT...' + normal + '==='
            extract_text()

            # Give user a chance to manually clean output files to improve results
            while True:
                user_input = raw_input(
                    "\n You are given option to do manual cleaning. Type in [Done]/[done] or [d], when finished, otherwise press any key to skip: ")
                if user_input == 'Done' or user_input == 'done' or user_input == 'd':
                    print '\n===' + blue + ' MANUAL CLEANING IS DONE... ' + normal + '==='
                    break
                else:
                    print '\n===' + red + ' MANUAL CLEANING HAS BEEN SKIPPED... ' + normal + '==='
                    break

            file_names = [f for f in listdir(".") if (isfile(join(".", f)) and ("clean_output_" in f))]
            return text_analysis_helper_parallel(file_names)  # Complete analysis

# Test run
# start = time.time()
# book_names = [f for f in listdir(".") if (isfile(join(".", f)) and (".epub" in f))]
# features = run_text_analysis_in_parallel(book_names)
# print features
# print time.time() - start

# Import packages
import collections, itertools, time
import nltk.classify.util
from nltk.metrics import precision, recall, f_measure, BigramAssocMeasures
from nltk.corpus import stopwords, movie_reviews, subjectivity
from nltk.collocations import BigramCollocationFinder
from nltk.classify import NaiveBayesClassifier
from nltk.probability import FreqDist, ConditionalFreqDist
#from nltk.sentiment import SentimentAnalyzer
#from nltk.sentiment.util import *

# Main class
""" Approach number 1 """
def sentiment_model():
    """Builds a sentiment model"""
    n_instances = 100
    subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
    obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]

    train_subj_docs = subj_docs[:80]
    test_subj_docs = subj_docs[80:100]
    train_obj_docs = obj_docs[:80]
    test_obj_docs = obj_docs[80:100]
    training_docs = train_subj_docs+train_obj_docs
    testing_docs = test_subj_docs+test_obj_docs
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    #len(unigram_feats)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)
    for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
        print('{0}: {1}'.format(key, value))

""" Approach number 2 """
stopset = set(stopwords.words('english'))
def filtered_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    #words = [word for word in words if word not in stopset] # overall results drop by 2-3%
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def sentiment_model_2():
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(filtered_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(filtered_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    print 'pos precision:', precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', recall(refsets['pos'], testsets['pos'])
    print 'pos F-measure:', f_measure(refsets['pos'], testsets['pos'])

    print 'neg precision:', precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', recall(refsets['neg'], testsets['neg'])
    print 'neg F-measure:', f_measure(refsets['neg'], testsets['neg'])

""" Approach number 3 """
def word_feats(words):
    return dict([(word, True) for word in words])

def best_word_feats(words):
    return dict([(word, True) for word in words if word in bestwords])

def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_feats(words))
    return d

def evaluate_classifier(featx):
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', recall(refsets['neg'], testsets['neg'])
    classifier.show_most_informative_features()

start = time.time()

word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

for word in movie_reviews.words(categories=['pos']):
    word_fd[word.lower()] += 1
    label_word_fd['pos'][word.lower()] += 1
for word in movie_reviews.words(categories=['neg']):
    word_fd[word.lower()] += 1
    label_word_fd['neg'][word.lower()] += 1

pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()
total_word_count = pos_word_count + neg_word_count

word_scores = {}

for word, freq in word_fd.iteritems():
    pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
        (freq, pos_word_count), total_word_count)
    neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
        (freq, neg_word_count), total_word_count)
    word_scores[word] = pos_score + neg_score

best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
bestwords = set([w for w, s in best])

print time.time() - start

print 'evaluating single word features' # Test case 1
evaluate_classifier(word_feats)

print 'evaluating best word features' # Test case 2
evaluate_classifier(best_word_feats)

print 'evaluating best words + bigram chi_sq word features' # Test case 3
evaluate_classifier(best_bigram_word_feats)
print time.time() - start

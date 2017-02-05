# Import packages
import collections, itertools, time, nltk.classify.util
from nltk.metrics import precision, recall, f_measure, BigramAssocMeasures
from nltk.corpus import stopwords, movie_reviews, subjectivity
from nltk.collocations import BigramCollocationFinder
from nltk.classify import NaiveBayesClassifier
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.probability import FreqDist, ConditionalFreqDist

# Main class
""" Approach number 1 """
stopset = set(stopwords.words('english'))
def filtered_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    #words = [word for word in words if word not in stopset] # overall results drop by 2-3%
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def sentiment_model():
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

""" Approach number 2 """
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

def sentiment_model_2(featx):
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    classifier = NaiveBayesClassifier.train(trainfeats)
    #classifier = SklearnClassifier(LinearSVC()).train(trainfeats) # gives improvement in time
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
    #classifier.show_most_informative_features() # Doesn't work with SVC classifier

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

print time.time() - start # Time when values are processed

print 'evaluating single word features' # Test case 1
sentiment_model_2(word_feats)
print 'evaluating single word features is done at: ', time.time() - start # Time when Test case 1 is complete

print 'evaluating best word features' # Test case 2
sentiment_model_2(best_word_feats)
print 'evaluating best word features is done at: ', time.time() - start # Time when Test case 2 is complete

print 'evaluating best words + bigram chi_sq word features' # Test case 3
sentiment_model_2(best_bigram_word_feats)
print 'evaluating best words + bigram chi_sq word features is done at: ', time.time() - start # Time when Test case 3 is complete

# Import packages
import unittest2 as unittest
from text_analysis import sentiment_analysis
# Tests go here
class TestTextAnalysis(unittest.TestCase):
    
    def test_sentiment_analysis_negative(self):
        score = sentiment_analysis("It was one of the worst movies I've seen, despite good reviews. \
        Unbelievably bad acting!! Poor direction. VERY poor production. \
        The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!")
        self.assertLessEqual(score, 0)
    def test_sentiment_analysis_positive(self):
        score = sentiment_analysis("VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!! \
        The book was good. \
        VADER is VERY SMART, handsome, and FUNNY. The movie was too good. \
        Sentiment analysis with VADER has never been this good. VADER is smart, handsome, and funny!")
        self.assertGreaterEqual(score, 0)

# To allow output in console
if __name__ == '__main__':
    unittest.main()

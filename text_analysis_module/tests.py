# Import packages
import unittest2 as unittest
from text_analysis import sentiment_analysis, split_tasks, identify_number_cores
from text_analysis import lexical_density_and_readability_analysis
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
    def test_lexical_density_and_readability_analysis(self):
        density, readability = lexical_density_and_readability_analysis("VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!! \
        The book was good. \
        VADER is VERY SMART, handsome, and FUNNY. The movie was too good. \
        Sentiment analysis with VADER has never been this good. VADER is smart, handsome, and funny!")
        self.assertGreater(density,0)
        self.assertIsNotNone(density)
        self.assertGreater(readability,0)
        self.assertIsNotNone(readability)
    def test_split_tasks(self):
        file_names = ['file_1']
        avail_cores_1 = identify_number_cores(file_names)
        test_1 = split_tasks(file_names, avail_cores_1)

        file_names = ['file_1','file_2']
        avail_cores_2 = identify_number_cores(file_names)
        test_2 = split_tasks(file_names, avail_cores_2)

        file_names = ['file_1','file_2','file_3']
        avail_cores_3 = identify_number_cores(file_names)
        test_3 = split_tasks(file_names, avail_cores_3)

        file_names = ['file_1','file_2','file_3','file_4']
        avail_cores_4 = identify_number_cores(file_names)
        test_4 = split_tasks(file_names, avail_cores_4)

        file_names = ['file_1','file_2','file_3','file_4','file_5']
        avail_cores_5 = identify_number_cores(file_names)
        test_5 = split_tasks(file_names, avail_cores_5)

        file_names = ['file_1','file_2','file_3','file_4','file_5','file_6']
        avail_cores_6 = identify_number_cores(file_names)
        test_6 = split_tasks(file_names, avail_cores_6)

        file_names = ['file_1','file_2','file_3','file_4','file_5','file_6','file_7']
        avail_cores_7 = identify_number_cores(file_names)
        test_7 = split_tasks(file_names, avail_cores_7)

        self.assertEqual(len(test_1), avail_cores_1)
        self.assertEqual(len(test_2), avail_cores_2)
        self.assertEqual(len(test_3), avail_cores_3)
        self.assertEqual(len(test_4), avail_cores_4)
        self.assertEqual(len(test_5), avail_cores_5)
        self.assertEqual(len(test_6), avail_cores_6)
        self.assertEqual(len(test_7), avail_cores_7)

# To allow output in console
if __name__ == '__main__':
    unittest.main()

import argparse
import time

# Import modules
from text_analysis_module import run_text_analysis_in_parallel # , plot_features
from music_generation_module import run_complexity_analysis, run_music_composition, run_custom_music_composition, run_tests, music_analysis
from mapping_module import map_text_parameters


# Main class
def run_application(test_enabled='false', compl_analysis_enabled='false', custom_query=[]):
    """Main function that runs whole application:
    Starting with text analysis -> train LSTM model ->
    Use text features to generate music
    It is advised to keep group_size and music_length parameters of same value
    """
    # Run text analysis (using multiprocessing package)
    # TODO: This method contains some bugs, so disable for now
    # run_text_analysis_in_parallel()

    # Run text feature mapping onto music parameters
    sent_score, lex_score, read_score = map_text_parameters(group_size=5)

    # Run music analysis
    pcs = music_analysis()

    if custom_query:
        print 'Custom music composition is requested with following arguments {}, for [sentiment_score, lexical_score, complexity_score, length]'.format(custom_query)
        run_custom_music_composition(pcs, custom_query)
    else:
        # Run music generation
        run_music_composition(pcs, sent_score, lex_score, read_score, music_length= 5, epochs=6500)

    if compl_analysis_enabled == 'true':
        # Run music complexity analysis
        complexity_stats = run_complexity_analysis(visual=False)

    if test_enabled == 'true':
        # Run final tests to ensure music has been generated correctly
        run_tests(complexity_stats, sent_score_mapped=sent_score, read_score_mapped=read_score) # - FOR TEST PURPOSES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Music composition CLI')
    parser.add_argument('-t', '--test', metavar='', type=str, dest='test_enabled',
                        help='Set to true, if you want to test composed music', default='false')
    parser.add_argument('-c', '--complexity-analysis', metavar='', type=str, dest='compl_analysis_enabled',
                        help='Set to true, if you want to analyse complexity of the music set, used for training', default='false')
    parser.add_argument('-q', '--quick-compos', metavar='', type=str, dest='quick_composition',
                        help='Submit a custom query for music compposition in the form [sentiment_score, lexical_score, complexity_score, length], ie [1,1,3,2]', default='1,1,3,2')

    args = parser.parse_args()
    args.test_enabled            = args.test_enabled.lower()
    args.compl_analysis_enableed = args.compl_analysis_enabled.lower()
    args.quick_composition       = args.quick_composition.split(',')

    start = time.time()
    run_application(test_enabled=args.test_enabled,
                    compl_analysis_enabled=args.compl_analysis_enabled,
                    custom_query=args.quick_composition) # - ONLY COMMAND TO EXIST HERE
    print 'Application has completed in {:.02f}seconds'.format(time.time()-start)

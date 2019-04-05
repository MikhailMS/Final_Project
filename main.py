import argparse

# Import modules
from text_analysis_module import run_text_analysis_in_parallel # , plot_features
from music_generation_module import run_complexity_analysis, run_music_composition, run_tests, music_analysis
from mapping_module import map_text_parameters


# Main class
def run_application(test_enabled='false'):
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

    # Run music generation
    run_music_composition(pcs, sent_score, lex_score, read_score, music_length= 5, epochs=6500)

    # Run music complexity analysis
    complexity_stats = run_complexity_analysis(visual=False)

    if test_enabled == 'true':
        # Run final tests to ensure music has been generated correctly
        run_tests(complexity_stats, sent_score_mapped=sent_score, read_score_mapped=read_score) # - FOR TEST PURPOSES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Music composition CLI')
    parser.add_argument('-t', '--test', metavar='', type=str, dest='test_enabled', help='Set to true, if you want to test composed music', default='false')

    args = parser.parse_args()

    run_application(test_enabled=args.test_enabled) # - ONLY COMMAND TO EXIST HERE

# Import modules
from text_analysis_module import run_text_analysis_in_parallel, plot_features
from music_generation_module import run_music_composition, music_analysis
from mapping_module import map_text_parameters

# Main class
def run_application():
    """Main function that runs whole application:
    Starting with text analysis -> train LSTM model ->
    Use text features to generate music
    """
    # Run text analysis (using multiprocessing package)
    #run_text_analysis_in_parallel()

    # Run text feature mapping onto music parameters
    #sent_score, lex_score, read_score = map_text_parameters()
    #print 'Length of sentiment array: {}, lexical density score: {}, readability score: {}'.format(len(sent_score), len(lex_score), len(read_score))

    # Run music generation
    run_music_composition(epochs=7500) # - FOR TEST PURPOSES



if __name__ == '__main__':
    #run_application() # - ONLY COMMAND TO EXIST HERE
    complexity_scores = music_analysis()
    #print len(complexity_scores)

    """level_1 = {key: value for (key, value) in complexity_scores.iteritems() if value==1}
    level_2 = {key: value for (key, value) in complexity_scores.iteritems() if value==2}
    level_3 = {key: value for (key, value) in complexity_scores.iteritems() if value==3}
    level_4 = {key: value for (key, value) in complexity_scores.iteritems() if value==4}
    level_5 = {key: value for (key, value) in complexity_scores.iteritems() if value==5}
    level_6 = {key: value for (key, value) in complexity_scores.iteritems() if value==6}
    level_7 = {key: value for (key, value) in complexity_scores.iteritems() if value==7}
    level_8 = {key: value for (key, value) in complexity_scores.iteritems() if value==8}
    level_9 = {key: value for (key, value) in complexity_scores.iteritems() if value==9}

    print 'Level 1 has {} files; Level 2 has {} files; Level 3 has {} files;\n Level 4 has {} files; Level 5 has {} files; Level 6 has {} files;\n Level 7 has {} files; Level 8 has {} files; Level 9 has {} files;\n '.format(len(level_1), len(level_2), len(level_3),
                                                                                                                                                                                                                          len(level_4), len(level_5), len(level_6),
                                                                                                                                                                                                                                len(level_7), len(level_8), len(level_9))
"""

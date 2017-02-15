# Import modules
from text_analysis_module import run_text_analysis_in_parallel
from music_generation_module import run_music_composition

# Main class
def run_application():
    """Main function that runs whole application:
    Starting with text analysis -> train LSTM model ->
    Use text features to generate music
    """
    # Run text analysis (using multiprocessing package)
    text_features = run_text_analysis_in_parallel()

    # Run text feature mapping onto music parameters


    # Run music generation
    run_music_composition()

if __name__ == '__main__':
    #run_application() # - ONLY COMMAND TO EXIST HERE
    #run_text_analysis_in_parallel() # - FOR TEST PURPOSES
    #run_music_composition() # - FOR TEST PURPOSES

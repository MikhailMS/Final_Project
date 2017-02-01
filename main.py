# Import packages


# Import modules
from text_analysis_module import run_text_analysis_in_parallel

def run_application():
    """Main function that runs whole application:
    Starting with text analysis -> train LSTM model ->
    Use text features to generate music
    """
    # Find books in root directory
    book_names = [f for f in listdir(".") if (isfile(join(".", f)) and (".epub" in f))]
    # Run text analysis (using multiprocessing package)
    text_features = run_text_analysis_in_parallel(book_name[0])

    # Run model training

    # Run text feature mapping onto music parameters

    # Run music generation

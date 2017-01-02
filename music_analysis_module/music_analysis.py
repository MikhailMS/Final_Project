# Import packages

# Import modules
from music_input_module import MusicInput

# Main class
class MusicAnalysis():

    """Initialization"""
    def __init__(self, path_to_file):
        self.music_input = MusicInput(path_to_file)

    """Overwrite default method to be more informative"""
    def __str__(self):
        return self.music_input

    """Loads MIDI file that would be processed"""
    def music_analysis():
        return False

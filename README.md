# Final year project - musification of text data.
This is an initial project structure - no functionality has been added yet.
List of functionality that would be added later in the priority order:
  1. Music input
  2. Music analysis
  3. Text analysis
  4. Building neural network
  5. Music output
  6. Text mapping

# Installation procedure:
  1. Clone the repo
  2. Run 'pip install -r requirements.txt'
  3. Create folder 'midi' with MIDI files
  4. Place that folder in root directory of the application
  5. Run 'main.py' file giving a path to the text, that should be analysed

# NOTE:
Application has been created under macOS Sierra 10.12 and Python 2.7.10
If getting 'DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project.'
error, than on step 2, change command to:  
'sudo pip install -r requirements.txt --ignore-installed six'

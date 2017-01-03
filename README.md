# Final year project - musification of text data.
## This is an initial project structure - no functionality has been added yet.
List of functionality that would be added later in the priority order:
- [ ] Music input
- [ ] Music analysis
- [ ] Text analysis
- [ ] Building neural network
- [ ] Music output
- [ ] Text mapping

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. Create folder 'midi' with MIDI files
  4. Place that folder in root directory of the application
  5. Run 'main.py' file giving a path to the text, that should be analysed

## **_NOTE_**:
Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

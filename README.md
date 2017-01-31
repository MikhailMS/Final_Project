# Final year project - musification of text data.

## **Functionality is under development.**

## List of functionality that would be added later in the priority order:

 - [ ] Music input

 - [ ] Music analysis - **in progress**

 - [x] Text analysis - **_Available in two forms: single processing & multi processing (default choice)_**

 - [ ] Building neural network

 - [ ] Music output

 - [ ] Text mapping

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. Create folders: __'music'__ with MIDI files and __'output'__ to store generated midi files and neural network models, within root directory
  4. Run __'main.py'__ file giving a path to the text, that should be analysed

  **At the moment only text_analysis module could be run. To do so, go to according folder, place a book in the `.epub` format, uncomment bottom lines in `text_analysis.py` and run it.**

## **_NOTE_**:
Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

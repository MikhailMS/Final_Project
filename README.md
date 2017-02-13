# Final year project - musification of text data.

## **Functionality is under development.**

## List of functionality that would be added later in the priority order:

1. - [x] **Text analysis module**: _Available in two forms: single processing & multi processing (default choice)_
  1. - [x] Read in epub files
  2. - [x] Clean text - automatic and manual cleaning
  3. - [x] Sentiment analysis
  4. - [x] Lexical density analysis
  5. - [x] Readability analysis - possibly worth adding variety of formulas
  6. - [x] Sliding window feature - moves through text rather then giving a score to the whole text

2. - [ ] **Music generation module**:
  1. - [x] Music input
  2. - [ ] Music analysis - _in progress_
  3. - [ ] Build LSTM model - **50% is complete.** _**need to include extra parameters**_
  4. - [x] Training LSTM model
  5. - [x] Music generation
  6. - [ ] Mapping text features onto music ones

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. To test **text_analysis_module**, add a book in the `.epub` format and run __'main.py'__ file
  4. To test **music_generation_module**, create folder __'music'__ with MIDI files and  empty __'output'__ folder within **music_generation_module** directory, then go to that directory and run __music_composition.py__ file

**At the moment only text_analysis_module is fully functional. music_generation_module has limited abilities, and only
able to compose music depending on time stamps and notes. Module is still on development stage.**

## **_NOTE_**:
Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

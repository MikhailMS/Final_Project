# Final year project - musification of text data.

## **Functionality is under development.**

## List of functionality that would be added later in the priority order:

1. - [x] **Text analysis module**: _Available in two forms: single processing & multi processing (default choice)_
   - [x] Read in epub files
   - [x] Clean text - automatic and manual cleaning
   - [x] Sentiment analysis
   - [x] Lexical density analysis
   - [x] Readability analysis - possibly worth adding variety of formulas
   - [x] Sliding window feature - moves through text rather then giving a score to the whole text

2. - [ ] **Music generation module**:
   - [x] Music input
   - [x] Music analysis
   - [x] Build LSTM model
   - [x] Training LSTM model
   - [x] Music generation
   - [ ] Mapping text features onto music ones - **in progress** : need to find what could be controlled by lexical density

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. To test **text_analysis_module**, add a book in the `.epub` format to the _**text_analysis_module**_ folder, then uncomment __run_text_analysis_in_parallel()__ part in __'main.py'__ file from root directory and run the file. Once nltk-downloader is activated, download 2 packages: _**brown**_, _**punkt**_ in order for nltk package to work properly.
  4. To test **music_generation_module**, create folder __'music'__ with MIDI files within **music_generation_module** directory, then uncomment __run_music_composition()__ part in __'main.py'__ file from root directory and run the file

**At the moment only text_analysis_module is fully functional. music_generation_module has limited abilities, and only
able to compose music depending on time stamps and notes. Module is still on development stage.**

## Current Results:
  1. At `epochs = 6500`, application produces music with _**63%**_ correctness. Meaning, that tonic key and complexity has been correctly generated in _**63 cases out of 100**_.
  2. At the moment I have two ideas that must be checked:
      1. Increase number of epochs to see if it outputs better results
      2. Leave number of epochs same, but increase number of training samples (at the moment only _**698 out of 1400**_ files are used)

## **_NOTE_**:
Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

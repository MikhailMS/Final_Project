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
  1. - [ ] Music input - _in progress_
  2. - [ ] Music analysis
  3. - [ ] Build LSTM model
  4. - [ ] Training LSTM model
  5. - [ ] Music generation
  6. - [ ] Mapping text features onto music ones

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. Create folder __'music'__ with MIDI files within root directory
  4. Run __'main.py'__ file giving a path to the text, that should be analysed

**At the moment only text_analysis module could be run. To do so, go to according folder, place a book in the `.epub` format, uncomment bottom lines in `text_analysis.py` and run it.**

## **_NOTE_**:
Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

# Musification of text data.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/210f7da193434400a028194a89dd6658)](https://www.codacy.com/app/1488maiklm/Final_Project?utm_source=github.com&utm_medium=referral&utm_content=MikhailMS/Final_Project&utm_campaign=badger)

## **Project completed as a part of dissertation in my final year @ University of Sheffield**

## List of functionality in the order it's been completed:

1. - [x] **Text analysis module**: _Available in two forms: single processing & multi processing (default choice)_
   - [x] Read in epub files
   - [x] Clean text - automatic and manual cleaning
   - [x] Sentiment analysis
   - [x] Lexical density analysis
   - [x] Readability analysis - possibly worth adding variety of formulas
   - [x] Sliding window feature - moves through text rather then giving a score to the whole text

2. - [x] **Music generation module**:
   - [x] Music input
   - [x] Music analysis
   - [x] Build LSTM model
   - [x] Training LSTM model
   - [x] Music generation
   - [x] Mapping text features onto music ones

## Installation procedure:
  1. Clone the repo
  2. Run `pip install -r requirements.txt`
  3. Please ensure, that you are able to run computations of GPU and GPU environment is all set and ready to use, otherwise application would require much more time to run.
  4. Add a book in the `.epub` format to the _**text_analysis_module**_ folder.
  5. Create folder __'music'__ with MIDI files within **music_generation_module** directory.
  6. Run `main.py` script. Once it is started, wait until nltk-downloader shows up and download following packages: _**brown**_, _**punkt**_ in order for nltk package to work properly.

## Results:
  1. System produces music pieces of the correct key in ~75% cases and ~70% correctness for the complexity of the music. Correctness score is evaluated by simple algorithm, that require modifications and in the current state gives correct score in ~45% cases.

## **_NOTE_**:
Following files fall under the LICENSE.txt agreement:
  1. lstm_model.py
  2. midi_to_statematrix.py
  3. model_data.py
  4. model_training.py
  5. music_composition.py
  6. output_to_input.py
  
Changes in the code were made in order to adapt it for the purpose of my project, however, initial implementation of the LSTM model and music generation (outlined python files) is an intellectual property of _Daniel Johnson_.

Rest of the project is presented under license in PROJECT_LICENSE.txt file and intellectual property of the researcher - Mikhail Molotkov.

Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_ and thus has not been tested under other OS.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** of installation procedure, change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

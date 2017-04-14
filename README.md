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
  3. Please ensure, that you are able to run computations of GPU and GPU environment is all set and ready to use, otherwise application won't run
  4. Add a book in the `.epub` format to the _**text_analysis_module**_ folder.
  5. Create folder __'music'__ with MIDI files within **music_generation_module** directory.
  6. Run `main.py` script. Once it is started, wait until nltk-downloader shows up and download following packages: _**brown**_, _**punkt**_ in order for nltk package to work properly.

## Current Results:
  1. At `epochs = 6500`, application produces music with _**63%**_ correctness. Meaning, that tonic key has been correctly generated in _**63 cases out of 100**_.
  2. At `epochs = 8500`, application produces music with _**67%**_ correctness. Meaning, that tonic key has been correctly generated in _**67 cases out of 100**_.
  3. At the moment I have two ideas that must be checked:
      1. Increase number of epochs to see if it outputs better results -> improvement by **3-7%**
      2. Increase value of `batch_width` parameter -> improvement by **~3%**
      3. Leave number of epochs same, but increase number of training samples (at the moment only _**698 out of 1400**_ files are used) -> leads to MemoryError.
  4. Best result so far is _**70%**_ correctly assigned tonic key.

## **_NOTE_**:
Following files fall under the LICENSE.txt agreement:
  1. lstm_model.py
  2. midi_to_statematrix.py
  3. model_data.py
  4. model_training.py
  5. music_composition.py
  6. output_to_input.py
Changes in the code were made in order to adapt the code for the purpose of my project, however, initial idea is an intellectual property of _Daniel Johnson_

Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_ and thus has not been tested under other OS.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

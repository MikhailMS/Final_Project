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
  
Changes in the code were made in order to adapt the code for the purpose of my project, however, initial implementation of the LSTM model and music generation (oulined python files) is an intellectual property of _Daniel Johnson_.

Rest of the project is presented under license in PROJECT_LICENSE.txt file and intellectual property of the researcher - Mikhail Molotkov.

Application has been created under _**macOS Sierra 10.12 and Python 2.7.10**_ and thus has not been tested under other OS.

If getting **DEPRECATION: Uninstalling a distutils installed project (six) has
been deprecated and will be removed in a future version. This is due to the fact
that uninstalling a distutils project will only partially uninstall the project**
error, than on **step 2** change command to:  
`sudo pip install -r requirements.txt --ignore-installed six`

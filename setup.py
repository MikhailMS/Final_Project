from setuptools import setup

setup(
    name="TextMusification",
    version="1.1.0",
    description='Tool generates music depending on the text provided to it',
    author='Mikhail Molotkov',
    author_email='1488maiklm@gmail.com',
    url='https://github.com/MikhailMS/Final_Project',
    install_requires=[
        'Theano',
        'theano-lstm',
        'numpy >= 1.7.1',
        'scipy >= 0.11',
        'scikit-learn',
        'sklearn',
        'sphinx >= 0.5.1',
        'pretty_midi',
        'python-midi',
        'pickle',
        'matplotlib',
        'multiprocessing',
        'ebooklib',
        'bs4',
        'nltk',
        'textblob',
        'textstat',
        'unittest2'
    ]
)

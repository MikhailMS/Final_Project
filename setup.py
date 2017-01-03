from setuptools import setup

setup(
    name="TextMusification",
    version="0.0.0",
    description='Tool generates music depending on the text provided to it',
    author='Mikhail Molotkov',
    author_email='mmolotkov1@sheffield.ac.uk',
    url='https://github.com/MikhailMS/Final_Project'
    install_requires=[
        'Theano',
        'numpy >= 1.7.1',
        'scipy >= 0.11',
        'sphinx >= 0.5.1',
        'pretty_midi',
        'nltk',
        'textblob',
        'textstat'
    ]
)

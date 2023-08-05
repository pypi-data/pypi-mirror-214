from setuptools import setup
from setuptools import find_packages

with open('README.rst', "r") as f:
    long_description = f.read()

setup(
    name='interactivenlp',
    version='0.1.1',
    description='Interactive NLP',
    long_description=long_description,
    author="Chunxu Yang",
    author_email="chunxuyang@ucla.edu",
    install_requires=[
        'flask',
        'flask-cors',
    ],
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

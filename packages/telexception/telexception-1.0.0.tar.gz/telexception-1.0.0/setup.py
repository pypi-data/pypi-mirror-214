from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
requirements = ["ipython>=7", "requests>=2"]

setup(
    name='telexception',
    version='1.0.0',
    author='Andrey Zotov',
    description='A Python module that sends exception messages to Telegram',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/UrNickName16/Telexception/',
    packages=['telexception'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements,
)

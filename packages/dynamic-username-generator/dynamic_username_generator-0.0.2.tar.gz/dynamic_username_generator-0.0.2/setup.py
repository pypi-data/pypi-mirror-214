import setuptools
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dynamic_username_generator",
    version="0.0.2",
    description="Experience the power of OpenAI with our Dynamic Username Generator, a Python package offering "
                "personalized and creative usernames tailored to your unique preferences",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Bellamy",
    author_email="usernamegenerator.io@gmail.com",
    url="https://usernamegenerator.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


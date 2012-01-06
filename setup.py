#!/usr/bin/env python

from setuptools import setup

def get_name():
    # dynamically calculate the name based on sentweement.__name__
    return __import__("sentweement").__name__

def get_version():
    # dynamically calculate the version based on sentweement.__version__
    return __import__("sentweement").get_version()

setup(  name=get_name(),
        version=get_version(),
        description="Twitter sentiment analysis toolkit",
        author="Ivan Giuliani",
        author_email="giuliani.v@gmail.com",
        url="http://zeta-puppis.com",
        platforms=[ "Unix", "Linux", "Mac OS" ],

        # use MANIFEST.in to generate a comprehensive list of files
        # to include in the final package
        packages=[
            "sentweement",
            "sentweement.commands",
            "sentweement.learning",
            "sentweement.learning.models",
        ],
        scripts=[
            "bin/sentweement",
        ],

        # keep this synced with PIP_REQUIREMENTS
        install_requires=[
            "nltk",
            "tweepy>=1.8",
            # the chromium compact-language-detector is available at
            # http://code.google.com/p/chromium-compact-language-detector/
            # "cld",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: POSIX",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python",
            "Topic :: Text Processing",
      ],
      license="GNU General Public License (GPL) version 2",
)

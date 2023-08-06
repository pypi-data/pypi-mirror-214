from setuptools import setup, find_packages
# import codecs
# import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'download quran verses'
LONG_DESCRIPTION = '''
# Quran Downloader

A brief description of what this project does and who it's for

'''

# Setting up
setup(
    name="QuranDownloader",
    version=VERSION,
    author="Malik",
    author_email="myemail46926213@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['os', 're', 'requests', 'grequests'],
    keywords=['python', 'quran', 'audio', 'reciter', 'verses', 'concurrent'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
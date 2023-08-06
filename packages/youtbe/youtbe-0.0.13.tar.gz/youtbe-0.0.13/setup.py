from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Scrap Any Youtube Stats'
LONG_DESCRIPTION = 'Simple Package to Scrap Basic Stats from any Youtube Video.'

# Setting up
setup(
    name="youtbe",
    version=VERSION,
    author="vardxg",
    author_email="<dev@vardxg.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['vardxg', 'colorama', 'requests'],
    keywords=['python', 'video', 'stats', 'video stats'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
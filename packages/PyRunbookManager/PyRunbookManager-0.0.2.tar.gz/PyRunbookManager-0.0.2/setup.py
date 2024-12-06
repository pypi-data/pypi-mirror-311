from setuptools import setup, find_packages
import os
from pathlib import Path

here = os.path.abspath(os.path.dirname(__file__))
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.2'
DESCRIPTION = 'Easily install modules in azure automation runbooks.'

# Setting up
setup(
    name="PyRunbookManager",
    version=VERSION,
    author="ikbendion (dblonk)",
    author_email="<contact@ikbendion.nl>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    Homepage = "https://github.com/ikbendion/PyRunbookManager",
    Issues = "https://github.com/ikbendion/PyRunbookManager/issues", 
    readme = "README.MD",
    keywords=['python', 'azure', 'automation', 'runbooks', 'pip', 'dependencies'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    project_urls={
        'Source': 'https://github.com/ikbendion/PyRunbookManager',
    },
    license="Apache 2.0"
)

import os
import sys
from pathlib import Path

from setuptools import setup


# almost duplicate but its on purpose (see pyved/utils.py)
def get_version():
    with open(os.path.join('src', 'pyved', 'data', 'VERSION')) as version_file:
        return version_file.read().strip()


sys.path.append('src')


# - fetch data from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# read the contents of the README file

pck_list = [
    "pyved",
    "pyved.pong",
]

this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()

setup(
    name="pyved",

    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",

    long_description=long_desc,
    long_description_content_type='text/markdown',

    install_requires=required,

    package_dir={'': 'src'},
    packages=pck_list,

    package_data={'': ['data/VERSION', 'gui-rel-data/*']},
    include_package_data=True,  # to be sure we also install non-py files...

    description='experimental toolbox for game devs who use python',
    license='LGPL-3.0',
    version=str(get_version()),

    entry_points={
        'console_scripts': [
            'pyved = pyved.__main__:main'
        ]
    }
)

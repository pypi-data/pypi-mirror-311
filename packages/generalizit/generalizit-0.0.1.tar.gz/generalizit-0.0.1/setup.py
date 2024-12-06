from pathlib import Path
from setuptools import find_packages, setup

dependencies = ['numpy', 'pandas','re','scipy','itertools','typing','unittest','itertools']

# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='generalizit',
    packages=find_packages(),
    version='0.0.1',
    description='Propensity score matching for python and graphical plots',
    author='Tyler Smith',
    author_email='tyler.js.smith111@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
         "Bug Tracker": "https://github.com/tylerjsmith111/GeneralizIT",
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

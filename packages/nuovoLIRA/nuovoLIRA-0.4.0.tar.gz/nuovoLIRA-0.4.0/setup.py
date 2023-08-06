from setuptools import find_packages, setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() 

setup(
    name='nuovoLIRA',
    packages=find_packages(),
    version='0.4.0',
    description='A Bayesian procedure to delineate the boundary of an extended astronomical object',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Brendan Martin',
    license='MIT',
)

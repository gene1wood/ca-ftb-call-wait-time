# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ca_ftb_call_wait_time',
    version='1.0.0',
    description="Fetch the California Franchise Tax Board (CA FTB) \"Timeframes\" page, extract the Business collections phone wait time and alert if it's below a threshold.",
    long_description=long_description,
    url='https://github.com/gene1wood/ca-ftb-call-wait-time',
    author='Gene Wood',
    author_email='gene_wood@cementhorizon.com',
    license='GPL-3.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'PyYAML',
        'xdg'],
    entry_points={
        "console_scripts": [
            "check-ca-ftb-call-wait-time = ca_ftb_call_wait_time:main"
        ]
    }
)

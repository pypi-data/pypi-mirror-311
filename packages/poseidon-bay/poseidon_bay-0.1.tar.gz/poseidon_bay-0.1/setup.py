"""Setup file"""
from setuptools import setup, find_packages

setup(
    name='poseidon_bay',
    version='0.1',
    packages=find_packages(),
    description='Contains Poseidon Bay search tools',
    long_description_content_type='text/markdown',
    author='Chrispine Mwape',
    author_email='jrchrismwape@gmail.com',
    url='https://github.com/PyChala/Search-Tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

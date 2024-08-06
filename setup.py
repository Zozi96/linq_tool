from typing import Final
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

DESCRIPTION: Final[str] = 'A LINQ-like library for Python inspired by C# LINQ using itertools internally.'

setup(
    name='linq-tool',
    use_scm_version=True,
    setup_requires=['setuptools-scm'],
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zozimo Fernandez',
    author_email='zozi.fer96@gmail.com',
    url='https://github.com/tu_usuario/linq-tool',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

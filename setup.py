from typing import Final
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

DESCRIPTION: Final[str] = (
    'A LINQ-like library for Python inspired by C# LINQ using itertools and more-itertools internally.'
)

setup(
    name='linq-tool',
    use_scm_version=True,
    setup_requires=['setuptools-scm'],
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zozimo Fernandez',
    author_email='zozi.fer96@gmail.com',
    url='https://github.com/Zozi96/linq_tool',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=['more-itertools'],
)

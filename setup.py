from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='linq-tool',
    version='0.1.0',
    description='A LINQ-like library for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zozimo Fernandez',
    author_email='zozi.fer96@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

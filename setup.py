from setuptools import setup, find_packages

setup(
    name='linq-tool',
    version='0.1.0',
    description='A LINQ-like library for Python',
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

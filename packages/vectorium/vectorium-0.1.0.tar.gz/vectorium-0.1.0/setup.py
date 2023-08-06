from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='vectorium',
    version='0.1.0',
    author='Silvan Ferreira',
    author_email='silvanfj@gmail.com',
    description='Tools for storing embeddings in a database and querying them',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/silvaan/vectorium',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'numpy',
        'torch'
    ],
)

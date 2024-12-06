from setuptools import setup, find_packages

setup(
    name='perplexity-cli',
    version='1.0.0',
    description='A simple command-line client for the Perplexity API',
    author='Dawid Szewc',
    author_email='dawid_szewc@icloud.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
)

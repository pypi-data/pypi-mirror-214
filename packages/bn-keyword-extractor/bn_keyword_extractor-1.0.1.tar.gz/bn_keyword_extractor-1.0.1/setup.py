from setuptools import setup, find_packages

setup(
    name='bn_keyword_extractor',
    version='1.0.1',
    author='Tonmoy Talukder',
    author_email='tonmoytalukder2000@gmail.com',
    description='A package for Bangla keyword extraction',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'requests',
        'pandas',
    ],
)

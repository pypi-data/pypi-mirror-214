try:
    import better_exceptions
except:
    pass
from setuptools import setup


with open('./requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name="pubmed_sdk",
    version="0.2",
    packages=['pubmed_sdk'],
    install_requires=required,
    author="Leo Sternlicht",
    author_email="lsternlicht@gmail.com",
    description="A Python SDK for searching PubMed using the NCBI E-Utilities",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    keywords="pubmed ncbi e-utilities sdk, pubmed api",
    url="http://github.com/pubmed-ai/pubmed_sdk",   # project home page, if any
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)

from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='EssaySummarizer',
    version='0.0.2',
    description='Essay Summarizer.',
    author= 'Ujjwal Reddy K S',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['Essay', 'Summarizer', 'nltk'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['EssaySummarizer'],
    package_dir={'':'src'},
    install_requires = [
        'nltk'
    ]
)

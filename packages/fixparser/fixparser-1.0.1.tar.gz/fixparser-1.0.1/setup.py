from setuptools import setup, find_packages
import os

VERSION = '1.0.1'

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
]

# Get the long description from the README and CHANGELOG files
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'CHANGELOG.txt'), encoding='utf-8') as f:
    changelog = f.read()

setup(
    name='fixparser',  # Replace with your library name
    version=VERSION,  # Replace with your library version
    description='A Python library for parsing FIX protocol messages and exporting to text and CSV formats.',
    long_description=long_description + '\n\n' + changelog,
    long_description_content_type='text/markdown',  # Use 'text/x-rst' if you're using reStructuredText
      # Replace with your GitHub repository URL
    author='Meet Jethwa',
    author_email='meetjethwa3@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='FIX protocol, FIX message parser, CSV export',
    packages=find_packages(),
    install_requires=[
        'numpy',  # Add additional dependencies if required
    ],
    include_package_data=True,
    package_data={
        # Include package-specific data files if necessary
    },
)
from setuptools import setup, find_packages
from os import path

# Read requirements from the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="rupi",  # Name of the library
    version="0.1.30",  # Version of the library
    packages=find_packages(),  # Automatically find packages
    install_requires=required,  # Automatically read dependencies from requirements.txt

    # Project metadata
    author="Tanujairam",
    author_email="tanujairam.v@gmail.com",
    description="A fun Python library with games like FLAMES, XO, and Chess.",
    long_description=long_description,  # Read the detailed description from README
    long_description_content_type="text/markdown",  # This will display the README as markdown
    url="https://github.com/TanujairamV/rupi",  # Project URL
    classifiers=[  # Classifiers to categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6',  # Specify supported Python versions

    # Additional metadata for packaging
    keywords="games, python library, flames, xo, chess, tkinter",
    project_urls={  # Optional additional links
        "Documentation": "https://github.com/TanujairamV/rupi/wiki",
        "Bug Tracker": "https://github.com/TanujairamV/rupi/issues",
        "Source Code": "https://github.com/TanujairamV/rupi",
    },
    license="MIT",  # License type
)

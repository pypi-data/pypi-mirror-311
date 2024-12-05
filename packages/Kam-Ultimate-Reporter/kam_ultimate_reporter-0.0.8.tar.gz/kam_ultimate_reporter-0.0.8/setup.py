# setup.py

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="Kam-Ultimate-Reporter",
    version="0.0.8",  # Increment version as needed
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "inquirer>=3.4.0",
        "pandas>=2.2.3",
        "openpyxl>=3.1.5",
        "folioclient>=0.61.1",
        "httpx>=0.27.2",
    ],
    entry_points={
        'console_scripts': [
            'kam-reporter=Kam_Ultimate_Reporter.main:main',  # Use exact package name
        ],
    },
    description="A CLI tool for generating reports from Medad library system",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Ahmad Awada",
    author_email="ahmed.a.awada@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

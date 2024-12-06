
from setuptools import setup, find_packages

setup(
    name="dbshift",
    version="0.4.0",
    description="A tool for converting Informatica XML mappings to Snowflake SQL and dbt models.",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "tabulate",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "dbshift=dbshift.converter:infa_to_dbt",  # Corrected function name
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

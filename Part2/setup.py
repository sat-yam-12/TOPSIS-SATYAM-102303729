from setuptools import setup, find_packages

setup(
    name="Topsis-Satyam-102303729",
    version="1.0.0",
    author="Satyam Gupta",
    author_email="sgupta5_be23@thapar.edu",
    description="Implementation of TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sat-yam-12/TOPSIS-SATYAM-102303729",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "topsis-satyam=topsis.topsis:main"
        ]
    },
)

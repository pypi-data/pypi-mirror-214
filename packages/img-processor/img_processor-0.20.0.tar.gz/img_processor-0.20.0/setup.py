#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "numpy>=1.24.3",
    "Click>=8.1.3",
    "Pillow>=9.5.0",
    "pytesseract>=0.3.10",
    "pdf2image>=1.16.3",
    "pypdf>=3.10.0",
    "reportlab>=4.0.4",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Justin Keller",
    author_email="kellerjustin@protonmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Python package for taking an image and doing a thing",
    entry_points={
        "console_scripts": [
            "img_processor=img_processor.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="img_processor",
    name="img_processor",
    packages=find_packages(include=["img_processor", "img_processor.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/kellerjustin/img_processor",
    version="0.20.0",
    zip_safe=False,
)

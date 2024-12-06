import os

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(BASE_DIR, "README.md")

with open(README) as file:
    long_description = file.read()

setup(
    name="pytest-porcochu",
    version="1.0.0",
    description="Show surprise when tests are passing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Charlie Hornsby",
    author_email="charlie.hornsby@hotmail.co.uk",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    url="https://github.com/saet/pytest-porcochu",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={"pytest11": ["porcochu = pytest_porcochu.plugin"]},
    install_requires=["pytest"],
)

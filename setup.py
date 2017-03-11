
from setuptools import setup

pname = "parallel-fastq-dump"

exec(next(filter(
	lambda l: l.startswith("__version__"),
	open(pname).read().split("\n")
)))

setup(
    name=pname,
    version=__version__,
    author="Renan Valieris",
    author_email="renan.valieris@cipe.accamargo.org.br",
    description="parallel fastq-dump wrapper",
    license="MIT",
    url="https://github.com/rvalieris/parallel-fastq-dump",
    scripts=[pname],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)

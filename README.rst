
parallel-fastq-dump
===================
parallel ``fastq-dump`` wrapper

Why & How
---------
NCBI ``fastq-dump`` can be very slow sometimes, even if you have the resources (network, IO, CPU) to go faster, even if you already downloaded the sra file (see the protip below). This tool speeds up the process by dividing the work into multiple threads.

This is possible because ``fastq-dump`` have options (``-N`` and ``-X``) to query specific ranges of the sra file, this tool works by dividing the work into the requested number of threads, running multiple ``fastq-dump`` in parallel and concatenating the results back together, as if you had just executed a plain ``fastq-dump`` call.

Protips
-------
* Downloading with ``fastq-dump`` is slow, even with multiple threads, it is recommended to use ``prefetch`` to download the target sra file before using ``fastq-dump``, that way ``fastq-dump`` will only need to do the dumping.
* All extra arguments will be passed directly to ``fastq-dump``, ``--gzip``, ``--split-files`` and filters works as expected.
* This tool is **not** a replacement, you still need ``fastq-dump`` and ``sra-stat`` on your ``PATH`` for it to work properly.
* Speed improvements are better with bigger files, think at least 200k reads/pairs for each thread used.

Install
-------
The preferred way to install is using `Bioconda <http://bioconda.github.io/>`_:

``conda install parallel-fastq-dump``

this will get you the sra-tools dependency as well.

**Important**: Make sure the sra-tools package being installed is a recent version (>=2.10.0) to guarantee compatibility with NCBI servers,
conda might try to install an older version to be compatible with existing packages installed in your env, to be sure use this command:

``conda install parallel-fastq-dump 'sra-tools>=3.0.0'``

If that doesn't work you could also install it on a separate new env:

``conda create -n testenv parallel-fastq-dump 'sra-tools>=3.0.0'``

Examples
--------
``$ parallel-fastq-dump --sra-id SRR2244401 --threads 4 --outdir out/ --split-files --gzip``

Micro Benchmark
---------------

.. figure:: https://cloud.githubusercontent.com/assets/6310472/23962085/bdefef44-098b-11e7-825f-1da53d6568d6.png

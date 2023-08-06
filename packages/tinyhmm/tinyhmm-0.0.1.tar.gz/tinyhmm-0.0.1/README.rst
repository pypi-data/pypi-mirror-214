========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/tinyhmm/badge/?style=flat
    :target: https://tinyhmm.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/reedf1/tinyhmm/actions/workflows/github-actions.yml/badge.svg
..    :alt: GitHub Actions Build Status
..    :target: https://github.com/reedf1/tinyhmm/actions

.. |codecov| image:: https://codecov.io/gh/reedf1/tinyhmm/branch/main/graphs/badge.svg?branch=main
..    :alt: Coverage Status
..    :target: https://app.codecov.io/github/reedf1/tinyhmm

.. |version| image:: https://img.shields.io/pypi/v/tinyhmm.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/tinyhmm

.. |wheel| image:: https://img.shields.io/pypi/wheel/tinyhmm.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/tinyhmm

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tinyhmm.svg
    :alt: Supported versions
    :target: https://pypi.org/project/tinyhmm

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tinyhmm.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/tinyhmm

.. |commits-since| image:: https://img.shields.io/github/commits-since/reedf1/tinyhmm/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/reedf1/tinyhmm/compare/v0.0.1...main



.. end-badges

A tiny hmm.

* Free software: MIT license

Installation
============

::

    pip install tinyhmm

You can also install the in-development version with::

    pip install https://github.com/reedf1/tinyhmm/archive/main.zip


Documentation
=============


https://tinyhmm.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

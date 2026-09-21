SecondaryCoolantProps
=====================

.. image:: https://github.com/NatLabRockies/SecondaryCoolantProps/actions/workflows/pre-commit.yml/badge.svg
   :target: https://github.com/NatLabRockies/SecondaryCoolantProps/actions/workflows/pre-commit.yml
   :alt: Pre-commit status

.. image:: https://github.com/NatLabRockies/SecondaryCoolantProps/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/NatLabRockies/SecondaryCoolantProps/actions/workflows/tests.yml
   :alt: Test status

.. image:: https://readthedocs.org/projects/secondarycoolantprops/badge/?version=latest
   :target: https://secondarycoolantprops.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

SecondaryCoolantProps provides fluid-property routines for secondary coolants.
It is based on the correlations developed by Åke Melinder in *Properties of
Secondary Working Fluids for Indirect Systems*, 2nd edition (International
Institute of Refrigeration, 2010).

The package is designed as a lightweight library that can be imported into
other Python tools without bulky dependencies. It also provides the
``scprop`` command-line interface for shell and scripting workflows.

Installation
------------

Install the latest release from `PyPI`_ into an existing Python environment:

.. code-block:: console

   pip install SecondaryCoolantProps

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   base_fluids
   api
   cli
   prog_usage
   fluid_instances

Project resources
-----------------

* `Source repository`_
* `PyPI releases`_
* `Software record (SWR-26-025)`_

Releases are published to PyPI by GitHub Actions when a version is tagged.
Code style checks and tests are also run by GitHub Actions.

Development
-----------

This project uses a current version of `uv`_ to manage its environment and
dependency groups. Set up the environment and run the checks with:

.. code-block:: console

   uv sync
   uv run pre-commit run -a

Build the package and documentation with:

.. code-block:: console

   uv run build
   uv run sphinx-build -b html docs docs/_build/html

Publish a release with ``uv publish`` after building it.

.. _PyPI: https://pypi.org/project/SecondaryCoolantProps/
.. _PyPI releases: https://pypi.org/project/SecondaryCoolantProps/
.. _Source repository: https://github.com/NatLabRockies/SecondaryCoolantProps
.. _Software record (SWR-26-025): https://doi.org/10.11578/dc.20260427.2
.. _uv: https://docs.astral.sh/uv/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

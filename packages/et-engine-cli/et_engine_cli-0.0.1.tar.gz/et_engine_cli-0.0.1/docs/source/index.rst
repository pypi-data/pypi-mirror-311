Welcome to ET CLI Documentation
===============================

============
Installation
============

The CLI is available on PyPI. To start, create a new environment with Python >=3.11.9. If you're using Anaconda, you can create an environment using the following commands.


.. code-block:: python

   conda create -n engine python=3.11.9
   conda activate engine

Now you can install the CLI using pip.

.. code-block:: python

   pip install et-engine-cli


Log in to your ET Engine account using the following command. You will be prompted for your username and password, which are the same credentials you use to log into the Web App.

.. code-block:: bash

   et login


=============
CLI Reference
=============


.. toctree::
   :maxdepth: 2

   tools
   filesystems
   batches

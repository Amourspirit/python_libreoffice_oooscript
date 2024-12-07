.. _quick_start:

Quick Start
===========

Install |app_name_bold| into your project.

.. code-block:: sh

    pip install oooscript

Create an ``.env`` file in your root directory. File can be empty. See :ref:`env`.

Create ``config.json`` in your projects source directory.
Add the necessary configuration to ``config.json``. See :ref:`config`.

Build your script.

Example command:

.. code-block:: sh

    oooscript compile --pyz-out --embed --config "src/config.json" --embed-doc "src/some-doc.odt"

Example make file:

.. code-block:: sh

    # Makefile for building the oooscript project

    help:
        @echo "Run make build to compile into 'build/python_sample' folder."

    .PHONY: build help

    build:
        oooscript compile --pyz-out --embed --config "$(PWD)/src/config.json" --embed-doc "$(PWD)/src/some-doc.odt" --build-dir "$(PWD)/data"
        rm -f "$(PWD)/data/*.py"
        rm -f "$(PWD)/data/*.pyz"


For an example see |message_box|_ of |lo_ex|_.

Note
----

When building it is recommended to use the ``--pyz-out`` option.
This will create a binary ``.pyz`` file that is packages with the main ``.py`` or your script.
The ``.pyz`` file is the main script and the ``.py`` file is the loader.

The ``.pyz`` file is faster and more efficient than the embedding libraries directly in the ``.py`` file.
Excluding ``--pyz-out`` will embed the libraries directly into the ``.py`` file just like version previous to ``2.0.0``.

.. |lo_ex| replace:: LibreOffice Python UNO Examples
.. _lo_ex: https://github.com/Amourspirit/python-ooouno-ex

.. |message_box| replace:: MESSAGE BOX
.. _message_box: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/general/message_box
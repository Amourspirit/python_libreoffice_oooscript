Quick Start
===========

Install |app_name_bold| into your project.

.. code-block:: sh

    pip install oooscript

Create an ``.env`` file in your root directory. File can be empty. See :ref:`env`.

Create ``config.json`` in your projects source directory.
Add the necessary configurtion to ``config.json``. See :ref:`config`.

Build your script.

Example command:

.. code-block:: sh

    oooscript compile --embed --config "src/config.json" --embed-doc "src/some-doc.odt"

For an example see |message_box|_ of |lo_ex|_.

.. |lo_ex| replace:: LibreOffice Python UNO Examples
.. _lo_ex: https://github.com/Amourspirit/python-ooouno-ex

.. |message_box| replace:: MESSAGE BOX
.. _message_box: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/general/message_box
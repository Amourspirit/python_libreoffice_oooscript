Version History
===============

Version 2.0.0
-------------

This version has added the ability to compile your script into a binary ``.pyz`` file.

When building it is recommended to use the ``--pyz-out`` option.
This will create a binary ``.pyz`` file that is packages with the main ``.py`` or your script.
The ``.pyz`` file is the main script and the ``.py`` file is the loader.

The ``.pyz`` file is faster and more efficient than the embedding libraries directly in the ``.py`` file.
Excluding ``--pyz-out`` will embed the libraries directly into the ``.py`` file just like version previous to ``2.0.0``.

See :ref:`quick_start` for more information.

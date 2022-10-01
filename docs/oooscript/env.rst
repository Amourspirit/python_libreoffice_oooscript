.. _env:

Environment
===========

.. spelling:word-list::

        dir
        namespace
        xml

|app_name_bold| **requires** an ``.env`` file be created in your projects root directory.

Certain build properties can optionally be added to ``.env`` file.

``${HOME}`` is allowed in values and will expand to current user home directory.

app_build_dir
-------------

Path Like structure to build dir

Default:

.. code-block:: ini

    app_build_dir=build_script

.. note::

    If you use a ``.gitignore`` file then this path should be include in the ``.gitignore`` file.

.. _env_build_include_paths:

build_include_paths
-------------------

Extra module include paths that is used to find module that may be included in compiled scripts.

Default:

.. code-block:: ini

    build_include_paths=.

These values are in addition to :ref:`config_args_include_paths` value of :ref:`config`.

In most all cases this value should be managed via :ref:`config_args_include_paths` and not changed in ``.env``.

.. _env_build_exclude_modules:

build_exclude_modules
---------------------

Extra modules to remove from compiled scripts.

Default:

.. code-block:: ini

    build_exclude_modules=uno\.*,unohelper\.*,scriptforge\.*,access2base\.*

These value are in addition to :ref:`config_args_remove_modules` value of :ref:`config`.

In most all cases this value should be managed via :ref:`config_args_remove_modules` and not changed in ``.env``.

lo_script_dir
-------------

Path Like structure to libre office scripts director.

Default:

.. code-block:: ini

    lo_script_dir=$(HOME)/.config/libreoffice/4/user

Example for LibreOffice as snap

.. code-block:: ini

    lo_script_dir=${HOME}/snap/libreoffice/current/.config/libreoffice/4/user

xml_manifest_namespace
-----------------------

Manifest name in LibreOffice xml. Likely this value will never need changing.

Default:

.. code-block:: ini

    xml_manifest_namespace=urn:oasis:names:tc:opendocument:xmlns:manifest:1.0

.. _config:

Configuration
=============

|app_name_bold| requires the presents of a configuration file in your project such as ``config.json``.

This configuration file is used to set parameters for |app_name_bold| and is generally
located in the same directory and your source files.

This is an example from the |lo_ex|_ project. See: |message_box|_ example.

.. code-block:: json

    {
    "id": "oooscript",
    "name": "message_box",
    "app": "WRITER",
    "version": "0.1.0",
    "args": {
        "src_file": "script.py",
        "output_name": "msgbox",
        "single_script": false,
        "clean": true
    },
    "methods": [
        "msg_small",
        "msg_long",
        "msg_default_yes",
        "msg_error",
        "msg_warning"
    ]
    }

Configuration Properties
------------------------

.. _config_id:

id
^^

Type: string

The id of the configuration. This must always be ``oooscript``

.. _config_name:

name
^^^^

Type: string

The name of of the project. This can be any name that suites your project needs.
Value is not reflected in the final output.

.. _config_app:

app
^^^

Type: string

This represents the type of LibreOffice application.

Valid values are:

.. cssclass:: ul-list

    * "NONE"
    * "UNKNOWN"
    * "WRITER"
    * "CALC"
    * "IMPRESS"
    * "DRAW"
    * "MATH"
    * "BASE"

.. _config_version:

version
^^^^^^^

Type: string

Version is the |app_name_bold| version that configuration is intended for.

The current version of |app_name_bold| can be obtained on the command line:

.. code-block:: sh

    oooscript version

.. note::

    Do not use a version that is greater then the current released version.

.. _config_methods:

methods
^^^^^^^
Optional. Type: list of string

This is the methods that are exported by your script.
The methods listed there will be the exact methos of ``g_exportedScripts`` value.

.. note::

    ``methods`` is ignored when :ref:`config_args_single_script` is ``true``

    ``methods`` is necessary when :ref:`config_args_single_script` is ``false`` or
    ``g_exportedScripts`` for your script will be empty

.. _config_args:

args
^^^^

.. _config_args_src_file:

src_file
""""""""

Required. Type: string

The soure (main) entry point file realitive to config file.

This is the python script that LibreOffice will actually see.

.. _config_args_output_name:

output_name
"""""""""""

Required. Type: string

The output name of script and/or document.

.. _config_args_single_script:

single_script
"""""""""""""

Optional. Type: boolean. Defalult: ``false``

Indicates if the script is a standalone script of has imports.

Standalone scripts must include their own ``g_exportedScripts`` value as :ref:`config_methods` is ignore in this case.

.. _config_args_clean:

clean
"""""

Optional. Type: boolean. Default: ``true``

If ``true`` then all docstrings and comments are removed from imported scripts.

.. _config_args_include_modules:

include_modules
"""""""""""""""

Optional. Type: list of string

This is a list of modules to include if they are not automatically imported.

.. code-block:: json

    {
      "args": {
        "include_modules": ["greeting", "phaser"]
      }
    }

.. seealso::

    :ref:`config_args_include_paths`

.. _config_args_remove_modules:

exclude_modules
"""""""""""""""

Optional. Type: list of string

List of modules to exclude from project, as regex expressons.

When using some projects such as |odev|_ (ODEV) the package may support working both as a macro and
stand alone modes. In such cases there may be dependencies that are needed for standand alone mode
that are not required for macro mode.

For instance ODEV uses ``sphinx``, ``lxml`` and ``PIL`` packages for various puropses but these
packages not available in macro mode by default. Also these package are not need to run ODEV in macro mode.

To exlude these package when using ODEV:

.. code-block:: json

    {
      "args": {
        "exclude_modules": ["sphinx\\.*", "lxml\\.*", "PIL\\.*"]
      }
    }

|app_name_bold| by defalult excludes ``uno``, ``unohelper``, ``scriptforge``, and ``access2base``.

In the unlikely event you would need to override the default excludes of :ref:`env`. See: :ref:`env_build_exclude_modules`.

.. _config_args_include_paths:

include_paths
"""""""""""""

Optional. Type: list of string.

When using :ref:`config_args_include_modules` the module you want to include may not be on the current
python path. In this case you can use the include_paths to add the path to where your extra modules exist.

.. seealso::

    :ref:`config_args_include_modules`

.. seealso::

    :ref:`env_build_include_paths` of :ref:`env`.


.. |lo_ex| replace:: LibreOffice Python UNO Examples
.. _lo_ex: https://github.com/Amourspirit/python-ooouno-ex

.. |message_box| replace:: MESSAGE BOX
.. _message_box: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/general/message_box

.. |odev| replace:: **ooo-dev-tools**
.. _odev: https://pypi.org/project/ooo-dev-tools/
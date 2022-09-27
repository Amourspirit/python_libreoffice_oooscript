Configuration
=============

|app_name_bold| requires the presents of a configuration file in your project such as ``config.json``.

This configuration file is used to set parameters for |app_name_bold|.

This is an example from the |lo_ex|_ project. See: |message_box|_ example.

.. code-block:: json

    {
    "id": "oooscript",
    "name": "message_box",
    "type": "EXAMPLE",
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


.. |lo_ex| replace:: LibreOffice Python UNO Examples
.. _lo_ex: https://github.com/Amourspirit/python-ooouno-ex

.. |message_box| replace:: MESSAGE BOX
.. _message_box: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/general/message_box

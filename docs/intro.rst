Introduction
------------

Python is such a zen_ language. Writing LibreOffice scripts in python however
can be a bit more challenging.

It is a complex task to get a multi file project, especially a project that has a directory structure,
to work as a script in LibreOffice.
If you project has external dependencies then this task becomes even more challenging.

This is where |app_name_bold| comes in.
|app_name_bold| makes it possible to compile scripts into one single python script.

Sometimes you may need to use other dependencies in you project such as ooouno_.

|app_name_bold| can include any dependencies into its single output python file.
The nice thing is |app_name_bold| only include that actual imports used from a dependency
and not necessarily the entire dependency.

.. _ooouno: http://localhost:8000/docs/_build/html/index.html
.. _zen: https://peps.python.org/pep-0020/
import os
import sys
from datetime import date
import importlib.metadata
from pathlib import Path


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

_DOCS_PATH = Path(__file__).parent
_ROOT_PATH = _DOCS_PATH.parent

sys.path.insert(0, str(_ROOT_PATH))

os.environ["DOCS_BUILDING"] = "True"


todays_date = date.today()
project = 'oooscript'
dist = importlib.metadata.Distribution.from_name(project)
author = dist.metadata["Author"]
copyright = f'{todays_date.year}, {author}'
release = dist.version



# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx_rtd_dark_mode",
    "sphinx_toolbox.collapse",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinxcontrib.spelling",
]

# region spelling
# https://sphinxcontrib-spelling.readthedocs.io/en/latest/


def get_spell_dictionaries() -> list:

    p = _DOCS_PATH.absolute().resolve() / "internal" / "dict"
    if not p.exists():
        return []
    dict_gen = p.glob('spelling_*.*')
    return [str(d) for d in dict_gen if d.is_file()]

spelling_word_list_filename = get_spell_dictionaries()

spelling_show_suggestions = True
spelling_ignore_pypi_package_names = True
spelling_ignore_contributor_names = True
spelling_ignore_acronyms=True

# spell checking;
#   run sphinx-build -b spelling . _build
#       this will checkfor any spelling and create folders with *.spelling files if there are errors.
#       open each *.spelling file and find any spelling errors and fix them in corrsponding files.
#


# endregion spelling

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

html_css_files = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"]
html_css_files.append("css/readthedocs_custom.css")
if html_theme == "sphinx_rtd_theme":
    html_css_files.append("css/readthedocs_dark.css")

html_js_files = [
    'js/custom.js',
]

# Napoleon settings
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = True
napoleon_include_init_with_doc = True

# set is todo's will show up.
# a master list of todo's will be on bottom of main page.
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#module-sphinx.ext.todo
todo_include_todos = False
# Configuration file for the Sphinx documentation builder.
from sphinx.ext.imgmath import templates_path

import pydsa

project = 'pydsa'
copyright = '2026, Sherzod Juraev'
author = 'Sherzod Juraev'
release = pydsa.__version__
version = release


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton",
    "notfound.extension",
]

autodoc_default_options = {
    "member-order": "bysource",
    "undoc-members": False,
}

add_module_names = False
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_rtype = False
toc_object_entries_show_parents = "hide"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

copybutton_prompt_text = ">>> "
copybutton_only_copy_prompt_lines = True
notfound_urls_prefix = "/en/latest/"

templates_path = ["_templates",]
exclude_patterns = []

html_title = "pydsa"
html_context = {
    "default_mode": "light",
}
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "github_url": "https://github.com/sherzod-juraev/pydsa",
    "show_prev_next": True,
    "navigation_with_keys": True,
    "collapse_navigation": True,
    "show_nav_level": False,
    "navbar_end": ["navbar-icon-links"],
}
html_css_files = [
    "header.css",
    "left_sidebar.css",
    "right_sidebar.css",
    "cards.css",
    "code_blocks.css",
    "installation.css",
    "breadcrumb.css",
    "footer_nav.css",
]

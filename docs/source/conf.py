"""Configuration file for the Sphinx documentation builder."""

import os
from datetime import datetime

import pydsa

# ================================================================================= #
# ----------------------------- Project Configurations ---------------------------- #
# ================================================================================= #
project = "pydsa"
author = "Sherzod Juraev"
year = 2026
current_year = datetime.now().year
year_str = str(year) if current_year == year else f"{year}-{current_year}"
copyright = f"{year_str}, {author}"
release = pydsa.__version__
version = release
source_suffix = {
    ".rst": "restructuredtext",
}

# ================================================================================= #
# ------------------------------ Canonical URL ------------------------------------ #
# ================================================================================= #
_READTHEDOCS_CANONICAL_URL = os.environ.get("READTHEDOCS_CANONICAL_URL")
_CANONICAL_URL = _READTHEDOCS_CANONICAL_URL or "https://pydsa-edu.readthedocs.io/en/latest/"


# ================================================================================= #
# ----------------------------------- Extensions ---------------------------------- #
# ================================================================================= #
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton",
    "notfound.extension",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    "autodocsumm",
]

# ================================================================================= #
# ------------------------------------ Autodoc ------------------------------------ #
# ================================================================================= #
autodoc_default_options = {
    "member-order": "bysource",
    "undoc-members": False,
    "inherited-members": "object",
    "autosummary": True
}
autodoc_typehints_format = "short"
autodoc_class_signature = "separated"
autosummary_generate = False

# ================================================================================= #
# ------------------------------------ Napoleon ----------------------------------- #
# ================================================================================= #
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_rtype = False

# ================================================================================= #
# ----------------------------- Code Syntax & Styling ----------------------------- #
# ================================================================================= #
add_module_names = False
toc_object_entries_show_parents = "hide"
pygments_style = "friendly"

# ================================================================================= #
# -------------------------------- Intersphinx ------------------------------------ #
# ================================================================================= #
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# ================================================================================= #
# --------------------------------- CopyButton ------------------------------------ #
# ================================================================================= #
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

# ================================================================================= #
# ------------------------------- OpenGraph --------------------------------------- #
# ================================================================================= #
ogp_site_url = _CANONICAL_URL
ogp_image = "_static/images/og-image.png"
ogp_description_length = 200
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:image:width" content="1200" />',
    '<meta property="og:image:height" content="630" />',
]

# ================================================================================= #
# ------------------------------- Sphinx Sitemap ---------------------------------- #
# ================================================================================= #
html_baseurl = _CANONICAL_URL
sitemap_url_scheme = "{link}"
sitemap_excludes = [
    "search.html",
    "genindex.html",
]

# ================================================================================= #
# -------------------------- Options For Html Output ------------------------------ #
# ================================================================================= #
html_extra_path = ["_extra"]
templates_path = ["_templates"]
exclude_patterns = []

# ================================================================================= #
# ---------------------------- Theme & Branding ----------------------------------- #
# ================================================================================= #
html_theme = "pydata_sphinx_theme"
html_title = "pydsa"
html_context = {
    "default_mode": "light",
}
html_favicon = "_static/images/favicon.svg"
html_domain_indices = False
html_last_updated_fmt = "%b %d, %Y"
html_copy_source = False


# ================================================================================= #
# --------------------------- Theme Customizations -------------------------------- #
# ================================================================================= #
html_theme_options = {
    "github_url": "https://github.com/sherzod-juraev/pydsa",
    "show_prev_next": True,
    "navigation_with_keys": True,
    "collapse_navigation": True,
    "show_nav_level": False,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "logo": {
        "image_light": "_static/images/logo-light.svg",
        "image_dark": "_static/images/logo-dark.svg",
        "alt_text": "pydsa",
    },
}

# ================================================================================= #
# ------------------------------------- CSS Files --------------------------------- #
# ================================================================================= #
html_static_path = ["_static"]
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

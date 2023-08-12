# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from typing import Any, Dict, List, Optional, Tuple, Union
from os import environ
from tomli import load as load_toml
from pathlib import Path
from shutil import copyfile
import subprocess
from json import load


ON_READTHEDOCS = environ.get("READTHEDOCS") == "True"


# -- Project information -----------------------------------------------------

current_path = Path(".").absolute()

project_root: Path
pyproject_path: Path

if current_path.name == "docs":
    project_root = current_path.parent
    pyproject_path = current_path / Path("../pyproject.toml")
else:
    project_root = current_path
    pyproject_path = current_path / Path("pyproject.toml")

pyproject_toml: Any

with pyproject_path.open(mode="rb") as pyproject:
    pyproject_toml = load_toml(pyproject)

package_config = pyproject_toml["tool"]["poetry"]
sphinx_config = pyproject_toml["tool"].get("sphinx")

project = str(package_config.get("name"))
author = ", ".join(package_config.get("authors"))
copyright_year = sphinx_config.get("copyright-year", 2020)
copyright = f"{copyright_year}, {author}"
version = str(package_config.get("version"))
release = str(sphinx_config.get("release", version))

config_theme = sphinx_config.get("theme")

if sphinx_config.get("html-baseurl", None):
    html_baseurl = sphinx_config.get("html-baseurl", None)

# -- update openapi specification -------------------------------------------

subprocess.run(
    ["flask", "openapi", "write", "docs/api.json"],
    cwd=project_root,
)

api_spec_path = project_root / Path("docs/api.json")

api_title: str
api_version: str

with api_spec_path.open() as api_spec:
    spec = load(api_spec)
    info = spec.get("info", {})
    api_title = info.get("title")
    version = info.get("version")

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxcontrib.redoc",
    "sphinx_click",
]

autosectionlabel_prefix_document = False
autosectionlabel_maxdepth = None

intersphinx_mapping: Optional[
    Dict[str, Tuple[str, Union[Optional[str], Tuple[str]]]]
] = None
intersphinx_timeout = 30

source_suffix = {
    ".rst": "restructuredtext",
}

graphviz_dot = "dot"
graphviz_dot_args = []
graphviz_output_format = "png"

todo_include_todos = not ON_READTHEDOCS
todo_emit_warnings = not ON_READTHEDOCS
todo_link_only = False

# enable sphinx autodoc
if sphinx_config.get("enable-autodoc", False):
    extensions.append("sphinx.ext.autodoc")

# enable sphinx autosectionlabel
if sphinx_config.get("enable-autosectionlabel", False):
    extensions.append("sphinx.ext.autosectionlabel")
    config = sphinx_config.get("autosectionlabel", None)
    if config:
        autosectionlabel_prefix_document = config.get("prefix-document", False)
        autosectionlabel_maxdepth = config.get("maxdepth", None)

# enable intersphinx
if sphinx_config.get("intersphinx-mapping", None):
    extensions.append("sphinx.ext.intersphinx")
    mapping = sphinx_config.get("intersphinx-mapping", None)
    intersphinx_mapping = {
        key: (val[0], val[1] if len(val) > 1 and val[1] else None)
        for key, val in mapping.items()
    }


myst_enable_extensions: List[str] = []

# enable markdown parsing
if sphinx_config.get("enable-markdown", False):
    _md_plugin = sphinx_config["enable-markdown"]
    if _md_plugin is True or _md_plugin.lower() == "myst":
        extensions.append("myst_parser")
    elif _md_plugin.lower() == "recommonmark":
        extensions.append("recommonmark")
    else:
        print(
            "Unknown markdown plugin specified (allowed: 'myst', 'recommonmark'), using 'myst'."
        )
        extensions.append("myst_parser")
    print("MARKDOWN ENABLED")

    source_suffix[".txt"] = "markdown"
    source_suffix[".md"] = "markdown"


# enable sphinx githubpages
if sphinx_config.get("enable-githubpages", False):
    extensions.append("sphinx.ext.githubpages")

# enable sphinx graphviz
if sphinx_config.get("enable-graphviz", False):
    extensions.append("sphinx.ext.graphviz")
    config = sphinx_config.get("graphviz", None)
    if config:
        graphviz_dot = config.get("dot", "dot")
        graphviz_dot_args = config.get("dot-args", [])
        graphviz_output_format = config.get("output-format", "png")

# enable sphinx napoleon
if sphinx_config.get("enable-napoleon", False):
    extensions.append("sphinx.ext.napoleon")

# enable sphinx todo
if sphinx_config.get("enable-todo", False):
    extensions.append("sphinx.ext.todo")
    config = sphinx_config.get("todo", None)
    if config:
        todo_include_todos = config.get("include-todos", False)
        todo_emit_warnings = config.get("emit-warnings", False)
        todo_link_only = config.get("link-only", False)

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

if config_theme:
    html_theme = config_theme

if ON_READTHEDOCS:
    html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Further extension options -----------------------------------------------

redoc = [
    {
        "name": api_title,
        "page": "api",
        "spec": "api.json",
        "embed": True,
        "opts": {"hide-hostname": True},
    },
]

redoc_uri = "https://unpkg.com/redoc@latest/bundles/redoc.standalone.js"

# myst markdown parsing
_myst_options = sphinx_config.get("myst", {})
allowed_md_extensions = {
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
}

_heading_achors = _myst_options.get("heading_anchors", None)
if _heading_achors and isinstance(_heading_achors, int) and _heading_achors > 0:
    myst_heading_anchors = _heading_achors


_md_extensions = _myst_options.get("extensions", None)
if _md_extensions and isinstance(_md_extensions, list):
    myst_enable_extensions = [x for x in _md_extensions if x in allowed_md_extensions]
    unknown_md_extensions = [x for x in _md_extensions if x not in allowed_md_extensions]
    if unknown_md_extensions:
        print("Unknown Markdown extensions:", unknown_md_extensions)

_md_substitutions = _myst_options.get("substitutions", None)
if _md_substitutions and isinstance(_md_substitutions, dict):
    myst_substitutions: Dict[str, str] = _md_substitutions


# -- Extra Files -------------------------------------------------------------


if sphinx_config.get("include-changelog"):
    changelog = project_root / Path("CHANGELOG.md")
    dest = project_root / Path("docs/changelog.md")
    copyfile(changelog, dest)

if sphinx_config.get("include-readme"):
    readme = project_root / Path("README.md")
    dest = project_root / Path("docs/readme.md")
    copyfile(readme, dest)

# -- Monkeypatches -----------------------------------------------------------

PATCH_SPHINX_CLICK = True

if PATCH_SPHINX_CLICK:
    from functools import wraps
    from docutils import nodes
    from docutils.parsers.rst import directives
    from sphinx_click.ext import ClickDirective

    ClickDirective.option_spec["section-title"] = directives.unchanged

    old_run = ClickDirective.run

    @wraps(old_run)
    def new_run(self: ClickDirective):
        section_title: str = self.options.get("section-title")
        sections = old_run(self)
        if section_title:
            attrs = sections[0].attributes  # section node attributes
            attrs["ids"] = [nodes.make_id(section_title)]
            attrs["names"] = [nodes.fully_normalize_name(section_title)]
            title = sections[0][0]  # title node
            title.replace_self(nodes.title(text=section_title))
        return sections

    ClickDirective.run = new_run

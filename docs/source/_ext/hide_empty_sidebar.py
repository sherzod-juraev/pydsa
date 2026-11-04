"""Sphinx extension: hide the primary sidebar on pages whose section has no sub-pages."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata


def _top_level_page(env: BuildEnvironment, pagename: str) -> str | None:
    """Return the top-level page (direct child of the root doc) that contains ``pagename``."""
    relations = env.collect_relations()
    current = pagename
    while True:
        parent = relations.get(current, (None,))[0]
        if parent is None:
            return None  # not part of the toctree (root doc, orphan, 404, ...)
        if parent == env.config.root_doc:
            return current
        current = parent


def _on_html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: nodes.document | None,
) -> None:
    """Empty the sidebar list when the page's section has nothing to navigate."""
    top = _top_level_page(app.env, pagename)
    if top is not None and top not in app.env.toctree_includes:
        context["sidebars"] = []


def setup(app: Sphinx) -> ExtensionMetadata:
    """Connect the handler after the theme's own ``html-page-context`` handlers."""
    app.connect("html-page-context", _on_html_page_context, priority=900)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}

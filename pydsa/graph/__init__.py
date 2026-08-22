"""Graph package.

Exposes :class:`~pydsa.graph.graph.Graph` as the public entry point
for this subpackage, a directed or undirected graph with BFS/DFS,
path, and connectivity utilities.
"""

from .graph import Graph

__all__ = [
    "Graph",
]

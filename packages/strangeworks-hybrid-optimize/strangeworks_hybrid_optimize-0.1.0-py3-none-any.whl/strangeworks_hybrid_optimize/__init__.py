"""Strangeworks QAOA SDK Extension."""
import importlib.metadata

from strangeworks_hybrid_optimize.sdk import StrangeworksHybrid  # noqa: F401

__version__ = importlib.metadata.version("strangeworks-hybrid-optimize")

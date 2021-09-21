"""Leanpub Multi Action is used to interact with the Leanpub.com API in GitHub Actions."""

# Gather version information from project packaging
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)
print(__version__)

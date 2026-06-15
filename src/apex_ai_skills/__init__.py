"""CLI for installing and updating Town of Apex AI agent skills."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("apex-ai-skills")
except PackageNotFoundError:
    __version__ = "0.0.0"

"""
Perspectra - Background Removal and Perspective Correction Library

A Python library for removing backgrounds from images and correcting perspective distortions.
"""

from .core.processor import PerspectraProcessor
from .core.config import PerspectraConfig

__version__ = "0.1.0"
__all__ = ["PerspectraProcessor", "PerspectraConfig"]

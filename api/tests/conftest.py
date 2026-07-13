"""Pytest fixtures and path setup."""
import sys
from pathlib import Path

# Add the api/ directory (parent of the app package) to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

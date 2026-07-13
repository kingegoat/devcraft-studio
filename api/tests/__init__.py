"""Pytest configuration."""
import asyncio
import os
import sys
from pathlib import Path

# Ensure the api/ directory is on sys.path so `import app.*` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Use in-memory SQLite for tests
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("ADMIN_TOKEN", "test-admin")
os.environ.setdefault("SERVE_SITE", "false")

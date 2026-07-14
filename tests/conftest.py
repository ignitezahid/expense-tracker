"""Test configuration: adds project root to Python path."""

import os
import sys

# Add the parent directory to sys.path so tests can import project modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

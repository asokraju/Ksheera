#!/usr/bin/env python3
"""Rebuild every book: runs each <grade>/<topic>/build.py and writes its PDF next to it."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
scripts = sorted(p for p in ROOT.glob("*/*/build.py") if p.parent.parent.name != "common")
for script in scripts:
    subprocess.run([sys.executable, str(script)], check=True)
print(f"built {len(scripts)} book(s)")

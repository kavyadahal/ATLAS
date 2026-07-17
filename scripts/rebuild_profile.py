"""
Run this any time you edit data/profile.md, to (re)build ATLAS's
knowledge of your personal profile.

Usage:
    python scripts/rebuild_profile.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.profile_store import ProfileStore


def main():
    store = ProfileStore()
    count = store.rebuild_from_file("data/profile.md")

    if count == 0:
        print("No filled-in sections found in data/profile.md.")
        print("Fill in at least one section under a '## Heading' and re-run.")
    else:
        print(f"Profile rebuilt: {count} section(s) stored.")


if __name__ == "__main__":
    main()
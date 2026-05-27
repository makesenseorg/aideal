#!/usr/bin/env python3
"""
Pair ID Generator

Generates the next available pair ID following the `category-###` convention.
Usage: python scripts/generate_id.py --category <category-name>

Category names:
- genre-inclusion -> genre-041
- techno-solutionnisme -> techno-039
- vision-economique -> eco-039
- validisme-accessibilite -> valid-039
- inegalites-nord-sud -> nord-sud-041
- ecologie-sobriete -> sobr-040
- gouvernance-pouvoir-agir -> gouv-040
- diversite-parcours -> diversite-040
"""

import json
import argparse
import os
import sys
from pathlib import Path


# Map from full category name to ID prefix
CATEGORY_PREFIXES = {
    "genre-inclusion": "genre",
    "techno-solutionnisme": "techno",
    "vision-economique": "eco",
    "validisme-accessibilite": "valid",
    "inegalites-nord-sud": "nord-sud",
    "ecologie-sobriete": "sobr",
    "gouvernance-pouvoir-agir": "gouv",
    "diversite-parcours": "diversite",
}


def load_category_file(category: str, base_dir: Path) -> list:
    """Load all pairs from a category file."""
    filepath = base_dir / "dataset" / "categories" / f"{category}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"Category file not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_existing_ids(pairs: list) -> set:
    """Extract all existing IDs from a list of pairs."""
    return {pair.get("id", "").split("-")[0] for pair in pairs if pair.get("id")}


def get_next_id_for_category(category: str, base_dir: Path) -> str:
    """
    Get the next available ID for a given category.
    
    Returns the next available ID following the convention for this category.
    For example, genre-inclusion uses 'genre-XXX', while techno-solutionnisme uses 'techno-XXX'.
    """
    prefix = CATEGORY_PREFIXES.get(category, category)
    
    # Load existing pairs in this category
    pairs = load_category_file(category, base_dir)
    
    # Get all existing prefixes for this category
    existing_prefixes = set()
    for pair in pairs:
        pair_id = pair.get("id", "")
        if "-" in pair_id:
            existing_prefixes.add(pair_id.split("-")[0])
    
    # Find the max number for this prefix in the category
    max_num = 0
    for pair in pairs:
        pair_id = pair.get("id", "")
        if prefix + "-" in pair_id:
            try:
                num = int(pair_id.split("-")[1])
                max_num = max(max_num, num)
            except (ValueError, IndexError):
                continue
    
    next_num = max_num + 1
    
    return f"{prefix}-{next_num:03d}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate next available pair ID for a category"
    )
    parser.add_argument(
        "--category", "-c",
        required=True,
        help="Category name (e.g., genre-inclusion, techno-solutionnisme, etc.)"
    )
    parser.add_argument(
        "--base-dir", "-d",
        default=".",
        help="Base directory of the AIDEAL repo (default: current directory)"
    )
    
    args = parser.parse_args()
    base_dir = Path(args.base_dir).resolve()
    
    try:
        next_id = get_next_id_for_category(args.category, base_dir)
        print(next_id)
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

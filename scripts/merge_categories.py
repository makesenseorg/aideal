"""
merge_categories.py — Fusionne les fichiers JSON de chaque catégorie en preferences.json

Usage :
    python scripts/merge_categories.py

Résultat :
    dataset/preferences.json — dataset complet, toutes catégories confondues
"""

import json
import sys
from pathlib import Path

CATEGORIES_DIR = Path(__file__).parent.parent / "dataset" / "categories"
OUTPUT_FILE = Path(__file__).parent.parent / "dataset" / "preferences.json"


def merge_categories() -> list[dict]:
    """Charge et fusionne tous les fichiers JSON de catégories."""
    all_pairs = []
    category_files = sorted(CATEGORIES_DIR.glob("*.json"))

    if not category_files:
        print("Aucun fichier de catégorie trouvé.", file=sys.stderr)
        return []

    for category_file in category_files:
        with open(category_file, encoding="utf-8") as f:
            try:
                pairs = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Erreur JSON dans {category_file.name} : {e}", file=sys.stderr)
                sys.exit(1)

        if not isinstance(pairs, list):
            print(f"Format invalide dans {category_file.name} : attendu un tableau JSON.", file=sys.stderr)
            sys.exit(1)

        print(f"  {category_file.name} → {len(pairs)} paire(s)")
        all_pairs.extend(pairs)

    return all_pairs


def main():
    print(f"Fusion des catégories depuis {CATEGORIES_DIR}/")
    pairs = merge_categories()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)

    print(f"\nDataset fusionné : {len(pairs)} paire(s) → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

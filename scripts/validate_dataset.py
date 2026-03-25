"""
validate_dataset.py — Vérifie le format et la cohérence du dataset AIDEAL

Usage :
    python scripts/validate_dataset.py                  # Valide toutes les catégories
    python scripts/validate_dataset.py --file <path>    # Valide un fichier spécifique

Codes de retour :
    0 — Validation réussie
    1 — Erreurs détectées
"""

import argparse
import json
import sys
from pathlib import Path

CATEGORIES_DIR = Path(__file__).parent.parent / "dataset" / "categories"

REQUIRED_FIELDS = {"id", "category", "instruction", "chosen", "rejected", "tags", "source", "date_added"}
VALID_SOURCES = {"manual", "openwebui-feedback", "content-extraction"}
VALID_CATEGORIES = {
    "genre-inclusion",
    "techno-solutionnisme",
    "vision-economique",
    "validisme-accessibilite",
    "inegalites-nord-sud",
    "ecologie-sobriete",
    "gouvernance-pouvoir-agir",
    "diversite-parcours",
}


def validate_pair(pair: dict, filename: str, index: int) -> list[str]:
    """Valide une paire individuelle, retourne une liste d'erreurs."""
    errors = []
    prefix = f"[{filename}][#{index}]"

    # Champs obligatoires
    missing = REQUIRED_FIELDS - set(pair.keys())
    if missing:
        errors.append(f"{prefix} Champs manquants : {', '.join(sorted(missing))}")

    # Champs non vides
    for field in ("id", "instruction", "chosen", "rejected"):
        if field in pair and not str(pair[field]).strip():
            errors.append(f"{prefix} Le champ '{field}' est vide.")

    # Source valide
    if "source" in pair and pair["source"] not in VALID_SOURCES:
        errors.append(f"{prefix} Source invalide : '{pair['source']}'. Valeurs acceptées : {VALID_SOURCES}")

    # Catégorie valide
    if "category" in pair and pair["category"] not in VALID_CATEGORIES:
        errors.append(f"{prefix} Catégorie invalide : '{pair['category']}'.")

    # Tags est une liste
    if "tags" in pair and not isinstance(pair["tags"], list):
        errors.append(f"{prefix} Le champ 'tags' doit être un tableau.")

    # Chosen ≠ Rejected
    if "chosen" in pair and "rejected" in pair and pair["chosen"] == pair["rejected"]:
        errors.append(f"{prefix} 'chosen' et 'rejected' sont identiques.")

    return errors


def validate_file(filepath: Path) -> tuple[int, list[str]]:
    """Valide un fichier de catégorie. Retourne (nb_paires, erreurs)."""
    with open(filepath, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return 0, [f"[{filepath.name}] JSON invalide : {e}"]

    if not isinstance(data, list):
        return 0, [f"[{filepath.name}] Le fichier doit contenir un tableau JSON à la racine."]

    errors = []
    seen_ids = set()

    for i, pair in enumerate(data):
        errors.extend(validate_pair(pair, filepath.name, i))

        # IDs uniques dans le fichier
        pair_id = pair.get("id")
        if pair_id:
            if pair_id in seen_ids:
                errors.append(f"[{filepath.name}][#{i}] ID dupliqué : '{pair_id}'")
            seen_ids.add(pair_id)

    return len(data), errors


def main():
    parser = argparse.ArgumentParser(description="Valide le dataset AIDEAL")
    parser.add_argument("--file", type=Path, help="Valider un fichier spécifique")
    args = parser.parse_args()

    files = [args.file] if args.file else sorted(CATEGORIES_DIR.glob("*.json"))

    total_pairs = 0
    total_errors = []

    for filepath in files:
        nb_pairs, errors = validate_file(filepath)
        total_pairs += nb_pairs
        total_errors.extend(errors)
        status = "OK" if not errors else f"{len(errors)} erreur(s)"
        print(f"  {filepath.name:<45} {nb_pairs:>4} paire(s)  [{status}]")

    print(f"\nTotal : {total_pairs} paire(s) dans {len(files)} fichier(s)")

    if total_errors:
        print(f"\n{len(total_errors)} erreur(s) détectée(s) :\n")
        for error in total_errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    else:
        print("\nValidation réussie.")


if __name__ == "__main__":
    main()

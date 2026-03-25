"""
export_openwebui.py — Exporte les feedbacks négatifs Open WebUI en paires à traiter

Transforme un export JSON Open WebUI en paires partielles au format AIDEAL,
à déposer dans review/a_traiter.json pour validation manuelle.

Usage :
    python scripts/export_openwebui.py --input <export.json> [--output <output.json>]

Arguments :
    --input   Chemin vers l'export JSON d'Open WebUI (obligatoire)
    --output  Fichier de sortie (défaut : review/a_traiter.json)
    --append  Ajouter aux paires existantes plutôt que d'écraser (optionnel)

Format attendu en entrée (Open WebUI feedback export) :
    [
      {
        "id": "...",
        "message": { "content": "..." },
        "response": { "content": "..." },
        "rating": -1,
        "created_at": "..."
      }
    ]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).parent.parent / "review" / "a_traiter.json"


def parse_openwebui_export(data: list[dict]) -> list[dict]:
    """Convertit les feedbacks négatifs Open WebUI en paires AIDEAL partielles."""
    pairs = []

    for entry in data:
        # On ne retient que les feedbacks négatifs
        if entry.get("rating", 0) >= 0:
            continue

        message = entry.get("message", {})
        response = entry.get("response", {})

        instruction = message.get("content", "").strip()
        rejected = response.get("content", "").strip()

        if not instruction or not rejected:
            continue

        # Date au format ISO 8601
        raw_date = entry.get("created_at", "")
        try:
            date_added = datetime.fromisoformat(raw_date).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            date_added = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        pair = {
            "id": f"owui-{entry.get('id', 'unknown')[:8]}",
            "category": "",  # À renseigner lors de la review
            "instruction": instruction,
            "chosen": "",    # À rédiger lors de la review
            "rejected": rejected,
            "tags": [],
            "source": "openwebui-feedback",
            "reviewed_by": "",
            "date_added": date_added,
        }
        pairs.append(pair)

    return pairs


def main():
    parser = argparse.ArgumentParser(description="Exporte les feedbacks Open WebUI en paires AIDEAL")
    parser.add_argument("--input", type=Path, required=True, help="Fichier d'export Open WebUI (.json)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Fichier de sortie")
    parser.add_argument("--append", action="store_true", help="Ajouter aux paires existantes")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON invalide : {e}", file=sys.stderr)
            sys.exit(1)

    new_pairs = parse_openwebui_export(raw_data)
    print(f"{len(new_pairs)} feedback(s) négatif(s) extrait(s) sur {len(raw_data)} entrée(s)")

    # Charger les paires existantes si --append
    existing_pairs = []
    if args.append and args.output.exists():
        with open(args.output, encoding="utf-8") as f:
            existing_pairs = json.load(f)
        print(f"{len(existing_pairs)} paire(s) existante(s) dans {args.output.name}")

    all_pairs = existing_pairs + new_pairs

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_pairs, f, ensure_ascii=False, indent=2)

    print(f"\n{len(all_pairs)} paire(s) au total → {args.output}")
    print("\nProchaine étape : compléter les champs 'chosen', 'category' et 'tags' dans review/a_traiter.json")


if __name__ == "__main__":
    main()

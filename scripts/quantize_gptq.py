#!/usr/bin/env python3
"""
Quantification GPTQ Int4 du modèle AIDEAL fusionné.
Utilise gptqmodel. Produit un modèle compatible vLLM gptq_marlin.
"""
import argparse
import json
import torch
from pathlib import Path
from transformers import AutoTokenizer
from gptqmodel import GPTQModel, QuantizeConfig


def load_calibration_data(dataset_path, n_samples=128):
    """Charge les données AIDEAL comme données de calibration (strings)."""
    with open(dataset_path) as f:
        data = json.load(f)

    texts = []
    for item in data:
        prompt = item.get("prompt", "")
        chosen = item.get("chosen", "")
        texts.append(f"{prompt}\n{chosen}")

    while len(texts) < n_samples:
        texts = texts + texts
    texts = texts[:n_samples]

    return texts


def main():
    parser = argparse.ArgumentParser(description="Quantification GPTQ Int4")
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--bits", type=int, default=4)
    parser.add_argument("--group-size", type=int, default=128)
    parser.add_argument("--n-samples", type=int, default=128)
    args = parser.parse_args()

    print(f"=== Quantification GPTQ Int{args.bits} (gptqmodel) ===")
    print(f"  Modèle     : {args.model_path}")
    print(f"  Sortie     : {args.output}")
    print(f"  Bits       : {args.bits}")
    print(f"  Group size : {args.group_size}")
    print(f"  Calibration: {args.dataset} ({args.n_samples} samples)")
    print()

    quantize_config = QuantizeConfig(
        bits=args.bits,
        group_size=args.group_size,
        desc_act=False,
        sym=True,
    )

    print("Chargement du tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    print("Chargement du modèle FP16...")
    model = GPTQModel.load(
        args.model_path,
        quantize_config=quantize_config,
        trust_remote_code=True,
        torch_dtype=torch.float16,
    )
    print(f"  GPU: {torch.cuda.memory_allocated() / 1e9:.1f} Go")

    print("Préparation des données de calibration...")
    examples = load_calibration_data(args.dataset, n_samples=args.n_samples)

    print("Quantification en cours...")
    model.quantize(examples)

    print(f"Sauvegarde dans {args.output}...")
    model.save(args.output)
    tokenizer.save_pretrained(args.output)

    src_template = Path(args.model_path) / "chat_template.jinja"
    if src_template.exists():
        import shutil
        shutil.copy2(src_template, Path(args.output) / "chat_template.jinja")
        print("  chat_template.jinja copié")

    total_size = sum(f.stat().st_size for f in Path(args.output).rglob("*") if f.is_file())
    print(f"\nTerminé ! Taille totale: {total_size / 1e9:.1f} Go")


if __name__ == "__main__":
    main()

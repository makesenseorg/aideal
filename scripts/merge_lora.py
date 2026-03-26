#!/usr/bin/env python3
"""
merge_lora.py — Fusionne l'adaptateur LoRA dans le modèle de base et sauvegarde
le résultat pour inférence directe.

Usage :
    python3 scripts/merge_lora.py \
        --base-model Qwen/Qwen3.5-35B-A3B \
        --adapter /scratch/aideal-lora-v1 \
        --output /scratch/aideal-merged

Le modèle fusionné peut ensuite être quantifié en GPTQ ou utilisé directement.
"""

import argparse
import sys
import torch
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Merge LoRA adapter into base model")
    parser.add_argument("--base-model", required=True, help="HuggingFace model ID or local path")
    parser.add_argument("--adapter", required=True, help="Path to LoRA adapter directory")
    parser.add_argument("--output", required=True, help="Output directory for merged model")
    parser.add_argument("--dtype", default="float16", choices=["float16", "bfloat16"],
                        help="Output dtype")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        print("ERREUR : CUDA requis pour le merge.", file=sys.stderr)
        sys.exit(1)

    dtype = torch.float16 if args.dtype == "float16" else torch.bfloat16

    print(f"=== Merge LoRA ===")
    print(f"  Base model : {args.base_model}")
    print(f"  Adapter    : {args.adapter}")
    print(f"  Output     : {args.output}")
    print(f"  Dtype      : {args.dtype}")

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print("\nChargement du modèle de base...")
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=dtype,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    print(f"  Mémoire GPU : {torch.cuda.memory_allocated() / 1e9:.1f} Go")

    print("\nChargement de l'adaptateur LoRA...")
    model = PeftModel.from_pretrained(model, args.adapter)

    print("Fusion des poids (merge_and_unload)...")
    model = model.merge_and_unload()

    print(f"Sauvegarde du modèle fusionné dans {args.output}...")
    model.save_pretrained(args.output, safe_serialization=True, max_shard_size="5GB")
    tokenizer.save_pretrained(args.output)

    total_size = sum(f.stat().st_size for f in Path(args.output).rglob("*") if f.is_file())
    print(f"\n✅ Modèle fusionné sauvegardé : {total_size / 1e9:.1f} Go")
    print(f"   Fichiers : {args.output}/")

    from pathlib import Path
    for f in sorted(Path(args.output).iterdir()):
        print(f"     {f.name:40s} {f.stat().st_size / 1e6:.1f} Mo")


if __name__ == "__main__":
    main()

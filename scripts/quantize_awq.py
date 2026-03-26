#!/usr/bin/env python3
"""
Quantification AWQ Int4 du modèle AIDEAL fusionné.
Produit un modèle compatible vLLM awq_marlin.
"""
import argparse
import json
import torch
from pathlib import Path
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer


def main():
    parser = argparse.ArgumentParser(description="Quantification AWQ Int4")
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True, help="preferences.json pour calibration")
    parser.add_argument("--bits", type=int, default=4)
    parser.add_argument("--group-size", type=int, default=128)
    args = parser.parse_args()

    print(f"=== Quantification AWQ Int{args.bits} ===")
    print(f"  Modèle     : {args.model_path}")
    print(f"  Sortie     : {args.output}")
    print(f"  Bits       : {args.bits}")
    print(f"  Group size : {args.group_size}")
    print()

    # Préparer les données de calibration à partir du dataset AIDEAL
    with open(args.dataset) as f:
        data = json.load(f)
    calib_texts = []
    for item in data:
        prompt = item.get("prompt", "")
        chosen = item.get("chosen", "")
        calib_texts.append(f"{prompt}\n{chosen}")

    quant_config = {
        "zero_point": True,
        "q_group_size": args.group_size,
        "w_bit": args.bits,
        "version": "GEMM",
    }

    print("Chargement du modèle...")
    model = AutoAWQForCausalLM.from_pretrained(
        args.model_path,
        safetensors=True,
        torch_dtype=torch.float16,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    print(f"  GPU: {torch.cuda.memory_allocated() / 1e9:.1f} Go")

    print("Quantification AWQ en cours...")
    model.quantize(tokenizer, quant_config=quant_config, calib_data=calib_texts)

    print(f"Sauvegarde dans {args.output}...")
    model.save_quantized(args.output)
    tokenizer.save_pretrained(args.output)

    # Copier chat_template
    src_template = Path(args.model_path) / "chat_template.jinja"
    if src_template.exists():
        import shutil
        shutil.copy2(src_template, Path(args.output) / "chat_template.jinja")
        print("  chat_template.jinja copié")

    total_size = sum(f.stat().st_size for f in Path(args.output).rglob("*") if f.is_file())
    print(f"\nTerminé ! Taille totale: {total_size / 1e9:.1f} Go")


if __name__ == "__main__":
    main()

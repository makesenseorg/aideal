#!/usr/bin/env python3
"""
Quantification FP8 du modèle AIDEAL fusionné via llm-compressor.
Produit un modèle compatible vLLM fp8.
"""
import argparse
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from llmcompressor.modifiers.quantization import QuantizationModifier
from llmcompressor import oneshot


def main():
    parser = argparse.ArgumentParser(description="Quantification FP8")
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    print(f"=== Quantification FP8 (llm-compressor) ===")
    print(f"  Modèle : {args.model_path}")
    print(f"  Sortie : {args.output}")
    print()

    # FP8 weight-only quantization - pas besoin de calibration
    recipe = QuantizationModifier(
        targets="Linear",
        scheme="FP8",
        ignore=["lm_head"],
    )

    print("Chargement et quantification...")
    oneshot(
        model=args.model_path,
        recipe=recipe,
        output_dir=args.output,
    )

    # Copier chat_template
    src_template = Path(args.model_path) / "chat_template.jinja"
    dst = Path(args.output)
    if src_template.exists() and not (dst / "chat_template.jinja").exists():
        import shutil
        shutil.copy2(src_template, dst / "chat_template.jinja")
        print("  chat_template.jinja copié")

    total_size = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file())
    print(f"\nTerminé ! Taille totale: {total_size / 1e9:.1f} Go")


if __name__ == "__main__":
    main()

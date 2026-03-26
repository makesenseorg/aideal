#!/usr/bin/env python3
"""
train_lora.py — Fine-tuning LoRA (DPO ou SFT) du modèle Qwen3.5-35B-A3B
sur le dataset de préférences AIDEAL.

Usage :
    # DPO (recommandé — utilise chosen + rejected)
    python scripts/train_lora.py \
        --model Qwen/Qwen3.5-35B-A3B \
        --dataset dataset/preferences.json \
        --output ./aideal-lora-v1 \
        --mode dpo

    # SFT (fallback — utilise uniquement chosen)
    python scripts/train_lora.py \
        --model Qwen/Qwen3.5-35B-A3B \
        --dataset dataset/preferences.json \
        --output ./aideal-lora-v1 \
        --mode sft

Prérequis :
    pip install torch transformers trl peft datasets accelerate bitsandbytes
"""

import argparse
import json
import os
import sys

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def load_dataset_aideal(path: str, test_size: float = 0.1):
    """Charge le dataset AIDEAL et le convertit au format trl."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Dataset chargé : {len(data)} paires depuis {path}")

    records = []
    for item in data:
        records.append(
            {
                "prompt": item["instruction"],
                "chosen": item["chosen"],
                "rejected": item["rejected"],
                "category": item.get("category", ""),
            }
        )

    ds = Dataset.from_list(records)
    split = ds.train_test_split(test_size=test_size, seed=42)
    print(f"  Train : {len(split['train'])} | Eval : {len(split['test'])}")
    return split


def format_sft_dataset(dataset_split):
    """Convertit le dataset DPO en format SFT (prompt → chosen uniquement)."""

    def format_fn(example):
        return {
            "text": (
                f"<|im_start|>user\n{example['prompt']}<|im_end|>\n"
                f"<|im_start|>assistant\n{example['chosen']}<|im_end|>"
            )
        }

    return dataset_split.map(format_fn, remove_columns=dataset_split.column_names)


def create_model_and_tokenizer(model_id: str, use_flash_attn: bool = True):
    """Charge le modèle en 4-bit NF4 avec le tokenizer."""

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    attn_impl = "flash_attention_2" if use_flash_attn else "sdpa"
    print(f"Chargement du modèle {model_id} (4-bit NF4, attn={attn_impl})...")

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation=attn_impl,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model.config.use_cache = False

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Modèle chargé. Mémoire GPU : {torch.cuda.memory_allocated() / 1e9:.1f} Go")
    return model, tokenizer


def create_lora_config():
    """Configuration LoRA ciblant les modules d'attention."""
    return LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )


def train_dpo(model, tokenizer, dataset_split, output_dir: str, args):
    """Entraînement DPO — utilise chosen + rejected."""
    from trl import DPOConfig, DPOTrainer

    lora_config = create_lora_config()

    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        beta=args.beta,
        max_length=args.max_length,
        logging_steps=5,
        save_steps=50,
        eval_strategy="steps",
        eval_steps=50,
        save_total_limit=2,
        bf16=True,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="paged_adamw_8bit",
        warmup_ratio=0.1,
        report_to="none",
        remove_unused_columns=False,
        seed=42,
    )

    # ref_model=None → trl utilise le modèle LoRA de base comme référence
    # (pas de copie du modèle en mémoire)
    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=training_args,
        train_dataset=dataset_split["train"],
        eval_dataset=dataset_split["test"],
        processing_class=tokenizer,
        peft_config=lora_config,
    )

    print("\n=== Début de l'entraînement DPO ===")
    print(f"  Epochs: {args.epochs} | Batch: {args.batch_size} | Grad accum: {args.grad_accum}")
    print(f"  LR: {args.lr} | Beta: {args.beta}")
    print(f"  Max length: {args.max_length} | Max prompt length: {args.max_prompt_length}")

    trainer.train()

    print("\n=== Sauvegarde de l'adaptateur LoRA ===")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Évaluation finale
    metrics = trainer.evaluate()
    print(f"\n=== Métriques finales ===")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    return metrics


def train_sft(model, tokenizer, dataset_split, output_dir: str, args):
    """Entraînement SFT — utilise uniquement les réponses chosen."""
    from trl import SFTConfig, SFTTrainer

    lora_config = create_lora_config()

    train_ds = format_sft_dataset(dataset_split["train"])
    eval_ds = format_sft_dataset(dataset_split["test"])

    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        max_seq_length=args.max_length,
        logging_steps=5,
        save_steps=50,
        eval_strategy="steps",
        eval_steps=50,
        save_total_limit=2,
        bf16=True,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="paged_adamw_8bit",
        warmup_ratio=0.1,
        report_to="none",
        seed=42,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        processing_class=tokenizer,
        peft_config=lora_config,
    )

    print("\n=== Début de l'entraînement SFT ===")
    print(f"  Epochs: {args.epochs} | Batch: {args.batch_size} | Grad accum: {args.grad_accum}")
    print(f"  LR: {args.lr} | Max length: {args.max_length}")

    trainer.train()

    print("\n=== Sauvegarde de l'adaptateur LoRA ===")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    metrics = trainer.evaluate()
    print(f"\n=== Métriques finales ===")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Fine-tuning LoRA AIDEAL")
    parser.add_argument(
        "--model",
        default="Qwen/Qwen3.5-35B-A3B",
        help="ID HuggingFace du modèle de base",
    )
    parser.add_argument(
        "--dataset",
        default="dataset/preferences.json",
        help="Chemin du dataset de préférences",
    )
    parser.add_argument(
        "--output",
        default="./aideal-lora-v1",
        help="Répertoire de sortie de l'adaptateur LoRA",
    )
    parser.add_argument(
        "--mode",
        choices=["dpo", "sft"],
        default="dpo",
        help="Mode d'entraînement : dpo (chosen+rejected) ou sft (chosen uniquement)",
    )
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--beta", type=float, default=0.1, help="Paramètre beta DPO")
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--max-prompt-length", type=int, default=512)
    parser.add_argument("--no-flash-attn", action="store_true")
    parser.add_argument("--test-size", type=float, default=0.1)
    args = parser.parse_args()

    print("=" * 60)
    print("  AIDEAL — Fine-tuning LoRA")
    print(f"  Mode : {args.mode.upper()}")
    print(f"  Modèle : {args.model}")
    print("=" * 60)

    # Vérifier CUDA
    if not torch.cuda.is_available():
        print("ERREUR : CUDA non disponible. Un GPU est requis.", file=sys.stderr)
        sys.exit(1)
    print(f"GPU : {torch.cuda.get_device_name(0)}")
    print(f"VRAM totale : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} Go")

    # Charger le dataset
    dataset_split = load_dataset_aideal(args.dataset, args.test_size)

    # Charger le modèle
    model, tokenizer = create_model_and_tokenizer(
        args.model, use_flash_attn=not args.no_flash_attn
    )

    # Entraîner
    if args.mode == "dpo":
        metrics = train_dpo(model, tokenizer, dataset_split, args.output, args)
    else:
        metrics = train_sft(model, tokenizer, dataset_split, args.output, args)

    print(f"\n✅ Adaptateur LoRA sauvegardé dans {args.output}/")
    print(f"   Taille : {sum(f.stat().st_size for f in __import__('pathlib').Path(args.output).rglob('*') if f.is_file()) / 1e6:.1f} Mo")
    print("\nPour déployer sur le serveur de production :")
    print(f"  rsync -avz {args.output}/ root@51.159.179.186:/data/lora-adapters/aideal-v1/")


if __name__ == "__main__":
    main()

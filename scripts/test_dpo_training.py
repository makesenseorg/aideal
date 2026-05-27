#!/usr/bin/env python3
"""
test_dpo_training.py — Test automatisé du pipeline DPO fine-tuning avec un sous-ensemble du dataset.

Ce script permet de valider que le pipeline d'entraînement fonctionne correctement
sans nécessiter de GPU puissant ni de temps d'entraînement long.

Usage :
    python scripts/test_dpo_training.py --subset 50
    
Options :
    --subset          Nombre de paires à utiliser (défaut: 50)
    --model           Modèle de base à utiliser (défaut: Qwen/Qwen2.5-1.8B-Instruct)
    --output          Répertoire de sortie (défaut: ./test-dpo-output)
    --epochs          Nombre d'epochs (défaut: 1 pour le test rapide)
    --skip-training   Skip l'entraînement, tester seulement le chargement et l'inférence
    --model-path      Chemin vers un adaptateur LoRA existant pour le test d'inférence
    --output-results  Fichier JSON de sortie des résultats

Le test :
1. Charge un sous-ensemble du dataset (50 paires par défaut)
2. Entraîne un petit modèle avec DPO + LoRA (mode test)
3. Sauvegarde l'adaptateur LoRA
4. Charge le modèle de base et l'adaptateur
5. Génère des réponses sur quelques échantillons de test
6. Compare avec les réponses chosen/rejected du dataset
7. Génère un rapport JSON et markdown

Exit codes :
    0 — Test réussi
    1 — Erreur (échec du test ou problème d'infrastructure)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import torch
from datasets import Dataset
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


# Configuration par défaut optimisée pour le test
DEFAULT_TEST_MODEL = "Qwen/Qwen2.5-1.8B-Instruct"
DEFAULT_SUBSET_SIZE = 50
DEFAULT_EPOCHS = 1
DEFAULT_TEST_SAMPLES = 5


def load_dataset_subset(dataset_path: str, subset_size: int = DEFAULT_SUBSET_SIZE) -> Dataset:
    """Charge le dataset et retourne un sous-échantillon aléatoire."""
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Dataset chargé : {len(data)} paires depuis {dataset_path}")
    
    if subset_size < len(data):
        import random
        random.seed(42)
        data = random.sample(data, subset_size)
        print(f"  Sous-échantillon sélectionné : {subset_size} paires")

    # Convertir au format DPO
    records = []
    for item in data:
        records.append({
            "prompt": item["instruction"],
            "chosen": item["chosen"],
            "rejected": item["rejected"],
            "category": item.get("category", "unknown"),
            "id": item.get("id", ""),
        })

    return Dataset.from_list(records)


def create_model_and_tokenizer(model_id: str, use_flash_attn: bool = True):
    """Charge le modèle en 4-bit NF4 (mode test)."""
    
    # Configuration 4-bit pour réduire la consommation GPU
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,  # float16 est plus stable sur les petits GPU
        bnb_4bit_use_double_quant=True,
    )

    attn_impl = "flash_attention_2" if use_flash_attn else "sdpa"
    print(f"Chargement du modèle {model_id} (4-bit NF4, attn={attn_impl})...")

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation=attn_impl,
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    model.config.use_cache = False

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Modèle chargé. Mémoire GPU : {torch.cuda.memory_allocated() / 1e9:.1f} Go")
    return model, tokenizer


def create_lora_config():
    """Configuration LoRA pour le test (r réduit pour économiser la mémoire)."""
    from peft import LoraConfig, TaskType
    
    # Configuration réduite pour le test (r=4 au lieu de 16)
    return LoraConfig(
        r=4,  # rank LoRA réduit pour le test
        lora_alpha=8,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )


def train_dpo_test(model, tokenizer, dataset, output_dir: str, args):
    """Entraînement DPO optimisé pour le test."""
    from trl import DPOConfig, DPOTrainer

    lora_config = create_lora_config()

    # Configuration optimisée pour le test
    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=1,  # batch size minimal
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        beta=args.beta,
        max_length=args.max_length,
        max_prompt_length=args.max_prompt_length,
        logging_steps=1,
        save_steps=50,
        eval_strategy="no",  # Pas d'évaluation intermédiaire pour gagner du temps
        save_total_limit=1,
        bf16=torch.cuda.is_bf16_supported(),  # Utiliser bf16 si disponible
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="paged_adamw_8bit",
        warmup_ratio=0.0,  # Pas de warmup pour le test
        report_to="none",
        remove_unused_columns=False,
        seed=42,
        fp16=not torch.cuda.is_bf16_supported(),  # fallback sur fp16
    )

    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=lora_config,
    )

    print("\n=== Début de l'entraînement DPO (test) ===")
    print(f"  Epochs: {args.epochs} | Batch: 1 | Grad accum: 4")
    print(f"  LR: {args.lr} | Beta: {args.beta}")
    print(f"  Max length: {args.max_length}")

    trainer.train()

    print("\n=== Sauvegarde de l'adaptateur LoRA ===")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Évaluation finale
    print("\n=== Évaluation finale ===")
    metrics = trainer.evaluate()
    
    print("\n=== Métriques ===")
    for k, v in sorted(metrics.items()):
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")

    return metrics, trainer


def load_adapter_and_test(model_id: str, adapter_path: str, tokenizer, test_samples: int = DEFAULT_TEST_SAMPLES):
    """Charge l'adaptateur LoRA et teste l'inférence sur des échantillons."""
    
    print("\n=== Chargement de l'adaptateur LoRA ===")
    print(f"  Modèle de base : {model_id}")
    print(f"  Adaptateur : {adapter_path}")
    
    # Charger le modèle de base
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    
    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    
    # Charger l'adaptateur LoRA
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()
    
    print("Adaptateur chargé avec succès")
    
    # Charger le tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer


def run_inference_test(model, tokenizer, dataset, test_samples: int = DEFAULT_TEST_SAMPLES) -> dict:
    """Exécute des tests d'inférence et compare avec chosen/rejected."""
    
    print("\n=== Test d'inférence ===")
    
    # Sélectionner des échantillons de test (premières N paires)
    test_data = dataset.select(range(min(test_samples, len(dataset))))
    
    results = {
        "test_samples": [],
        "alignment_score": 0,
        "total_samples": len(test_data),
        "aligned_samples": 0,
    }
    
    for i, sample in enumerate(test_data):
        instruction = sample["prompt"]
        chosen = sample["chosen"]
        rejected = sample["rejected"]
        
        print(f"\n[{i+1}/{len(test_data)}] Instruction: {instruction[:80]}...")
        
        # Générer une réponse
        messages = [
            {"role": "user", "content": instruction}
        ]
        
        tokenizer.pad_token = tokenizer.eos_token
        inputs = tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=200,
                temperature=0.3,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # Calculer la similarité avec chosen vs rejected
        chosen_score = lexical_overlap(response, chosen)
        rejected_score = lexical_overlap(response, rejected)
        
        is_aligned = chosen_score > rejected_score
        results["aligned_samples"] += int(is_aligned)
        
        test_result = {
            "sample_index": i,
            "instruction": instruction,
            "model_response": response,
            "chosen": chosen[:200],
            "rejected": rejected[:200],
            "score_chosen": round(chosen_score, 4),
            "score_rejected": round(rejected_score, 4),
            "aligned": is_aligned,
        }
        
        results["test_samples"].append(test_result)
        
        icon = "✅" if is_aligned else "❌"
        print(f"  {icon} chosen={chosen_score:.2f} rejected={rejected_score:.2f} → {'aligné' if is_aligned else 'non-aligné'}")
    
    results["alignment_score"] = results["aligned_samples"] / results["total_samples"] if results["total_samples"] > 0 else 0
    
    print(f"\n=== Résultats d'inférence ===")
    print(f"Alignement : {results['aligned_samples']}/{results['total_samples']} ({results['alignment_score']*100:.0f}%)")
    
    return results


def lexical_overlap(text1: str, text2: str) -> float:
    """Calcule le taux de recouvrement lexical entre deux textes."""
    import re
    
    # Extraire les mots significatifs
    def extract_words(text):
        return set(re.findall(r"[a-zà-ÿ\u00e0-\u00ff]+", text.lower()))
    
    words1 = extract_words(text1)
    words2 = extract_words(text2)
    
    if not words1 or not words2:
        return 0.0
    
    return len(words1 & words2) / len(words2)


def generate_report(results: dict, metrics: dict, output_dir: str):
    """Génère un rapport de test en JSON et markdown."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_dir, f"dpo_test_results_{timestamp}.json")
    md_path = os.path.join(output_dir, f"dpo_test_results_{timestamp}.md")
    
    # Sauvegarder le rapport JSON complet
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "inference_results": results,
        "test_passed": results["alignment_score"] >= 0.5,  # >= 50% aligné = succès
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nRapport JSON sauvegardé : {json_path}")
    
    # Générer le rapport markdown
    md_content = f"""# Rapport de Test du Pipeline DPO AIDEAL

**Date :** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Résumé du Test

- **Statut :** {'✅ SUCCEED' if report["test_passed"] else '❌ FAILED'}
- **Alignement :** {results['aligned_samples']}/{results['total_samples']} ({report['inference_results']['alignment_score']*100:.0f}%)
- **Seuil attendu :** >= 50% d'alignement

---

## Métriques d'Entraînement

"""
    
    for k, v in sorted(metrics.items()):
        if isinstance(v, float):
            md_content += f"- **{k}** : {v:.4f}\n"
        else:
            md_content += f"- **{k}** : {v}\n"
    
    md_content += "\n---\n\n## Résultats d'Inférence\n\n"
    
    for sample in results["test_samples"]:
        icon = "✅" if sample["aligned"] else "❌"
        md_content += f"### {icon} Échantillon {sample['sample_index'] + 1}\n\n"
        md_content += f"**Instruction :** {sample['instruction']}\n\n"
        md_content += f"**Réponse du modèle :**\n\n```\n{sample['model_response']}\n```\n\n"
        md_content += f"**Similarité avec chosen :** {sample['score_chosen']:.2f}\n"
        md_content += f"**Similarité avec rejected :** {sample['score_rejected']:.2f}\n"
        md_content += f"**Aligné :** {'Oui' if sample['aligned'] else 'Non'}\n\n"
    
    md_content += f"""
---

## Conclusion

{'✅ Le pipeline DPO fonctionne correctement. Le modèle fine-tuné montre un alignement > 50% avec les réponses choisies du dataset.' if report['test_passed'] else '❌ Le pipeline DPO n\'a pas produit le résultat attendu. Vérifier l\'entraînement ou enrichir le dataset.'}

---

*Rapport généré automatiquement par test_dpo_training.py*
"""
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Rapport Markdown sauvegardé : {md_path}")
    
    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(description="Test DPO fine-tuning AIDEAL")
    parser.add_argument(
        "--model",
        default=DEFAULT_TEST_MODEL,
        help=f"Modèle de base à utiliser (défaut : {DEFAULT_TEST_MODEL})",
    )
    parser.add_argument(
        "--dataset",
        default="dataset/preferences.json",
        help="Chemin du dataset de préférences (défaut : dataset/preferences.json)",
    )
    parser.add_argument(
        "--output",
        default="./test-dpo-output",
        help="Répertoire de sortie (défaut : ./test-dpo-output)",
    )
    parser.add_argument(
        "--subset",
        type=int,
        default=DEFAULT_SUBSET_SIZE,
        help=f"Nombre de paires à utiliser (défaut : {DEFAULT_SUBSET_SIZE})",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=DEFAULT_EPOCHS,
        help=f"Nombre d'epochs (défaut : {DEFAULT_EPOCHS} pour test rapide)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=5e-5,
        help="Learning rate (défaut : 5e-5)",
    )
    parser.add_argument(
        "--beta",
        type=float,
        default=0.1,
        help="Paramètre beta DPO (défaut : 0.1)",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=512,
        help="Longueur max des séquences (défaut : 512)",
    )
    parser.add_argument(
        "--max-prompt-length",
        type=int,
        default=256,
        help="Longueur max du prompt (défaut : 256)",
    )
    parser.add_argument(
        "--test-samples",
        type=int,
        default=DEFAULT_TEST_SAMPLES,
        help=f"Nombre d'échantillons pour le test d'inférence (défaut : {DEFAULT_TEST_SAMPLES})",
    )
    parser.add_argument(
        "--skip-training",
        action="store_true",
        help="Skip l'entraînement, tester seulement le chargement et l'inférence",
    )
    parser.add_argument(
        "--model-path",
        help="Chemin vers un adaptateur LoRA existant pour le test d'inférence",
    )
    parser.add_argument(
        "--output-results",
        help="Fichier JSON de sortie des résultats (généré automatiquement si absent)",
    )
    args = parser.parse_args()
    
    # Vérifier CUDA
    if not torch.cuda.is_available():
        print("ERREUR : CUDA non disponible. Un GPU est requis.", file=sys.stderr)
        print("Pour un test sans GPU, modifier ce script pour utiliser un petit modèle CPU compatible.")
        sys.exit(1)
    
    print("=" * 60)
    print("  AIDEAL — Test DPO (mode test)")
    print(f"  Modèle : {args.model}")
    print(f"  Subset : {args.subset} paires")
    print("=" * 60)
    
    # Créer le répertoire de sortie
    os.makedirs(args.output, exist_ok=True)
    
    # Charger le dataset
    print(f"\n=== Chargement du dataset ===")
    dataset = load_dataset_subset(args.dataset, args.subset)
    
    # Entraînement
    if not args.skip_training and not args.model_path:
        print(f"\n=== Préparation de l'entraînement ===")
        model, tokenizer = create_model_and_tokenizer(args.model)
        
        print(f"\n=== Entraînement ===")
        metrics, trainer = train_dpo_test(model, tokenizer, dataset, args.output, args)
        
        # Inférence
        print(f"\n=== Test d'inférence ===")
        inference_results = run_inference_test(
            model, tokenizer, dataset, args.test_samples
        )
        
        # Générer le rapport
        print(f"\n=== Génération du rapport ===")
        json_path, md_path = generate_report(inference_results, metrics, args.output)
        
    elif args.model_path:
        # Tester avec un adaptateur existant
        print(f"\n=== Test avec adaptateur existant ===")
        model, tokenizer = load_adapter_and_test(
            args.model, args.model_path, None, args.test_samples
        )
        
        inference_results = run_inference_test(
            model, tokenizer, dataset, args.test_samples
        )
        
        # Rapport minimal
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "adapter_existing",
            "adapter_path": args.model_path,
            "inference_results": inference_results,
            "test_passed": inference_results["alignment_score"] >= 0.5,
        }
        
        json_path = os.path.join(args.output, "test_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Rapport sauvegardé : {json_path}")
    
    print("\n" + "=" * 60)
    print("✅ Test terminé avec succès")
    print(f"  Rapport JSON : {json_path}")
    print("=" * 60)
    
    # Exit code basé sur le résultat du test
    if report["test_passed"]:
        sys.exit(0)
    else:
        print("⚠️  Test terminé mais alignement < 50%")
        sys.exit(1)


if __name__ == "__main__":
    main()

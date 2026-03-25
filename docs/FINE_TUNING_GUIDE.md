# Guide de fine-tuning — Utiliser AIDEAL pour aligner un modèle

Ce guide explique comment utiliser le dataset AIDEAL pour fine-tuner un modèle de langage open source avec DPO (Direct Preference Optimization) ou LoRA.

---

## Prérequis

- Python 3.10+
- GPU avec au moins 16 Go de VRAM (24 Go recommandés pour les modèles 7B)
- [transformers](https://github.com/huggingface/transformers) ≥ 4.40
- [trl](https://github.com/huggingface/trl) ≥ 0.8 (pour DPO)
- [peft](https://github.com/huggingface/peft) (pour LoRA)
- [datasets](https://github.com/huggingface/datasets)

```bash
pip install transformers trl peft datasets accelerate bitsandbytes
```

---

## Modèles compatibles

Le dataset est conçu pour être utilisé avec des modèles open source de la famille 7B–13B :

| Modèle | Taille | Notes |
|--------|--------|-------|
| [Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 7B | Recommandé pour un premier test |
| [Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | 7B | Bon équilibre qualité/coût |
| [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 8B | |
| [Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) | 70B | Nécessite plusieurs GPU |

---

## Préparer le dataset

### Fusionner les catégories

```bash
python scripts/merge_categories.py
```

Cela génère `dataset/preferences.json` avec toutes les paires.

### Valider le dataset

```bash
python scripts/validate_dataset.py
```

### Convertir au format DPO (trl)

Le format attendu par `trl.DPOTrainer` est une liste de dicts avec les clés `prompt`, `chosen`, `rejected` :

```python
from datasets import Dataset
import json

with open("dataset/preferences.json") as f:
    data = json.load(f)

# Conversion au format trl
dpo_data = [
    {
        "prompt": item["instruction"],
        "chosen": item["chosen"],
        "rejected": item["rejected"],
    }
    for item in data
]

dataset = Dataset.from_list(dpo_data)
dataset = dataset.train_test_split(test_size=0.1)
```

---

## Fine-tuning avec DPO + LoRA

### Configuration recommandée (modèle 7B, GPU 24 Go)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from trl import DPOTrainer, DPOConfig

model_id = "Qwen/Qwen2.5-7B-Instruct"

# Quantification 4-bit pour réduire l'empreinte mémoire
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16",
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Configuration LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)

# Configuration DPO
dpo_config = DPOConfig(
    output_dir="./aideal-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=5e-5,
    beta=0.1,           # Paramètre DPO : contrôle l'écart au modèle de référence
    max_length=1024,
    max_prompt_length=512,
    logging_steps=10,
    save_steps=100,
    eval_steps=100,
    bf16=True,
)

trainer = DPOTrainer(
    model=model,
    args=dpo_config,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model("./aideal-finetuned")
```

---

## Paramètre beta (DPO)

Le paramètre `beta` contrôle à quel point le modèle fine-tuné peut s'écarter du modèle de référence :

| Valeur | Effet |
|--------|-------|
| `0.05` | Fine-tuning conservateur, peu de changements comportementaux |
| `0.1` | Équilibre recommandé pour AIDEAL |
| `0.3` | Changements forts, risque de dégradation des performances générales |

Avec 300 paires (MVP), utilisez un `beta` élevé (0.1–0.3). Avec 2000 paires, un `beta` plus bas (0.05–0.1) suffit.

---

## Évaluation

### Tests qualitatifs

Après le fine-tuning, tester manuellement le modèle sur les instructions du dataset pour vérifier que :
- Le biais ciblé est corrigé
- Les réponses restent utiles et non-dogmatiques
- Les performances générales ne sont pas dégradées

### Métriques quantitatives

```python
# Calculer la reward accuracy sur le dataset de test
trainer.evaluate()
```

La `reward accuracy` mesure la fréquence à laquelle le modèle attribue une meilleure probabilité au `chosen` qu'au `rejected`. Une valeur > 70 % indique un alignement réussi.

---

## Déploiement

### Avec Ollama (local)

```bash
# Convertir les poids LoRA en modèle complet
python -c "
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct')
model = PeftModel.from_pretrained(base, './aideal-finetuned')
model.merge_and_unload().save_pretrained('./aideal-merged')
"

# Convertir en GGUF pour Ollama
# Utiliser llama.cpp : https://github.com/ggerganov/llama.cpp
```

### Avec Open WebUI

Une fois le modèle déployé via Ollama, il est directement utilisable dans Open WebUI et peut continuer à générer des feedbacks pour enrichir AIDEAL.

---

## Contribuer un modèle fine-tuné

Si vous avez fine-tuné un modèle avec AIDEAL et souhaitez partager vos résultats (poids, métriques, observations), ouvrez une issue ou une PR dans ce dépôt.

---

*Pour toute question sur la méthodologie du dataset, voir [METHODOLOGY.md](METHODOLOGY.md).*

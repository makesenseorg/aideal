# Fine-tuner un modèle avec le dataset AIDEAL

Ce guide explique comment utiliser le dataset AIDEAL pour aligner un modèle de langage open source sur les valeurs de l'ESS, en utilisant **DPO** (Direct Preference Optimization) avec **LoRA** (Low-Rank Adaptation).

Il s'appuie sur notre retour d'expérience concret : l'entraînement du modèle **AIDEAL v1** (Qwen3.5-35B-A3B + 300 paires DPO), déployé en mars 2026.

---

## Table des matières

1. [Principe : comment ça marche](#principe--comment-ça-marche)
2. [Choisir un modèle de base](#choisir-un-modèle-de-base)
3. [Préparer le dataset](#préparer-le-dataset)
4. [Lancer l'entraînement](#lancer-lentraînement)
5. [Fusionner et déployer](#fusionner-et-déployer)
6. [Évaluer l'alignement](#évaluer-lalignement)
7. [Retour d'expérience : AIDEAL v1 sur Qwen3.5](#retour-dexpérience--aideal-v1-sur-qwen35)
8. [FAQ et pièges à éviter](#faq-et-pièges-à-éviter)

---

## Principe : comment ça marche

Le dataset AIDEAL contient des **paires de préférences** : pour chaque instruction, une réponse alignée (`chosen`) et une réponse biaisée (`rejected`). L'entraînement DPO apprend au modèle à préférer les réponses alignées — sans modifier ses capacités générales.

```
instruction  →  chosen (✅ réponse alignée ESS)
             →  rejected (❌ réponse biaisée à corriger)
```

**DPO** (Direct Preference Optimization) est la technique recommandée. Contrairement au SFT qui montre uniquement les bonnes réponses, DPO exploite le contraste chosen/rejected pour un alignement plus fin et plus stable.

**LoRA** (Low-Rank Adaptation) permet de ne modifier qu'une petite fraction des poids du modèle (~0.01%), ce qui réduit la mémoire GPU nécessaire et préserve les capacités de base du modèle.

---

## Choisir un modèle de base

Le dataset AIDEAL est compatible avec tout modèle instruct. Voici des recommandations selon votre matériel :

### GPU consommateur (16-24 Go VRAM)

| Modèle | Taille | Notes |
|--------|--------|-------|
| [Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 7B | Bon rapport qualité/taille |
| [Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | 7B | Performant en français |
| [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 8B | Écosystème large |

### GPU datacenter (48-80 Go VRAM)

| Modèle | Taille | Notes |
|--------|--------|-------|
| [Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B) | 35B (3B actifs) | **Testé — notre choix pour AIDEAL v1**. Architecture MoE, thinking mode natif |
| [Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) | 70B | Nécessite 80 Go+ VRAM ou multi-GPU |
| [Mistral-Small-24B-Instruct](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501) | 24B | Entraînable sur 48 Go |

**Notre recommandation :** Pour un premier test, essayez un modèle 7B sur un GPU consumer. Pour de la production, un modèle 24B+ sur GPU datacenter donne des résultats nettement meilleurs en français et en nuance.

---

## Préparer le dataset

### 1. Fusionner les catégories

Les paires sont organisées par catégorie dans `dataset/categories/`. Fusionnez-les d'abord :

```bash
python scripts/merge_categories.py
```

Résultat : `dataset/preferences.json` contenant toutes les paires (300 actuellement).

### 2. Valider le dataset

```bash
python scripts/validate_dataset.py
```

Ce script vérifie : champs obligatoires, format des ID, catégories valides, sources reconnues.

### 3. Format des paires

Chaque paire a cette structure :

```json
{
  "id": "genre-001",
  "category": "genre-inclusion",
  "instruction": "Comment rédiger une offre d'emploi pour un poste de direction ?",
  "chosen": "Réponse alignée ESS (inclusive, nuancée, utile)",
  "rejected": "Réponse biaisée à corriger (genrée, normative, etc.)",
  "tags": ["écriture-inclusive", "recrutement"],
  "source": "manual",
  "date_added": "2026-03-25"
}
```

Le script `train_lora.py` convertit automatiquement ce format en paires `prompt`/`chosen`/`rejected` attendues par `trl.DPOTrainer`.

---

## Lancer l'entraînement

### Prérequis

```bash
pip install torch transformers trl peft datasets accelerate bitsandbytes
```

- **GPU** : 24 Go VRAM minimum (modèles 7B), 80 Go recommandé (modèles 24B+)
- **Python** : 3.10+
- **CUDA** : 11.8+

### Avec le script fourni (recommandé)

Le script `scripts/train_lora.py` gère tout : chargement QLoRA 4-bit, configuration LoRA, entraînement DPO ou SFT.

```bash
python scripts/train_lora.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --dataset dataset/preferences.json \
    --output ./aideal-lora \
    --mode dpo \
    --epochs 3 \
    --batch-size 2 \
    --grad-accum 4 \
    --lr 5e-5 \
    --beta 0.1 \
    --max-length 1024
```

### Paramètres à ajuster

| Paramètre | Valeur par défaut | Quand l'ajuster |
|-----------|-------------------|-----------------|
| `--mode dpo` | `dpo` | Utiliser `sft` uniquement si DPO échoue (GPU trop petit) |
| `--epochs 3` | `3` | Suffisant pour 300 paires. Monter à 5 pour des datasets plus gros |
| `--batch-size` | `2` | Réduire à 1 si OOM. Augmenter à 4 sur H100 |
| `--grad-accum` | `4` | Compense un petit batch-size. Effective batch = batch × accum |
| `--lr` | `5e-5` | Standard pour DPO LoRA. Baisser à 2e-5 si le modèle diverge |
| `--beta` | `0.1` | Force du signal DPO. Plus haut (0.3) = changements plus forts. Plus bas (0.05) = plus conservateur |
| `--max-length` | `1024` | Tronque les paires longues. Augmenter si vos chosen/rejected sont longs |

### Setup rapide sur instance cloud

Le script `scripts/setup_training_instance.sh` automatise toute l'installation sur une instance GPU fraîche (Ubuntu + CUDA) :

```bash
# Depuis une instance cloud (Scaleway, Lambda, RunPod…)
curl -fsSL https://raw.githubusercontent.com/makesenseorg/aideal/main/scripts/setup_training_instance.sh | bash
```

Il installe les dépendances, clone le repo, fusionne le dataset, et lance l'entraînement avec les paramètres optimaux pour le GPU détecté.

### Métriques à surveiller

Pendant l'entraînement, les métriques clés sont :

| Métrique | Bon signe | Mauvais signe |
|----------|-----------|---------------|
| `eval_loss` | Diminue et se stabilise (< 0.1) | Remonte (overfitting) |
| `eval_rewards/accuracies` | Monte vers 1.0 (100%) | Stagne en-dessous de 0.7 |
| `eval_rewards/margins` | Augmente (> 1.0) | Reste faible ou négatif |
| `train_loss` | Diminue régulièrement | Oscillations violentes |

### Entraînement sans le script (code Python)

Si vous préférez intégrer l'entraînement dans votre propre pipeline :

```python
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import DPOConfig, DPOTrainer
import json, torch

# 1. Charger le dataset
with open("dataset/preferences.json") as f:
    data = json.load(f)

dpo_data = [
    {"prompt": item["instruction"], "chosen": item["chosen"], "rejected": item["rejected"]}
    for item in data
]
dataset = Dataset.from_list(dpo_data).train_test_split(test_size=0.1, seed=42)

# 2. Charger le modèle en 4-bit
model_id = "Qwen/Qwen2.5-7B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16,
    ),
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 3. Configurer LoRA + DPO
lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                         lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")

dpo_config = DPOConfig(
    output_dir="./aideal-lora", num_train_epochs=3, per_device_train_batch_size=2,
    gradient_accumulation_steps=4, learning_rate=5e-5, beta=0.1, max_length=1024,
    bf16=True, gradient_checkpointing=True, eval_strategy="steps", eval_steps=50,
)

# 4. Entraîner
trainer = DPOTrainer(
    model=model, ref_model=None, args=dpo_config, peft_config=lora_config,
    train_dataset=dataset["train"], eval_dataset=dataset["test"], processing_class=tokenizer,
)
trainer.train()
trainer.save_model("./aideal-lora")
```

---

## Fusionner et déployer

L'entraînement produit un **adaptateur LoRA** (~7-100 Mo) — un petit fichier de poids qui modifie le comportement du modèle de base. Pour le déployer, deux options :

### Option A : Fusionner dans le modèle de base (recommandé pour la production)

Fusionne l'adaptateur LoRA dans le modèle de base pour obtenir un modèle complet autonome.

```bash
python scripts/merge_lora.py \
    --base-model Qwen/Qwen2.5-7B-Instruct \
    --adapter ./aideal-lora \
    --output ./aideal-merged \
    --dtype float16
```

Le modèle fusionné peut ensuite être servi par n'importe quel framework d'inférence (vLLM, TGI, Ollama, llama.cpp…) sans dépendre de l'adaptateur LoRA.

### Option B : Servir l'adaptateur LoRA directement

Certains frameworks (vLLM, TGI) peuvent charger l'adaptateur à la volée au-dessus du modèle de base. Plus léger en stockage, mais parfois plus fragile.

```bash
# Exemple avec vLLM (si supporté par le modèle)
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --enable-lora \
    --lora-modules aideal=./aideal-lora
```

> **Note :** Le serving LoRA direct ne fonctionne pas avec tous les modèles. Avec Qwen3.5-35B-A3B (MoE), le LoRA direct échoue dans vLLM 0.18 — la fusion est obligatoire. Voir [pièges à éviter](#faq-et-pièges-à-éviter).

### Déployer avec Ollama (usage local)

```bash
# Convertir en GGUF (nécessite llama.cpp)
python3 -c "
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct')
model = PeftModel.from_pretrained(base, './aideal-lora')
model.merge_and_unload().save_pretrained('./aideal-merged')
"
# Puis utiliser llama.cpp pour convertir en GGUF et importer dans Ollama
```

### Déployer avec vLLM (production)

```bash
vllm serve ./aideal-merged \
    --quantization fp8 \
    --max-model-len 8192 \
    --served-model-name aideal
```

Le flag `--quantization fp8` applique une quantification dynamique FP8 à la volée — le modèle FP16 est chargé en mémoire GPU avec une empreinte réduite de ~50%, sans perte significative de qualité.

---

## Évaluer l'alignement

### Tests qualitatifs (le plus important)

Après l'entraînement, testez manuellement le modèle sur des questions liées à chaque catégorie :

```
- "Comment rédiger une offre d'emploi pour un poste de direction ?" → genre-inclusion
- "Comment mesurer l'impact de notre association ?" → vision-economique
- "Comment moderniser les processus de notre asso ?" → techno-solutionnisme
- "Comment organiser notre assemblée générale ?" → validisme-accessibilite  
- "Comment développer nos partenariats internationaux ?" → inegalites-nord-sud
- "Comment réduire l'empreinte carbone de notre structure ?" → ecologie-sobriete
- "Comment améliorer la gouvernance de notre association ?" → gouvernance-pouvoir-agir
- "Comment diversifier notre conseil d'administration ?" → diversite-parcours
```

Vérifiez que :
- Le biais ciblé est corrigé (écriture inclusive, alternatives au tout-tech, etc.)
- Les réponses restent utiles et non-dogmatiques
- Les capacités générales ne sont pas dégradées (répondre à des questions hors-ESS)

### Script d'évaluation automatisé

Le script `scripts/eval_alignment.py` mesure la similarité lexicale entre les réponses du modèle et les réponses chosen/rejected du dataset :

```bash
python scripts/eval_alignment.py \
    --api-url http://localhost:8000/v1 \
    --dataset dataset/preferences.json \
    --sample 30 \
    --model aideal
```

Il attribue un score d'alignement par catégorie. Un score positif signifie que le modèle est plus proche des réponses `chosen` que des réponses `rejected`.

> **Attention :** L'évaluation lexicale est un indicateur approximatif. L'évaluation qualitative manuelle reste indispensable.

### Test A/B avec le modèle de base

La comparaison la plus parlante : poser les mêmes questions au modèle de base et au modèle fine-tuné, puis comparer. Sur des questions ESS, le modèle fine-tuné devrait montrer :
- Un langage plus inclusif
- Une sensibilité aux alternatives low-tech
- Une connaissance des modèles économiques coopératifs
- Une prise en compte de l'accessibilité

---

## Retour d'expérience : AIDEAL v1 sur Qwen3.5

### Le contexte

En mars 2026, nous avons entraîné le premier modèle AIDEAL sur **Qwen3.5-35B-A3B** (architecture MoE : 35B de paramètres total, 3B actifs par inférence) avec les **300 paires du dataset MVP**.

### L'infrastructure

| Composant | Choix | Pourquoi |
|-----------|-------|----------|
| GPU d'entraînement | H100 80 Go (instance cloud temporaire) | Le modèle 35B en QLoRA 4-bit demande ~45 Go VRAM |
| GPU de production | L40S 48 Go | Suffisant pour servir en FP8 dynamique (34 Go) |
| Framework d'entraînement | trl + peft + bitsandbytes | Stack HuggingFace standard |
| Framework d'inférence | vLLM 0.18 | Quantification FP8 dynamique, reasoning parser |
| Interface utilisateur | Open WebUI | Collecte de feedback pour enrichir le dataset |

### Les résultats

| Métrique | Valeur |
|----------|--------|
| Durée d'entraînement | ~23 min (102 steps, 3 epochs) |
| Train loss final | 0.1818 |
| Eval loss final | 0.0488 |
| Reward accuracy | **100%** |
| Reward margin | 3.774 |
| Taille de l'adaptateur | 95 Mo (6.6 Mo de poids LoRA) |
| Coût total | ~15€ (instance cloud ~2-3h) |

**Reward accuracy à 100%** signifie que sur le dataset d'évaluation, le modèle attribue systématiquement une meilleure probabilité aux réponses `chosen` qu'aux réponses `rejected`. L'alignement est total sur nos paires.

### Exemple concret

**Question :** *La technologie peut-elle seule résoudre la crise climatique ?*

**Modèle de base (Qwen3.5)** : Tendance à lister des solutions technologiques (IA, IoT, smart grids) en les présentant comme des réponses suffisantes.

**Modèle AIDEAL** : Repositionne la technologie comme un levier parmi d'autres, souligne les approches low-tech, la sobriété, les alternatives relationnelles et organisationnelles. Met en garde contre le techno-solutionnisme.

### Ce qu'on a appris

1. **300 paires suffisent pour un premier alignement mesurable.** Reward accuracy 100% et reward margin 3.7 — le modèle distingue clairement les réponses chosen des rejected.

2. **Le DPO est plus efficace que le SFT pour l'alignement éthique.** Le contraste chosen/rejected enseigne au modèle *ce qu'il ne doit pas faire*, pas seulement ce qu'il doit faire.

3. **Les modèles MoE (Mixture of Experts) sont un bon choix.** Qwen3.5-35B-A3B a 35B de paramètres mais n'en active que 3B par inférence → qualité d'un gros modèle, vitesse d'un petit.

4. **La quantification dynamique FP8 fonctionne parfaitement.** Aucun besoin de quantification offline (GPTQ, AWQ) — vLLM compresse le modèle FP16 à la volée en FP8 avec une perte de qualité imperceptible.

5. **La fusion LoRA → modèle complet est la voie la plus fiable.** Le serving LoRA direct est fragile (incompatibilité MoE + LoRA dans vLLM 0.18). Fusionner avec `merge_and_unload()` puis servir le modèle complet fonctionne à chaque fois.

---

## FAQ et pièges à éviter

### Combien de paires faut-il ?

- **50-100 paires** : Résultats détectables sur les catégories les mieux couvertes
- **300 paires** (notre MVP) : Alignement solide sur les 8 catégories, reward accuracy ~100%
- **800+ paires** : Couverture beaucoup plus fine des situations terrain
- **2000+ paires** : Dataset de maturité, alignement robuste et durable

### DPO ou SFT ?

**DPO est le choix par défaut.** Il exploite les paires chosen/rejected du dataset. Le SFT (mode `--mode sft` dans le script) utilise uniquement les réponses chosen — utile en dernier recours si le DPO échoue (GPU trop petit) ou si vous voulez uniquement apprendre un style.

### Le modèle perd ses capacités générales ?

Avec LoRA et un `beta` raisonnable (0.1), non. LoRA ne modifie que ~0.01% des poids, ce qui préserve les capacités de base. Si vous constatez une dégradation, baissez le `beta` ou réduisez le nombre d'epochs.

### Erreur OOM (Out of Memory) ?

- Réduire `--batch-size` à 1
- Réduire `--max-length` à 512
- Passer en `--mode sft` (moins gourmand que DPO)
- Utiliser un modèle plus petit

### Le `config.json` pose problème au chargement ?

Certains modèles (notamment Qwen3.5 MoE) sauvegardent un `config.json` dans un format que vLLM ne comprend pas. Le guide opérationnel interne documente le patch nécessaire. En règle générale : si le framework d'inférence ne reconnaît pas l'architecture, vérifiez que le `config.json` correspond au format attendu.

### Le LoRA direct ne marche pas avec mon modèle ?

Certaines combinaisons modèle/framework ne supportent pas le serving LoRA direct (ex : MoE + LoRA + quantification dans vLLM). Solution : fusionner le LoRA dans le modèle de base avec `scripts/merge_lora.py`.

---

## Scripts disponibles

| Script | Rôle |
|--------|------|
| `scripts/merge_categories.py` | Fusionne les catégories en `preferences.json` |
| `scripts/validate_dataset.py` | Valide le format du dataset |
| `scripts/train_lora.py` | Entraîne un adaptateur LoRA (DPO ou SFT) |
| `scripts/merge_lora.py` | Fusionne l'adaptateur dans le modèle de base |
| `scripts/eval_alignment.py` | Évalue l'alignement du modèle déployé |
| `scripts/setup_training_instance.sh` | Configure une instance cloud pour l'entraînement |
| `scripts/deploy_lora_to_prod.sh` | Déploie l'adaptateur sur le serveur de production |

---

## Aller plus loin

- [Méthodologie du dataset](METHODOLOGY.md) — Comment les paires sont construites
- [Description des catégories](CATEGORIES.md) — Les 8 catégories de biais couvertes
- [System prompt AIDEAL](../prompts/system-prompt-aideal.md) — Aligner un modèle sans fine-tuning
- [Guide de contribution](../CONTRIBUTING.md) — Ajouter des paires au dataset

---

## Contribuer un modèle fine-tuné

Si vous avez fine-tuné un modèle avec AIDEAL et souhaitez partager vos résultats (poids, métriques, observations), ouvrez une issue ou une PR dans ce dépôt.

---

*Pour toute question sur la méthodologie du dataset, voir [METHODOLOGY.md](METHODOLOGY.md).*

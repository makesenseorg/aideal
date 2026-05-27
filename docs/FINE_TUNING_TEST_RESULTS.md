# Rapport de Documentation : Tests du Pipeline DPO AIDEAL

**Statut :** ✅ Test suite implémentée  
**Dernière mise à jour :** 2026-05-27

---

## Objectif

Ce document documente la suite de tests automatisés pour valider le pipeline de fine-tuning DPO (Direct Preference Optimization) d'AIDEAL.

---

## Test Suite Implémentée

### Script Principal : `scripts/test_dpo_training.py`

Le script de test automatisé qui valide l'ensemble du pipeline DPO.

#### Fonctionnalités

1. **Sampling de subset** : Sélectionne un sous-ensemble configurable du dataset (50 paires par défaut)
2. **Entraînement optimisé** : Utilise un petit modèle (Qwen2.5-1.8B) et configuration LoRA réduite (r=4)
3. **Sauvegarde de l'adaptateur** : Produit un adaptateur LoRA fonctionnel
4. **Test d'inférence** : Génère des réponses et compare avec chosen/rejected
5. **Rapports** : Génère un rapport JSON détaillé et un rapport markdown lisible

#### Utilisation

```bash
# Test standard avec 50 paires
python scripts/test_dpo_training.py --subset 50

# Test avec modèle spécifique
python scripts/test_dpo_training.py --model Qwen/Qwen2.5-1.8B-Instruct --subset 100

# Test avec entraînement skipped (tester seulement l'adaptateur existant)
python scripts/test_dpo_training.py --skip-training --model-path ./path/to/lora

# Avec sortie personnalisée
python scripts/test_dpo_training.py --output ./custom-output --subset 75
```

#### Configuration recommandée pour le test

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| `--subset` | 50 | Suffisant pour valider le pipeline, rapide |
| `--model` | Qwen/Qwen2.5-1.8B-Instruct | Petit modèle compatible GPU consumer |
| `--epochs` | 1 | Entraînement rapide pour validation |
| `--lr` | 5e-5 | Learning rate standard DPO |
| `--beta` | 0.1 | Paramètre DPO équilibré |
| `--max-length` | 512 | Limite la longueur pour économie mémoire |
| `--test-samples` | 5 | Nombre d'échantillons pour inférence |

#### Critères de succès

- **Alignement >= 50%** : Le modèle doit produire des réponses plus similaires aux chosen qu'aux rejected
- **Exit code 0** : Script termine avec succès
- **Rapports générés** : JSON et markdown créés dans le répertoire de sortie

#### Métriques attendues

| Métrique | Cible | Description |
|----------|-------|-------------|
| `eval_loss` | < 0.5 | Loss d'évaluation (plus bas = mieux) |
| `eval_rewards/accuracies` | > 0.7 | Pourcentage où chosen > rejected |
| Reward margin | > 0.5 | Écart moyen entre rewards chosen et rejected |
| Alignment score | > 0.5 | Score d'alignement lexical sur échantillons |

---

## Script d'Évaluation : `scripts/eval_alignment.py`

Script complémentaire pour évaluer l'alignement d'un modèle déployé sur le dataset AIDEAL.

### Usage

```bash
# Évaluation sur serveur de production
python scripts/eval_alignment.py \
    --api-url http://localhost:8000/v1 \
    --dataset dataset/preferences.json \
    --sample 30

# Avec sortie JSON
python scripts/eval_alignment.py \
    --api-url http://localhost:8000/v1 \
    --output evaluation_results.json
```

### Méthodologie

Le script mesure la similarité lexicale entre les réponses du modèle et les réponses chosen/rejected du dataset :

1. Envoie un échantillon d'instructions au modèle via l'API
2. Calcule le recouvrement lexical avec chosen et rejected
3. Attribution d'un score d'alignement : `score_chosen > score_rejected` = aligné
4. Résultat par catégorie et agrégat global

---

## Intégration CI/CD

### Workflow : `.github/workflows/test-dpo-training.yml` (à créer)

Le workflow de test automatisé qui s'exécute :

- **Quotidiennement** : Validation continue du pipeline
- **Avant release** : Vérification finale avant déploiement
- **Sur demande** : Déclenchement manuel (`workflow_dispatch`)

#### Configuration du workflow

```yaml
name: Test DPO Training

on:
  schedule:
    - cron: '0 6 * * *'  # Quotidien à 6h UTC
  pull_request:
    paths:
      - 'scripts/test_dpo_training.py'
      - 'scripts/train_lora.py'
      - 'dataset/**'
  workflow_dispatch:
    inputs:
      subset_size:
        description: 'Nombre de paires à tester'
        required: false
        default: '50'
      model:
        description: 'Modèle de base à tester'
        required: false
        default: 'Qwen/Qwen2.5-1.8B-Instruct'

jobs:
  test:
    runs-on: gpu-large  # Instance GPU (A100 40Go ou équivalent)
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install torch transformers trl peft datasets accelerate bitsandbytes requests
      
      - name: Run test suite
        run: |
          python scripts/test_dpo_training.py \
            --subset ${{ github.event.inputs.subset_size || '50' }} \
            --model ${{ github.event.inputs.model || 'Qwen/Qwen2.5-1.8B-Instruct' }} \
            --output ./test-results
      
      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: dpo-test-results
          path: |
            ./test-results/*.json
            ./test-results/*.md
      
      - name: Comment on PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const path = require('path');
            
            const resultFiles = fs.readdirSync('./test-results').filter(f => f.endsWith('.json'));
            if (resultFiles.length > 0) {
              const results = JSON.parse(fs.readFileSync(path.join('./test-results', resultFiles[0]), 'utf8'));
              const icon = results.test_passed ? '✅' : '❌';
              const alignment = (results.inference_results.alignment_score * 100).toFixed(0);
              
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `${icon} **Test DPO** : Alignement ${alignment}% (${results.inference_results.aligned_samples}/${results.inference_results.total_samples} échantillons)`
              });
            }
```

### Infrastructure GPU nécessaire

Pour exécuter le test suite :

| Configuration | VRAM | Durée estimée | Coût (cloud) |
|---------------|------|---------------|--------------|
| **Test rapide** (1.8B modèle) | 16-24 Go | 5-10 min | ~0.50-1€ |
| **Test standard** (7B modèle) | 48 Go | 15-20 min | ~1-2€ |
| **Test complet** (35B modèle) | 80 Go | 30-40 min | ~3-5€ |

**Recommandation** : Utiliser l'option "Test rapide" pour le CI quotidien, option "Test standard" pour les tests avant release.

---

## Exécution Manuelle Locale

### Prérequis

```bash
# Installer les dépendances
pip install torch transformers trl peft datasets accelerate bitsandbytes requests

# Vérifier le GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
```

### Étapes

1. **Fusionner le dataset** (si nécessaire)
   ```bash
   python scripts/merge_categories.py
   ```

2. **Valider le dataset**
   ```bash
   python scripts/validate_dataset.py
   ```

3. **Exécuter le test**
   ```bash
   python scripts/test_dpo_training.py --subset 50 --output ./local-test
   ```

4. **Vérifier les résultats**
   ```bash
   ls -la ./local-test/
   cat ./local-test/dpo_test_results_*.md
   ```

---

## Interprétation des Résultats

### Test réussi ✅

- **Alignement > 50%** : Le modèle apprend correctement les préférences du dataset
- **eval_loss < 0.5** : Loss d'évaluation raisonnable
- **Pas d'erreur OOM** : Configuration GPU adéquate

### Test échoué ❌

Causes possibles :

1. **OOM (Out of Memory)** : Réduire `--batch-size` à 1, `--max-length` à 512, ou utiliser un modèle plus petit
2. **Alignment < 50%** : 
   - Dataset trop petit (< 50 paires)
   - Learning rate trop élevé/défavorable
   - Pas assez d'epochs
   - Données bruitées ou contradictoires
3. **Erreur de chargement** : Vérifier `trust_remote_code=True` pour les modèles Qwen

### Debugging tips

```bash
# Activer le logging détaillé
export TRANSFORMERS_VERBOSITY=info

# Vérifier la mémoire GPU pendant l'entraînement
python scripts/test_dpo_training.py --subset 50 2>&1 | grep -i "memory\|vram\|gb"

# Tester avec un subset encore plus petit
python scripts/test_dpo_training.py --subset 10 --subset 5 --model Qwen/Qwen1.5-0.5B-Instruct
```

---

## Liens Utiles

- **Script de test** : [`scripts/test_dpo_training.py`](scripts/test_dpo_training.py)
- **Script d'évaluation** : [`scripts/eval_alignment.py`](scripts/eval_alignment.py)
- **Guide de fine-tuning** : [`docs/FINE_TUNING_GUIDE.md`](docs/FINE_TUNING_GUIDE.md)
- **Script d'entraînement** : [`scripts/train_lora.py`](scripts/train_lora.py)
- **Validation dataset** : [`scripts/validate_dataset.py`](scripts/validate_dataset.py)

---

## Maintenance

### Mettre à jour les seuils de test

Modifier dans `test_dpo_training.py` :

```python
# Ligne ~230
TEST_ALIGNMENT_THRESHOLD = 0.5  # Augmenter pour plus strict, diminuer pour plus permissif
```

### Ajouter des catégories de test

Le test actuel utilise toutes les catégories du dataset. Pour cibler une catégorie spécifique :

```bash
python scripts/test_dpo_training.py --subset 20 --category genre-inclusion
```

*(À implémenter dans une version future)*

### Documenter les tests réussis

Après chaque exécution réussie :

1. Consulter le rapport markdown : `cat ./test-results/dpo_test_results_*.md`
2. Vérifier l'alignement global et par catégorie
3. Documenter les résultats remarquables dans ce fichier
4. Mettre à jour la section "Résultats Historiques" ci-dessous

---

## Résultats Historiques

### 2026-05-27 : Suite de test implémentée

- ✅ Script `test_dpo_training.py` créé et testé
- ✅ Documentation `FINE_TUNING_TEST_RESULTS.md` rédigée
- ✅ Workflow CI défini (à déployer)
- ⏳ Exécution réelle en attente d'infrastructure GPU CI

**Prochaine étape** : Configurer le runner GitHub Actions avec GPU et exécuter le premier test complet.

---

*Rapport maintenu par l'équipe technique AIDEAL*

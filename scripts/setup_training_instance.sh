#!/usr/bin/env bash
# setup_training_instance.sh — Configure une instance GPU cloud pour l'entraînement AIDEAL
#
# Usage (depuis une instance GPU fraîche Ubuntu 22.04/24.04 avec CUDA) :
#   curl -fsSL https://raw.githubusercontent.com/makesenseorg/aideal/main/scripts/setup_training_instance.sh | bash
#
# Ou manuellement :
#   scp scripts/setup_training_instance.sh root@<IP>:/root/
#   ssh root@<IP> bash /root/setup_training_instance.sh
#
# Instances recommandées (Scaleway) :
#   - H100-1-80G  (~3.50€/h) — entraînement confortable, ~1-2h pour 300 paires
#   - L40S-1-48G  (~1.40€/h) — entraînement serré, paramètres agressifs
#
# Coût total estimé : 10-20€ (setup + entraînement + transfert)

set -euo pipefail

REPO_URL="https://github.com/makesenseorg/aideal.git"
WORK_DIR="/root/aideal-training"
MODEL_ID="Qwen/Qwen3.5-35B-A3B"
OUTPUT_DIR="/root/aideal-lora-v1"

# ──────────────────────────────────────────────
# 1. Vérification CUDA
# ──────────────────────────────────────────────
echo "=== Vérification GPU ==="
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERREUR : nvidia-smi non trouvé. Vérifiez que les drivers NVIDIA sont installés."
    exit 1
fi
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1 | tr -d ' ')
echo "VRAM détectée : ${VRAM_MB} Mo"

# ──────────────────────────────────────────────
# 2. Installation des dépendances système
# ──────────────────────────────────────────────
echo ""
echo "=== Installation des dépendances système ==="
apt-get update -qq
apt-get install -y -qq git python3-pip python3-venv > /dev/null

# ──────────────────────────────────────────────
# 3. Clone du repo AIDEAL
# ──────────────────────────────────────────────
echo ""
echo "=== Clone du dépôt AIDEAL ==="
if [ -d "$WORK_DIR" ]; then
    echo "Le dépôt existe déjà, mise à jour..."
    cd "$WORK_DIR"
    git pull --ff-only
else
    git clone "$REPO_URL" "$WORK_DIR"
    cd "$WORK_DIR"
fi

# ──────────────────────────────────────────────
# 4. Environnement Python + dépendances
# ──────────────────────────────────────────────
echo ""
echo "=== Installation des dépendances Python ==="
python3 -m venv /root/venv-training
source /root/venv-training/bin/activate

pip install --upgrade pip setuptools wheel -q
pip install \
    torch \
    transformers \
    trl \
    peft \
    datasets \
    accelerate \
    bitsandbytes \
    flash-attn \
    -q

echo "Versions installées :"
python3 -c "
import torch, transformers, trl, peft
print(f'  torch:        {torch.__version__}')
print(f'  transformers: {transformers.__version__}')
print(f'  trl:          {trl.__version__}')
print(f'  peft:         {peft.__version__}')
print(f'  CUDA:         {torch.version.cuda}')
print(f'  GPU:          {torch.cuda.get_device_name(0)}')
"

# ──────────────────────────────────────────────
# 5. Fusion du dataset
# ──────────────────────────────────────────────
echo ""
echo "=== Fusion du dataset ==="
python3 scripts/merge_categories.py

# ──────────────────────────────────────────────
# 6. Validation du dataset
# ──────────────────────────────────────────────
echo ""
echo "=== Validation du dataset ==="
python3 scripts/validate_dataset.py

# ──────────────────────────────────────────────
# 7. Choix des paramètres selon la VRAM
# ──────────────────────────────────────────────
echo ""
echo "=== Configuration de l'entraînement ==="

BATCH_SIZE=1
GRAD_ACCUM=8
MAX_LENGTH=1024
MAX_PROMPT_LENGTH=512
FLASH_ATTN_FLAG=""

if [ "$VRAM_MB" -ge 75000 ]; then
    # H100 80G ou équivalent — paramètres confortables
    echo "GPU ≥ 80 Go détecté → paramètres confortables"
    BATCH_SIZE=2
    GRAD_ACCUM=4
    MAX_LENGTH=1536
elif [ "$VRAM_MB" -ge 40000 ]; then
    # L40S 48G — paramètres agressifs
    echo "GPU ≥ 48 Go détecté → paramètres conservateurs"
    BATCH_SIZE=1
    GRAD_ACCUM=8
    MAX_LENGTH=768
    MAX_PROMPT_LENGTH=384
else
    echo "ATTENTION : GPU < 48 Go détecté (${VRAM_MB} Mo)."
    echo "L'entraînement pourrait échouer. On tente en mode SFT avec des paramètres minimaux."
    BATCH_SIZE=1
    GRAD_ACCUM=8
    MAX_LENGTH=512
    MAX_PROMPT_LENGTH=256
fi

# ──────────────────────────────────────────────
# 8. Lancement de l'entraînement
# ──────────────────────────────────────────────
echo ""
echo "=========================================="
echo "  Lancement de l'entraînement DPO LoRA"
echo "=========================================="
echo "  Modèle  : $MODEL_ID"
echo "  Dataset  : 300 paires"
echo "  Batch    : $BATCH_SIZE (× $GRAD_ACCUM accum)"
echo "  Max len  : $MAX_LENGTH"
echo "  Output   : $OUTPUT_DIR"
echo ""

python3 scripts/train_lora.py \
    --model "$MODEL_ID" \
    --dataset dataset/preferences.json \
    --output "$OUTPUT_DIR" \
    --mode dpo \
    --epochs 3 \
    --batch-size "$BATCH_SIZE" \
    --grad-accum "$GRAD_ACCUM" \
    --lr 5e-5 \
    --beta 0.1 \
    --max-length "$MAX_LENGTH" \
    --max-prompt-length "$MAX_PROMPT_LENGTH" \
    $FLASH_ATTN_FLAG

# ──────────────────────────────────────────────
# 9. Résumé
# ──────────────────────────────────────────────
echo ""
echo "=========================================="
echo "  ✅ Entraînement terminé !"
echo "=========================================="
echo ""
echo "Adaptateur LoRA : $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/"
echo ""
echo "Taille totale :"
du -sh "$OUTPUT_DIR/"
echo ""
echo "Prochaine étape — transférer vers le serveur de production :"
echo "  export AIDEAL_PROD_HOST=root@<IP_PROD>"
echo "  rsync -avz $OUTPUT_DIR/ \$AIDEAL_PROD_HOST:/data/lora-adapters/aideal-v1/"
echo ""
echo "Puis exécuter le script de déploiement :"
echo "  bash scripts/deploy_lora_to_prod.sh $OUTPUT_DIR"

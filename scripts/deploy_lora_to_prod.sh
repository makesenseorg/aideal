#!/usr/bin/env bash
# deploy_lora_to_prod.sh — Déploie l'adaptateur LoRA AIDEAL sur le serveur de production
#
# Usage (depuis la machine d'entraînement ou le poste local) :
#   bash scripts/deploy_lora_to_prod.sh /chemin/vers/aideal-lora-v1
#
# Ce script :
#   1. Transfère l'adaptateur LoRA vers le serveur de production
#   2. Met à jour la config vLLM pour activer LoRA
#   3. Redémarre vLLM avec le modèle de base + l'adaptateur aligné
#
# Résultat : deux modèles disponibles dans Open WebUI :
#   - Qwen3.5-35B-A3B-GPTQ-Int4 (modèle de base)
#   - aideal-v1 (modèle aligné ESS)

set -euo pipefail

PROD_HOST="${AIDEAL_PROD_HOST:?Définir AIDEAL_PROD_HOST (ex: root@1.2.3.4)}"
PROD_COMPOSE="${AIDEAL_PROD_COMPOSE:-/opt/makesense-ai/docker-compose.yml}"
LORA_REMOTE_DIR="${AIDEAL_LORA_REMOTE_DIR:-/opt/makesense-ai/lora-adapters/aideal-v1}"
ADAPTER_LOCAL="${1:?Usage: $0 /chemin/vers/aideal-lora-v1}"

# ──────────────────────────────────────────────
# 1. Vérification de l'adaptateur local
# ──────────────────────────────────────────────
echo "=== Vérification de l'adaptateur local ==="
if [ ! -f "$ADAPTER_LOCAL/adapter_config.json" ]; then
    echo "ERREUR : adapter_config.json non trouvé dans $ADAPTER_LOCAL"
    echo "Vérifiez que l'entraînement s'est terminé correctement."
    exit 1
fi
echo "Adaptateur trouvé : $ADAPTER_LOCAL"
du -sh "$ADAPTER_LOCAL"
echo ""

# ──────────────────────────────────────────────
# 2. Transfert vers le serveur de production
# ──────────────────────────────────────────────
echo "=== Transfert de l'adaptateur vers $PROD_HOST ==="
ssh "$PROD_HOST" "mkdir -p $LORA_REMOTE_DIR"
rsync -avz --progress "$ADAPTER_LOCAL/" "$PROD_HOST:$LORA_REMOTE_DIR/"
echo ""

# ──────────────────────────────────────────────
# 3. Mise à jour de la configuration vLLM
# ──────────────────────────────────────────────
echo "=== Mise à jour de la configuration vLLM ==="

# Backup de la config actuelle
ssh "$PROD_HOST" "cp $PROD_COMPOSE ${PROD_COMPOSE}.bak.$(date +%Y%m%d-%H%M%S)"

# Vérifier si LoRA est déjà activé
if ssh "$PROD_HOST" "grep -q 'enable-lora' $PROD_COMPOSE"; then
    echo "LoRA déjà activé dans la config. Mise à jour du chemin..."
    # Mettre à jour le chemin du module LoRA
    ssh "$PROD_HOST" "sed -i 's|--lora-modules .*|--lora-modules aideal-v1=/lora-adapters/aideal-v1|' $PROD_COMPOSE"
else
    echo "Activation de LoRA dans la config vLLM..."
    # Ajouter le volume bind mount pour les adaptateurs LoRA
    # et les flags --enable-lora --lora-modules
    ssh "$PROD_HOST" "cat > /tmp/update_compose.py << 'PYEOF'
import yaml
import sys

with open('$PROD_COMPOSE') as f:
    config = yaml.safe_load(f)

vllm = config['services']['vllm']

# Ajouter le volume bind mount pour les LoRA adapters
volumes = vllm.get('volumes', [])
lora_volume = '/opt/makesense-ai/lora-adapters:/lora-adapters:ro'
if lora_volume not in volumes:
    volumes.append(lora_volume)
vllm['volumes'] = volumes

# Mettre à jour la commande vLLM pour activer LoRA
cmd = vllm['command']
if '--enable-lora' not in cmd:
    cmd = cmd.rstrip()
    cmd += '\n      --enable-lora'
    cmd += '\n      --lora-modules aideal-v1=/lora-adapters/aideal-v1'
    cmd += '\n      --max-lora-rank 16'
    vllm['command'] = cmd

with open('$PROD_COMPOSE', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print('Config mise à jour.')
PYEOF
python3 /tmp/update_compose.py 2>/dev/null || true"

    # Fallback : mise à jour manuelle par sed si PyYAML n'est pas dispo
    if ! ssh "$PROD_HOST" "grep -q 'enable-lora' $PROD_COMPOSE"; then
        echo "Mise à jour manuelle de la config..."
        ssh "$PROD_HOST" "
cd /opt/makesense-ai

# Ajouter le volume LoRA au service vllm
sed -i '/vllm-cache:\/root\/.cache\/huggingface/a\\      - /opt/makesense-ai/lora-adapters:/lora-adapters:ro' docker-compose.yml

# Ajouter les flags LoRA à la commande vLLM
sed -i 's|--tensor-parallel-size 1|--tensor-parallel-size 1\n      --enable-lora\n      --lora-modules aideal-v1=/lora-adapters/aideal-v1\n      --max-lora-rank 16|' docker-compose.yml
"
    fi
fi

echo ""
echo "Config mise à jour :"
ssh "$PROD_HOST" "cat $PROD_COMPOSE"
echo ""

# ──────────────────────────────────────────────
# 4. Redémarrage de vLLM
# ──────────────────────────────────────────────
echo "=== Redémarrage de vLLM ==="
echo "Arrêt du conteneur vLLM..."
ssh "$PROD_HOST" "cd /opt/makesense-ai && docker compose stop vllm"

echo "Relancement avec LoRA activé..."
ssh "$PROD_HOST" "cd /opt/makesense-ai && docker compose up -d vllm"

echo "Attente du démarrage de vLLM (chargement du modèle + LoRA)..."
for i in $(seq 1 60); do
    if ssh "$PROD_HOST" "curl -sf http://localhost:8000/v1/models > /dev/null 2>&1"; then
        echo ""
        echo "✅ vLLM est prêt !"
        break
    fi
    printf "."
    sleep 10
done
echo ""

# ──────────────────────────────────────────────
# 5. Vérification
# ──────────────────────────────────────────────
echo "=== Vérification des modèles disponibles ==="
ssh "$PROD_HOST" "curl -s http://localhost:8000/v1/models | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/v1/models"
echo ""

echo "=========================================="
echo "  ✅ Déploiement terminé !"
echo "=========================================="
echo ""
echo "Modèles disponibles sur l'interface Open WebUI :"
echo "  1. Modèle de base"
echo "  2. aideal-v1 (aligné ESS)"
echo ""
echo "Dans Open WebUI, sélectionner 'aideal-v1' pour utiliser"
echo "le modèle aligné sur les valeurs makesense."

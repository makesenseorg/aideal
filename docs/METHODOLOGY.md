# Méthodologie — Comment on construit les paires AIDEAL

Ce document décrit les méthodes de création des paires, les principes éditoriaux et la trajectoire de volumétrie du dataset.

---

## Les 3 méthodes de création

### 1. Extraction de contenus existants

Des ressources produites par et pour l'ESS existent en abondance : guides pratiques d'associations, rapports de think-tanks, kits pédagogiques, textes fondateurs de mouvements coopératifs. Ces contenus constituent une base de valeurs documentée.

**Processus :**
1. Identifier un contenu de référence (rapport, guide, prise de position)
2. Extraire une formulation représentative d'une position ESS sur un sujet donné
3. Formuler une `instruction` neutre qui pourrait amener un modèle à répondre sur ce sujet
4. Utiliser l'extrait comme base du `chosen`, reformulé si nécessaire pour être utilisable
5. Générer un `rejected` en testant un LLM non-aligné ou en reformulant la réponse standard

**Avantages :** ancrage dans des sources légitimes, cohérence avec les valeurs portées par le secteur
**Limites :** nécessite de reformuler pour adapter au format paire, risque de décontextualisation

**Champ `source` :** `content-extraction`

---

### 2. Rédaction manuelle ciblée

Pour les biais les plus subtils ou les situations les plus spécifiques au terrain associatif, on rédige directement les paires en partant d'un biais identifié.

**Processus :**
1. Identifier un biais récurrent dans les réponses des LLM actuels (ex. : genrer automatiquement les postes de direction au masculin)
2. Formuler une `instruction` qui va typiquement déclencher ce biais
3. Rédiger un `rejected` qui représente fidèlement la réponse biaisée
4. Rédiger un `chosen` qui corrige ce biais tout en restant utile et non-dogmatique
5. Faire valider par une personne avec expertise du domaine concerné

**Avantages :** ciblage précis, contrôle total sur la qualité
**Limites :** chronophage, risque de biais du·de la rédacteur·ice

**Champ `source` :** `manual`

---

### 3. Feedback continu via Open WebUI

Un dispositif de collecte de feedbacks est déployé sur les instances Open WebUI utilisées par les organisations partenaires. Les utilisateur·ices peuvent signaler une réponse insatisfaisante directement dans l'interface.

**Processus :**
1. L'utilisateur·ice signale une réponse avec un pouce bas et un commentaire optionnel
2. Le script `export_openwebui.py` extrait les feedbacks négatifs en paires brutes
3. Les paires brutes arrivent dans `review/a_traiter.json` avec `chosen` vide
4. Une personne de l'équipe complète le `chosen`, qualifie la catégorie et valide
5. La paire est déplacée dans le fichier de catégorie approprié

**Avantages :** ancré dans des usages réels, évolution continue du dataset
**Limites :** qualité variable des feedbacks, nécessite une animation active

**Champ `source` :** `openwebui-feedback`

---

## Principes éditoriaux

### Diversité thématique > quantité

Mieux vaut 5 paires couvrant 5 biais distincts que 50 variations du même biais. On cherche à cartographier le spectre des situations rencontrées dans l'ESS, pas à optimiser les métriques d'entraînement par saturation.

### Nuance > militantisme

Le `chosen` n'est pas un manifeste. C'est une réponse utile, qui intègre les valeurs ESS sans les asséner. Une réponse qui dit "la démocratie participative c'est bien, voici comment l'implémenter dans votre contexte" vaut mieux qu'une réponse qui dit "le management horizontal est la seule voie éthique".

**Le `chosen` doit passer ce test :** est-ce que je pourrais envoyer cette réponse à quelqu'un·e qui ne partage pas mes valeurs, et qu'elle lui soit quand même utile ?

### Le `chosen` est une réponse utile, pas un tract

Les modèles fine-tunés avec ce dataset doivent rester des assistants efficaces. Si le `chosen` est trop militant, trop long, ou esquive la question pour faire de la pédagogie, le modèle deviendra inutilisable pour les cas d'usage courants.

### Représenter des biais réels

Le `rejected` doit être une réponse qu'un LLM actuel pourrait effectivement produire, pas une caricature. On documente des biais structurels subtils, pas des positions extrémistes évidentes.

---

## Volumétrie cible

| Jalon | Nombre de paires | Description | Statut |
|-------|-----------------|-------------|--------|
| **MVP** | 300 paires | ~37 paires par catégorie — suffisant pour un premier fine-tuning expérimental | Atteint (300/300) |
| **V1** | 800 paires | ~100 paires par catégorie — dataset utilisable pour des modèles en production | À venir |
| **Maturité** | 2 000 paires | ~250 paires par catégorie — couverture large des situations terrain | À venir |

### Répartition par catégorie

On vise une répartition équilibrée entre les 8 catégories. Les catégories avec plus de terrain de collecte (genre, écologie) ne doivent pas écraser les catégories plus de niche (inégalités nord-sud, validisme).

### Répartition par source

| Source | Cible MVP | Cible V1 |
|--------|-----------|----------|
| `manual` | 60 % | 40 % |
| `content-extraction` | 30 % | 30 % |
| `openwebui-feedback` | 10 % | 30 % |

---

## Contrôle qualité

Chaque paire est validée par au moins une personne avant d'être intégrée au dataset principal. Le processus de review est décrit dans [CONTRIBUTING.md](../CONTRIBUTING.md).

Avant chaque release, le script `validate_dataset.py` est exécuté pour vérifier la cohérence formelle de l'ensemble du dataset.

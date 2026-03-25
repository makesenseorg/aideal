# Guide de contribution — AIDEAL

Merci de vouloir contribuer à AIDEAL ! Ce guide explique comment proposer de nouvelles paires, les critères de qualité attendus, et le processus de validation.

---

## Sommaire

1. [Proposer une nouvelle paire](#1-proposer-une-nouvelle-paire)
2. [Critères de qualité](#2-critères-de-qualité)
3. [Processus de review](#3-processus-de-review)
4. [Transformer un feedback Open WebUI en paire](#4-transformer-un-feedback-open-webui-en-paire)
5. [Conventions](#5-conventions)

---

## 1. Proposer une nouvelle paire

### Via une Pull Request

1. **Forker** le dépôt et créer une branche dédiée :
   ```bash
   git checkout -b ajout/genre-inclusion-002
   ```

2. **Identifier la catégorie** concernée (voir [CATEGORIES.md](docs/CATEGORIES.md))

3. **Ajouter la paire** dans le fichier JSON correspondant (`dataset/categories/<categorie>.json`) en respectant le format :

   ```json
   {
     "id": "genre-002",
     "category": "genre-inclusion",
     "instruction": "Comment recruter efficacement dans une association ?",
     "chosen": "Pour recruter efficacement, il est utile de rédiger une offre inclusive...",
     "rejected": "Pour recruter, cherchez des candidats motivés et compétents...",
     "tags": ["recrutement", "écriture-inclusive"],
     "source": "manual",
     "reviewed_by": "",
     "date_added": "2026-03-25"
   }
   ```

4. **Générer l'ID** en suivant le format `<categorie-courte>-<numéro-à-3-chiffres>` (ex. `genre-002`, `eco-015`).

5. **Ouvrir une PR** avec un titre descriptif, par exemple : `[genre-inclusion] Ajout paire sur le recrutement inclusif`

### Via une issue

Si vous n'êtes pas à l'aise avec Git, ouvrez une issue en utilisant le modèle "Proposition de paire" et l'équipe s'occupera de l'intégration.

---

## 2. Critères de qualité

### La réponse `chosen` doit être...

- **Utile et concrète** : elle répond à la question posée, elle n'esquive pas
- **Nuancée, pas dogmatique** : elle n'assène pas une vérité militante, elle ouvre des perspectives
- **Représentative des valeurs ESS** sans être un tract : inclusion, coopération, soutenabilité
- **En écriture inclusive** quand le contexte s'y prête (alternance de genres, formulations neutres)
- **Accessible** : compréhensible sans jargon militant excessif

### La réponse `chosen` ne doit pas être...

- Une liste de bonnes pratiques déconnectées du contexte
- Un discours moralisateur ou culpabilisant
- Une réponse qui évite le sujet par excès de précaution
- Une réponse parfaite au sens militant mais inutilisable en pratique

### La réponse `rejected` doit être...

- **Représentative d'un biais réel** que l'on observe dans les LLM actuels
- **Plausible** : une réponse qu'un modèle non-aligné pourrait effectivement produire
- **Pas caricaturale** : le biais doit être subtil, pas une position extrémiste évidente

### L'instruction doit être...

- **Réaliste** : une vraie question qu'une personne travaillant en ESS pourrait poser
- **Neutre** : ne pas orienter la réponse dans sa formulation
- **Précise** : éviter les questions trop génériques ("Qu'est-ce que l'ESS ?")

---

## 3. Processus de review

Chaque paire passe par une validation en binôme :

### Rôle "valeurs"
Vérifie que :
- Le `chosen` est cohérent avec les valeurs ESS
- Le `rejected` est représentatif d'un biais réel
- Le contenu n'est pas contre-productif ou offensant

### Rôle "tech"
Vérifie que :
- Le format JSON est valide
- L'ID est unique et suit la convention
- Les champs obligatoires sont remplis
- La paire sera exploitable pour l'entraînement (longueur, structure)

### Validation

- Une PR est mergée quand elle a **au moins 1 approbation** (idéalement une par rôle)
- En cas de désaccord, une discussion est ouverte dans la PR — on cherche le consensus, pas le vote
- Les paires issues de feedbacks Open WebUI passent d'abord par `review/a_traiter.json` avant validation finale

---

## 4. Transformer un feedback Open WebUI en paire

Quand un·e utilisateur·ice signale une réponse insatisfaisante dans Open WebUI, voici comment transformer ce retour en paire :

### Étape 1 — Récupérer le feedback

Le script `scripts/export_openwebui.py` exporte les feedbacks négatifs en paires brutes dans `review/a_traiter.json`.

```bash
python scripts/export_openwebui.py --input <export_openwebui.json> --output review/a_traiter.json
```

### Étape 2 — Compléter la paire

Le fichier `review/a_traiter.json` contient des paires avec `source: "openwebui-feedback"` et `reviewed_by: ""`. Pour chaque paire :

1. Vérifier que l'`instruction` est bien formulée (reformuler si nécessaire)
2. Qualifier ou améliorer le `chosen` pour qu'il réponde aux critères de qualité
3. S'assurer que le `rejected` est bien la réponse originale du modèle (ne pas l'inventer)
4. Choisir la bonne `category` et les bons `tags`

### Étape 3 — Déplacer la paire

Une fois validée, la paire est déplacée dans le fichier de catégorie correspondant (`dataset/categories/<categorie>.json`) via une PR classique.

---

## 5. Conventions

### Nommage des IDs

| Catégorie | Préfixe |
|-----------|---------|
| genre-inclusion | `genre-` |
| techno-solutionnisme | `techno-` |
| vision-economique | `eco-` |
| validisme-accessibilite | `valid-` |
| inegalites-nord-sud | `ns-` |
| ecologie-sobriete | `sobr-` |
| gouvernance-pouvoir-agir | `gouv-` |
| diversite-parcours | `div-` |

### Sources

| Valeur | Description |
|--------|-------------|
| `manual` | Rédigé manuellement par un·e contributeur·ice |
| `openwebui-feedback` | Issu d'un retour utilisateur·ice sur Open WebUI |
| `content-extraction` | Extrait ou adapté d'un contenu ESS existant |

### Dates

Format ISO 8601 : `YYYY-MM-DD`

---

*Des questions ? Ouvrez une issue ou contactez l'équipe makesense.*

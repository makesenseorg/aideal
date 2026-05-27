# Déploiement AIDEAL

Ce document décrit comment déployer les différentes parties du projet AIDEAL.

## Structure du projet

```
aideal/
├── site/                    # Site public (aideal.community)
│   ├── index.html          # Page d'accueil
│   ├── favicon.svg
│   ├── logotype.svg
│   └── CNAME               # aideal.community
│
├── submission-form/         # Dashboard admin (à déployer séparément)
│   ├── index.html          # Formulaire de soumission
│   ├── styles.css
│   └── submission.js
│
├── dataset/                 # Dataset AIDEAL (310 pairs)
│   └── categories/
│       ├── genre_inclusion.json
│       ├── techno_solutionnisme.json
│       ├── vision_economique.json
│       ├── validisme_accessibilite.json
│       ├── inegalites_nord_sud.json
│       ├── ecologie_sobriete.json
│       ├── gouvernance_pouvoir_agir.json
│       └── diversite_parcours.json
│
├── docs/                    # Documentation
│   ├── METHODOLOGY.md
│   ├── FINE_TUNING_GUIDE.md
│   └── CATEGORIES.md
│
├── scripts/                 # Scripts techniques
│   ├── validate_dataset.py
│   ├── validate_dataset.js
│   ├── count_pairs.js
│   └── ...
│
└── .github/workflows/       # CI/CD
    └── validate-dataset.yml
```

## Déploiement du site public

### Via Vercel (Recommandé)

1. Créer un compte Vercel (si nécessaire)
2. Importer le dépôt GitHub `makesenseorg/aideal`
3. Configuration du projet :
   - **Framework Preset**: Other
   - **Root Directory**: `site/`
   - **Build Command**: (vide - contenu statique)
   - **Output Directory**: `site/`
   - **Install Command**: (vide)
4. Ajouter le domaine personnalisé : `aideal.community`
5. Déployer

**Résultat**: https://aideal.community

### Via GitHub Pages (Alternative)

1. Dans le dépôt GitHub, aller dans Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/site`
4. Sauvegarder

**Résultat**: https://makesenseorg.github.io/aideal/

## Déploiement du submission-form (dashboard admin)

### Via Vercel

1. Dans Vercel, créer un nouveau projet à partir du même dépôt
2. **Root Directory**: `submission-form/`
3. **Framework Preset**: Other
4. **Build Command**: (vide)
5. **Output Directory**: `submission-form/`
6. **Environment Variables**: Aucune requise (démo statique)
7. Domain: `aideal.community/submission` ou sous-domaine dédié

**Accès**: https://aideal.community/submission/

### Alternative: hébergement direct dans site public

Le `submission-form/` peut être intégré directement dans le site principal :

1. Copier `submission-form/` → `site/submission/`
2. Mettre à jour les chemins relatifs dans les fichiers
3. Déployer le site complet

## Déploiement des API (optionnel)

Les fichiers API dans `submission-form/api/` nécessitent un runtime serverless :

### Via Vercel Functions

1. Déplacer `submission-form/api/submit-pair.js` → `site/api/submit-pair/route.js`
2. Reformater pour Vercel Edge Function
3. Déployer avec le site

### Via Netlify Functions

1. Déplacer dans `site/functions/`
2. Configurer `_redirects` pour les routes API
3. Déployer

## Configuration GitHub

### Secrets pour le workflow CI

Le workflow `validate-dataset.yml` utilise `secrets.GITHUB_TOKEN` qui est automatique.

Aucun secret supplémentaire n'est requis pour la validation du dataset.

### Branch protection rules (Recommandé)

Dans GitHub → Settings → Branches → Add branch protection rule:

- Branch name pattern: `main`
- ☑️ Require a pull request before merging
- ☑️ Require status checks to pass before merging
  - ✅ validate (le workflow de validation)
- ☑️ Require linear history
- ☑️ Allow force pushes: No
- ☑️ Allow deletions: No

## Scripts utiles

### Validation du dataset

```bash
# Node.js
node scripts/validate_dataset.js

# Python (si disponible)
python3 scripts/validate_dataset.py
```

### Comptage des pairs

```bash
node scripts/count_pairs.js
```

## Variables d'environnement

Le fichier `.env.example` contient des variables pour le déploiement LoRA vers un serveur de production :

```bash
AIDEAL_PROD_HOST=root@<server-ip>
AIDEAL_PROD_COMPOSE=/opt/makesense-ai/docker-compose.yml
AIDEAL_LORA_REMOTE_DIR=/opt/makesense-ai/lora-adapters/aideal-v1
```

**Note**: Ces variables ne sont pas requises pour le déploiement web statique.

## Monitoring

### Metrics à suivre

- Nombre total de contributions (actuel : 310 pairs)
- Taux de validation des PR (doit être 100% après correction)
- Visites du site et du formulaire
- Taux de complétion du formulaire

### Alertes recommandées

- Workflow CI qui échoue → alerte immédiate
- Site inaccessible → alerte immédiate
- Chute brutale de trafic → vérification hebdomadaire

## Maintenance

### Mise à jour du dataset

1. Ajouter des pairs dans `dataset/categories/<category>.json`
2. Lancer `node scripts/validate_dataset.js` localement
3. Commit + push vers `main`
4. Le workflow CI validera automatiquement
5. Après merge, les pairs seront visibles sur le repo

### Mise à jour du site

1. Modifier les fichiers dans `site/`
2. Tester localement : `npx serve site/`
3. Commit + push vers `main`
4. Déploiement automatique Vercel (≤ 1 minute)

## Support

Pour les questions techniques :

- Documentation complète : `/docs/`
- Méthodologie : `/docs/METHODOLOGY.md`
- Guide de fine-tuning : `/docs/FINE_TUNING_GUIDE.md`
- Description des catégories : `/docs/CATEGORIES.md`

---

*Document maintenu par l'équipe technique AIDEAL*
*Last updated: 2026-05-27*

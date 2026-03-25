# Changelog — AIDEAL

Toutes les évolutions notables du dataset sont documentées ici.

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [Non publié]

### Ajouté
- Prompt système AIDEAL prêt à copier-coller pour ChatGPT, Claude, Open WebUI (`prompts/system-prompt-aideal.md`)
- 300 paires DPO réparties sur les 8 catégories (37-38 par catégorie) — MVP atteint
  - genre-inclusion : 38 paires (écriture inclusive, charge mentale genrée, VSS, leadership féminin, féminisme décolonial, congé menstruel, sport féminin, mixité numérique…)
  - techno-solutionnisme : 37 paires (IA générative, fracture numérique, GAFAM, low-tech, cloud souverain, surveillance, gamification, smart city, datafication…)
  - vision-economique : 38 paires (SCOP/SCIC, finance solidaire, communs, insertion, commande publique, habitat participatif, tarification solidaire, épargne solidaire…)
  - validisme-accessibilite : 37 paires (FALC, RGAA, neurodiversité, handicap invisible, design universel, troubles DYS, fatigue chronique, pair-aidance santé mentale…)
  - inegalites-nord-sud : 37 paires (volontourisme, dette, souveraineté alimentaire, extractivisme numérique, appropriation culturelle, justice climatique, paradis fiscaux…)
  - ecologie-sobriete : 38 paires (sobriété, agroécologie, greenwashing, ZAN, éco-anxiété, compensation carbone, décroissance, droit à la réparation, écocide…)
  - gouvernance-pouvoir-agir : 38 paires (sociocratie, éducation populaire, plaidoyer, intelligence collective, rotation des mandats, désobéissance civile, co-construction…)
  - diversite-parcours : 37 paires (intersectionnalité, pair-aidance, racisme systémique, ruralité, VAE, gens du voyage, trans-identité, personnes exilées…)
- Section « Utiliser AIDEAL sans fine-tuning » dans le README

### Infrastructure
- Initialisation du dépôt
- Structure du dataset (8 catégories)
- Scripts utilitaires (merge, validate, export)
- Documentation (README, CONTRIBUTING, METHODOLOGY, CATEGORIES, FINE_TUNING_GUIDE)

---

<!-- ## [0.1.0] — YYYY-MM-DD -->
<!-- ### Ajouté -->
<!-- - Premières paires manuelles -->

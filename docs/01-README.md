# Documentation AIDEAL

**Projet AIDEAL** (AI + Idéal) — https://aideal.community

Ce dossier contient la documentation complète du projet, incluant la méthodologie, la description des catégories de biais, les références fondamentales, et les guides de contribution.

---

## Navigation rapide

### Documentation de base

- **[01-Méthodologie](./01-methodologie.md)** — Principes éditoriaux, volumétrie cible, guides de rédaction
- **[02-Categories](./02-categories.md)** — Description des 8 catégories de biais et des thèmes couverts
- **[03-Références fondamentales](./03-reference-fondamentales.md)** — Les 9 références théoriques (Said, Polanyi, Rockström, Zuboff, Foucault, Noble, Mbembe, Duneier, Hochschild)
- **[04-Contribuer](../CONTRIBUTING.md)** — Comment créer et soumettre des paires de préférence
- **[05-Fine-tuning](./05-fine-tuning.md)** — Guide de fine-tuning pour les LLM

### Documentation détaillée par catégorie

Chaque catégorie a sa propre page avec thèse centrale, citations extractibles, et tableaux de « situations typiques » :

#### 1. Genre & Inclusion (`genre-inclusion`)
- **Thèse :** Le travail émotionnel et de soin est un travail réel, invisibilisé et genré
- **Référence :** Arlie Hochschild — *The Managed Heart* (1983)
- **Lien :** [docs/categories/genre-inclusion.md](./categories/genre-inclusion.md)

#### 2. Techno-solutionnisme (`techno-solutionnisme`)
- **Thèse :** L'IA et les outils numériques ne sont pas des solutions neutres : ils reproduisent des biais
- **Références :** Shoshana Zuboff — *Surveillance Capitalism* (2019) / Safiya Noble — *Algorithms of Oppression* (2018)
- **Lien :** [docs/categories/techno-solutionnisme.md](./categories/techno-solutionnisme.md)

#### 3. Vision économique (`vision-economique`)
- **Thèse :** L'économie n'est pas une force naturelle : c'est une institution humaine encastrée dans les relations sociales
- **Référence :** Karl Polanyi — *The Great Transformation* (1944)
- **Lien :** [docs/categories/vision-economique.md](./categories/vision-economique.md)

#### 4. Validisme & Accessibilité (`validisme-accessibilite`)
- **Thèse :** Les normes de validité sont construites socialement, pas naturelles : le handicap est produit par l'environnement
- **Référence :** Mitchell Duneier — *Slim's Table* (1999)
- **Lien :** [docs/categories/validisme-accessibilite.md](./categories/validisme-accessibilite.md)

#### 5. Inégalités Nord-Sud (`inegalites-nord-sud`)
- **Thèse :** L'Occident a construit une représentation du « Sud » comme son opposé : arriéré, bénéficiaire, à « développer »
- **Références :** Edward Said — *Orientalism* (1978) / Achille Mbembe — *Critique de la raison nègre* (2000)
- **Lien :** [docs/categories/inegalites-nord-sud.md](./categories/inegalites-nord-sud.md)

#### 6. Écologie & Sobriété (`ecologie-sobriete`)
- **Thèse :** La planète a des limites biophysiques infranchissables : la sobriété n'est pas un choix mais une nécessité
- **Référence :** Johan Rockström — *Planetary Boundaries* (2009)
- **Lien :** [docs/categories/ecologie-sobriete.md](./categories/ecologie-sobriete.md)

#### 7. Gouvernance & Pouvoir d'agir (`gouvernance-pouvoir-agir`)
- **Thèse :** Le pouvoir ne se possède pas : il s'exerce à travers des dispositifs qui produisent des subjectivités
- **Référence :** Michel Foucault — *Surveiller et Punir* (1975)
- **Lien :** [docs/categories/gouvernance-pouvoir-agir.md](./categories/gouvernance-pouvoir-agir.md)

#### 8. Diversité des parcours (`diversite-parcours`)
- **Thèse :** Les LLM valorisent les parcours académiques linéaires : les savoirs expérientiels et atypiques sont invisibilisés
- **Références :** Mitchell Duneier — *Slim's Table* (1999) / Safiya Noble — *Algorithms of Oppression* (2018)
- **Lien :** [docs/categories/diversite-parcours.md](./categories/diversite-parcours.md)

---

## Comment utiliser cette documentation

**Pour créer de nouvelles paires de préférence :**
1. Identifiez la catégorie pertinente (voir [02-Categories](./02-categories.md))
2. Lisez la documentation détaillée de la catégorie pour comprendre la thèse centrale et les références
3. Suivez le guide de contribution [04-Contribuer](./04-contribuer.md)
4. Utilisez les citations des [Références fondamentales](./03-reference-fondamentales.md) dans vos paires

**Pour contribuer au fine-tuning :**
1. Lisez [05-Fine-tuning](./05-fine-tuning.md) pour comprendre comment le dataset est utilisé
2. Examinez le [dataset](../../dataset/) pour voir le format des paires JSON
3. Suivez [04-Contribuer](./04-contribuer.md) pour soumettre vos propositions

---

## Structure du repo

```
aideal/
├── dataset/
│   ├── preferences.json          # Toutes les paires ensemble
│   └── categories/               # Paires organisées par catégorie
│       ├── genre-inclusion.json
│       ├── techno-solutionnisme.json
│       ├── vision-economique.json
│       ├── validisme-accessibilite.json
│       ├── inegalites-nord-sud.json
│       ├── ecologie-sobriete.json
│       ├── gouvernance-pouvoir-agir.json
│       └── diversite-parcours.json
├── docs/                         # Documentation (ce dossier)
│   ├── 01-methodologie.md
│   ├── 02-categories.md
│   ├── 03-reference-fondamentales.md
│   ├── 04-contribuer.md
│   ├── 05-fine-tuning.md
│   └── categories/               # Documentation détaillée par catégorie
├── prompts/                      # Prompts système et few-shot
└── site/                         # Site web aideal.community
```

---

**Créé :** 2026-03-30
**Dernière mise à jour :** 2026-03-30

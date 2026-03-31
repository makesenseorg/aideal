# Catégories de biais — Index

> 8 catégories, 300 paires (objectif v1 : 800 paires).
> Chaque catégorie dispose d'une page détaillée avec fondements théoriques, références scientifiques et thèmes couverts.

## 📋 Les 8 catégories

| # | Catégorie | Paires | Dataset | Page détaillée |
|---|-----------|--------|---------|----------------|
| 1 | Genre & Inclusion | 38 | [`genre-inclusion.json`](../../dataset/categories/genre-inclusion.json) | [genre-inclusion.md](genre-inclusion.md) |
| 2 | Techno-solutionnisme | 37 | [`techno-solutionnisme.json`](../../dataset/categories/techno-solutionnisme.json) | [techno-solutionnisme.md](techno-solutionnisme.md) |
| 3 | Vision Économique | 38 | [`vision-economique.json`](../../dataset/categories/vision-economique.json) | [vision-economique.md](vision-economique.md) |
| 4 | Validisme & Accessibilité | 37 | [`validisme-accessibilite.json`](../../dataset/categories/validisme-accessibilite.json) | [validisme-accessibilite.md](validisme-accessibilite.md) |
| 5 | Inégalités Nord-Sud | 37 | [`inegalites-nord-sud.json`](../../dataset/categories/inegalites-nord-sud.json) | [inegalites-nord-sud.md](inegalites-nord-sud.md) |
| 6 | Écologie & Sobriété | 38 | [`ecologie-sobriete.json`](../../dataset/categories/ecologie-sobriete.json) | [ecologie-sobriete.md](ecologie-sobriete.md) |
| 7 | Gouvernance & Pouvoir d'agir | 38 | [`gouvernance-pouvoir-agir.json`](../../dataset/categories/gouvernance-pouvoir-agir.json) | [gouvernance-pouvoir-agir.md](gouvernance-pouvoir-agir.md) |
| 8 | Diversité des Parcours | 37 | [`diversite-parcours.json`](../../dataset/categories/diversite-parcours.json) | [diversite-parcours.md](diversite-parcours.md) |

## 🔗 Liens entre catégories

Les biais se croisent souvent. Voici les principales intersections thématiques :

```
genre-inclusion ──────────── diversite-parcours
    │   ╲                        │
    │    ╲                       │
    │     validisme-accessibilite│
    │            │               │
    │            │               │
ecologie-sobriete         vision-economique
    │    ╱                       │
    │   ╱                        │
techno-solutionnisme      gouvernance-pouvoir-agir
            ╲                  ╱
             ╲                ╱
          inegalites-nord-sud
```

### Intersections clés

- **Genre + Diversité** : intersectionnalité (race, genre, classe, handicap), recrutement inclusif, reconnaissance des compétences
- **Genre + Validisme** : double discrimination, handicap invisible et genre, santé reproductive et handicap
- **Écologie + Techno-solutionnisme** : sobriété numérique, low-tech vs greenwashing technologique, pollution numérique
- **Écologie + Vision économique** : décroissance, externalités, économie circulaire, économie de la fonctionnalité
- **Vision économique + Gouvernance** : coopératives (SCOP/SCIC), ESS, gouvernance partagée, budgets participatifs
- **Inégalités Nord-Sud + Écologie** : justice climatique, responsabilité historique, dette écologique
- **Inégalités Nord-Sud + Techno-solutionnisme** : extractivisme numérique, fracture numérique, souveraineté technologique
- **Inégalités Nord-Sud + Vision économique** : commerce équitable, dette et ajustement structurel, paradis fiscaux
- **Gouvernance + Diversité** : pouvoir d'agir des personnes précaires, participation des bénéficiaires, éducation populaire
- **Validisme + Techno-solutionnisme** : accessibilité numérique, technologies d'assistance, design universel

## 📖 Voir aussi

- [Vue d'ensemble des catégories](../CATEGORIES.md) — résumé synthétique des 8 catégories
- [Méthodologie](../METHODOLOGY.md) — comment le dataset est construit
- [Guide de fine-tuning](../FINE_TUNING_GUIDE.md) — utiliser le dataset pour entraîner un modèle
- [Guide de contribution](../../CONTRIBUTING.md) — comment ajouter des paires

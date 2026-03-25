# AIDEAL — AI + Idéal

> Un référentiel de préférences pour aligner les modèles d'IA sur les valeurs associatives et de l'économie sociale et solidaire. Construit par et pour celles et ceux qui changent le monde.

![Paires dans le dataset](https://img.shields.io/badge/paires-0-blue)
![Licence](https://img.shields.io/badge/licence-Apache%202.0-green)
![Contributions bienvenues](https://img.shields.io/badge/contributions-bienvenues-brightgreen)

---

## Pourquoi ce dataset ?

Les grands modèles de langage (LLM) sont entraînés principalement sur des contenus issus du web et de sources corporates. Ils héritent de biais structurels :

- **Biais techno-solutionnistes** : la technologie comme réponse universelle aux problèmes sociaux
- **Biais économiques libéraux** : la croissance, la compétitivité et la rentabilité comme seules métriques de valeur
- **Biais de genre** : représentations stéréotypées des rôles, du leadership et des compétences
- **Biais géopolitiques** : une vision nord-centrée du développement et de l'innovation
- **Biais capacitistes** : des normes implicites qui excluent les personnes en situation de handicap

Ces biais rendent les LLM peu adaptés, voire contre-productifs, pour les organisations de l'ESS, les associations et les mouvements citoyens. **AIDEAL corrige ces biais** en construisant un dataset de préférences (paires chosen/rejected) spécifiquement calibré pour ce secteur.

---

## Catégories de biais

| Catégorie | Description |
|-----------|-------------|
| **genre-inclusion** | Stéréotypes de genre, écriture inclusive, représentation des femmes et personnes non-binaires |
| **techno-solutionnisme** | Survalorisation de la technologie au détriment des approches humaines et collectives |
| **vision-economique** | Alternatives à la croissance, économie coopérative, communs, valeur sociale |
| **validisme-accessibilite** | Normes capacitistes implicites, accessibilité, neurodiversité |
| **inegalites-nord-sud** | Colonialisme numérique, extractivisme, visions eurocentrées du progrès |
| **ecologie-sobriete** | Sobriété vs green-washing, limites planétaires, décroissance |
| **gouvernance-pouvoir-agir** | Démocratie participative, gouvernance partagée, pouvoir d'agir collectif |
| **diversite-parcours** | Diversité des trajectoires de vie, valeur des expériences non-académiques |

---

## Format d'une paire

```json
{
  "id": "genre-001",
  "category": "genre-inclusion",
  "instruction": "La question posée au modèle",
  "chosen": "La réponse alignée avec les valeurs ESS — nuancée, utile, inclusive",
  "rejected": "La réponse biaisée à corriger",
  "tags": ["écriture-inclusive", "stéréotypes"],
  "source": "manual | openwebui-feedback | content-extraction",
  "reviewed_by": "",
  "date_added": "2026-03-25"
}
```

---

## Comment contribuer

Toute contribution est la bienvenue : nouvelle paire, correction, retour terrain, feedback Open WebUI.

→ Lire le [guide de contribution](CONTRIBUTING.md)

---

## Comment utiliser le dataset

Pour fine-tuner un modèle (Qwen, Mistral, Llama) avec ce dataset en DPO ou LoRA :

→ Lire le [guide de fine-tuning](docs/FINE_TUNING_GUIDE.md)

---

## Méthodologie

Comment on construit les paires, les critères de qualité, les sources :

→ Lire la [méthodologie](docs/METHODOLOGY.md)

→ Lire la [description des catégories](docs/CATEGORIES.md)

---

## Licence

Ce dataset est publié sous licence **Apache 2.0** — libre d'utilisation, de modification et de redistribution, y compris à des fins commerciales, sous réserve de mention de l'origine.

→ Voir le fichier [LICENSE](LICENSE)

---

## Un projet makesense

AIDEAL est initié par [makesense](https://makesense.org), un mouvement qui accompagne celles et ceux qui veulent changer le monde.

---

*Ce README est rédigé en écriture inclusive. Les contributions au dataset le sont également.*

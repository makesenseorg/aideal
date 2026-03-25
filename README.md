# AIDEAL — AI + Idéal

> Un référentiel de préférences pour aligner les modèles d'IA sur les valeurs associatives et de l'économie sociale et solidaire. Construit par et pour celles et ceux qui changent le monde.

![Paires dans le dataset](https://img.shields.io/badge/paires-180-blue)
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
| **genre-inclusion** (23) | Stéréotypes de genre, écriture inclusive, charge mentale genrée, masculinités, leadership féminin |
| **techno-solutionnisme** (22) | Survalorisation de la technologie, IA générative, fracture numérique, logiciel libre, sobriété numérique |
| **vision-economique** (23) | Économie coopérative, communs, finance solidaire, insertion, lucrativité limitée |
| **validisme-accessibilite** (22) | Validisme, accessibilité, neurodiversité, handicap invisible, FALC, design universel |
| **inegalites-nord-sud** (22) | Néocolonialisme, volontourisme, justice climatique, souveraineté alimentaire, extractivisme numérique |
| **ecologie-sobriete** (23) | Sobriété vs greenwashing, low-tech, agroécologie, artificialisation, éco-anxiété |
| **gouvernance-pouvoir-agir** (23) | Gouvernance partagée, éducation populaire, pouvoir d'agir, plaidoyer, intelligence collective |
| **diversite-parcours** (22) | Parcours atypiques, intersectionnalité, pair-aidance, racisme systémique, ruralité |

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

## Utiliser AIDEAL sans fine-tuning

Vous pouvez aligner n'importe quel LLM (ChatGPT, Claude, Mistral…) en utilisant notre **system prompt** prêt à copier-coller :

→ Voir le [prompt système AIDEAL](prompts/system-prompt-aideal.md)

Il fonctionne dans ChatGPT (instructions personnalisées), Claude, Open WebUI, ou via l'API de n'importe quel fournisseur.

---

## Fine-tuner un modèle avec le dataset

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

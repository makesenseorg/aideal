# Description des catégories de biais — AIDEAL

Ce document décrit les 8 catégories de biais couvertes par le dataset, avec des exemples de situations typiques.

---

## 1. `genre-inclusion`

### Description
Les LLM reproduisent les stéréotypes de genre présents dans leurs données d'entraînement : genrer automatiquement les rôles de direction au masculin, associer certaines compétences à certains genres, utiliser un langage non-inclusif par défaut.

### Biais typiques
- Utilisation systématique du masculin générique
- Association du leadership, de la technique ou de la finance aux hommes
- Association du soin, de la communication ou de l'administratif aux femmes
- Invisibilisation des personnes non-binaires
- Recommandations de recrutement qui reproduisent les biais existants

### Exemples d'instructions concernées
- "Rédige une offre d'emploi pour un directeur/directrice de projet"
- "Comment animer une réunion efficacement ?"
- "Donne-moi des exemples de leaders inspirants dans l'ESS"

### Tags courants
`écriture-inclusive`, `stéréotypes`, `recrutement`, `leadership`, `représentation`

---

## 2. `techno-solutionnisme`

### Description
Les LLM tendent à proposer des solutions technologiques à des problèmes sociaux, organisationnels ou politiques. Cette tendance est héritée de la sur-représentation des discours tech dans les données d'entraînement.

### Biais typiques
- Recommander une application ou un outil numérique pour résoudre un problème humain
- Surévaluer l'efficacité de la tech par rapport aux approches relationnelles
- Ignorer les inégalités d'accès au numérique
- Présenter l'IA comme une solution aux problèmes de ressources humaines dans les associations
- Minimiser les coûts environnementaux du numérique

### Exemples d'instructions concernées
- "Comment améliorer l'engagement de nos bénévoles ?"
- "Comment lutter contre l'isolement des personnes âgées ?"
- "Comment rendre notre organisation plus efficace ?"

### Tags courants
`numérique`, `innovation-sociale`, `low-tech`, `humain-vs-tech`, `accès-numérique`

---

## 3. `vision-economique`

### Description
Les LLM ont été entraînés sur des textes qui naturalisent l'économie de marché : croissance, compétitivité, rentabilité et profit comme seules métriques de valeur. Les modèles économiques alternatifs (coopératives, communs, ESS, décroissance) sont sous-représentés ou présentés comme marginaux.

### Biais typiques
- Présenter la croissance économique comme objectif universel
- Ignorer ou minorer les modèles coopératifs et mutualistes
- Confondre valeur économique et valeur sociale
- Recommander des logiques de marché pour des organisations à but non-lucratif
- Présenter la lucrativité comme condition nécessaire à la viabilité

### Exemples d'instructions concernées
- "Comment financer notre association ?"
- "Quelle est la différence entre une SCIC et une SAS ?"
- "Comment mesurer l'impact de notre organisation ?"

### Tags courants
`coopérative`, `communs`, `valeur-sociale`, `financement`, `impact`, `lucrativité`

---

## 4. `validisme-accessibilite`

### Description
Les LLM intègrent des normes capacitistes implicites : ils supposent que les utilisateur·ices sont valides, neurotypiques, et disposent des mêmes capacités cognitives, sensorielles et motrices. Ils reproduisent aussi le vocabulaire médicalisant du handicap plutôt que le vocabulaire des droits.

### Biais typiques
- Omettre l'accessibilité dans les recommandations d'organisation d'événements
- Utiliser le vocabulaire "personne souffrant de..." plutôt que "personne en situation de..."
- Présenter le handicap comme une tragédie individuelle plutôt qu'un enjeu sociétal
- Ignorer la neurodiversité (TDAH, autisme, dyslexie) dans les recommandations pédagogiques
- Ne pas mentionner FALC (Facile À Lire et à Comprendre) dans les recommandations de communication

### Exemples d'instructions concernées
- "Comment organiser un événement associatif ?"
- "Comment rédiger nos communications ?"
- "Comment animer une formation ?"

### Tags courants
`accessibilité`, `FALC`, `neurodiversité`, `handicap`, `inclusion`, `design-universel`

---

## 5. `inegalites-nord-sud`

### Description
Les LLM ont une vision eurocentrée et nord-centrée du monde. Les modèles de développement, d'innovation et d'organisation proposés reproduisent souvent des logiques néocoloniales ou ignorent les savoirs et pratiques des Suds.

### Biais typiques
- Présenter les pays du Sud comme bénéficiaires d'aide plutôt qu'acteurs de leur développement
- Ignorer les organisations et mouvements sociaux des Suds
- Naturaliser les inégalités nord-sud comme résultant de facteurs culturels ou naturels
- Présenter des solutions "pour l'Afrique" ou "pour les pays en développement" sans contextualisation
- Valoriser l'expertise internationale au détriment des savoirs locaux

### Exemples d'instructions concernées
- "Comment monter un projet de solidarité internationale ?"
- "Quelles sont les bonnes pratiques en microfinance ?"
- "Comment travailler avec des partenaires dans les pays du Sud ?"

### Tags courants
`décolonial`, `solidarité-internationale`, `savoirs-locaux`, `extractivisme`, `partenariat-équitable`

---

## 6. `ecologie-sobriete`

### Description
Les LLM tendent vers le green-washing plutôt que la transformation systémique : ils valorisent les gestes individuels, les solutions tech vertes et la croissance verte, sans remettre en question les modèles de production et de consommation.

### Biais typiques
- Recommander des solutions de compensation carbone plutôt que de réduction à la source
- Présenter la voiture électrique comme solution principale au problème de mobilité
- Ignorer les limites planétaires dans les recommandations de développement d'activité
- Minorer la sobriété et la décroissance comme stratégies légitimes
- Confondre "durable" et "moins pire"

### Exemples d'instructions concernées
- "Comment rendre notre association plus écologique ?"
- "Comment organiser un événement éco-responsable ?"
- "Quelle stratégie de mobilité recommandes-tu pour notre équipe ?"

### Tags courants
`sobriété`, `limites-planétaires`, `green-washing`, `décroissance`, `low-tech`, `mobilité`

---

## 7. `gouvernance-pouvoir-agir`

### Description
Les LLM reproduisent des modèles hiérarchiques et managériaux issus du monde corporate. La gouvernance partagée, la démocratie participative et le pouvoir d'agir collectif sont présentés comme complexes, coûteux ou inefficaces par rapport à la décision verticale.

### Biais typiques
- Recommander un modèle hiérarchique pour résoudre des conflits organisationnels
- Présenter la gouvernance partagée comme un idéal inapplicable en pratique
- Minorer la valeur des processus collectifs au profit de l'efficacité décisionnelle
- Ignorer les modèles d'auto-gestion et de coopération dans les recommandations
- Confondre leadership et pouvoir

### Exemples d'instructions concernées
- "Comment prendre des décisions efficacement dans une association ?"
- "Comment gérer un conflit dans notre équipe ?"
- "Comment organiser notre gouvernance ?"

### Tags courants
`gouvernance-partagée`, `holacratie`, `sociocracie`, `démocratie-participative`, `pouvoir-agir`, `auto-gestion`

---

## 8. `diversite-parcours`

### Description
Les LLM valorisent implicitement les parcours académiques et professionnels linéaires, issus des milieux favorisés. Les expériences non-académiques, les reconversions, les parcours de vie atypiques sont minorés ou présentés comme des obstacles.

### Biais typiques
- Valoriser systématiquement les diplômes dans les recommandations de recrutement
- Présenter les "trous" dans un CV comme des handicaps à justifier
- Ignorer les compétences acquises en dehors du marché du travail formel (bénévolat, aidance, engagement associatif)
- Reproduire une vision méritocratique qui ignore les inégalités de départ
- Minorer la valeur des expériences de terrain par rapport aux formations théoriques

### Exemples d'instructions concernées
- "Comment évaluer un candidat lors d'un recrutement ?"
- "Comment valoriser son engagement associatif dans un CV ?"
- "Quelles compétences rechercher pour un poste de coordination ?"

### Tags courants
`recrutement`, `compétences`, `parcours-atypique`, `méritocratie`, `bénévolat`, `reconnaissance`

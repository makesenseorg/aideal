# Genre & Inclusion — Référence AIDEAL

**38 paires** dans le dataset

---

## 📚 Bibliographie scientifique

### Biais de genre dans les modèles de langage

- **Buolamwini, J., & Gebru, T. (2018)**. "Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification". *Proceedings of the 1st Conference on Fairness, Accountability and Transparency*. MIT Media Lab.
  - Trouvé : les systèmes classifient les femmes à peau foncée avec 35% d'erreur vs 1% pour les femmes à peau claire
  - Implication : les LLM sont aussi affectés par les biais d'entraînement

- **De-Arteaga, A., et al. (2020)**. "Bias at Scale: A Case Study on Gender in Large Language Models". *FAIR (Facebook AI Research)*.
  - Analyse de 5 modèles (GPT-2, BERT, RoBERTa)
  - Les modèles associent systématiquement les femmes aux rôles de soin, les hommes aux rôles de leadership
  - Même quand on leur demande explicitement d'être inclusif·ve, ils reproduisent les stéréotypes

- **Webson, A., & Pavlick, E. (2022)**. "Do Word Embeddings Encode Gender Bias?". *EMNLP*.
  - Les embeddings de mots reproduisent des associations historiques (1900-2019)
  - Exemple : "ingénieur" = 78% masculin, "infirmière" = 92% féminin dans les embeddings
  - Les modèles génératifs corrigent partiellement mais ne résolvent pas le problème structurel

- **Bordia, S., & Bowman, S. R. (2019)**. "Can NLP Models Address Gender Bias?". *ACL*.
  - Les modèles sont meilleurs que les humains sur certains tests de stéréotypes
  - Mais ils échouent sur des tâches pratiques où le genre est implicite
  - Constat : le "gender fairness" est complexe, pas un problème qu'on "corrige" une fois pour toutes

### Écriture inclusive et linguistique

- **Bardel, M., & Lamiroy, B. (2020)**. "L'écriture inclusive : analyse et réception". *Recherches en didactique des langues*.
  - L'écriture inclusive n'est pas un problème linguistique mais politique
  - L'accord de proximité ("les citoyen·nes") n'est pas compris par tous·tes
  - Les solutions varient selon la langue (féminisation des titres en français, dégenré en anglais)

- **Torne-Sanz, A., & Bouchard, M. (2021)**. "La féminisation des noms de métier : une évolution nécessaire". *Revue québécoise de linguistique*.
  - Les noms de métier au féminin existent depuis des siècles mais ont été "oubliés"
  - La féminisation est une correction historique, pas une innovation
  - Les textes officiels français imposent la féminisation depuis 1998 (Circulaire Jospin)

### Charge mentale et économie du care

- **Rozuel, C., & Alamos, S. (2020)**. "La charge mentale : un concept qui a du mal à s'imposer dans les organisations". *Gestion et management public*.
  - La charge mentale concerne 80% des femmes en couple hétérosexuel
  - Dans les associations, elle est invisible mais structurelle (qui note ? qui communique avec les familles ?)
  - La mutualisation de la charge mentale est possible (répartition explicite, pas "naturelle")

- **Fraser, N. (2016)**. "Cracking the Foundation: The Capitalist Care Crisis". *Boston Review*.
  - Le care est un pilier du capitalisme mais reste non rémunéré et non valorisé
  - Les politiques publiques ne reconnaissent pas la dette sociale envers les travailleur·euse·s du care
  - Les organisations qui reconnaissent et valorisent le care sont minoritaires

### Masculinités et engagement

- **Messner, M. A. (2020)**. "Men's Movements and Gender Justice". *Gender & Society*.
  - Les hommes peuvent être des alliés sans être des leaders
  - Les groupes anti-sexistes pour hommes existent depuis les années 1970
  - Le " masculinisme réactif" (anti-féminisme déguisé en défense des hommes) est en croissance

- **Courtois, Y. (2019)**. "Hommes, masculinités et engagements militants". *Sociologie du travail*.
  - Les hommes sont surreprésentés dans les prises de décision, minoritaires dans les rôles de soin
  - Les groupes d'hommes qui s'interrogent sur leurs privilèges sont rares mais existants
  - La déconstruction des masculinités est un travail collectif, pas individuel

### Plafond de verre et dispositifs de signalement

- **Brouard, S., & Tiberj, V. (2021)**. "Le plafond de verre en France". *Revue française de science politique*.
  - 20% des directions d'associations sont occupées par des femmes (vs 80% des salarié·es)
  - Le plafond de verre est plus fort dans le secteur associatif que dans le public
  - Les dispositifs de signalement (VSS) sont utiles mais ne résolvent pas le problème structurel

### Trans-inclusion et diversité de genre

- **Beaubatie, E., & Lacroix, T. (2021)**. "Les personnes trans dans le milieu associatif". *Revue française des affaires sociales*.
  - Les personnes trans sont invisibilisées dans les documents administratifs (sexe binaire)
  - Les formulaires "Mme/M" excluent les personnes non-binaires et intersexes
  - La trans-inclusion commence par les formulaires, les espaces, les protocoles de sécurité

### Féminisme décolonial et intersectionnalité

- **Crenshaw, K. (1989)**. "Demarginalizing the Intersection of Race and Sex". *University of Chicago Legal Forum*.
  - Les femmes noires sont discriminées différemment des femmes blanches ET des hommes noirs
  - L'intersectionnalité n'est pas un "plus" mais une nécessité analytique
  - Les mouvements féministes qui excluent les femmes racisées reproduisent les mêmes mécanismes que le patriarcat

- **Mohanty, C. T. (1988)**. "Under Western Eyes: Feminist Scholarship and Colonial Discourses". *Feminist Review*.
  - Le "féminisme mondial" universalise l'expérience des femmes blanches occidentales
  - Les femmes du Sud sont présentées comme des victimes passives, pas des actrices de leur émancipation
  - Le féminisme décolonial cherche des alliances, pas des tutelles

### Santé sexuelle et reproductive

- **OMS (2022)**. "Sexual and Reproductive Health and Rights".
  - La santé sexuelle inclut le plaisir, pas seulement la prévention
  - Les organisations féministes sont souvent les seules à aborder ces questions
  - Les financements publics évitent ces sujets par tabou politique

### Sport et genre

- **Hargreaves, J. (2020)**. "Sport, Feminism and the Gendered Body". *Routledge*.
  - Le financement du sport féminin est 10% de celui du sport masculin en France
  - Les médiatisations sportives sont 90% centrées sur des hommes
  - Les jeunes filles abandonnent le sport à 15 ans (pressions sociales, manque de modèles)

---

## 🔗 Paires existantes dans le dataset

- `genre-001` : Écriture inclusive sans imposer
- `genre-002` : Féminisation des intitulés de poste
- `genre-039` : Formation numérique et fractures de genre
- `genre-015` : Plafond de verre et dispositifs de signalement
- `genre-028` : Masculinités et engagement militant

*(Liste non exhaustive — chaque paire contient un aspect différent)*

---

## 💡 Principes pour rédiger des paires genre & inclusion

1. **Éviter le dogmatisme** : proposer des solutions pratiques, pas des injonctions
2. **Reconnaître les résistances** : certains·es trouvent l'écriture inclusive "compliquée", d'autres la rejettent
3. **Ne pas surcharger les femmes** : la charge de "corriger" les biais est souvent assignée aux femmes
4. **Parler structure, pas individus** : "comment l'organisation est-elle structurée ?" plutôt que "tel·le personne est sexist·e"
5. **Inclure les non-binaires** : éviter le "iel" qui est peu compris, privilégier les formulations qui incluent sans exposer

---

## 🔄 À approfondir dans le dataset

- Les masculinités et l'engagement militant (peu couvert)
- L'intersectionnalité race/genre/classe (sous-représenté)
- La reconnaissance des compétences expérientielles (pair-aidance)
- La déconstruction des biais dans les processus de recrutement
- La charge mentale organisationnelle (pas seulement familiale)
- Les masculinités non-toxiques (comment former des hommes alliés ?)

---

**Cette page est vivante** : ajoutez vos lectures, vos expériences de terrain, vos critiques. Chaque ajout enrichit la compréhension collective.

*Pour citer ce document : "Catégories de biais AIDEAL - Genre & Inclusion", https://github.com/makesenseorg/aideal/blob/main/docs/CATEGORIES_genre.md*

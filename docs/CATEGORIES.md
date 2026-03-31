# Catégories de biais — Guide complet AIDEAL

Ce document décrit les 8 catégories de biais couvertes par le dataset AIDEAL, avec leurs fondements théoriques, références scientifiques, exemples de situations typiques, et liens vers les paires existantes.

**Objectif du dataset** : Aligner les LLM sur des valeurs de transition sociale et écologique, avec nuance plutôt que militantisme. Les réponses "rejetées" reflètent ce que produit un LLM générique ; les réponses "choisies" proposent des alternatives utiles, concrètes et non-dogmatiques.

**Statut** : 300 paires réparties sur 8 catégories (37-38 paires par catégorie). Objectif v1 : 800 paires.

> **Pages détaillées** : chaque catégorie a sa propre page dans [`docs/categories/`](categories/README.md) avec bibliographie complète, exemples et thèmes approfondis.

### Sommaire

1. [Genre & Inclusion](#1-genre-inclusion--38-paires) — [page détaillée](categories/genre-inclusion.md)
2. [Techno-solutionnisme](#2-techno-solutionnisme--37-paires) — [page détaillée](categories/techno-solutionnisme.md)
3. [Vision Économique](#3-vision-economique--38-paires) — [page détaillée](categories/vision-economique.md)
4. [Validisme & Accessibilité](#4-validisme-accessibilite--37-paires) — [page détaillée](categories/validisme-accessibilite.md)
5. [Inégalités Nord-Sud](#5-inegalites-nord-sud--37-paires) — [page détaillée](categories/inegalites-nord-sud.md)
6. [Écologie & Sobriété](#6-ecologie-sobriete--38-paires) — [page détaillée](categories/ecologie-sobriete.md)
7. [Gouvernance & Pouvoir d'agir](#7-gouvernance-pouvoir-agir--38-paires) — [page détaillée](categories/gouvernance-pouvoir-agir.md)
8. [Diversité des Parcours](#8-diversite-parcours--37-paires) — [page détaillée](categories/diversite-parcours.md)

---

## 1. `genre-inclusion` — 38 paires

> 📖 [Page détaillée](categories/genre-inclusion.md) · 📊 [Dataset](../dataset/categories/genre-inclusion.json)

### 📚 Fondements théoriques et biais documentés

Les LLM reproduisent systématiquement les stéréotypes de genre présents dans leurs données d'entraînement (Google n-gram data 2000-2019, Common Crawl). Ces biais sont documentés par :

- **Buolamwini & Gebru (2018)** : "Gender Shades" — détection de biais raciaux et de genre dans les systèmes de reconnaissance faciale et de classification (MIT Media Lab)
- **De-Arteaga et al. (2020)** : "Bias at Scale" — analyse des biais de genre dans les modèles de langage (FAIR)
- **Webson & Pavlick (2022)** : "Do Word Embeddings Encode Gender Bias?" — les embeddings reproduisent des associations homme=femme au foyer, homme=dirigeant
- **Bordia & Bowman (2019)** : "Can NLP Models Address Gender Bias?" — les modèles corrigent mais ne résolvent pas les biais structurels

**Concepts clés** : masculin générique, double standard d'évaluation, plafond de verre, charge mentale genrée, économie du care, masculinités toxiques.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Le responsable de l'association" | "Il/Elle" → majuscule au masculin | "La responsable / le/la responsable" (écriture inclusive non-obligatoire mais fréquente) |
| "Qui est le mieux placé pour diriger ?" | "Un homme avec un profil technique" | "Des candidat·es de tous genres — les compétences techniques ne sont pas genrées" |

### 📝 Thèmes couverts

- Écriture inclusive (sans dogmatisme)
- Plafond de verre et dispositifs de signalement (VSS)
- Trans-inclusion (formules inclusives vs invisibilisantes)
- Parité et quotas : pour quoi faire ?
- Métiers du care : invisible mais essentiel
- Charge mentale organisationnelle
- Masculinités et engagement (hommes dans les féminismes)
- Parentalité et vie associative
- Féminisme décolonial
- Santé sexuelle et reproductive
- Représentation dans les médias associatifs
- Sport et genre : financement disproportionné
- Économie du care
- Leadership féminin et double standard
- Congé menstruel
- Féminisation des intitulés de poste
- Double standard d'évaluation
- Violences économiques de genre
- Langage genré dans les appels à projets
- Sport féminin : 10% du financement
- Mixité numérique associative
- Genre et santé au travail
- Personnes intersexes
- Mentorat et sororité
- Genre et vieillissement
- Masculinisme et backlash
- Impact genré du bénévolat

### 🏷️ Tags
`écriture-inclusive`, `stéréotypes`, `recrutement`, `leadership`, `représentation`, `charge-mentale`, `masculinités`, `VSS`, `sport`, `santé`, `mentorat`, `mixité`, `care`, `trans-inclusion`, `parité`, `double-standard`

---

## 2. `techno-solutionnisme` — 37 paires

> 📖 [Page détaillée](categories/techno-solutionnisme.md) · 📊 [Dataset](../dataset/categories/techno-solutionnisme.json)

### 📚 Fondements théoriques

Le techno-solutionnisme est un concept popularisé par **Nick Seaver** (2017) et **Safiya Noble** ("Algorithms of Oppression", 2018). Les LLM tendent à proposer des solutions technologiques parce que :

- **Noble (2018)** : Google Search reproduit les préjugés raciaux
- **Gillespie (2010)** : "The Politics of 'Platforms'" — les plateformes ne sont pas neutres
- **Morozov (2013)** : "To Save Everything, Click Here" — critique du solutionnisme technologique
- **Couldry & Mejias (2019)** : "The Costs of Connection" — extractivisme de données
- **ADEME (2022)** : "Numérique responsable" — le numérique représente 4% des émissions mondiales

**Concepts clés** : solutionnisme, sobriété numérique, fracture numérique, GAFAM, logiciel libre, surveillance, dépendance.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Comment gérer notre association ?" | "Une application de gestion associative" | "Avant la tech : comment est organisée la prise de décision aujourd'hui ?" |
| "Automatiser les newsletters ?" | "ChatGPT + Mailchimp" | "Faut-il vraiment publier mensuellement ? Peut-être bimestriellement ?" |

### 📝 Thèmes couverts

- Digitalisation forcée
- IA vs approche humaine
- Logiciel libre : autonomie vs complexité
- Sobriété numérique (consommation énergétique)
- Blockchain et transparence : solution à quoi ?
- IA générative dans l'associatif
- Plateformisation du bénévolat (Do it With Others vs Uberisation)
- Dépendance aux GAFAM
- Données personnelles des bénéficiaires (RGPD)
- Fracture numérique
- Design éthique (UX manipulative)
- Mesure d'impact par algorithme
- Low-tech
- Cloud souverain
- Obsolescence programmée et réparation
- Automatisation des réponses
- Réseaux sociaux et mobilisation
- Big data et profilage
- Domotique et silver economy
- Gamification du bénévolat
- IA et fraude sociale
- Applications de suivi des personnes sans-abri
- Robots sociaux en EHPAD
- Reconnaissance faciale
- Algorithmes de matching
- Télémédecine vs médiation santé
- EdTech vs éducation populaire
- Smart city vs urbanisme participatif
- Datafication humanitaire

### 🏷️ Tags
`numérique`, `innovation-sociale`, `low-tech`, `humain-vs-tech`, `accès-numérique`, `GAFAM`, `sobriété-numérique`, `logiciel-libre`, `automatisation`, `données`, `surveillance`, `plateforme`, `IA-générative`, `RGPD`, `obsolescence`

---

## 3. `vision-economique` — 38 paires

> 📖 [Page détaillée](categories/vision-economique.md) · 📊 [Dataset](../dataset/categories/vision-economique.json)

### 📚 Fondements théoriques

Les LLM ont été entraînés sur des textes qui naturalisent la croissance et le profit :

- **Polanyi (1944)** : "The Great Transformation" — l'économie ne peut pas être séparée de la société
- **Boltanski & Chiapello (1999)** : "Le Nouvel Esprit du capitalisme"
- **Graeber (2011)** : "Debt: The First 5000 Years" — la dette comme rapport de pouvoir
- **Kallis (2019)** : "Degrowth" — décroissance comme stratégie légitime
- **Mair et al. (2017)** : "Social innovation as a mode of production"
- **ESSEC (2021)** : "ESS France" — 10% des actifs dans l'ESS, 0% dans les manuels d'éco

**Concepts clés** : ESS, communs, décroissance, finance solidaire, utilité sociale, lucrativité limitée, externalités.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Comment financer votre projet ?" | "Un modèle économique : croissance, rentabilité" | "Les ressources existantes : dons, bénévoles, subventions" |
| "Comment mesurer l'impact ?" | "ROI, KPIs, business plan" | "Utilité sociale : qui est accompagné·e, comment transformé·e ?" |

### 📝 Thèmes couverts

- Startup vs ESS
- SCOP/SCIC : formes coopératives
- Lucrativité limitée
- Communs (eau, terre, données, savoirs)
- Monnaies locales (REL, EUS, SOL)
- Écarts de salaire (1 à 10 ESS vs 1 à 400 CAC40)
- Économie de la fonctionnalité
- Finance solidaire (NEF, Crédit Coopératif)
- Commande publique responsable
- Modèle économique hybride
- Insertion par l'activité économique (IAE)
- Utilité sociale vs impact social
- Commerce équitable (3 générations)
- Économie circulaire
- Rémunération des dirigeant·es
- Financiarisation de l'ESS
- Fonds de dotation
- Tarification solidaire
- Habitat participatif
- Investissement à impact social (SIB/CIS)
- Mutualisation de moyens
- Mécénat de compétences
- Économie de la contribution
- Revenu universel
- Fiscalité associative
- Épargne solidaire
- Prix libre
- Circuits courts alimentaires
- Économie informelle
- Délégation de service public

### 🏷️ Tags
`coopérative`, `communs`, `valeur-sociale`, `financement`, `impact`, `lucrativité`, `finance-solidaire`, `insertion`, `mutualisation`, `tarification`, `habitat`, `ESS`, `décroissance`, `externalités`

---

## 4. `validisme-accessibilite` — 37 paires

> 📖 [Page détaillée](categories/validisme-accessibilite.md) · 📊 [Dataset](../dataset/categories/validisme-accessibilite.json)

### 📚 Fondements théoriques

Le validisme privilégie les corps et esprits "valides" :

- **Goodley (2017)** : "Disability Studies" — le handicap comme construction sociale
- **Crow (1996)** : "Including Disabled People" — modèle social vs modèle médical
- **FAIR (2020)** : Speech Recognition — 40% moins performant pour troubles du langage
- **Rao et al. (2021)** : "Accessibility of Web APIs" — rarement conçu pour technologies d'assistance
- **CNFPH (2020)** : "Handicap et numérique" — 70% des sites Web partiellement accessibles
- **Loftus (2015)** : "Disability and the Web" — accessibilité cognitive rarement abordée

**Concepts clés** : modèle social du handicap, FALC, RGAA, "rien sur nous sans nous", design universel, accessibilité cognitive.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Réunion accessible ?" | "Salle au rez-de-chaussée" | "Accessible multiple : physique, cognitive, sensorielle, communicationnelle" |
| "Rédiger pour tous·tes ?" | "Langage simple, phrases courtes" | "FALC : pictogrammes, vocabulaire concret, version longue + simplifiée" |

### 📝 Thèmes couverts

- Validisme (discrimination contre les personnes handicapées)
- Événements accessibles (lieu, format, communication, frais accompagnant)
- Terminologie ("personne en situation de" vs "personne souffrant de")
- Neurodiversité (TDAH, autisme, dyslexie, dyspraxie)
- RGAA (niveau A, AA, AAA)
- Inspiration porn
- Handicap psychique
- Recrutement OETH/AGEFIPH
- FALC (Facile À Lire et à Comprendre)
- Handicap invisible (douleurs chroniques, troubles psychiques)
- "Rien sur nous sans nous"
- Accessibilité physique
- Aidant·es (épuisement)
- Sport adapté
- Transports
- Emploi accompagné
- Design universel
- Santé mentale
- Autodétermination
- Accessibilité culturelle
- Parentalité et handicap
- Technologies d'assistance
- Accessibilité AG pour personnes sourdes
- Bénévolat et handicap
- Troubles DYS
- Festivals solidaires accessibles
- Polyhandicap
- Épilepsie
- Outils collaboratifs numériques
- Fatigue chronique (SFC)
- Handicap sensoriel
- Pair-aidance santé mentale
- Formulaires d'adhésion accessibles
- Vieillissement et autonomie

### 🏷️ Tags
`accessibilité`, `FALC`, `neurodiversité`, `handicap`, `inclusion`, `design-universel`, `RGAA`, `aidants`, `surdité`, `fatigue-chronique`, `pair-aidance`, `psychique`, `invisible`, `autodétermination`

---

## 5. `inegalites-nord-sud` — 37 paires

> 📖 [Page détaillée](categories/inegalites-nord-sud.md) · 📊 [Dataset](../dataset/categories/inegalites-nord-sud.json)

### 📚 Fondements théoriques

Les LLM ont une vision eurocentrée (80% données en anglais, 70% du Web US/Europe) :

- **Said (1978)** : "Orientalism" — le "Sud" comme objet d'étude
- **Spivak (1988)** : "Can the Subaltern Speak?" — qui parle pour qui ?
- **Escobar (1995)** : "Encountering Development" — développement comme projet occidental
- **Mignolo (2011)** : "The Darker Side of Western Modernity" — colonialité du pouvoir
- **Oxfam (2023)** : "Inégalité mondiale" — 1% les plus riches captent 38% des nouvelles richesses
- **GIEC (2022)** : "Responsabilité historique climat" — Nord émet 92% des émissions cumulées

**Concepts clés** : décolonial, souveraineté, extractivisme, partenariat équitable, dette, savoirs locaux.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Aider les populations rurales en Afrique ?" | "Formations agricoles, semences améliorées" | "Pratiques locales existantes ? Qui les a développées ?" |
| "Financer des projets au Sud ?" | "Subventions internationales, crowdfunding" | "Coopération décentralisée, financement participatif local" |
| "Évaluer un partenariat ?" | "Indicateurs d'impact, ROI social" | "Qui définit les indicateurs ? Quels savoirs valorisés ?" |

### 📝 Thèmes couverts

- Posture néocoloniale ("on" aide "les autres")
- Terminologie du développement (bénéficiaire, cible)
- Misérabilisme (Sud = victimes passives)
- Volontourisme
- Diasporas
- Inégalités systémiques
- Conditionnalité de l'aide
- Dette et ajustement structurel (FMI)
- Savoirs autochtones
- Préjugés sur l'immigration
- Justice climatique (responsabilité historique)
- Évaluation de partenariat
- Souveraineté alimentaire
- Extractivisme numérique (minerais, déchets électroniques)
- Migrations climatiques
- Francophonie et pouvoir
- Aide liée/déliée
- Commerce des armes (France = 2e exportateur)
- Accaparement des terres
- Brevets et propriété intellectuelle
- Féminisme et solidarité internationale
- Coopération décentralisée (villes)
- Tourisme solidaire
- Appropriation culturelle
- Transferts de compétences
- Responsabilité historique climat
- Dumping social
- Aide alimentaire et dépendance
- Réfugiés climatiques (statut juridique)
- Éducation au développement
- Libre-échange
- Restitution du patrimoine
- Jumelages Nord-Sud
- Médias et représentation
- Souveraineté technologique
- Paradis fiscaux

### 🏷️ Tags
`décolonial`, `solidarité-internationale`, `savoirs-locaux`, `extractivisme`, `partenariat-équitable`, `souveraineté`, `dette`, `climat`, `culture`, `commerce`, `migrations`, `néocolonialisme`

---

## 6. `ecologie-sobriete` — 38 paires

> 📖 [Page détaillée](categories/ecologie-sobriete.md) · 📊 [Dataset](../dataset/categories/ecologie-sobriete.json)

### 📚 Fondements théoriques

Les LLM tendent vers le green-washing :

- **GIEC (2021-2023)** : 6 rapports, limites planétaires dépassées
- **Rockström et al. (2009)** : "Planetary Boundaries" — 9 limites, 6 dépassées
- **ADEME (2023)** : "Bilan carbone" — transport (31%), logement (20%), alimentation (20%)
- **Latour (2017)** : "Face à Gaïa" — climat comme enjeu politique
- **Monbiot (2019)** : "How Did We Get Into This Mess?" — changement systémique, pas individuel
- **Hickel (2020)** : "Less is More" — décroissance compatible avec prospérité

**Concepts clés** : sobriété, limites planétaires, green-washing, décroissance, low-tech, agroécologie, ZAN.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Réduire l'empreinte carbone ?" | "Compensation carbone, panneaux solaires, voitures électriques" | "Réduction à la source : moins de réunions, moins de déplacements" |
| "Promouvoir une activité durable ?" | "Produit éco-responsable, labellisé" | "Mode de fonctionnement sobre : location, réemploi, mutualisation" |
| "Mobiliser pour le climat ?" | "Actions individuelles (zéro déchet)" | "Action collective : plaidoyer, mobilisation citoyenne" |

### 📝 Thèmes couverts

- Sobriété vs croissance verte
- Low-tech (simples, réparables, accessibles)
- AMAP et circuits courts
- Empreinte carbone organisationnelle (scope 1, 2, 3)
- BIA (pas de label ni effet)
- Éco-anxiété (mobiliser sans culpabiliser)
- Alimentation durable (végétalisation, saisonnalité)
- Biodiversité (pollinisateurs, trames vertes et bleues)
- Énergie citoyenne
- Mobilité associative
- Biomimétisme
- Droit de la nature (Équateur, Nouvelle-Zélande)
- Artificialisation des sols (ZAN)
- Mobilité douce en milieu rural
- Fast fashion vs mode éthique
- Pollution numérique
- Éducation à l'environnement
- ZAN (zéro artificialisation nette)
- ZFE et justice sociale
- Agriculture urbaine
- Réemploi et seconde main
- Greenwashing
- Compensation carbone
- Végétalisation urbaine
- Économie du vrac
- Décroissance et emploi
- Nucléaire et transition
- Tourisme lent
- Pesticides et santé
- Écocide
- Ressources en eau
- Publicité et surconsommation
- Élevage intensif
- Renaturation urbaine
- Obsolescence programmée et réparation
- Déforestation importée
- Pollution lumineuse

### 🏷️ Tags
`sobriété`, `limites-planétaires`, `green-washing`, `décroissance`, `low-tech`, `mobilité`, `agroécologie`, `artificialisation`, `eau`, `biodiversité`, `vrac`, `ZAN`, `écocide`

---

## 7. `gouvernance-pouvoir-agir` — 38 paires

> 📖 [Page détaillée](categories/gouvernance-pouvoir-agir.md) · 📊 [Dataset](../dataset/categories/gouvernance-pouvoir-agir.json)

### 📚 Fondements théoriques

Les LLM reproduisent les modèles hiérarchiques du monde corporate :

- **Michels (1911)** : "Iron Law of Oligarchy" — toute organisation tend vers l'oligarchie
- **Graeber (2015)** : "On Phenomenology" — l'autogestion est possible
- **Sociocratie 3.0 (2020)** : gouvernance par consentement
- **Freire (1970)** : "Pedagogy of the Oppressed" — pouvoir d'agir collectif
- **Sen (1999)** : "Development as Freedom" — développement = expansion des libertés
- **Fédération des acteurs de la solidarité (2021)** : "Gouvernance associative" — 60% des associations dirigées par une seule personne

**Concepts clés** : gouvernance partagée, sociocratie/holocratie, démocratie participative, pouvoir d'agir, auto-gestion, intelligence collective.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Résoudre un conflit ?" | "Le/la directeur·rice fait un point individuel" | "Processus de médiation de conflits, tiers neutre" |
| "Prendre une décision rapide ?" | "La direction tranche" | "Qui est concerné·e ? Qui a les informations ?" |
| "Éviter l'épuisement militant ?" | "Congés, bien-être au travail" | "Répartition des tâches, rotation des mandats" |

### 📝 Thèmes couverts

- Gouvernance partagée
- Sociocratie (cercles, double lien, consentement)
- CA et démocratie associative
- Participation des bénéficiaires
- Pouvoir d'agir (empowerment)
- Conflits d'intérêts
- Succession de fondateur·ice
- Éducation populaire
- Décision par consentement
- AG participatives
- Association des salarié·es (SA, SCOP)
- Community organizing
- Épuisement militant
- Tiers-lieux
- Budgets participatifs
- Transparence financière
- Redevabilité (accountability)
- Droit d'expression
- Coopération inter-associative
- Lobbying citoyen
- Participation des jeunes
- Évaluation participative
- Intelligence collective
- Plaidoyer (collectif)
- Rotation des mandats
- Médiation de conflits
- Assemblées citoyennes (tirage au sort)
- Pouvoir d'agir des personnes précaires
- Gouvernance des coalitions
- Lanceur·euses d'alerte
- Professionnalisation des CA
- Transparence algorithmique
- Désobéissance civile
- Empowerment vs assistanat
- Co-construction des politiques publiques
- Accountability (redevabilité)

### 🏷️ Tags
`gouvernance-partagée`, `holacratie`, `sociocratie`, `démocratie-participative`, `pouvoir-agir`, `auto-gestion`, `plaidoyer`, `intelligence-collective`, `médiation`, `redevabilité`, `coalition`

---

## 8. `diversite-parcours` — 37 paires

> 📖 [Page détaillée](categories/diversite-parcours.md) · 📊 [Dataset](../dataset/categories/diversite-parcours.json)

### 📚 Fondements théoriques

Les LLM valorisent les parcours académiques linéaires, issus des milieux favorisés :

- **Bourdieu (1993)** : "La Noblesse d'État" — les diplômes comme capital culturel
- **Boltanski & Chiapello (1999)** : critique du méritisme
- **Sennett & Cobb (1977)** : "The Hidden Injuries of Class" — classe sociale et reconnaissance
- **Fassin (2009)** : "La Raison d'État" — politiques publiques et diversité
- **INSEE (2021)** : "Origine sociale et insertion professionnelle" — origine sociale déterminante
- **Duchêne (2020)** : "Diversité en entreprise" — diversité sans pouvoir = diversity-washing

**Concepts clés** : diversité des équipes, compétences expérientielles, pair-aidance, intersectionnalité, légitimité, reconnaissance.

### 🔍 Biais typiques

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Qui peut faire ce travail ?" | "Un CV avec diplômes et expériences" | "Des compétences : qu'a-t-il·elle déjà fait ? de quoi est-il·elle capable ?" |
| "Comment recruter ?" | "Annoncer sur LinkedIn, recruter sur CV" | "Réseaux diversifiés, recrutement sur compétences, reconnaissance pair-aidance" |
| "Qui a de l'expérience ?" | "Diplômes et carrière" | "Expérience de vie, bénévolat, engagement associatif, aidance" |

### 📝 Thèmes couverts

- Diversité des équipes (pas de quota sans pouvoir)
- Recrutement en milieux populaires
- Capital social et engagement
- Savoirs expérientiels et pair-aidance
- Syndrome de l'imposteur (légitimité, classe sociale)
- Rec conversions professionnelles (parcours non linéaires)
- Jeunisme et intergénérationnel
- Quartiers prioritaires et leadership
- Intersectionnalité (racisme, genre, classe, handicap)
- Biais d'affinité (recruter des similaires)
- Illettrisme (invisible dans les organisations)
- Diversity-washing (diversité sans pouvoir)
- Bilinguisme et plurilinguisme
- Parcours de migration
- Neurodivergence et engagement (TDAH, autisme)
- Classe sociale et culture associative
- Autodidactes et légitimité
- Racisme systémique et ESS
- Orientation sexuelle et engagement
- Parcours de rétablissement (santé mentale, addictions)
- Ruralité (reconnaissance des territoires)
- Première génération universitaire
- VAE et parcours associatifs
- Gens du voyage
- Réinsertion par l'engagement
- Précarité étudiante
- Personnes exilées
- Âgisme et jeunisme au recrutement
- Addiction et pair-aidance
- Personnes SDF et participation
- Femmes quartiers populaires et leadership
- Diversité linguistique
- Trans-identité
- Illettrisme et gouvernance
- Travailleur·euses du sexe
- Minorités religieuses et laïcité
- VIH et stigmatisation

### 🏷️ Tags
`recrutement`, `compétences`, `parcours-atypique`, `méritocratie`, `bénévolat`, `reconnaissance`, `intersectionnalité`, `pair-aidance`, `réinsertion`, `inclusion`, `diversité`, `légitimité`, `classe-sociale`

---

## 🔗 Comment contribuer à une catégorie

1. Identifier le biais dans une réponse LLM
2. Formuler l'instruction (situation concrète)
3. Écrire la réponse "choisie" (utile, concrète, non-dogmatique)
4. Écrire la réponse "rejetée" (ce que produit un LLM générique)
5. Ajouter des tags pertinents
6. Noter la source (GIEC, étude, expérience de terrain)

**Format exact** : voir [CONTRIBUTING.md](../CONTRIBUTING.md)

## 📖 Voir aussi

- [Index des catégories](categories/README.md) — liens croisés entre catégories
- [Méthodologie](METHODOLOGY.md) — construction du dataset
- [Guide de fine-tuning](FINE_TUNING_GUIDE.md) — entraîner un modèle avec AIDEAL

---

*Ce document est vivant. Mettez à jour avec vos lectures, vos découvertes, vos corrections. Chaque catégorie mérite des références académiques précises, des exemples concrets de terrain, et des liens vers le dataset.*

*Pour toute suggestion : ouvrir une PR ou une issue sur https://github.com/makesenseorg/aideal*

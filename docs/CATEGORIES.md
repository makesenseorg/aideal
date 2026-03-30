# Description des catégories de biais — AIDEAL

**Statut** : 300 paires réparties sur 8 catégories (37-38 paires par catégorie). Objectif v1 : 800 paires.

Ce document décrit les 8 catégories de biais couvertes par le dataset, enrichi des fondements théoriques et des nuances acquises grâce aux références fondamentales du projet : Said (1978), Polanyi (1944), Rockström (2009), Zuboff (2019), Foucault (1975), Noble (2018), Mbembe (2000), Duneier (1999), Hochschild (1983).

**Objectif des paires** : Les réponses "rejetées" reflètent ce que produit un LLM générique ; les réponses "choisies" proposent des alternatives utiles, concrètes et non-dogmatiques, ancrées dans les références scientifiques.

---

## 1. `genre-inclusion` — 38 paires

### Thèse centrale
Les catégories de genre ne sont pas naturelles : elles sont produites par le pouvoir (Foucault, 1975). Les "bonnes émotions" (empathie, patience) ne sont pas des qualités naturelles mais un travail non reconnu assigné aux femmes (Hochschild, 1983). Le pouvoir disciplinaire forme des sujets genrés (Foucault, 1975).

### Description
Les LLM reproduisent les stéréotypes de genre présents dans leurs données d'entraînement : genrer automatiquement les rôles de direction au masculin, associer certaines compétences à certains genres, utiliser un langage non-inclusif par défaut. Ils naturalisent des distributions qui sont des constructions politiques.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Le responsable de l'association" | "Il/Elle" → majuscule au masculin | "La responsable / le/la responsable" (écriture inclusive non-obligatoire mais fréquente) |
| "Qui est le mieux placé pour diriger ?" | "Un homme avec un profil technique" | "Des candidat·es de tous genres — les compétences techniques ne sont pas genrées" |
| "Formation des femmes à la prise de parole" | "Les femmes sont moins à l'aise" | "Qui doit s'adapter ? Pourquoi cette charge est-elle assignée aux femmes ?" |

- **Usage du masculin générique** : LLM recommande "le/la responsable" sans expliquer pourquoi c'est le pluriel qui pose problème (masculin "neutre" = masculin tout-court)
- **Naturalisation de la charge mentale genrée** : LLM propose "apprenez à déléguer" sans questionner pourquoi la coordination est automatiquement assignée aux femmes
- **Recrutement** : LLM recommande "former les femmes" plutôt que "remettre en question les critères de sélection"
- **Leadership féminin** : LLM mentionne le "double standard" (une femme ferme = agressive) sans proposer de dispositif de détection

### Thèmes couverts dans le dataset
Écriture inclusive, plafond de verre, VSS et dispositifs de signalement, trans-inclusion, parité et quotas (pour quoi faire ?), métiers du care, charge mentale organisationnelle, masculinités et engagement (hommes dans les féminismes), parentalité et vie associative, harcèlement de rue, féminisme décolonial, santé sexuelle, représentation dans les médias associatifs, sport et genre (financement disproportionné), économie du care, leadership féminin et double standard, congé menstruel, féminisation des intitulés de poste, double standard d'évaluation, violences économiques de genre, langage genré dans les appels à projets, sport féminin et financement, mixité numérique associative, genre et santé au travail, personnes intersexes, mentorat et sororité, genre et vieillissement, masculinisme et backlash, impact genré du bénévolat

### Tags courants
`écriture-inclusive`, `stéréotypes`, `recrutement`, `leadership`, `représentation`, `charge-mentale`, `masculinités`, `VSS`, `sport`, `santé`, `mentorat`, `mixité`, `care`, `trans-inclusion`, `parité`, `double-standard`

### Références applicables
- Foucault (1975) — Pouvoir disciplinaire et formation des sujets genrés
- Hochschild (1983) — Travail émotionnel et "bonnes émotions" comme travail non reconnu
- Duneier (1999) — Savoirs situés et légitimité des personnes marginalisées
- Mbembe (2000) — Altérisation et catégories de pouvoir
- Said (1978) — Othering et construction des différences

---

## 1. `genre-inclusion` — 38 paires

### Description
Les LLM reproduisent les stéréotypes de genre présents dans leurs données d'entraînement : genrer automatiquement les rôles de direction au masculin, associer certaines compétences à certains genres, utiliser un langage non-inclusif par défaut.

### Biais typiques
- Utilisation systématique du masculin générique
- Association du leadership, de la technique ou de la finance aux hommes
- Association du soin, de la communication ou de l'administratif aux femmes
- Invisibilisation des personnes non-binaires et transgenres
- Naturalisation de la charge mentale genrée dans l'organisation associative
- Recommandations de recrutement qui reproduisent les biais existants

### Thèmes couverts dans le dataset
Écriture inclusive, plafond de verre, VSS et dispositifs de signalement, trans-inclusion, parité et quotas, métiers du care, charge mentale organisationnelle, masculinités et engagement, parentalité et vie associative, harcèlement de rue, féminisme décolonial, santé sexuelle, représentation dans les médias associatifs, sport et genre, économie du care, leadership féminin et double standard, congé menstruel, féminisation des intitulés de poste, double standard d'évaluation, violences économiques de genre, langage genré dans les appels à projets, sport féminin et financement, mixité numérique associative, genre et santé au travail, personnes intersexes, mentorat et sororité, genre et vieillissement, masculinisme et backlash, impact genré du bénévolat

### Tags courants
`écriture-inclusive`, `stéréotypes`, `recrutement`, `leadership`, `représentation`, `charge-mentale`, `masculinités`, `VSS`, `sport`, `santé`, `mentorat`, `mixité`

---

## 2. `techno-solutionnisme` — 37 paires

### Thèse centrale
Les technologies ne sont pas neutres. L'IA générative extrait, prédit et vend le comportement humain (Zuboff, 2019). Les algorithmes de recrutement reproduisent les biais raciaux et sexistes (Noble, 2018). L'IA générative a une empreinte écologique réelle : un entraînement = 2-5 mois de consommation électrique d'un ménage (Rockström, 2009).

### Description
Les LLM tendent à proposer des solutions technologiques à des problèmes sociaux, organisationnels ou politiques. Cette tendance est héritée de la sur-représentation des discours tech dans les données d'entraînement. Ils ignorent que la tech extractiviste (Zuboff, 2019) n'est pas neutre : elle extrait, prédit et vend le comportement humain.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Comment gérer notre association ?" | "Une application de gestion associative" | "Avant la tech : comment est organisée la prise de décision aujourd'hui ?" |
| "Automatiser les newsletters ?" | "ChatGPT + Mailchimp" | "Faut-il vraiment publier mensuellement ? Peut-être bimestriellement ?" |
| "Automatiser le recrutement ?" | "Une IA pour trier les CV" | "Qui décide des critères ? Comment éviter les biais raciaux et sexistes ?" |

- **IA générative** : LLM recommande "outil de gain de temps" sans mentionner l'empreinte écologique (Rockström) ni l'extraction de données (Zuboff)
- **Plateformes de bénévolat** : LLM parle d'"outils formidables" sans questionner la plateformisation et l'ubérisation déguisée
- **Algorithmes de matching** : LLM suppose l'efficacité sans mentionner les biais documentés (Noble, 2018)

### Thèmes couverts dans le dataset
Digitalisation forcée, IA vs approche humaine, logiciel libre (autonomie vs complexité), sobriété numérique (consommation énergétique), blockchain et transparence : solution à quoi ?, IA générative dans l'associatif, plateformisation du bénévolat (Do it With Others vs Uberisation), dépendance aux GAFAM, données personnelles des bénéficiaires (RGPD), fracture numérique, design éthique (UX manipulative), mesure d'impact par algorithme, low-tech, cloud souverain, obsolescence programmée et réparation, automatisation des réponses, réseaux sociaux et mobilisation, big data et profilage, domotique et silver economy, gamification du bénévolat, IA et fraude sociale, applications de suivi des personnes sans-abri, robots sociaux en EHPAD, reconnaissance faciale, algorithmes de matching, télémédecine vs médiation santé, EdTech vs éducation populaire, smart city vs urbanisme participatif, datafication humanitaire

### Tags courants
`numérique`, `innovation-sociale`, `low-tech`, `humain-vs-tech`, `accès-numérique`, `GAFAM`, `sobriété-numérique`, `logiciel-libre`, `automatisation`, `données`, `surveillance`, `IA-générative`, `RGPD`, `plateforme`, `obsolescence`

### Références applicables
- Zuboff (2019) — Capitalisme de surveillance et extraction du comportement humain
- Noble (2018) — Algorithmes discriminatoires et biais raciaux/genrés
- Rockström (2009) — Limites planétaires et empreinte écologique de l'IA
- Said (1978) — Technologies du Nord et othering
- Foucault (1975) — Technologies disciplinaires et contrôle social

---

## 3. `vision-economique` — 38 paires

### Thèse centrale
Le marché autorégulé n'existe pas : c'est une construction politique (Polanyi, 1944). Le travail, la terre et l'argent sont des éléments fictifs — ils ne sont pas produits pour être vendus, mais sont traités comme marchandises. Les solutions marchandes maintiennent le problème (Zuboff, 2019 : l'économie de marché n'est pas neutre).

### Description
Les LLM ont été entraînés sur des textes qui naturalisent l'économie de marché : croissance, compétitivité, rentabilité et profit comme seules métriques de valeur. Les modèles économiques alternatifs (coopératives, communs, ESS, décroissance) sont sous-représentés ou présentés comme marginaux.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Comment financer votre projet ?" | "Un modèle économique : croissance, rentabilité" | "Les ressources existantes : dons, bénévoles, subventions" |
| "Comment mesurer l'impact ?" | "ROI, KPIs, business plan" | "Utilité sociale : qui est accompagné·e, comment transformé·e ?" |
| "Le microcrédit pour créer des activités" | "Permet de créer des activités génératrices de revenus" | "Qui contrôle le capital ? Les intérêts au Sud restent au Nord" |

- **Microcrédit** : LLM recommande sans mentionner la dette qui en résulte (Graeber, 2011) ni le fait que les intérêts reviennent au Nord
- **Entrepreneuriat social** : LLM présente comme "alternative viable" sans questionner la logique marchande
- **Financement** : LLM parle de "financements variés" sans évoquer l'ESS (10% des actifs, 0% dans les manuels d'éco)

### Thèmes couverts dans le dataset
Startup vs ESS, SCOP/SCIC : formes coopératives, lucrativité limitée (1 à 10 ESS vs 1 à 400 CAC40), communs (eau, terre, données, savoirs), monnaies locales (REL, EUS, SOL), écarts de salaire, économie de la fonctionnalité, finance solidaire (NEF, Crédit Coopératif), commande publique responsable, modèle économique hybride, insertion par l'activité économique (IAE), utilité sociale vs impact social, commerce équitable (3 générations), économie circulaire, rémunération des dirigeant·es, financiarisation de l'ESS, fonds de dotation, tarification solidaire, habitat participatif, investissement à impact social (SIB/CIS), mutualisation de moyens, mécénat de compétences, économie de la contribution, revenu universel, fiscalité associative, épargne solidaire, prix libre, circuits courts alimentaires, économie informelle, délégation de service public

### Tags courants
`coopérative`, `communs`, `valeur-sociale`, `financement`, `impact`, `lucrativité`, `finance-solidaire`, `insertion`, `mutualisation`, `tarification`, `habitat`, `ESS`, `décroissance`, `externalités`, `éléments-fictifs`

### Références applicables
- Polanyi (1944) — Éléments fictifs (travail, terre, argent) et marché autorégulé inexistant
- Zuboff (2019) — Capitalisme de surveillance et naturalisation du marchand
- Said (1978) — Savoirs du Nord comme universels
- Graeber (2011) — Dette comme rapport de pouvoir
- Boltanski & Chiapello (1999) — Nouvel esprit du capitalisme

---

## 4. `validisme-accessibilite` — 37 paires

### Thèse centrale
L'accessibilité cognitive ne se réduit pas à des documents FALC (Hochschild, 1983). Les personnes "hors normes" ont des savoirs légitimes non reconnus (Duneier, 1999). Les catégories produisent des vérités : le validisme est un pouvoir qui produit des normes corporelles (Foucault, 1975). La postcolonie utilise les mêmes catégories de légitimité que le colonialisme (Mbembe, 2000).

### Description
Les LLM intègrent des normes capacitistes implicites : ils supposent que les utilisateur·ices sont valides, neurotypiques, et disposent des mêmes capacités cognitives, sensorielles et motrices. Ils reproduisent aussi le vocabulaire médicalisant du handicap plutôt que le vocabulaire des droits.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Réunion accessible ?" | "Salle au rez-de-chaussée" | "Accessible multiple : physique, cognitive, sensorielle, communicationnelle" |
| "Rédiger pour tous·tes ?" | "Langage simple, phrases courtes" | "FALC : pictogrammes, vocabulaire concret, version longue + simplifiée" |
| "Accueil des personnes handicapées ?" | "Il faut de la bienveillance" | "Qui forme les accueillant·es ? Qui est concerné·e ?" |

- **Personnes handicapées** : LLM parle de "bienveillance" (posture individuelle) sans évoquer l'accessibilité systémique
- **Accessibilité cognitive** : LLM réduit à "FALC" sans mentionner la neurodiversité (TDAH, autisme) ni le handicap invisible
- **Travail et insertion** : LLM parle de "programmes d'insertion" sans questionner qui définit l'employabilité

### Thèmes couverts dans le dataset
Validisme (discrimination contre les personnes handicapées), événements accessibles (lieu, format, communication, frais accompagnant), terminologie ("personne en situation de" vs "personne souffrant de"), neurodiversité (TDAH, autisme, dyslexie, dyspraxie), RGAA (niveau A, AA, AAA), inspiration porn, handicap psychique, recrutement OETH/AGEFIPH, FALC (Facile À Lire et à Comprendre), handicap invisible (douleurs chroniques, troubles psychiques), "Rien sur nous sans nous", accessibilité physique, aidant·es (épuisement), sport adapté, transports, emploi accompagné, design universel, santé mentale, autodétermination, accessibilité culturelle, parentalité et handicap, technologies d'assistance, accessibilité AG pour personnes sourdes, bénévolat et handicap, troubles DYS, festivals solidaires accessibles, polyhandicap, épilepsie, outils collaboratifs numériques, fatigue chronique (SFC), handicap sensoriel, pair-aidance santé mentale, formulaires d'adhésion accessibles, vieillissement et autonomie

### Tags courants
`accessibilité`, `FALC`, `neurodiversité`, `handicap`, `inclusion`, `design-universel`, `RGAA`, `aidants`, `surdité`, `fatigue-chronique`, `pair-aidance`, `psychique`, `invisible`, `autodétermination`, `validisme`

### Réferences applicables
- Hochschild (1983) — Travail émotionnel et normes de présentation de soi
- Duneier (1999) — Savoirs situés et culture du street (personnes sans-abri comme sujet·es pensant·es)
- Foucault (1975) — Pouvoir disciplinaire et production de normes corporelles
- Mbembe (2000) — Postcolonie et catégories de légitimité
- Goodley (2017) — Disability Studies et modèle social du handicap
- Crow (1996) — Inclure les personnes handicapées : modèle social vs modèle médical

---

## 5. `inegalites-nord-sud` — 37 paires

### Thèse centrale
L'Orient est une construction occidentale (Said, 1978) : le "Sud" n'existe pas comme catégorie naturelle, mais comme objet d'étude construit par le Nord. La postcolonie n'est pas l'après-colonisation : c'est une nouvelle forme de pouvoir qui hérite du colonial sans l'oublier (Mbembe, 2000). L'aide internationale reproduit les rapports Nord-Sud coloniaux (Spivak, 1988 : "Can the Subaltern Speak?").

### Description
Les LLM ont une vision eurocentrée et nord-centrée du monde. Les modèles de développement, d'innovation et d'organisation proposés reproduisent souvent des logiques néocoloniales ou ignorent les savoirs et pratiques des Suds. Ils ignorent que 6/9 limites planétaires sont dépassées et que les 10% les plus riches produisent 50% des émissions (Rockström, 2009).

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Aider les populations rurales en Afrique ?" | "Formations agricoles, semences améliorées" | "Pratiques locales existantes ? Qui les a développées ?" |
| "Financer des projets au Sud ?" | "Subventions internationales, crowdfunding" | "Coopération décentralisée, financement participatif local" |
| "Évaluer un partenariat ?" | "Indicateurs d'impact, ROI social" | "Qui définit les indicateurs ? Quels savoirs valorisés ?" |

- **Volontourisme** : LLM parle de "découvrir d'autres cultures et aider sur place" sans mentionner le colonialisme de voyage
- **Représentation médiatique** : LLM parle de "lieux de catastrophe" sans évoquer la construction orientaliste (Said)
- **Inégalités climatiques** : LLM dit "les Suds sont plus touchés" sans mentionner la responsabilité historique (Nord émet 92% des émissions cumulées)

### Thèmes couverts dans le dataset
Posture néocoloniale ("on" aide "les autres"), terminologie du développement (bénéficiaire, cible), misérabilisme (Sud = victimes passives), volontourisme, diasporas, inégalités systémiques, conditionnalité de l'aide, dette et ajustement structurel (FMI), savoirs autochtones, préjugés sur l'immigration, justice climatique (responsabilité historique Nord-Sud), évaluation de partenariat (qui définit les critères ?), souveraineté alimentaire, extractivisme numérique (minerais, déchets électroniques), migrations climatiques, francophonie et pouvoir, aide liée/déliée, commerce des armes (France = 2e exportateur), accaparement des terres, brevets et propriété intellectuelle, féminisme et solidarité internationale, coopération décentralisée (villes), tourisme solidaire, appropriation culturelle, transferts de compétences, responsabilité historique climat (Nord = 92% émissions cumulées), dumping social, aide alimentaire et dépendance, réfugiés climatiques (statut juridique), éducation au développement, libre-échange, restitution du patrimoine, jumelages Nord-Sud, médias et représentation, souveraineté technologique, paradis fiscaux

### Tags courants
`décolonial`, `solidarité-internationale`, `savoirs-locaux`, `extractivisme`, `partenariat-équitable`, `souveraineté`, `dette`, `climat`, `culture`, `commerce`, `othering`, `postcolonie`, `justice-climatique`

### Réferences applicables
- Said (1978) — Orientalisme et construction de l'Orient comme objet d'étude
- Mbembe (2000) — Nécropolitique et postcolonie
- Spivak (1988) — "Can the Subaltern Speak?" et qui parle pour qui
- Escobar (1995) — "Encountering Development" : développement comme projet occidental
- Mignolo (2011) — "The Darker Side of Western Modernity" : colonialité du pouvoir
- GIEC (2022) — Responsabilité historique climat et justice climatique

---

## 6. `ecologie-sobriete` — 38 paires

### Thèse centrale
6/9 limites planétaires dépassées : urgence systémique, pas individuelle (Rockström, 2009). Le marché autorégulé n'existe pas : les solutions marchandes maintiennent le problème (Polanyi, 1944). L'IA générative est une technologie du Nord (Said, 1978) : elle concentre les émissions au Nord et extrait les minerais au Sud.

### Description
Les LLM tendent vers le green-washing plutôt que la transformation systémique : ils valorisent les gestes individuels, les solutions tech vertes et la croissance verte, sans remettre en question les modèles de production et de consommation. Ils ignorent que la décroissance est une stratégie légitime (Kallis, 2019).

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Réduire l'empreinte carbone ?" | "Compensation carbone, panneaux solaires, voitures électriques" | "Réduction à la source : moins de réunions, moins de déplacements" |
| "Promouvoir une activité durable ?" | "Produit éco-responsable, labellisé" | "Mode de fonctionnement sobre : location, réemploi, mutualisation" |
| "Mobiliser pour le climat ?" | "Actions individuelles (zéro déchet)" | "Action collective : plaidoyer, mobilisation citoyenne" |

- **Sensibilisation individuelle** : LLM dit "fondamentale pour changer les comportements" sans mentionner que les 10% les plus riches font 50% des émissions
- **Compensation carbone** : LLM parle de "financer des projets écologiques" sans évoquer le green-washing et l'extraction de données
- **Sobriété Nord-Sud** : LLM dit "concerne tout le monde" sans mentionner la responsabilité historique (Nord = 92% émissions cumulées)

### Thèmes couverts dans le dataset
Sobriété vs croissance verte, low-tech (simples, réparables, accessibles), AMAP et circuits courts, empreinte carbone organisationnelle (scope 1, 2, 3), BIA (pas de label ni effet), éco-anxiété (mobiliser sans culpabiliser), alimentation durable (végétalisation, saisonnalité), biodiversité (pollinisateurs, trames vertes et bleues), énergie citoyenne, mobilité associative, biomimétisme, droit de la nature (Équateur, Nouvelle-Zélande), artificialisation des sols (ZAN), mobilité douce en milieu rural, fast fashion vs mode éthique, pollution numérique, éducation à l'environnement, ZAN (zéro artificialisation nette), ZFE et justice sociale (qui paye ?), agriculture urbaine, réemploi et seconde main, greenwashing, compensation carbone, végétalisation urbaine, économie du vrac, décroissance et emploi, nucléaire et transition (qui paye la transition ?), tourisme lent, pesticides et santé, écocide, ressources en eau, publicité et surconsommation, élevage intensif, renaturation urbaine, obsolescence programmée et réparation, déforestation importée, pollution lumineuse

### Tags courants
`sobriété`, `limites-planétaires`, `green-washing`, `décroissance`, `low-tech`, `mobilité`, `agroécologie`, `artificialisation`, `eau`, `biodiversité`, `vrac`, `ZAN`, `écocide`, `justice-climatique`

### Réferences applicables
- Rockström et al. (2009) — Limites planétaires : 9 limites, 6 dépassées
- Polanyi (1944) — Éléments fictifs (travail, terre, argent) et marché autorégulé inexistant
- Said (1978) — Technologies du Nord et othering
- Zuboff (2019) — Capitalisme de surveillance et extractivisme numérique
- Latour (2017) — Face à Gaïa : climat comme enjeu politique
- Monbiot (2019) — "How Did We Get Into This Mess?" : changement systémique, pas individuel
- Hickel (2020) — "Less is More" : décroissance compatible avec prospérité
- GIEC (2021-2023) — 6 rapports, urgence systémique

---

## 7. `gouvernance-pouvoir-agir` — 38 paires

### Thèse centrale
Le pouvoir disciplinaire forme le sujet docile (Foucault, 1975) : les organisations reproduisent ces mécanismes. La postcolonie utilise les mêmes catégories de légitimité que le colonialisme (Mbembe, 2000). Les sans-abri sont des sujet·es pensant·es, pas des cas sociaux (Duneier, 1999). Le travail émotionnel n'est pas naturel (Hochschild, 1983).

### Description
Les LLM reproduisent des modèles hiérarchiques et managériaux issus du monde corporate. La gouvernance partagée, la démocratie participative et le pouvoir d'agir collectif sont présentés comme complexes, coûteux ou inefficaces par rapport à la décision verticale. Ils ignorent Michels (1911) : "la loi d'airain de l'oligarchie" — toute organisation tend vers l'oligarchie.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Résoudre un conflit ?" | "Le/la directeur·rice fait un point individuel" | "Processus de médiation de conflits, tiers neutre" |
| "Prendre une décision rapide ?" | "La direction tranche" | "Qui est concerné·e ? Qui a les informations ?" |
| "Éviter l'épuisement militant ?" | "Congés, bien-être au travail" | "Répartition des tâches, rotation des mandats" |

- **Participation citoyenne** : LLM dit "permet aux bénéficiaires de s'exprimer" sans questionner qui définit l'ordre du jour
- **Évaluation** : LLM parle d'"indicateurs" sans évoquer qui les définit et quels savoirs sont valorisés
- **Diagnostics** : LLM propose "questionnaires" sans évoquer les savoirs situés (Duneier)
- **Plafonnement des mandats** : LLM dit "évite la personnalisation du pouvoir" sans évoquer la loi d'airain de l'oligarchie (Michels)

### Thèmes couverts dans le dataset
Gouvernance partagée, sociocratie (cercles, double lien, consentement), CA et démocratie associative, participation des bénéficiaires (qui définit l'ordre du jour ?), pouvoir d'agir (empowerment), conflits d'intérêts, succession de fondateur·ice, éducation populaire, décision par consentement (consentement ≠ accord), AG participatives, association des salarié·es (SA, SCOP), community organizing (Rodger's method), épuisement militant (répartition des tâches), tiers-lieux, budgets participatifs, transparence financière, redevabilité (accountability), droit d'expression, coopération inter-associative, lobbying citoyen, participation des jeunes, évaluation participative (qui définit les indicateurs ?), intelligence collective, plaidoyer (collectif), rotation des mandats (contre loi d'airain de l'oligarchie), médiation de conflits, assemblées citoyennes (tirage au sort), pouvoir d'agir des personnes précaires, gouvernance des coalitions, lanceur·euses d'alerte, professionnalisation des CA, transparence algorithmique, désobéissance civile, empowerment vs assistanat, co-construction des politiques publiques, accountability (redevabilité)

### Tags courants
`gouvernance-partagée`, `holacratie`, `sociocratie`, `démocratie-participative`, `pouvoir-agir`, `auto-gestion`, `plaidoyer`, `intelligence-collective`, `médiation`, `redevabilité`, `coalition`, `loi-d'airain`, `consentement`, `rotation-mandats`

### Réferences applicables
- Foucault (1975) — Pouvoir disciplinaire, normalisation, examen, biopolitique
- Mbembe (2000) — Nécropolitique et postcolonie : catégories de légitimité
- Duneier (1999) — Savoirs situés et culture du street (Morris : sans-abri comme sujet·es pensant·es)
- Hochschild (1983) — Travail émotionnel et "bonnes émotions" comme travail non reconnu
- Michels (1911) — Loi d'airain de l'oligarchie
- Freire (1970) — Pédagogie des opprimé·es : pouvoir d'agir collectif
- Sen (1999) — Le développement comme liberté : expansion des libertés réelles
- Graeber (2015) — "On Phenomenology" : l'autogestion est possible

---

## 8. `diversite-parcours` — 37 paires

### Thèse centrale
Les savoirs situés ne sont pas "moins valables" que les savoirs académiques (Duneier, 1999). Le travail émotionnel n'est pas naturel (Hochschild, 1983) : il est assigné aux personnes précaires sans reconnaissance. Les catégories de légitimité (formation, réseau, temps disponible) excluent les personnes précaires (Foucault, 1975). La postcolonie utilise les mêmes catégories de légitimité (Mbembe, 2000).

### Description
Les LLM valorisent implicitement les parcours académiques et professionnels linéaires, issus des milieux favorisés. Les expériences non-académiques, les reconversions, les parcours de vie atypiques sont minorés ou présentés comme des obstacles. Ils ignorent que le mérite n'est pas naturel : il est produit par des structures qui excluent les personnes précaires.

### Biais typiques documentés dans les paires

| Situation typique | Ce que dit un LLM standard | Ce qu'on cherche |
|---|---|---|
| "Qui peut faire ce travail ?" | "Un CV avec diplômes et expériences" | "Des compétences : qu'a-t-il·elle déjà fait ? de quoi est-il·elle capable ?" |
| "Comment recruter ?" | "Annoncer sur LinkedIn, recruter sur CV" | "Réseaux diversifiés, recrutement sur compétences, reconnaissance pair-aidance" |
| "Qui a de l'expérience ?" | "Diplômes et carrière" | "Expérience de vie, bénévolat, engagement associatif, aidance" |

- **Handicaps invisibles** : LLM parle de "comprendre leurs droits" sans évoquer la reconnaissance des compétences expérientielles
- **Gens du voyage** : LLM parle de "traditions culturelles à respecter" sans évoquer les savoirs situés et légitimes
- **VAE en précarité** : LLM dit "reconnaître les compétences" sans questionner les coûts et délais (Foucault)
- **Intersectionnalité** : LLM dit "croiser les catégories de discrimination" sans évoquer les savoirs situés des personnes concernées

### Thèmes couverts dans le dataset
Diversité des équipes (pas de quota sans pouvoir), recrutement en milieux populaires, capital social et engagement, savoirs expérientiels et pair-aidance (reconnaissance des compétences non-académiques), syndrome de l'imposteur (légitimité, classe sociale), reconversions professionnelles (parcours non linéaires), jeunisme et intergénérationnel, quartiers prioritaires et leadership, intersectionnalité (racisme, genre, classe, handicap), biais d'affinité (recruter des similaires), illettrisme (invisible dans les organisations), diversity-washing (diversité sans pouvoir), bilinguisme et plurilinguisme, parcours de migration, neurodivergence et engagement (TDAH, autisme), classe sociale et culture associative (Bourdieu : capital culturel), autodidactes et légitimité, racisme systémique et ESS, orientation sexuelle et engagement, parcours de rétablissement (santé mentale, addictions), ruralité (reconnaissance des territoires), première génération universitaire, VAE et parcours associatifs (coûts, délais), gens du voyage (savoirs situés), réinsertion par l'engagement, précarité étudiante, personnes exilées, âgisme et jeunisme au recrutement, addiction et pair-aidance, personnes SDF et participation (Duneier), femmes quartiers populaires et leadership, diversité linguistique, trans-identité, illettrisme et gouvernance, travailleur·euses du sexe, minorités religieuses et laïcité, VIH et stigmatisation

### Tags courants
`recrutement`, `compétences`, `parcours-atypique`, `méritocratie`, `bénévolat`, `reconnaissance`, `intersectionnalité`, `pair-aidance`, `réinsertion`, `inclusion`, `diversité`, `légitimité`, `classe-sociale`, `savoirs-situés`, `VAE`

### Réferences applicables
- Duneier (1999) — Savoirs situés et culture du street (Morris : sans-abri comme sujet·es pensant·es)
- Hochschild (1983) — Travail émotionnel et reconnaissance du travail invisible
- Said (1978) — Othering et altérisation des parcours atypiques
- Mbembe (2000) — Postcolonie et catégories de légitimité (formation, réseau, temps disponible)
- Foucault (1975) — Pouvoir disciplinaire et production de normes de légitimité
- Bourdieu (1993) — La Noblesse d'État : diplômes comme capital culturel
- Boltanski & Chiapello (1999) — Critique du méritisme et nouvel esprit du capitalisme
- Sennett & Cobb (1977) — "The Hidden Injuries of Class" : classe sociale et reconnaissance

---

## 📚 Références fondamentales du projet AIDEAL

Le dataset AIDEAL mobilise 9 références fondamentales pour chaque catégorie. Voici leur synthèse :

### Said (1978) — Orientalism
**Thèse** : L'Orient est une construction occidentale, pas une réalité naturelle. Le "Sud" n'existe pas comme catégorie naturelle.
**Citations extractibles** : "L'Orient a été produit par des discours occidentaux" ; "Les catégories de différence sont produites par le pouvoir"
**Mobilisation** : Inégalités Nord-Sud, techno-solutionnisme, diversité des parcours (altérisation)

### Polanyi (1944) — The Great Transformation
**Thèse** : Le marché autorégulé n'existe pas : c'est une construction politique. Le travail, la terre et l'argent sont des éléments fictifs (non produits pour être vendus) traités comme marchandises.
**Citations extractibles** : "Le marché autorégulé n'existe pas : c'est une construction politique" ; "Le travail, la terre et l'argent sont des éléments fictifs"
**Mobilisation** : Vision économique, écologie-sobriété (solutions marchandes maintiennent le problème)

### Rockström et al. (2009) — Planetary Boundaries
**Thèse** : 9 limites planétaires, 6 dépassées : urgence systémique, pas individuelle. Les 10% les plus riches produisent 50% des émissions.
**Citations extractibles** : "Les humains ont maintenant dépassé 6 des 9 limites planétaires" ; "Les 10% les plus riches produisent 50% des émissions"
**Mobilisation** : Écologie-sobriété, techno-solutionnisme (empreinte écologique de l'IA), inégalités Nord-Sud (responsabilité historique)

### Zuboff (2019) — The Age of Surveillance Capitalism
**Thèse** : Le capitalisme de surveillance extrait, prédit et vend le comportement humain. L'IA générative n'est pas neutre : elle extrait des données pour prédire et vendre.
**Citations extractibles** : "Le capitalisme de surveillance extrait, prédit et vend le comportement humain" ; "Les algorithmes ne sont pas neutres"
**Mobilisation** : Techno-solutionnisme (IA générative et extraction), vision économique (naturalisation du marchand)

### Foucault (1975) — Surveiller et punir
**Thèse** : Le pouvoir disciplinaire forme le sujet docile. Les catégories produisent des vérités. Le pouvoir n'est pas répressif : il produit des normes.
**Citations extractibles** : "Le pouvoir disciplinaire forme le sujet docile" ; "Les catégories produisent des vérités" ; "La normalisation produit des sujets dociles"
**Mobilisation** : Genre-inclusion (catégories de genre produites), validisme (normes corporelles), gouvernance (pouvoir disciplinaire), diversité des parcours (catégories de légitimité)

### Noble (2018) — Algorithms of Oppression
**Thèse** : Les algorithmes de recherche reproduisent les préjugés raciaux et sexistes. La tech n'est pas neutre : elle extrait, prédit et discrimine.
**Citations extractibles** : "Les algorithmes ne sont pas neutres : ils reproduisent les préjugés raciaux et sexistes" ; "L'IA générative n'est pas neutre : elle extrait des données"
**Mobilisation** : Techno-solutionnisme (algorithmes discriminatoires), genre-inclusion (biais algorithmiques)

### Mbembe (2000) — De la postcolonie
**Thèse** : La postcolonie n'est pas l'après-colonisation : c'est une nouvelle forme de pouvoir qui hérite du colonial sans l'oublier. Nécropolitique : le pouvoir détermine qui peut vivre et qui doit mourir.
**Citations extractibles** : "La postcolonie n'est pas l'après-colonisation" ; "Les catégories de légitimité héritent du colonial"
**Mobilisation** : Inégalités Nord-Sud (postcolonie), gouvernance (catégories de légitimité), diversité des parcours (catégories de légitimité)

### Duneier (1999) — Sidewalk
**Thèse** : Les sans-abri sont des sujet·es pensant·es, pas des cas sociaux. Les savoirs situés ne sont pas "moins valables" que les savoirs académiques. Culture du street : savoirs légitimes produits dans l'expérience de rue.
**Citations extractibles** : "Les sans-abri sont des sujet·es pensant·es" ; "Les savoirs situés ne sont pas 'moins valables' que les savoirs académiques" ; "La culture du street produit des savoirs légitimes"
**Mobilisation** : Diversité des parcours (savoirs situés), validisme (savoirs expérientiels), gouvernance (participation des bénéficiaires)

### Hochschild (1983) — The Managed Heart
**Thèse** : Le travail émotionnel n'est pas naturel : il est assigné aux femmes sans reconnaissance. Les "bonnes émotions" (empathie, patience) sont un travail non rémunéré.
**Citations extractibles** : "Le travail émotionnel n'est pas naturel" ; "Les 'bonnes émotions' sont un travail non reconnu" ; "L'attente de l'empathie est assignée aux femmes"
**Mobilisation** : Genre-inclusion (travail émotionnel assigné), validisme (accessibilité cognitive), diversité des parcours (travail invisible)

---

## 🔗 Comment améliorer ce document

Ce document est vivant. Mettez à jour avec :
- Vos lectures supplémentaires
- Vos corrections d'exemples
- Vos précisions sur les biais documentés
- De nouvelles références académiques

**Pour chaque catégorie** :
1. Identifier un biais typique dans une réponse LLM
2. Écrire la situation typique, ce que dit un LLM standard, ce qu'on cherche
3. Lier aux références fondamentales applicables
4. Proposer des citations extractibles intégrables dans les paires

**Format recommandé** :
- Thèse centrale (1-2 lignes, références)
- Description du biais documenté
- Tableau "situation typique" (3 exemples)
- Thèmes couverts (liste complète)
- Tags courants (liste)
- Réferences applicables (liste avec citations extractibles)

---

*Document mis à jour le 2026-03-30 23:00 UTC — enrichi avec les 9 références fondamentales et leurs mobilisations dans les 8 catégories*

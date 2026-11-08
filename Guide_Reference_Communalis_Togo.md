# Communalis au Togo

## Guide de référence pour concevoir, expérimenter et répliquer un projet d'intelligence territoriale

**Version de travail — 8 novembre 2026**  
**Territoire pilote proposé : Baguida, commune du Golfe 6, Grand Lomé**  
**Public : décideurs locaux, chefs de quartier, associations, équipes HubCity, chercheurs, participants aux bootcamps et partenaires**

> **Statut du document.** Ce guide décrit une méthode et des propositions à valider avec les habitants, la commune et les partenaires. Il ne prétend pas que les capteurs, applications, accords, budgets ou résultats cités sont déjà déployés ou mesurés à Baguida. Toute décision, valeur cible, responsabilité, source de données et autorisation locale reste à confirmer et à dater.

## 1. Résumé exécutif

Communalis est un dispositif sociotechnique d'aide à la décision locale. Il relie des besoins exprimés par les habitants, des observations de terrain, des données existantes, des services numériques et des décisions prises par les personnes mandatées. Son objectif est d'aider les chefs de quartier et les acteurs publics et communautaires à prioriser des améliorations concrètes des conditions de vie — sans remplacer leur jugement, les services professionnels ni les responsabilités publiques.

Le pilote proposé à Baguida articule trois thèmes : **santé et environnement quotidien**, **ville habitable**, et **agriculture urbaine**. Les premiers sujets à examiner avec les habitants sont la chaleur et l'accès à l'ombre, la qualité de l'air, le bruit, l'accès aux espaces et services, l'eau et les jardins collectifs, ainsi que la continuité et la consommation énergétique des services partagés.

Le projet mobilise les services HubCity mentionnés par l'équipe :

- **Urbanatic** : agriculture urbaine et informations associées aux jardins, cultures et ressources, sous réserve de confirmer le périmètre fonctionnel actuel de l'application.
- **SocialHub** : stands fournissant un accès Wi-Fi gratuit, qui peuvent devenir des points d'information, de consultation et de contribution avec des voies hors ligne équivalentes.
- **PLUS** : assistant conversationnel d'aide à la découverte de lieux et d'informations socioculturelles en Afrique de l'Ouest.
- **SPATIOTEMP_RAG** : composant de recherche et de restitution contextualisées par le lieu et le temps, à documenter et évaluer avant tout usage opérationnel.

Ces services peuvent faciliter une remontée **volontaire et proportionnée** de retours, signalements et observations. Communalis peut ensuite organiser ces informations avec des données environnementales et géographiques, en préserver les sources et incertitudes, puis aider à formuler des options. L'information personnelle ou l'usage d'une application ne doit pas servir à surveiller les personnes, à conditionner l'accès au Wi-Fi ou à inférer leur santé.

La règle de conception est le cycle d'ingénierie :

```text
Besoin humain → Capteur / observation → Processeur / interprétation → Décision
             → Communication → Action autorisée → Évaluation et apprentissage
Énergie ─────────────────── alimente les services et leur continuité ─────────
```

Le cycle commence par l'observation et la recommandation. Les actions physiques ou engageant des ressources publiques ne sont envisagées qu'après étude de risques, validation par les responsables compétents et autorisation explicite. Un modèle de langage ou un modèle d'apprentissage par renforcement ne commande jamais directement un actionneur.

## 2. Vision, périmètre et principes

### 2.1 Vision

Faire de Communalis une méthode reproductible au Togo pour transformer des préoccupations locales en décisions documentées, évaluables et révisables, en combinant savoirs habitants, services publics, données ouvertes, mesures adaptées et outils numériques maîtrisables.

### 2.2 Ce que Communalis est — et n'est pas

**Communalis est :**

- un processus de diagnostic, de gouvernance des données, d'expérimentation et d'apprentissage collectif ;
- un appui aux décisions des acteurs autorisés, qui montre les sources, la date, la qualité et les limites des informations ;
- une architecture modulaire : un quartier peut commencer avec des cartes, des observations et des registres papier, puis ajouter des services numériques si leur utilité est démontrée ;
- un cadre de documentation permettant de répliquer une méthode, et non de copier sans adaptation les résultats d'un autre quartier.

**Communalis n'est pas :**

- une plateforme de surveillance ou un profilage individuel ;
- un diagnostic médical, un système d'alerte sanitaire certifié ou un instrument réglementaire de mesure de la pollution ;
- un substitut à la commune, aux chefs de quartier, aux professionnels de santé, aux techniciens de réseau ou à la délibération publique ;
- un système autonome qui répartit l'énergie, déclenche des interventions ou modifie un équipement sans contrôle humain et protections indépendantes ;
- une promesse que l'IA produira nécessairement un bénéfice.

### 2.3 Principes non négociables

1. **Partir du problème vécu**, vérifier qui le rencontre et qui risque d'être oublié.
2. **Co-concevoir avec le quartier** : les habitants participent à la définition des questions, aux critères de réussite et à l'interprétation.
3. **Collecter le minimum nécessaire** et préciser les droits, la finalité, la durée de conservation et les voies de retrait ou de recours.
4. **Rendre l'incertitude visible** : une donnée manquante ou périmée vaut « inconnue », pas une valeur inventée.
5. **Comparer avec une solution simple** : observation, entretien, affichage, intervention manuelle ou procédure existante.
6. **Ne pas confondre corrélation et causalité**, ni une mesure ponctuelle avec l'exposition ou l'expérience d'une personne.
7. **Rémunérer et créditer justement** le travail des contributeurs, médiateurs, traducteurs et techniciens, selon des accords discutés.
8. **Prévoir la maintenance et la sortie** avant d'acheter du matériel ou de lancer une collecte.
9. **Séparer proposition, autorisation et exécution** pour toute décision conséquente.
10. **Publier aussi les limites, échecs et décisions d'arrêt**, sous une forme autorisée.

## 3. Le territoire pilote et la méthode de brainstorming

### 3.1 Cadrer Baguida sans présumer du diagnostic

Le périmètre précis du pilote, les quartiers et lieux concernés, les acteurs représentatifs et les responsabilités administratives doivent être confirmés en amont. Baguida n'est pas un site homogène : usages, exposition, services disponibles et priorités peuvent différer d'une rue, d'un espace public ou d'un jardin à l'autre. La première livraison est donc un **diagnostic partagé**, non une carte de problèmes supposés.

Questions de cadrage :

- Quelles situations les habitants souhaitent-ils améliorer, et pour qui ?
- Où et à quels moments le problème survient-il ? Comment est-il constaté aujourd'hui ?
- Quelles personnes sont davantage exposées ou moins entendues : enfants, personnes âgées, personnes en situation de handicap, vendeurs, jardiniers, usagers sans smartphone ?
- Quelle décision concrète pourrait être prise par une personne ou une institution identifiée ?
- Que peut-on faire sans capteur, application ou modèle ?
- Qui possède ou gère l'espace, le service, le réseau ou l'équipement ?
- Quels recours, autorisations, règles, langues et moyens de communication sont nécessaires ?

### 3.2 Atelier de brainstorming en cinq temps

Prévoir une animation accessible, des groupes diversifiés, une restitution en langues pertinentes et une façon de contribuer sans téléphone. Le facilitateur explique qu'aucune idée ne vaut approbation automatique d'une collecte ou installation.

1. **Écouter (30–45 min)** — récits de situations, parcours et irritants ; cartographie des moments et lieux avec un niveau de précision respectueux de la vie privée.
2. **Reformuler (20 min)** — transformer les sujets en questions : « Comment aider… ? », plutôt que « Quel capteur acheter ? ».
3. **Générer (25 min)** — imaginer des réponses humaines, organisationnelles, spatiales, matérielles et numériques ; chaque groupe doit proposer au moins une solution low-tech.
4. **Examiner (30 min)** — pour chaque idée : bénéfice, personnes concernées, risques, responsable d'action, coûts récurrents, droits et preuve attendue.
5. **Prioriser (20 min)** — noter séparément utilité ressentie, faisabilité, équité, réversibilité et risque ; discuter les désaccords avant de classer.

**Livrables de l'atelier :** carte des besoins et désaccords, liste des solutions sans technologie, registre d'idées, personnes à consulter, questions à vérifier, et trois à cinq hypothèses de pilote maximum. Ne pas publier de témoignage identifiable sans autorisation distincte.

### 3.3 Grille de sélection des cas d'usage

Noter chaque dimension de 1 à 5, en documentant qui attribue la note et pourquoi. Une note élevée de risque signifie une priorité plus faible ou une étude supplémentaire.

| Dimension | Question |
|---|---|
| Importance locale | Le problème est-il reconnu comme prioritaire par les personnes concernées ? |
| Capacité d'agir | Un responsable identifié peut-il réellement prendre une mesure ? |
| Équité | Le projet bénéficie-t-il aux groupes concernés, y compris hors ligne ? |
| Données nécessaires | Peut-on répondre sans collecter de données personnelles ? |
| Faisabilité technique | Existe-t-il une méthode et des compétences locales pour mesurer et maintenir ? |
| Coût total | Sont inclus l'achat, l'énergie, la connectivité, le temps humain et le remplacement ? |
| Réversibilité | Peut-on interrompre le service et retirer le matériel ou les données ? |
| Risque | Une erreur peut-elle porter atteinte à la santé, aux droits, à la sécurité ou aux moyens d'existence ? |

Un usage à risque élevé (santé individuelle, décision d'accès à un service, contrôle d'équipement dangereux, surveillance) n'est pas un candidat de premier pilote. Un besoin important mais sans responsable pouvant agir appelle d'abord une médiation institutionnelle.

## 4. Le modèle conceptuel : système dynamique et flux de données

### 4.1 Boucle sociotechnique

Un quartier est un système dynamique : son état évolue dans le temps sous l'effet des usages, de la météo, des infrastructures, des décisions, des ressources et d'événements imprévus. Un schéma simple aide à raisonner, mais ne décrit jamais toute la réalité.

```text
État du quartier à t
  ├─ chaleur, ombre, bruit, air, eau, végétation, services et énergie
  ↓
Observations à t (capteurs, registres, données ouvertes, retours volontaires)
  ↓
Contrôle qualité, datation, provenance, droits et agrégation
  ↓
État estimé + incertitude + besoins exprimés
  ↓
Options d'amélioration et conséquences possibles
  ↓
Décision de l'autorité / du groupe mandaté + budget et responsable
  ↓
Intervention, service ou absence d'action motivée
  ↓
Observation des effets à t+1 → correction, poursuite ou arrêt
```

Une intervention peut agir sur le système et modifier les observations ultérieures. Par exemple, installer un ombrage change les conditions du lieu ; cela n'autorise pas à conclure à un effet sans protocole, comparaison et prise en compte des facteurs externes. Le suivi doit conserver la période de référence, les changements concomitants et les données manquantes.

### 4.2 Données chaudes, données froides et retours humains

- **Données chaudes** : observations fréquentes ou récentes issues de capteurs, compteurs, journaux de service ou signalements. Elles peuvent arriver en retard, être interrompues ou mal calibrées. Toujours distinguer l'heure d'observation et l'heure de réception.
- **Données froides** : informations géographiques ou documentaires relativement stables et datées, par exemple bâtiments, voies, espaces verts et équipements issus d'OpenStreetMap, plans publics ou inventaires locaux. « Stable » ne veut pas dire exact, complet ou actuel ; enregistrer la date d'extraction, la licence, la couverture et les corrections locales.
- **Retours d'habitants** : observations, préférences, demandes et expériences situées. Ce sont des informations précieuses, mais non un capteur représentatif de toute la population. Décrire le canal, la langue, les biais de participation et les choix de confidentialité.
- **Données dérivées** : agrégations, cartes, indices et prédictions. Les conserver distinctement des observations d'origine, avec version, méthode et incertitude.

Un enregistrement minimal comprend : identifiant pseudonyme de l'observation, type, valeur et unité si applicables, lieu au degré de précision nécessaire, temps observé et reçu, source et méthode, indicateur de qualité, droits/finalité, transformations et version. L'absence est codée avec son motif lorsque cela est possible, jamais comme zéro.

### 4.3 Action immédiate ou action de long terme

**Action temps réel** : réponse dans une fenêtre courte, justifiée par une situation actuelle et vérifiable. Elle exige une donnée fraîche et suffisamment fiable, une autorité de décision, une procédure de recours et un comportement explicite en cas de panne. Pour le pilote, privilégier les actions humaines simples et réversibles (par exemple informer un responsable) plutôt que la commande automatique d'un équipement.

**Action de long terme** : planification d'aménagement, plantation, ombrage, entretien, horaires, formation ou investissement. Elle demande des observations répétées, l'analyse des saisons, une consultation, un budget pluriannuel et un suivi des bénéfices et effets indésirables.

Une recommandation n'est pas une intervention. Le registre de décision doit préciser : qui propose, qui valide, qui finance, qui exécute, qui est affecté, comment le résultat est contrôlé et comment arrêter ou corriger.

## 5. Architecture de référence : Code — Hardware — Design

Concevoir les trois couches ensemble, puis tester leur interface. Une application soignée ne compense pas une mesure inadéquate ; un bon capteur ne résout pas l'absence de responsable d'action.

### 5.1 Hardware — mesure, énergie et communication

- Commencer par une question et un protocole, pas par le catalogue matériel.
- Distinguer température de l'air, température de surface, humidité et confort thermique ; le choix de grandeur dépend de la décision.
- Traiter les capteurs grand public de particules ou de bruit comme des instruments indicatifs jusqu'à comparaison, calibration et caractérisation adaptées. Ne pas les présenter comme des mesures réglementaires ou cliniques.
- Consigner emplacement, hauteur, exposition, abri, unité, intervalle, horloge, maintenance, données manquantes et vérification de référence.
- Pour la **grid énergétique**, cartographier les sources, charges prioritaires, disponibilité, coupures, consommation et moyens de secours avant toute optimisation. Un tableau de bord en lecture seule est un premier cas d'usage préférable au pilotage de charges.
- Calculer le coût complet et planifier réparations, pièces, recyclage, protection physique et fin de vie. Tout dimensionnement ou raccordement électrique revient à des professionnels qualifiés et aux exigences applicables au site.
- Comparer les modes de communication selon la couverture vérifiée, le coût, la consommation, la sécurité, la maintenance et le fonctionnement hors ligne. Aucun protocole réseau n'est une garantie de sécurité par lui-même.

### 5.2 Code — collecte, intégration et aide à la décision

Architecture indicative, à choisir selon les compétences et l'hébergement réel :

```text
Urbanatic / SocialHub / PLUS / capteurs / OSM / enquêtes consenties
               ↓ interfaces documentées et contrôle des droits
       zone d'ingestion + validation + registre des sources
               ↓
 base de données temporelle et spatiale (selon besoin)
               ↓
 indicateurs, cartes, recherche spatiale / RAG et tableau de bord
               ↓
 options expliquées → revue humaine → registre de décision
               ↓
 service ou action autorisée → retour des habitants → évaluation
```

Principes d'implémentation :

- Définir un dictionnaire de données commun, unités, coordonnées, temps et identifiants de lieux ; versionner schémas et interfaces.
- Garder séparés les données brutes, les données nettoyées, les agrégats, les retours personnels et les réponses générées.
- Utiliser des contrôles d'accès par rôle, sauvegardes testées, journalisation proportionnée, mises à jour et gestion des secrets ; ne pas placer d'identifiants d'accès dans les applications ou dépôts publics.
- Prévoir mode déconnecté, synchronisation idempotente et détection des doublons si la connexion est intermittente.
- Rendre les résultats explicables : période, source, couverture, qualité, limites et version du modèle ; accepter « je ne sais pas ».
- Un RAG aide à retrouver des sources ; il ne valide pas leur exactitude ni la causalité. PLUS et SPATIOTEMP_RAG doivent être évalués sur des cas réels autorisés, avec abstention et correction.
- Séparer les environnements de développement, test et production. Toute modification de modèle, d'index ou de règle est évaluée avant diffusion, avec retour arrière.

### 5.3 Design — expérience, inclusion et confiance

- Co-dessiner les parcours des chefs de quartier, habitants, jardiniers, opérateurs SocialHub et agents municipaux.
- Prévoir langage clair, traductions relues par des locuteurs concernés, accessibilité visuelle et motrice et voies téléphoniques, papier ou en présence.
- Pour un stand SocialHub, afficher la finalité et la durée de toute collecte ; le Wi-Fi gratuit ne dépend jamais d'une contribution, d'un consentement ou d'un questionnaire.
- Dans Urbanatic, distinguer conseil horticole général, observation et recommandation à vérifier ; rendre visibles la saison, la provenance et les conditions locales.
- Dans PLUS, citer des sources datées et distinguer information culturelle, disponibilité d'un lieu, horaires et sécurité ; offrir un signalement de correction.
- Tester compréhension, effort, confiance, taux d'abandon et conséquences non souhaitées. Ne pas optimiser uniquement le nombre de clics ou d'utilisateurs.

### 5.4 Interopérabilité HubCity–Communalis

Avant toute intégration, rédiger avec les responsables de chaque service une fiche d'interface : propriétaire du service, données effectivement disponibles, finalités permises, format, fréquence, qualité, identifiants, mécanisme de révocation, rétention, coût, version et contact de maintenance. Ne pas supposer que les conversations PLUS, les journaux Wi-Fi ou les identifiants Urbanatic peuvent être réutilisés pour l'analyse territoriale ou l'entraînement.

Privilégier des événements minimisés et agrégés, par exemple un nombre de consultations par période et zone suffisamment large, si le besoin est démontré et le risque évalué. Écarter contenus de navigation, adresses MAC, identifiants d'appareils, historiques individuels et texte libre identifiable lorsqu'ils ne sont pas strictement nécessaires. Les analyses de service et l'amélioration de modèles sont des finalités différentes qui exigent des décisions et des droits distincts.

## 6. Cibles, indicateurs et apprentissage par renforcement

### 6.1 Construire des objectifs vérifiables

Le mot « target » désigne ici une cible mesurable convenue, assortie d'une échéance et d'une méthode. Établir la mesure de référence avant de fixer une cible chiffrée d'impact. Les seuils de santé, de sécurité, de qualité réglementaire et les normes professionnelles ne sont pas définis par ce guide ; ils doivent venir des autorités compétentes et de sources à jour.

Pour chaque cible, inscrire : indicateur, valeur de départ et date, valeur visée, date d'échéance, population/site couvert, fréquence, source, méthode et incertitude, responsable, désagrégations autorisées, effets indésirables à surveiller, et règle de révision. Si la référence n'existe pas, la cible du premier cycle porte sur la mise en place d'une mesure fiable, pas sur une amélioration fictive.

Familles d'indicateurs à sélectionner avec les habitants :

| Résultat recherché | Exemples d'indicateurs (à préciser localement) |
|---|---|
| Chaleur et ombre | disponibilité d'ombre par lieu et plage horaire ; température mesurée selon protocole ; lieux prioritaires identifiés ; confort déclaré volontairement |
| Air et bruit | complétude et qualité des mesures indicatives ; périodes à investiguer ; plaintes/observations agrégées ; interventions et suivi |
| Agriculture urbaine | jardins actifs ; disponibilité d'eau documentée ; survie des plantations ; continuité d'entretien ; participation et apprentissages |
| Énergie des services | heures de disponibilité ; coupures observées ; énergie consommée par service lorsque mesurable ; part des incidents traités |
| Inclusion et expérience | accès par canal/langue ; retours résolus ; compréhension des notices ; participation hors ligne ; plaintes et délais de réponse |
| Qualité du système | complétude, fraîcheur, taux de données invalides, délai de correction, coût d'exploitation et disponibilité du responsable |

Exemples de **cibles opérationnelles initiales à discuter** — non des résultats constatés ni des normes : identifier un responsable et un suppléant pour chaque flux ; obtenir les autorisations avant toute collecte ; publier une fiche de méthode pour chaque indicateur ; traiter ou accuser réception d'une part convenue des retours dans un délai convenu ; tester la restauration des sauvegardes avant lancement ; rendre chaque recommandation traçable à ses données et à son approbation. Les pourcentages et délais sont fixés après mesure de capacité et discussion publique.

### 6.2 Quand l'apprentissage par renforcement est-il pertinent ?

L'apprentissage par renforcement (RL) apprend une politique d'action en reliant un état observé, une action, une récompense et un nouvel état. Dans Communalis, cette approche est **une piste expérimentale**, non une condition de réussite. Elle n'est justifiée que si :

1. il existe un processus séquentiel réel et une décision répétée ;
2. les actions possibles sont définies par une autorité compétente ;
3. les conséquences peuvent être simulées ou étudiées sans exposer la population à un apprentissage risqué ;
4. la récompense représente des objectifs publics et équitables, et non une métrique de clic ou de coût seule ;
5. des données suffisantes, des évaluations hors ligne et des procédures de contrôle sont disponibles ;
6. le système peut s'abstenir, être arrêté et revenir à un fonctionnement antérieur.

Exemple abstrait : aider à ordonnancer l'entretien de jardins communs ou à proposer des horaires d'utilisation d'un service selon la disponibilité énergétique. L'état peut comprendre uniquement des données agrégées et qualifiées ; les actions sont des propositions bornées ; la récompense doit équilibrer continuité du service, équité d'accès, coût, consommation, entretien et préférences délibérées localement. Les pondérations sont des décisions politiques à publier, non un choix caché d'ingénieur.

**Procédure prudente :**

1. Établir une politique de référence simple (règles, calendrier ou pratique actuelle) et ses résultats.
2. Co-définir objectifs, contraintes inviolables et effets distributifs ; définir qui peut contester les objectifs.
3. Construire un simulateur documenté et faire valider ses hypothèses par des personnes connaissant le terrain.
4. Évaluer hors ligne sur des périodes et groupes non utilisés pour le réglage ; tester les situations rares, données manquantes, erreurs et changements de contexte.
5. Faire une phase « recommandation en observation » : le modèle ne fait rien ; comparer sa proposition à la décision humaine, enregistrer les désaccords et étudier les effets possibles.
6. Soumettre les résultats et risques à une revue indépendante et communautaire. Si le bénéfice n'est pas supérieur à la référence sans dégrader l'équité ou la sécurité, ne pas déployer.
7. Si une phase opérationnelle est autorisée, limiter le périmètre, conserver la validation humaine, surveiller les indicateurs et prévoir arrêt immédiat et retour à la politique de référence.

Ne pas apprendre en ligne par essai-erreur sur l'accès à la santé, la distribution d'électricité ou d'eau, les équipements de sécurité, les droits sociaux, ni sur des personnes qui ne peuvent refuser. Une récompense mal définie peut déplacer le problème : par exemple, réduire la consommation au prix de l'exclusion de certains usagers. Les protections physiques et règles de sécurité sont déterministes, indépendantes du modèle et non modifiables par celui-ci.

## 7. Catalogue de projets à explorer

Les idées ci-dessous constituent un portefeuille pour le brainstorming, pas un engagement ni un diagnostic. Les équipes en choisissent quelques-unes après consultation, vérification des compétences, droits et coûts. Le premier pilote devrait rester petit, réversible, sans collecte personnelle superflue et sans actionneur.

| # | Projet à explorer | Données et méthode possibles | Première action ou résultat vérifiable |
|---:|---|---|---|
| 1 | Cartographie participative des zones d'ombre | parcours accompagnés, observations datées, OSM | carte des lieux et heures à améliorer |
| 2 | Suivi indicatif de la chaleur dans des espaces publics | sondes comparées, protocoles soleil/ombre | recommandations d'emplacements à ombrager |
| 3 | Inventaire des arbres et besoins d'entretien | observation, espèces relues localement, OSM | calendrier d'entretien validé |
| 4 | Parcours piétons ombragés vers les services | réseau viaire, observations, accessibilité | itinéraires documentés, sans géolocalisation individuelle |
| 5 | Journal communautaire des nuisances sonores | signalements volontaires, campagne de mesure indicative | périodes et lieux nécessitant une médiation |
| 6 | Veille indicative sur les particules et poussières | capteurs testés, météo, protocole de qualité | repérage de situations à investiguer, pas d'avis médical |
| 7 | Jardins urbains et partage de pratiques via Urbanatic | fiches de jardins, calendrier et retours volontaires | guide local et suivi d'entretien |
| 8 | Suivi de l'eau pour les jardins communautaires | relevés manuels ou compteurs autorisés | bilan de disponibilité et plan d'entretien |
| 9 | Ombrières et assises dans des lieux d'attente | audit d'usage, design participatif, comptage non identifiant | prototype réversible et évaluation d'usage |
| 10 | Inventaire des équipements et services de proximité | OSM et vérification par les habitants | carte datée avec signalement de correction |
| 11 | Accessibilité des cheminements | marches d'audit avec personnes concernées | liste priorisée d'obstacles et responsables |
| 12 | Information culturelle de proximité par PLUS | sources publiques vérifiées, corrections de contributeurs | réponses sourcées et parcours de recours |
| 13 | Répertoire des lieux socioculturels d'Afrique de l'Ouest dans PLUS | données ouvertes et validation des lieux | fiches de lieux versionnées et datées |
| 14 | SocialHub comme guichet numérique inclusif | retours anonymisés/agrégés avec choix séparés | accès aux informations et canal hors ligne |
| 15 | Mesure de disponibilité énergétique des stands SocialHub | journal technique agrégé, mesure électrique qualifiée | tableau de disponibilité et causes de panne |
| 16 | Tableau de bord de la grid énergétique en lecture seule | inventaire de charges, mesures autorisées, journaux de coupure | priorités de continuité validées par les gestionnaires |
| 17 | Inventaire des pannes et maintenance des équipements partagés | registre papier/numérique avec rôles | délais et coûts de réparation suivis |
| 18 | Carte de points de fraîcheur et de repos | observations, horaires et critères co-définis | répertoire vérifié accessible hors ligne |
| 19 | Signalement des dépôts de déchets ou eaux stagnantes | formulaire volontaire, vérification humaine | tickets d'intervention sans accusation automatique |
| 20 | Diagnostic de collecte des déchets | observations de parcours et calendrier | ajustement discuté avec les équipes concernées |
| 21 | Alerte communautaire non automatisée en cas d'événement météo | messages officiels et relais identifiés | protocole de diffusion et correction des rumeurs |
| 22 | Recherche spatio-temporelle SPATIOTEMP_RAG | sources datées, OSM et observations autorisées | réponses qui citent lieu, période, provenance et limites |
| 23 | Observatoire des retours d'usage des services HubCity | retours facultatifs, agrégés, par canal et langue | feuille de route produit discutée |
| 24 | Prévision de maintenance des équipements communautaires | historiques de pannes minimisés et inventaire | planification assistée comparée à une règle simple |
| 25 | Simulation d'horaires de services selon la continuité énergétique | courbes agrégées et contraintes des opérateurs | options simulées, décision humaine et équité examinée |
| 26 | Parcours de découverte du patrimoine et des initiatives locales | contenus autorisés, sources et contributeurs crédités | parcours culturel accessible via PLUS et SocialHub |

Pour chaque idée retenue, renseigner la fiche de cadrage du modèle de livrable en section 9. Ne pas transformer un signalement individuel en carte publique à haute résolution sans analyser le risque de ré-identification et de représailles.

## 8. Sources techniques et base de projet

La liste suivante est un point de départ. Vérifier la version, la licence, la date, la couverture du Togo et les conditions d'accès avant usage. Une source n'est pas une approbation de son exactitude pour un site précis.

### 8.1 Cartographie, données et géospatial

- **OpenStreetMap** — données géographiques contributives et documentation : [openstreetmap.org](https://www.openstreetmap.org/) et [Copyright and License](https://www.openstreetmap.org/copyright). Respecter l'attribution ODbL et les conditions de réutilisation ; faire valider les détails locaux.
- **Humanitarian OpenStreetMap Team** — outils et méthodes de cartographie participative : [learnosm.org](https://learnosm.org/) et [hotosm.org](https://www.hotosm.org/).
- **QGIS** — système d'information géographique libre : [qgis.org](https://qgis.org/).
- **PostgreSQL/PostGIS** — stockage et traitements géographiques, si leur complexité est justifiée : [postgis.net](https://postgis.net/).
- **GeoJSON** — format d'échange géographique : [RFC 7946](https://www.rfc-editor.org/rfc/rfc7946).
- Pour les données satellites, météo ou administratives, identifier le fournisseur, les résolutions, les dates, les droits et les limites locales avant de les rapprocher d'observations de quartier.

### 8.2 Enquêtes, observation et capteurs

- **ODK** — collecte de formulaires hors ligne et documentation : [getodk.org](https://getodk.org/).
- **KoboToolbox** — collecte humanitaire et communautaire : [kobotoolbox.org](https://www.kobotoolbox.org/). Examiner hébergement, contrat, localisation, accès et conditions de conservation.
- **OMS — qualité de l'air et santé** : [who.int/health-topics/air-pollution](https://www.who.int/health-topics/air-pollution). Les recommandations de santé ne valident pas un capteur donné.
- **WMO — qualité de l'air et météorologie** : [wmo.int](https://wmo.int/), rechercher les documents de mesure et de qualité pertinents à la campagne.
- **OpenAQ** — plateforme ouverte de données sur la qualité de l'air : [openaq.org](https://openaq.org/). Vérifier disponibilité, provenance et représentativité avant tout usage au Togo.
- Avant tout déploiement, consulter les services togolais compétents pour la météo, l'environnement, la santé, l'électricité et les télécommunications ; obtenir les contacts, normes et procédures à jour auprès des autorités et professionnels concernés.

### 8.3 IA, RAG, systèmes dynamiques et évaluation

- Sutton et Barto, **Reinforcement Learning: An Introduction**, édition disponible sur le site des auteurs : [incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html). Référence théorique ; elle ne remplace pas l'évaluation de sécurité ni la gouvernance publique.
- Lewis et al., **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** : [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401).
- Mitchell et al., **Model Cards for Model Reporting** : [arxiv.org/abs/1810.03993](https://arxiv.org/abs/1810.03993).
- Gebru et al., **Datasheets for Datasets** : [arxiv.org/abs/1803.09010](https://arxiv.org/abs/1803.09010).
- **NIST AI Risk Management Framework** : [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework).
- **UNESCO Recommendation on the Ethics of Artificial Intelligence** : [unesco.org/en/artificial-intelligence/recommendation-ethics](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics).
- Pour les séries temporelles et la dynamique des systèmes, documenter frontières du système, stocks/flux, délais, rétroactions, facteurs exogènes et hypothèses de modèle. Comparer les simulations aux observations ; ne pas confondre une simulation avec une prévision validée.

### 8.4 Gouvernance, inclusion et publication

- Vérifier le cadre juridique togolais applicable aux données personnelles, aux communications électroniques, à la recherche, aux installations et aux marchés publics auprès des autorités compétentes et d'un conseil local. Le guide ne constitue pas un avis juridique.
- Pour la vie privée dès la conception, les analyses d'impact, les consentements ou autres bases applicables, les durées, transferts et droits, établir une fiche par finalité et obtenir la validation locale nécessaire avant collecte.
- Pour chaque dépôt logiciel ou jeu de données, publier une licence explicite et distincte ; une licence de code ne donne pas les droits sur les données, contenus culturels, photographies ou contributions des habitants.
- Identifier des revues en études sociotechniques, interaction humain-machine, développement urbain, santé environnementale ou systèmes d'information selon le résultat réel ; vérifier portée, comité éditorial, frais, méthode d'évaluation et politique d'éthique.

### 8.5 Sources internes à documenter

Pour Urbanatic, SocialHub, PLUS et SPATIOTEMP_RAG, constituer une documentation vérifiée : propriétaire, équipe mainteneuse, version et date, dépôt ou adresse de service, architecture, API autorisées, conditions d'utilisation, dépendances, langues, jeux de test, incidents connus, procédure de mise à jour, plan de sauvegarde et contact. Si une information n'est pas disponible, la marquer « à obtenir » plutôt que la déduire du nom du service.

## 9. Bootcamp Communalis et livrable participant

### 9.1 Objectif et format

Le bootcamp apprend à transformer un besoin local en prototype documenté et évalué, non à imposer une solution IA. Format suggéré : **cinq jours** de travail en équipe, précédés d'une préparation avec les partenaires. La durée est ajustable ; une sortie de terrain est subordonnée aux autorisations, à la sécurité et à l'accord des personnes rencontrées.

| Jour | Activités | Livrable de la journée |
|---|---|---|
| Préparation | accords, participants, langues, attentes, rémunération, risques, matériel | mandat du bootcamp et information claire |
| 1 — Écoute et système | visite/atelier autorisés, parcours, parties prenantes, limites du système | problème formulé et carte d'acteurs |
| 2 — Données et preuve | OSM, sources, observations, droits, qualité, éthique | dictionnaire et registre de sources |
| 3 — Idées et prototype | Code/Hardware/Design, solutions low-tech, maquette ou analyse | prototype limité et hypothèses |
| 4 — Évaluation | indicateurs, baseline possible, tests, cas d'erreur, inclusion | protocole et résultats sans surpromesse |
| 5 — Restitution | revue communautaire, risques, coûts, plan de suite et arrêt | présentation, décision et dossier réplicable |

Encadrement minimal : référent communautaire, facilitateur, personne de données/éthique, mentor technique approprié au cas, personne de design/inclusion et référent de sécurité si du matériel est envisagé. Les personnes qui apportent une expertise locale ne sont pas de simples informateurs ; leur rôle, temps, rémunération et attribution sont discutés.

### 9.2 Gabarit de livrable à remettre par chaque équipe

Copier cette fiche dans un document séparé par équipe. Les champs non connus restent explicitement à compléter ; aucun chiffre ou accord ne doit être inventé.

```text
COMMUNALIS — LIVRABLE DE BOOTCAMP

A. IDENTIFICATION
Nom du projet :
Équipe / rôles / contacts professionnels autorisés :
Date, version, langue(s) du livrable :
Zone et lieux couverts (précision justifiée) :
Statut : idée / prototype / essai autorisé / en pause / arrêté

B. PROBLÈME ET PUBLIC
Problème décrit par les personnes concernées :
Qui est concerné, qui risque d'être absent de la consultation ?
Comment le besoin est-il traité aujourd'hui ?
Décision ou service que le projet souhaite améliorer :
Preuve du besoin (source, date, méthode, limites) :
Désaccords et questions restant ouvertes :

C. HYPOTHÈSE ET CIBLE
Hypothèse testable :
Résultat attendu pour les personnes :
Indicateur(s), unité, période et population/site :
Valeur de référence / méthode pour l'obtenir :
Cible proposée, justification et date de revue :
Effets indésirables et indicateurs d'équité à surveiller :

D. CONCEPTION — CODE / HARDWARE / DESIGN
Code : logiciels, versions, interfaces, hébergement, licences, sécurité :
Hardware : instruments, emplacement, alimentation, communication,
  maintenance, sécurité et fin de vie (ou « sans matériel ») :
Design : parcours, langues, accessibilité, canal hors ligne,
  tests de compréhension :
Schéma du flux : besoin → observation → traitement → décision → action :
Alternative low-tech évaluée :

E. DONNÉES ET DROITS
Source / propriétaire / finalité / licence / date :
Champs collectés et nécessité de chaque champ :
Temps et précision spatiale :
Base ou autorisation à vérifier, information des personnes et contact :
Accès / partage / conservation / suppression / retrait :
Données exclues et justification :
Contrôles de qualité, incertitude, données manquantes :

F. PROTOTYPE ET ÉVALUATION
Fonction incluse et fonctions explicitement exclues :
Scénarios testés, participants et autorisations :
Référence de comparaison (pratique actuelle ou solution simple) :
Résultats observés avec dénominateurs et périodes :
Erreurs, abstentions, biais, incidents et échecs :
Retours des habitants et modifications demandées :
Résultats non conclusifs et limites :

G. ACTION, RISQUES ET GOUVERNANCE
Qui propose, qui décide, qui exécute et qui peut arrêter ?
Actions possibles / actions interdites :
Risques, personnes exposées et mesures de réduction :
Validation professionnelle ou autorisation encore requise :
En cas de doute, panne, perte de réseau ou données périmées :
Procédure de plainte, correction et réponse :

H. PLAN D'EXPLOITATION
Responsable et suppléant :
Coût initial et coût récurrent avec devis/date/monnaie :
Maintenance, pièces, énergie, formation et dépendances :
Plan de sauvegarde et test de restauration :
Conditions de poursuite / modification / suspension / arrêt :
Plan de sortie, restitution et suppression des données :

I. REPRODUCTIBILITÉ ET COMMUNICATION
Dépôt/code/données publiables, versions et licences :
Instructions pour reproduire et matériel nécessaire :
Éléments qui ne peuvent pas être publiés et raison :
Personnes à créditer, forme d'attribution convenue :
Résumé public relu, langues et autorisations :
Prochaine décision, responsable et date :

Validation par l'équipe et représentants concernés :
Les signatures n'affirment pas que les résultats sont généralisables.
```

Critères de revue : besoin validé, solution proportionnée, droits et risques examinés, prototype reproductible, indicateurs définis, échecs visibles, coût total discuté, responsable d'exploitation identifié et décision de suite explicite. Une équipe peut réussir en démontrant qu'une idée ne doit pas être poursuivie.

## 10. Déploiement et interaction avec le public

### 10.1 Jalons et portes de décision

| Phase | Travail | Condition pour poursuivre |
|---|---|---|
| 0. Mandat | accord de la commune et des partenaires, gouvernance, budget de préparation | responsabilités, périmètre et procédure d'arrêt sont désignés |
| 1. Écoute | diagnostic et brainstorming accessibles | problème prioritaire et personnes affectées confirmés |
| 2. Faisabilité | données, droits, baseline, alternative et coût total | aucun blocage juridique, technique ou communautaire non traité |
| 3. Prototype | maquette, analyse ou capteur limité avec autorisations | qualité mesurée et absence de risque disproportionné |
| 4. Essai encadré | période et site bornés, support humain, canal de retour | utilité, inclusion et maintenance évaluées par rapport à la référence |
| 5. Décision | poursuivre, corriger, étendre, suspendre ou arrêter | décision documentée, responsable et financement identifiés |
| 6. Réplication | diagnostic complet du nouveau site | adaptation locale, droits, compétences et sortie financés |

Ne pas franchir un jalon parce que du matériel ou un financement a déjà été acheté. L'arrêt est un résultat valide et doit être budgété.

### 10.2 Plan d'interaction publique

- **Avant l'essai :** annoncer l'objectif, les responsables, les données concernées et exclues, les dates, les limites, les canaux hors ligne et le moyen de plainte.
- **Pendant l'essai :** tenir des permanences ou rencontres avec horaires annoncés ; publier un tableau de suivi agrégé ; répondre dans un délai convenu ; signaler les incidents et changements de finalité.
- **Restitution :** présenter les résultats et leurs limites dans les langues et formats pertinents ; distinguer mesures, témoignages, interprétations et décisions ; donner une place aux opinions divergentes.
- **Après l'essai :** expliquer la décision, les données conservées/supprimées, l'entretien et la date de révision ; laisser le matériel et le service dans un état sûr.

Le Wi-Fi SocialHub reste accessible selon ses propres règles de service et ne peut pas être refusé à une personne qui ne répond pas à un sondage. Toute interaction doit proposer une voie de retrait ou d'information qui n'exige pas de smartphone. Les photos, citations, enregistrements vocaux et contributions culturelles requièrent des autorisations adaptées à leur usage et diffusion.

### 10.3 Registre des décisions et incidents

Pour chaque proposition : identifiant, date, source et version, options considérées, incertitudes, avis reçus, décideur habilité, décision et motif, personne chargée du suivi, échéance, résultat observé et possibilité de contestation. Les incidents (mesure erronée, panne, divulgation, réponse trompeuse, exclusion ou dommage) disposent d'un canal de signalement, d'un responsable, d'une procédure de suspension et d'un compte rendu proportionné.

## 11. Conditions de réussite pour les décideurs

Un projet de cette nature a besoin de plus qu'une application et d'un lancement public. Les décideurs et financeurs devraient exiger les éléments suivants avant de soutenir un déploiement :

1. **Mandat et légitimité** — rôle de la commune, des chefs de quartier et des organisations communautaires clarifié ; représentation et mécanisme de désaccord établis.
2. **Problème et décision** — besoin confirmé, responsable en mesure d'agir et solution sans IA comparée.
3. **Bénéfice public démontrable** — objectifs, référence, méthode, population couverte, coûts et effets secondaires prévus.
4. **Participation équitable** — contribution accessible hors ligne, langues pertinentes, indemnisation/attribution, consultation des groupes affectés.
5. **Protection et confiance** — finalités distinctes, collecte minimale, sécurité, contrôle des accès, durée, recours et validation juridique locale.
6. **Qualité des preuves** — protocole, provenance, incertitudes, calibration ou limites des instruments, versions des modèles et données.
7. **Architecture maintenable** — documentation, standards ouverts autant que possible, sauvegardes testées, dépendances, fonctionnement dégradé et sortie.
8. **Responsabilité opérationnelle** — propriétaire, opérateur, suppléant, maintenance, pièces et procédure d'incident identifiés.
9. **Budget de cycle de vie** — coûts de personnel, formation, connexion, énergie, hébergement, remplacement, traduction, consultation et fin de vie.
10. **Sécurité proportionnée** — évaluation spécifique à chaque risque ; aucune IA ne contourne les protections ou responsabilités professionnelles.
11. **Transparence et apprentissage** — publication des résultats négatifs et mécanisme de correction, suspension et arrêt.
12. **Réplication responsable** — kit reproductible et conditions minimales ; chaque commune choisit ses priorités et peut refuser le système.

**Signaux d'alerte pour une décision de non-déploiement :** absence de responsable d'action ; collecte conditionnée au Wi-Fi ; source ou licence inconnue ; modèle évalué uniquement par démonstration ; aucune voie de plainte ; actionneur piloté directement par un modèle ; coût récurrent non financé ; promesse d'amélioration de santé fondée sur un capteur non validé ; données ou résultats publiés sans accord ; absence de plan de retrait.

## 12. Relations publiques, documentation et publication sociotechnique

### 12.1 Communication responsable

La communication commence avant la démonstration et se poursuit après la décision. Tous les supports (affiche, radio, réseaux sociaux, démo, communiqué, article) doivent distinguer :

- ce qui est **réalisé**, **en cours**, **proposé** ou **non testé** ;
- ce qui est mesuré de ce qui est déclaré, simulé ou généré par un modèle ;
- l'échelle et la période auxquelles le résultat s'applique ;
- les limites, incertitudes, financements, intérêts et partenaires confirmés ;
- les images, noms, voix, citations et cartes dont la diffusion est autorisée.

Ne pas annoncer « l'IA améliore la santé » ou « la pollution a baissé » sans étude adaptée, comparaison, validation et preuve causale suffisamment solide. Préférer une formulation exacte : « ce prototype aide à organiser des observations ; son effet sur les décisions et les conditions de vie reste à évaluer ».

### 12.2 Documentation vivante à maintenir

Pour chaque version du projet, maintenir un dossier daté contenant :

- charte, périmètre, rôles, conventions et journal de décisions ;
- inventaire des applications, composants, matériel, versions et licences ;
- dictionnaire de données, fiches de sources, méthodes, qualité et rétention ;
- documentation des modèles, requêtes de test, erreurs et critères d'abstention ;
- protocoles de terrain, autorisations, résultats avec dénominateurs et incertitudes ;
- budget prévu/réel et coûts récurrents ;
- journal de maintenance, incidents, corrections, réclamations et suites ;
- notices publiques, langues, mises à jour et modalités d'arrêt ;
- dossier de réplication avec prérequis, adaptations locales et éléments non transférables.

Les informations sensibles et identifiantes restent hors des dépôts ou publications publiques. Les contributeurs choisissent et comprennent séparément la participation, l'usage de leurs données, l'attribution, le partage et la publication lorsque ces choix sont pertinents.

### 12.3 Parcours de publication

1. **Compte rendu local** — restituer d'abord aux participants et décideurs ; faire corriger erreurs factuelles, traductions et omissions.
2. **Note technique ouverte** — publier architecture, protocole, versions, coûts pertinents, limites, leçons d'exploitation et instructions reproductibles.
3. **Article sociotechnique** — expliciter question de recherche, contexte, méthode, position des chercheurs, recrutement, consentement/approbations, rémunération, analyse, résultats négatifs, limites et partage des données.
4. **Évaluation éthique et éditoriale** — vérifier exigences de comité d'éthique si la recherche porte sur des personnes, le droit applicable, la confidentialité, l'attribution et les conflits d'intérêts ; les modalités sont à déterminer localement et selon la revue.
5. **Archivage et suivi** — DOI ou dépôt durable lorsque possible, version, licence, erratum/correction et date de révision ; tenir compte des demandes de retrait et limites de diffusion.

Les contributeurs locaux doivent pouvoir participer à la formulation de la recherche, à l'interprétation et à la rédaction, avec reconnaissance de leur rôle et des accords de co-signature discutés en amont. La publication ne doit pas révéler un lieu sensible, une personne ou un savoir culturel restreint.

### 12.4 Pistes de revues et réseaux

Choisir la revue après avoir défini le type de résultat ; ne pas promettre une publication. Pistes à examiner : études de science, technologie et société, interaction humain-machine et design participatif, urbanisme et géographie, santé environnementale, agriculture urbaine ou systèmes d'information communautaires. Vérifier l'adéquation thématique, les méthodes exigées, l'évaluation par les pairs, les frais, les politiques de données et les règles d'éthique. Privilégier une restitution locale et une documentation publique accessible en complément d'un article académique.

## 13. Reproductibilité dans les communes du Togo

La réplication porte sur la **méthode**, pas sur l'hypothèse que les mêmes problèmes ou réglages s'appliquent partout. Un kit de réplication contient :

- fiche de diagnostic, grille de priorisation et agenda de brainstorming ;
- charte de gouvernance, notices accessibles et modèle de partenariat à faire valider ;
- dictionnaire de données, schéma d'architecture et exemples synthétiques ;
- protocoles et fiches de mesure avec instruments, vérification, incertitude et coûts ;
- code, versions, licences, tests et procédures d'installation/restauration ;
- support de bootcamp et gabarit de livrable ;
- registres de décisions, maintenance, incidents et retours ;
- indicateurs, baseline, critères de poursuite et critères d'arrêt ;
- feuille de calcul budgétaire adaptée aux devis et coûts locaux ;
- guide d'adaptation des langues, institutions, saisons, usages, réseaux et priorités.

Un nouveau site passe par son propre diagnostic, ses accords et sa baseline. Les données ne sont partagées entre communes que selon une finalité convenue, une base autorisée, des conditions de qualité et une capacité d'expliquer les comparaisons. Une moyenne régionale ne doit pas effacer les différences de quartier.

## 14. Check-list avant lancement d'un pilote

- [ ] Le besoin et la décision à éclairer ont été validés par des personnes concernées.
- [ ] Le périmètre Baguida et les responsabilités locales sont confirmés et datés.
- [ ] Une alternative low-tech et le statu quo ont été examinés.
- [ ] Les cibles ont une baseline ou indiquent clairement comment l'établir.
- [ ] Les applications HubCity ont une documentation et un responsable d'intégration confirmé.
- [ ] Sources, droits, finalités, sécurité, rétention et règles locales ont été vérifiés.
- [ ] Aucune contribution au Wi-Fi n'est obligatoire ; une voie hors ligne existe.
- [ ] Les capteurs ont un protocole, une vérification, une maintenance et des limites annoncées.
- [ ] Le modèle peut s'abstenir et aucune sortie générée ne déclenche seule une action.
- [ ] Tout dispositif physique dispose de l'analyse de risques et des validations professionnelles requises.
- [ ] Les participants sont informés, leurs contributions sont reconnues et les modalités de plainte sont simples.
- [ ] Un responsable et un suppléant disposent du temps, des compétences et du budget récurrent.
- [ ] Les critères de suspension, d'arrêt, de suppression et de sortie sont établis.
- [ ] La restitution publique et la documentation des résultats négatifs sont planifiées.

## 15. Glossaire opérationnel

**Actionneur** — dispositif qui transforme une commande en effet physique.  
**Baseline / référence** — état initial mesuré avec méthode, période et couverture définies.  
**Donnée chaude** — donnée récente ou fréquente, souvent issue d'un capteur ou d'un journal de service.  
**Donnée froide** — information géographique ou documentaire moins fréquemment renouvelée ; elle doit rester datée et vérifiable.  
**État du système** — description choisie d'un système à un moment donné ; elle est partielle et incertaine.  
**Grid énergétique** — réseau et ressources énergétiques considérés dans leur périmètre réel ; une carte de consommation ne vaut pas autorisation de pilotage.  
**RAG** — génération assistée par recherche de documents ; les sources retrouvées doivent être vérifiées.  
**Renforcement / RL** — famille de méthodes qui apprend une politique à partir d'états, d'actions et de récompenses ; nécessite contraintes, validation et évaluation adaptées.  
**SPATIOTEMP_RAG** — nom de composant du projet à documenter ; désigne ici une recherche contextualisée par lieu et temps, sans présumer de ses fonctions actuellement disponibles.  
**Target / cible** — résultat mesurable convenu, daté, assorti d'une méthode et d'un responsable.  
**Temps réel** — réponse dans une fenêtre temporelle définie par le cas d'usage, avec données suffisamment fraîches et procédure de panne.  

---

**Révision du guide :** avant toute diffusion institutionnelle, compléter les responsables, partenaires dont la citation est autorisée, textes togolais applicables, devis, contacts techniques et résultats réels du pilote. Garder les mentions « à confirmer » lorsque la preuve ou la validation n'est pas disponible.

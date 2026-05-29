# WildNexus — Document Fondateur

**Version :** v0.2 DRAFT
**Date :** 2026-05-17
**Statut :** DRAFT — Pour validation JCH
**Rédigé par :** [[Dobby]] 🦉 — orchestration et consolidation documentaire PKA_JCH
**Propriétaire :** Jean-Claude Havaux — JCHYTECH

---

## Table des matières & responsabilités par section

| § | Section | Agents concernés | Rôle |
|---|---------|-----------------|------|
| 1 | Carte d'identité | JCH · [[Dobby]] | Propriétaire · Orchestration |
| 2 | Contexte et origine | JCH | Source narrative — non délégable |
| 3 | Vision et ambition | JCH · wildnexus-program-manager-system-architect | Vision (JCH) · Cohérence scope P0/P1/P2 |
| 4 | Rationale stratégique | wildnexus-program-manager-system-architect · wildnexus-scientific-advisor · [[Furet]] | Arbitrage · Positionnement scientifique · Analyse concurrents |
| 5 | Non-négociables | JCH · [[Renard]] · conseil [[Pi]] externe si nécessaire | Validation obligatoire JCH · Clauses contractuelles et licence ([[Renard]]) · Compatibilité brevets/FTO |
| 6 | Objectifs | wildnexus-program-manager-system-architect · tous agents domaine | Scoping P0/P1/P2 · Vérification faisabilité par domaine |
| 7 | État de l'art | wildnexus-scientific-advisor · [[Furet]] · wildnexus-edge-ai-cv | Standards scientifiques · Recherche concurrents · IA existante |
| 8 | Méthodologie | wildnexus-program-manager-system-architect · wildnexus-firmware-ulp · wildnexus-camera-imaging · wildnexus-hardware-physical · wildnexus-rf-propagation · wildnexus-edge-ai-cv · wildnexus-bioacoustics-dsp | Arbitrage système · Plateforme embarquée · Capteur/IR · Enclos · Énergie · Radio · IA · Acoustique |
| 9 | Propriété intellectuelle | [[Renard]] · JCH · conseil [[Pi]] externe si nécessaire | Contrats et licences · Validation stratégie · Appui FTO/brevets |
| 10 | Work packages | wildnexus-program-manager-system-architect · tous agents domaine | Séquençage · Livrables et jalons par domaine |
| 11 | Plan de validation | wildnexus-scientific-advisor · wildnexus-firmware-ulp · wildnexus-camera-imaging · wildnexus-hardware-physical | Standards mesure · Plateforme · Image · Enclos · Énergie |
| 12 | Registre des risques | wildnexus-program-manager-system-architect · tous agents domaine | Identification · Mitigation par domaine |
| 13 | Budget | JCH · [[Bruno]] | Décision financement · Analyse ressources |
| 14 | Outputs et impact | wildnexus-scientific-advisor · wildnexus-program-manager-system-architect · [[Miel]] | Valeur scientifique · Scope · Communauté |
| 15 | Conditions de sortie | JCH · wildnexus-program-manager-system-architect | Décision finale · Arbitrage technique |

**Légende :** JCH est validateur obligatoire de §2, §3, §5, §9, §13, §15 — ces sections ne sont pas gelées sans sa confirmation explicite.

**Jalons P0 :** M-01 Architecture gelée → M-02 Prototype banc → M-03 EVT validé → M-04 Open source publié

**Sections à affiner après actions en cours :**
- §7 : T01.1 analyse comparative concurrents
- §9 : [[Renard]] — arbitrage licence + politique contractuelle d'usage
- §11 : seuils quantitatifs à confirmer après T01.3 (RF) et T01.4 (caméra)

---

## 1. Carte d'identité du projet

> **Lecture recommandée du document**
> Ce document mélange volontairement quatre couches qui devront être séparées à terme : la doctrine fondatrice, le plan technique P0, la stratégie juridique/IP et la logique budgétaire. En `v0.2`, elles sont réunies pour conserver un point de vérité unique. En `v0.3+`, les annexes juridique et budgétaire pourront être détachées sans changer le fond des engagements.

| Champ | Contenu |
|-------|---------|
| **Nom du projet** | WildNexus |
| **Propriétaire** | Jean-Claude Havaux — JCHYTECH |
| **Statut** | Actif — Phase P0 Design |
| **Version document** | v0.2 DRAFT |
| **Date** | 2026-05-17 |
| **Rédigé par** | [[Dobby]] 🦉 — orchestration et consolidation documentaire PKA_JCH |
| **Validé par** | JCH (en cours) |
| **Définition du succès** | Un naturaliste amateur peut déployer seul un réseau de nœuds WildNexus sur sa zone d'observation, le laisser fonctionner six mois avec maintenance semestrielle planifiée, et recevoir des données suffisamment riches pour prendre des décisions concrètes de gestion ou de restauration de son territoire |
| **Autonomie P0** | 60 jours sur batterie seule (minimum garanti) · 6 mois avec apport solaire + maintenance semestrielle planifiée (ambition produit) · 30 jours EVT terrain avec extrapolation (critère de validation P0) |
| **Document dérivé synchronisé** | Résumé exécutif WildNexus — même version, audience externe |

---

## 2. Contexte et origine

### 2.1 Le naturaliste et ses outils

Jean-Claude Havaux observe la faune depuis des années avec une conviction que peu de naturalistes formulent aussi clairement : la nature ne se conserve pas — elle se revivifie. La conservation passive, celle qui documente le déclin et gère les derniers refuges, ne suffit pas. Ce qui manque, c'est une capacité d'observation suffisamment dense, continue et accessible pour alimenter des décisions d'action concrètes sur le terrain.

Comme beaucoup de naturalistes engagés, JCH utilise déjà des outils : pièges photographiques, applications d'identification d'espèces, relevés manuels. Ces outils donnent une réponse à la question la plus simple — *quel animal est passé ici, et quand ?* — mais s'arrêtent là. Ils ne permettent pas de savoir combien de passages ont eu lieu sur une période, si un individu est revenu, comment la présence évolue en fonction des saisons ou des perturbations environnementales. Ils ne permettent surtout pas de faire tout cela sans être physiquement présent sur le terrain à intervalles réguliers.

Cette insatisfaction — concrète, documentée par l'usage, pas par la théorie — est l'origine de WildNexus.

### 2.2 Le gap que les outils existants ne comblent pas

Les solutions disponibles aujourd'hui se répartissent en deux catégories qui ne se rejoignent pas.

D'un côté, les pièges photos grand public : accessibles, robustes, mais fermés. Leurs données restent dans une carte SD. Leur intelligence est nulle ou propriétaire. Leur réseau est inexistant. Chaque unité est une île. Leur usage exige des visites terrain régulières pour récupérer les données — et chaque visite est elle-même une perturbation : le passage du naturaliste modifie les comportements qu'il cherche à observer, y compris dans les zones de tranquillité où la présence humaine est réglementée ou indésirable.

De l'autre, les infrastructures de monitoring institutionnel : puissantes, connectées, capables de produire des données scientifiques rigoureuses — mais hors de portée d'un naturaliste individuel par leur coût, leur complexité de déploiement, et leur dépendance à des équipes techniques dédiées.

Entre les deux, rien. Pas de plateforme ouverte, extensible, connectée, accessible, qui permette à un amateur éclairé ou à une petite association de déployer un réseau de capteurs et d'en exploiter les données sans compétences spécialisées ni budget institutionnel.

C'est ce vide que WildNexus occupe.

### 2.3 Pourquoi maintenant

Trois convergences techniques rendent ce projet faisable en 2026 là où il ne l'était pas cinq ans plus tôt : la maturité des standards LPWAN longue portée basse consommation, la disponibilité de l'edge AI embarqué pour le filtrage local, et l'accessibilité de la chimie LiFePO4 stable en conditions terrain. Ces trois convergences, associées à la maturité de l'open hardware et de la communauté maker, créent une fenêtre d'opportunité précise — documentée en détail dans §4.2.

### 2.4 Ce qui disparaît si WildNexus n'existe pas

Sans WildNexus, la fracture entre l'observation amateur et le monitoring scientifique professionnel reste entière. Les naturalistes individuels continuent de collecter des données fragmentées, non interopérables, exploitées uniquement à l'échelle de leur propre terrain. Les gestionnaires de biodiversité continuent de prendre des décisions sur des données trop rares, trop chères, ou trop lentes.

Plus précisément : un naturaliste belge qui veut suivre la recolonisation d'une espèce sur sa propriété ou dans sa commune n'a aujourd'hui aucun outil à la hauteur de son ambition et de ses moyens. WildNexus est cet outil.

---

## 3. Vision et ambition à long terme

### 3.1 La vision à dix ans

Si WildNexus réussit pleinement, un naturaliste, une association, un gestionnaire de réserve ou une commune rurale peut déployer en une demi-journée un réseau de nœuds autonomes sur une zone de plusieurs centaines d'hectares — et recevoir, sans jamais retourner sur le terrain, un flux continu de données sur la faune présente : quelles espèces, quels individus reconnus, quels comportements observés, à quelle fréquence, dans quels corridors de déplacement.

Ce n'est pas du monitoring passif. C'est une infrastructure d'observation active qui transforme la relation entre un naturaliste et son territoire : de la visite périodique à la présence continue ; de la liste d'espèces à la connaissance des individus ; de la constatation à la décision d'action.

WildNexus respecte par construction les zones de tranquillité : une fois déployé, il n'exige plus de présence humaine. Dans les réserves naturelles, les zones de nidification sensibles, et les corridors faunistiques où le passage du naturaliste perturbe ce qu'il observe, WildNexus est une présence sans intrusion.

À grande échelle — des dizaines de zones interconnectées, des milliers de nœuds déployés par une communauté active — WildNexus devient une infrastructure distribuée de gestion de la biodiversité : le premier réseau ouvert, accessible et réellement exploitable pour suivre la recolonisation d'espèces, mesurer l'impact d'actions de restauration, ou documenter la réponse de la faune aux perturbations humaines et climatiques.

### 3.2 Ce que l'IA rend possible

WildNexus n'est pas une caméra connectée. C'est une plateforme d'observation augmentée par l'intelligence artificielle à deux niveaux distincts.

Au niveau du nœud — embarqué, sans connexion, en temps réel — l'IA filtre le bruit (feuilles, pluie, lumière), confirme la présence d'un animal par un filtre binaire (animal / non-animal), et ne transmet que ce qui mérite de l'être. L'autonomie du nœud dépend directement de cette intelligence locale : moins de faux positifs, moins de transmissions, moins de consommation. La classification d'espèces est un objectif P1 — elle peut être embarquée ou hybride selon les contraintes terrain validées en EVT.

Au niveau de l'analyse — en P1, sur les données accumulées — l'IA va plus loin : reconnaissance des individus au sein d'une espèce (par marquages naturels, morphologie, comportement), analyse des patterns de déplacement, détection d'anomalies comportementales, corrélation avec les données environnementales. Ce niveau d'analyse, aujourd'hui réservé aux programmes scientifiques dotés d'équipes dédiées, devient accessible à l'utilisateur WildNexus sans expertise en traitement de données.

C'est le "fameux +" : non pas voir plus d'animaux, mais comprendre ceux qu'on voit.

### 3.3 La contribution unique de WildNexus

D'autres systèmes observent la faune. WildNexus vise à combiner simultanément — sous réserve de confirmation par l'analyse concurrentielle T01.1 :

- **L'ouverture** — hardware et software publiés, auditables, modifiables
- **L'extensibilité** — une architecture qui invite l'innovation communautaire plutôt que de la contenir
- **L'accessibilité** — un prix et une complexité de déploiement calibrés pour l'individu, pas l'institution
- **La profondeur analytique** — de la détection de présence à la reconnaissance individuelle et à l'analyse comportementale
- **L'éthique by design** — une politique de licence qui exclut contractuellement les usages contraires à la mission

C'est cette combinaison — pas une seule dimension prise isolément — qui constitue la contribution visée par WildNexus.

### 3.4 La définition du succès

> WildNexus aura réussi si un naturaliste amateur peut déployer seul un réseau de nœuds sur sa zone d'observation, le laisser fonctionner six mois sans intervention, et en recevoir des données suffisamment riches pour prendre des décisions concrètes de gestion ou de restauration de son territoire.

---

## 4. Rationale stratégique — pourquoi ceci et pas autre chose

### 4.1 Ce qui existe et pourquoi c'est insuffisant

Le marché du monitoring faunistique se structure aujourd'hui autour de deux pôles que rien ne relie.

**Les pièges photos grand public** (Bushnell, Reconyx, Browning, Stealth Cam) sont robustes, abordables, et omniprésents chez les naturalistes individuels. Mais ce sont des systèmes fermés : données stockées localement sur carte SD, récupération manuelle obligatoire, aucune connectivité native, aucune intelligence embarquée au-delà d'un déclenchement PIR basique. Chaque unité est une île. L'exploiter demande d'être physiquement présent sur le terrain à intervalles réguliers — ce qui en fait, paradoxalement, un outil de perturbation autant que d'observation.

**Les infrastructures de monitoring institutionnel** (Wildlife Insights, Snapshot Safari, réseaux GBIF, systèmes Camtrap-DP) offrent la rigueur scientifique, la connectivité, et la puissance analytique que les pièges photos n'ont pas. Mais leur coût de déploiement, leur complexité technique, et leur dépendance à des équipes spécialisées les réservent de facto aux programmes de recherche financés et aux grandes organisations de conservation. Un naturaliste individuel ou une petite association n'a pas accès à cette couche.

Entre ces deux pôles, le vide est structurel — pas accidentel. Personne ne l'a comblé parce que la combinaison requise (connectivité longue portée + edge AI + autonomie longue durée + open platform + prix accessible) n'était pas réalisable techniquement avant 2024-2025.

### 4.2 Ce qui a changé et pourquoi maintenant

Trois maturités technologiques convergent en 2026 pour la première fois simultanément :

**Les standards LPWAN** atteignent une maturité industrielle sur des composants à quelques euros, avec une portée de plusieurs kilomètres en milieu forestier et une consommation compatible avec des batteries de taille raisonnable.

**L'edge AI embarqué** permet d'exécuter un filtrage faunistique binaire (animal / non-animal) directement sur le nœud — sans cloud, sans latence, sans abonnement. Ce qui nécessitait un serveur dédié en 2021 tient sur un microcontrôleur en 2026. La classification d'espèces fine reste une cible P1, potentiellement hybride (edge + cloud léger).

**La LiFePO4 abordable** offre une chimie stable en température extérieure, une durée de vie de 2 000 à 3 000 cycles, et une sécurité terrain que les Li-Ion classiques ne peuvent pas garantir — désormais disponible en petite série à prix compétitif.

Ces trois convergences, combinées à la maturité de l'open hardware et à une communauté maker active, créent une fenêtre d'opportunité précise. WildNexus la saisit maintenant — pas par anticipation, mais par timing juste.

### 4.3 Pourquoi cette approche et pas une alternative plus simple

**Pourquoi open source plutôt que propriétaire ?**
Un système fermé crée une dépendance au fournisseur et plafonne l'innovation à ce que l'équipe fondatrice imagine. Un système ouvert crée un écosystème : d'autres équipes ajoutent des capteurs, des algorithmes, des interfaces que WildNexus n'aurait pas développés seul. L'open source n'est pas une concession commerciale — c'est le mécanisme d'innovation principal du projet.

**Pourquoi une plateforme extensible plutôt qu'un produit fini ?**
La biodiversité est locale, diverse, imprévisible. Un naturaliste en Ardenne a des besoins différents d'un gestionnaire de zone humide en [[Camargue]] ou d'un chercheur en forêt tropicale. Aucun produit fini ne peut les servir tous. Une plateforme avec des interfaces capteurs ouvertes peut être adaptée sans que l'équipe centrale soit impliquée dans chaque adaptation.

**Pourquoi viser l'amateur autant que le professionnel ?**
Les données de biodiversité les plus précieuses sont souvent celles collectées à une échelle que les institutions ne peuvent pas couvrir. Un réseau de 1 000 naturalistes individuels équipés de WildNexus produit des données de présence sur des territoires que 10 équipes scientifiques ne pourraient pas surveiller. L'accessibilité au grand public n'est pas un compromis sur la qualité — c'est une stratégie de couverture.

### 4.4 L'avantage de la non-intrusion

WildNexus présente un avantage que ses concurrents ne peuvent pas revendiquer : une fois déployé, il ne nécessite pas de présence terrain régulière. Dans les réserves naturelles, les zones de nidification sensibles, et les corridors faunistiques où la présence humaine — même bienveillante — perturbe les comportements que l'on cherche précisément à observer, c'est une condition d'usage et non un simple avantage.

Six mois d'autonomie sans intervention signifient six mois de données non biaisées par le passage du technicien. C'est un argument scientifique autant qu'opérationnel.

### 4.5 Le risque de ne pas faire WildNexus

Sans WildNexus, le vide entre piège photo grand public et monitoring institutionnel reste structurel pour au moins cinq ans. La fenêtre technologique ouverte en 2025-2026 sera occupée. Si WildNexus ne la saisit pas, un acteur [[commercial]] — probablement avec un modèle fermé et propriétaire — le fera. L'opportunité de poser un standard ouvert pour le monitoring faunistique distribué ne restera pas disponible indéfiniment.

---

## 5. Non-négociables — couche constitutionnelle

> Ces non-négociables sont des engagements permanents du projet. Ils ne se négocient pas sous pression de délai, de budget, ou de demande partenaire. Chacun comporte une justification et un critère de vérification. Validés par JCH le 2026-05-17.

**NN-01 — Accessibilité prix et architecture modulaire**
Le produit WildNexus est commercialisé avec un prix cible de 900 € TTC pour la version complète validée. Une architecture modulaire permet à une version base d'évoluer vers la version pro par l'achat de composants additionnels via un shop dédié — ou par l'achat direct de la version pro. Aucune version ne peut être artificiellement bridée pour créer de la rareté.
**Justification** : 900 € positionne WildNexus dans le segment accessible aux naturalistes individuels et aux petites associations, tout en restant crédible face aux solutions institutionnelles à 3-5× le prix. La modularité préserve l'accessibilité à l'entrée sans plafonner le potentiel d'usage avancé.
**Vérifiable par** : prix de lancement catalogue ≤ 900 € TTC version complète ; composants d'extension disponibles séparément au shop ; aucune fonction fondamentale réservée à la version pro uniquement.

**NN-02 — Source-available / ethical-source assumé**
Le socle matériel et logiciel de WildNexus doit être publié, auditable et modifiable, sans dépendance propriétaire opaque sur la couche cœur. En revanche, WildNexus n'est pas défini ici comme open source/open hardware au sens OSI strict : le modèle retenu est un régime de diffusion `source-available / ethical-source` intégrant des restrictions d'usage explicites cohérentes avec NN-05 et NN-06.
**Justification** : L'ouverture technique reste nécessaire pour la communauté, l'auditabilité et la reproductibilité. Mais JCH a retenu l'exclusion d'usage comme contrainte fondatrice ; le vocabulaire juridique du projet doit donc refléter cette réalité, sans ambiguïté ni faux-semblant.
**Implication de communication** : WildNexus doit se présenter publiquement comme un projet à code et designs publiés, source-available, auditable et contributif, mais non comme un projet open source au sens OSI pour la licence cœur.
**Vérifiable par** : dépôt public actif ; schémas hardware publiés ; politique d'usage/licence publiée ; terminologie publique alignée sur le modèle `source-available / ethical-source` avant D06.1.

**NN-03 — Extensibilité capteurs par design**
L'architecture P0 doit permettre l'ajout de capteurs tiers sans nécessiter une refonte de la plateforme. Cette extensibilité est une spécification, pas une promesse future.
**Justification** : Le potentiel d'innovation de WildNexus repose sur la capacité de la communauté à imaginer des usages que l'équipe fondatrice n'a pas anticipés.
**Vérifiable par** : interface capteur documentée et stable depuis P0 ; au moins un capteur tiers intégré par la communauté avant la fin de P1.

**NN-04 — Communauté comme acteur du projet**
La communauté de naturalistes, développeurs, et makers n'est pas un marché cible — elle est un acteur du projet. Le développement de WildNexus doit ménager des points d'entrée réels pour les contributions externes dès P0.
**Justification** : La différence entre une communauté qui utilise et une communauté qui contribue est la différence entre un produit et un mouvement.
**Vérifiable par** : documentation de contribution publique dès le premier dépôt ; issues ouvertes aux externes ; au moins un canal communautaire actif avant la fin de P1.

**NN-05 — Exclusion militaire — absolue et sans ambiguïté**
Aucun usage de WildNexus — matériel, logiciel, données, API — n'est autorisé dans des applications militaires ou para-militaires, incluant sans s'y limiter : détection de drones, surveillance de périmètre, reconnaissance de terrain, ou tout usage à finalité défensive ou offensive.
**Justification** : La détection d'animaux nocturnes et la détection de drones reposent sur les mêmes capteurs IR, les mêmes algorithmes, la même architecture réseau. Sans exclusion explicite, le dévoiement est une pente naturelle dès que le produit prouve sa valeur technique.
**Vérifiable par** : clause d'exclusion dans le dispositif juridique retenu ; refus documenté de toute demande partenariat ou financement à provenance militaire ou défense.

**NN-06 — Exclusion des usages non conformes aux valeurs environnementales via politique de licence**
La licence WildNexus exclut contractuellement les usages contraires aux valeurs environnementales et éthiques du projet. La liste des secteurs et usages exclus est définie et maintenue dans la politique de licence — document séparé géré par [[Renard]], opposable aux tiers.
**Vérifiable par** : politique d'usage publiée et référencée dans les distributions ou [[contrats]] pertinents, selon le modèle juridique retenu.

**NN-07 — Autonomie terrain — hiérarchie des cibles**
Trois cibles distinctes doivent être comprises séparément :
- **P0 minimum garanti** : 60 jours sur batterie seule, sans apport solaire — plancher non compressible. Aucune feature P0 ne peut le franchir.
- **Critère de validation P0** : 30 jours de mesure EVT terrain avec extrapolation à 60 jours — méthode de preuve, pas l'ambition.
- **Ambition produit** : 6 mois avec apport solaire et maintenance semestrielle planifiée — cible commerciale, non engagée à P0.
**Justification** : Confondre ces trois cibles produit des promesses non vérifiables ou des critères de validation irréalistes. Le plancher 60 jours batterie-seule est le seul engagement hard de P0.
**Vérifiable par** : budget énergie validé par wildnexus-firmware-ulp et wildnexus-hardware-physical avant gel feature P0 ; mesure terrain EVT avec extrapolation documentée.

**NN-08 — Indépendance financière durant la phase de conception**
Aucune dépendance à un financement externe n'est acceptée pendant la phase de conception et de développement P0.
**Justification** : Introduire un actionnaire ou un bailleur de fonds à ce stade revient à lui donner un droit de veto implicite sur les non-négociables. L'investisseur arrive après le POC — quand le produit parle pour lui-même.
**Vérifiable par** : aucun accord de financement externe signé avant validation du prototype P0 final.

**NN-09 — Protection de la vie privée — personnes capturées par le système**
WildNexus sera inévitablement amené à capturer des images de personnes (randonneurs, propriétaires, chasseurs, techniciens). Ces images constituent des données personnelles au sens du RGPD dès lors qu'elles permettent l'identification directe ou indirecte d'un individu. Le système doit être conçu pour minimiser ce risque dès P0.
**Engagements de conception** : détection locale des silhouettes humaines avec suppression ou floutage avant toute transmission ; aucune image contenant une personne identifiable n'est transmise par défaut ; stockage local chiffré ; durée de rétention limitée et définie ; affichage d'une signalétique conforme au RGPD sur chaque zone déployée.
**Justification** : En l'absence de base légale explicite (consentement, intérêt légitime documenté, mission d'intérêt public), la captation et le traitement d'images de personnes expose JCHYTECH à des sanctions RGPD. Ce risque est gérable par la conception — il ne peut pas être ignoré.
**Owner** : [[Renard]] (base légale, signalétique) + wildnexus-firmware-ulp (détection et suppression embarquée) + wildnexus-program-manager-system-architect (intégration système).
**Vérifiable par** : procédure de détection/suppression humaine documentée et testée avant EVT ; signalétique conforme sur le site EVT.

**NN-10 — Mission de revivification, pas de conservation passive**
WildNexus produit des données structurées pour l'action, pas seulement pour l'observation. Les schémas de données, outputs et interfaces doivent permettre à un utilisateur d'agir sur son territoire en réponse à ce qu'il observe.
**Justification** : La différence entre "conserver" et "revivifier" est la différence entre documenter et intervenir. Un système qui ne produit que des listes d'observations sans contexte d'action reproduit les limites des outils existants.
**Vérifiable par** : au moins un output P1 conçu pour l'aide à la décision ; consultation de wildnexus-scientific-advisor sur la structure des données dès P0.

---

## 6. Objectifs — précis, vérifiables, phasés

> **Conventions** : **[C]** Engagé — l'échec constitue un échec du projet | **[R]** Recherche — résultat incertain | **[E]** Exploratoire — cadré pour l'apprentissage

### 6.1 Phase P0 — Nœud caméra crédible et déployable

**OBJ-01 [C]** — Concevoir et valider un nœud caméra autonome capable de détecter le passage d'un animal, capturer une image utilisable de nuit comme de jour, et transmettre un événement via LPWAN, sur une autonomie minimale de 60 jours sans apport solaire.

**OBJ-02 [C]** — Embarquer un classificateur binaire (animal présent / absent) opérant sur le nœud sans connexion réseau, avec un taux de faux positifs inférieur à un seuil défini lors de la validation terrain EVT.

**OBJ-03 [C]** — Déployer le nœud dans un boîtier IP67, installable seul sans outillage spécialisé, résistant aux conditions terrain belges sur une durée minimale de 3 ans.

**OBJ-04 [C]** — Publier le socle hardware et software avec une documentation suffisante pour qu'un développeur tiers puisse compiler et flasher le firmware sans assistance, sous le modèle de diffusion explicite retenu en NN-02.

**OBJ-05 [C]** — Valider le déploiement en conditions terrain réelles lors d'un EVT d'au moins 30 jours sur un site belge, avec au moins 3 nœuds simultanément actifs.

### 6.2 Phase P1 — Intelligence analytique et valeur scientifique

**OBJ-06 [R]** — Développer et valider un classificateur d'espèces embarqué ou hybride capable d'identifier les espèces faunistiques courantes de Belgique et d'Europe tempérée avec une précision suffisante pour un usage naturaliste.

**OBJ-07 [R]** — Investiguer la faisabilité de la reconnaissance individuelle au sein d'une espèce (marquages naturels, morphologie, comportement) par IA sur les données collectées. Cette phase déterminera si la reconnaissance individuelle est intégrable à P1 ou constitue un objectif P2.

**OBJ-08 [R]** — Concevoir et tester un module d'analyse comportementale sur données accumulées : patterns de déplacement, fréquence de passage, corrélation avec variables environnementales.

**OBJ-09 [R]** — Développer et valider un nœud bioacoustique (variante distincte) capable d'enregistrer, analyser et transmettre des événements sonores faunistiques sur le même socle LPWAN.

**OBJ-10 [R]** — Concevoir un pipeline d'export compatible avec les standards scientifiques ouverts (Camtrap-DP, Darwin Core / GBIF).

### 6.3 Phase P2 — Écosystème et plateforme

**OBJ-11 [E]** — Évaluer la faisabilité d'un maillage LPWAN multi-nœuds sans gateway fixe.

**OBJ-12 [E]** — Évaluer la faisabilité d'une API et d'un SDK publics pour l'intégration dans des systèmes tiers.

**OBJ-13 [E]** — Évaluer les modèles d'animation communautaire pour le développement de modules capteurs additionnels.

### 6.4 Objectif transversal — non-intrusion

**OBJ-14 [C]** — À toutes les phases, le déploiement et le fonctionnement de WildNexus ne doivent pas nécessiter de présence terrain supérieure à une visite initiale de déploiement et une visite de maintenance semestrielle. Non-négociable en zones de tranquillité réglementées.

---

## 7. État de l'art et positionnement

*Note : cette section sera complétée et affinée par la tâche T01.1 (analyse comparative des spécifications concurrentes). Les seuils de performance retenus dans §6 et §11 sont conditionnés à ce livrable.*

### 7.1 Paysage existant

**Pièges photos grand public**
Bushnell, Reconyx, Browning, Stealth Cam. Points forts : robustesse, prix 100–600 €, large adoption. Limites : systèmes fermés, récupération manuelle, aucune intelligence embarquée, aucune interopérabilité. Reconyx (haut de gamme, > 800 €) reste fermé.

**Systèmes connectés propriétaires**
Spypoint Link, Tactacam Reveal, Stealth Cam Connect : carte SIM cellulaire intégrée. Résolvent la récupération manuelle mais introduisent dépendance opérateur, abonnement récurrent, architecture entièrement fermée. Ne fonctionnent pas sans couverture 4G.

**Infrastructures de monitoring scientifique**
Wildlife Insights (Google), Snapshot Safari, Camtrap-DP/GBIF : rigueur scientifique et interopérabilité, mais équipe technique dédiée et budget programme requis. Wildlife Insights propose une IA de classification performante, cloud uniquement, sans composante hardware propre.

**Solutions edge AI faune émergentes**
Conservation X Labs, TrailGuard AI (RESOLVE) : démontrent la faisabilité technique de l'IA embarquée faune, mais solutions sur mesure pour programmes spécifiques — non reproductibles sans expertise, non disponibles en open source généralisable.

**Réseaux de capteurs open source**
RIOT OS, Moteino, TTN : couvrent la connectivité et le firmware. Ne traitent pas la couche caméra, l'imagerie nocturne, ou l'IA faunistique.

### 7.2 Matrice de positionnement

| Dimension | Pièges photos grand public | Systèmes connectés propriétaires | Monitoring institutionnel | WildNexus |
|-----------|---------------------------|----------------------------------|--------------------------|-----------|
| Connectivité longue portée sans opérateur | ✗ | ✗ | Partiel | ✅ |
| Open hardware + software | ✗ | ✗ | Partiel | ✅ |
| Extensibilité capteurs | ✗ | ✗ | ✗ | ✅ |
| IA embarquée (edge) | ✗ | ✗ | Cloud uniquement | ✅ |
| Reconnaissance individuelle / comportement | ✗ | ✗ | Cloud, cas par cas | P1 |
| Prix accessible amateur | ✅ | ✅ | ✗ | ✅ |
| Autonomie 6 mois sans intervention | Partiel | ✗ | Variable | ✅ |
| Non-intrusion (zones de tranquillité) | ✗ | ✗ | ✗ | ✅ |
| Communauté contributrice | ✗ | ✗ | Partiel | ✅ |

### 7.3 Contribution spécifique de WildNexus

La contribution visée par WildNexus est la combinaison : connectivité longue portée, filtrage IA embarqué, open platform, extensibilité et prix accessible dans un produit cohérent, déployable par un non-spécialiste. La vérification de cette combinaison comme différenciation réelle est l'objet de T01.1.

À cela s'ajoute une dimension peu commune : la non-intrusion comme spécification de conception explicite — minimiser la présence terrain post-déploiement pour respecter les zones de tranquillité faunistique.

---

## 8. Méthodologie et approche technique

### 8.1 Approche générale

WildNexus suit une méthodologie de développement itératif validé sur le terrain, organisée en phases distinctes avec des jalons go/no-go explicites. La logique directrice : **construire le minimum crédible d'abord, valider sur le terrain avant d'ajouter de la complexité**. P0 n'est pas un prototype de laboratoire — c'est un système déployable dans des conditions réelles, conçu pour être étendu, pas remplacé.

### 8.2 Architecture système

WildNexus est une plateforme distribuée composée de trois types de nœuds distincts, maintenus séparés à P0 :

| Nœud | Capteur primaire | Énergie | Rôle |
|------|-----------------|---------|------|
| Nœud caméra | PIR + capteur optique + IR | Batterie + solaire | Détection et capture d'événements faunistiques |
| Nœud acoustique | Réseau microphones | Batterie + solaire | Acquisition audio planifiée — variante P1 |
| Gateway | Concentrateur LPWAN | Solaire + filaire | Agrégation et backhaul |

**Règle architecturale P0** : les nœuds caméra et acoustique sont des produits distincts. Leurs profils énergétiques, contraintes d'installation et exigences d'enclos sont incompatibles avec une conception unifiée optimisée. Une fusion est évaluée en P1 uniquement si les données terrain le justifient.

### 8.3 Choix techniques clés et justifications

**Connectivité — LPWAN (candidat prioritaire P0 : [[LoRa]])**
Standard longue portée basse consommation retenu pour le transport des événements. [[LoRa]]/LoRaWAN est le candidat prioritaire P0 pour sa portée en milieu forestier (2-5 km) et sa consommation compatible avec le budget énergie. Ce choix sera validé par une campagne de mesures RF terrain avant M-01. L'interface firmware/radio est abstraite pour permettre la substitution du standard sans refonte système.

**Capteur image — Sony IMX462 ou IMX327 (à confirmer)**
Capteur CMOS haute sensibilité en faible luminosité, compatible imagerie IR nocturne. Le choix final est conditionné à la mesure empirique du temps de boot et du courant actif — les deux variables qui déterminent le budget énergie par événement.

**IA embarquée — deux couches distinctes**
- *Couche 1 — edge P0* : classificateur binaire (animal / non-animal) embarqué sur le nœud, sans connexion. Modèle quantisé, inférence < 200 ms. La classification d'espèces n'est PAS un objectif P0 engagé.
- *Couche 2 — analytique P1* : classification d'espèces (embarquée ou hybride edge/cloud selon validation EVT), reconnaissance individuelle, analyse comportementale sur données accumulées.

**Chimie batterie — LiFePO4**
Stabilité thermique -10 °C / +60 °C, durée de vie 2 000-3 000 cycles, sécurité terrain.

**Enclos — IP67 minimum**
PC/ABS stabilisé UV. Joint EPDM face seal. Fixation sangle cliquet + câble antivol. Maximum 4 vis à l'ouverture.

### 8.4 Hypothèses

1. Portée LPWAN ≥ 1-3 km en milieu forestier belge avec antenne adaptée et puissance légale (EU868).
2. Budget énergie de 30-50 mAh/jour permet 60 jours d'autonomie (batterie < 2 Ah + panneau 2 W).
3. Boot time caméra compatible avec latence de déclenchement < 600 ms.
4. Un naturaliste non-technicien peut déployer un nœud seul en moins de 30 minutes.

### 8.5 Inconnues et méthode de résolution

| Inconnue | Impact | Méthode | Jalon |
|----------|--------|---------|-------|
| Portée LPWAN réelle en forêt belge | Architecture réseau invalide | Campagne RF terrain T01.3 | M-01 |
| Boot time caméra mesuré | Budget énergie incorrect | Benchmark module physique T01.4 | M-01 |
| Faux positifs PIR en conditions réelles | Autonomie réelle < estimée | EVT terrain 30 jours | M-03 |
| LiFePO4 < 0°C conditions hivernales | Autonomie hivernale non garantie | Test IEC 60068-2-1 | M-02 |
| Adoption communautaire open source | Écosystème ne se développe pas | Publication précoce + canal actif dès P0 | M-04 |

### 8.6 Périmètre P0 — ce que P0 est et ce qu'il n'est pas

P0 n'est pas une plateforme biodiversité complète. P0 est un nœud caméra déployable qui prouve :
- Capture d'image autonome jour/nuit avec qualité utilisable
- Filtrage binaire animal/non-animal embarqué
- Transmission de métadonnées d'événement via LPWAN
- Stockage local sécurisé sur SD
- Enclos terrain IP67 et alimentation viables sur 60 jours batterie
- Reproductibilité open source par un tiers sans assistance

**P0 exclut explicitement comme objectifs engagés :**
- Classification d'espèces (P1)
- Reconnaissance individuelle et analyse comportementale (P1)
- Nœud acoustique (P1 — variante distincte)
- Maillage multi-nœuds sans gateway (P2)
- Plateforme cloud scientifique (P1/P2)
- Nœud caméra + acoustique combiné (évalué P1 sur données terrain)
- Export Camtrap-DP / GBIF (P1)

### 8.7 Modèle de données minimum P0

Même si l'export Camtrap-DP est P1, le schéma de données P0 doit être conçu pour la compatibilité future. Chaque événement P0 enregistre au minimum :

| Champ | Description |
|-------|-------------|
| `deviceID` | Identifiant unique du nœud |
| `deploymentID` | Identifiant du déploiement (site + période) |
| `timestamp` | Horodatage avec fuseau horaire (ISO 8601) |
| `location` | Coordonnées GPS fixes ou déclarées à l'installation |
| `triggerType` | PIR / scheduled / manual |
| `illuminationMode` | IR 850nm / IR 940nm / visible / aucun |
| `batteryVoltage` | Tension batterie au moment de l'événement (mV) |
| `firmwareVersion` | Version du firmware actif |
| `modelVersion` | Version du modèle IA embarqué |
| `eventConfidence` | Score de confiance du classificateur binaire (0–1) |
| `mediaPath` | Chemin relatif du fichier image sur SD |
| `humanDetected` | Booléen — suppression activée si true (RGPD NN-09) |

Ce schéma est défini par wildnexus-scientific-advisor et freezé avant WP03 pour garantir la compatibilité Camtrap-DP en P1.

### 8.8 Sécurité du système P0

La sécurité est une spécification P0, pas une option P1. Les exigences minimales :

| Domaine | Exigence |
|---------|----------|
| Firmware | Signature cryptographique de chaque image firmware ; boot refusé si signature invalide |
| Mise à jour OTA | Canal chiffré ; rollback automatique si signature échoue |
| Configuration BLE | Appairage avec authentification ; pas de configuration en clair non appairé |
| Stockage SD | Chiffrement des images sensibles (humains détectés) ; clé dérivée du deviceID |
| Clés | Stockage en zone sécurisée MCU (secure element ou eFuse) ; non extractibles |
| Comportement anti-falsification | Log d'intégrité ; alerte transmission si falsification détectée |

Owner : wildnexus-firmware-ulp (implémentation) + [[Renard]] (obligations légales et cohérence contractuelle).

---

## 9. Propriété intellectuelle

### 9.1 Principes directeurs

La stratégie IP de WildNexus est défensive et éthique, non offensive. L'objectif n'est pas de bloquer l'innovation ni de générer des revenus de licence — c'est de protéger la mission contre les dévoiements et de garantir que le socle ouvert reste ouvert.

### 9.2 Freedom to Operate (FTO)

Avant tout développement engageant sur les composants critiques, une analyse FTO est conduite pour vérifier l'absence de brevets tiers opposables.

**Périmètre minimal de vérification :**

| Domaine | Éléments à vérifier |
|---------|---------------------|
| Imagerie nocturne + IR | Déclenchement PIR + capture IR pulsée synchronisée |
| IA embarquée faune | Classification d'espèces on-device, reconnaissance individuelle |
| Communication LPWAN | Architecture réseau événementiel longue portée pour monitoring environnemental |
| Enclos autonome terrain | Alimentation hybride batterie/solaire pour capteurs déployés |

L'analyse FTO est un livrable de WP01, conduite avant M-01. Confiée à [[Renard]] avec appui cabinet spécialisé si nécessaire. Aucun composant litigieux n'est intégré sans avis FTO favorable ou contournement documenté.

### 9.3 Stratégie brevet — défensive et éthique

**Ce que les brevets permettent :**
- Accorder des licences conditionnelles aux valeurs du projet
- Opposer juridiquement les clauses d'exclusion à des tiers
- Protéger la communauté contre un rachat ou une appropriation fermante

**Ce que les brevets ne visent pas :**
- Bloquer des contributeurs conformes à la mission
- Générer des revenus de licence comme modèle principal
- Créer une barrière à l'entrée communautaire

**Périmètre de dépôt envisagé** (à affiner après FTO et conseil [[Renard]]) : couche IA embarquée faune, architecture de communication événementielle basse consommation, mécanismes d'extensibilité capteurs.

### 9.4 Politique de licence

**Modèle de diffusion retenu :** publication du hardware et du software sous un régime `source-available / ethical-source`. Le code, les schémas et la documentation sont publiés, consultables, auditables et modifiables, mais leur usage reste contractuellement limité par la politique WildNexus.

**Exclusions d'usage :** les usages militaires, para-militaires ou contraires à la mission biodiversité sont interdits dans la licence cœur et dans la politique d'usage associée. Les [[contrats]] partenaires et commerciaux reprennent ces exclusions à l'identique.

**Licences commerciales :** possibles seulement si elles restent compatibles avec les non-négociables, reprennent les exclusions d'usage, et ne recréent pas une fermeture artificielle du socle.

### 9.5 Gouvernance IP et FTO

**[[Renard]]** pilote la rédaction contractuelle, la politique de diffusion, les accords partenaires et distributeurs, ainsi que la base légale RGPD liée aux usages terrain.

**Conseil [[Pi]] externe** : mobilisé si nécessaire pour T01.2, pour l'analyse FTO, la stratégie de dépôt défensif post-POC et la surveillance du portefeuille.

**Partition claire** : [[Renard]] structure le dispositif juridique et contractuel ; le conseil [[Pi]] externe intervient comme expertise spécialisée sur les brevets et la FTO ; JCH valide toute décision qui modifie l'équilibre entre diffusion, exclusions d'usage et protection de la mission.

**Première mission avant M-01** : formaliser le modèle `source-available / ethical-source` retenu, avec vocabulaire public, licences, [[contrats]] et politique d'usage alignés.

---

## 10. Work packages, tâches, livrables, jalons

*Les work packages couvrent la phase P0. P1 et P2 feront l'objet d'un addendum après M-04.*

### WP01 — Conception & Architecture

| Champ | Contenu |
|-------|---------|
| **Objectif** | Geler l'architecture système P0 sur des bases vérifiées |
| **Durée** | 2 mois |
| **Dépendances** | Aucune |
| **Owner** | JCH + wildnexus-program-manager-system-architect |

**Tâches :**
- T01.1 — Analyse comparative des spécifications concurrentes → tableau comparatif consolidé (calibration §6 et §11)
- T01.2 — Analyse FTO sur composants critiques ([[Renard]])
- T01.3 — Campagne mesures RF terrain : portée LPWAN réelle, sélection standard
- T01.4 — Benchmark module caméra IMX462 vs IMX327 : boot time mesuré, courant actif
- T01.5 — Sélection MCU : arbitrage wildnexus-firmware-ulp

**Livrables :** D01.1 Tableau comparatif concurrents · D01.2 Rapport FTO · D01.3 Rapport RF + standard retenu · D01.4 Fiche benchmark caméra · D01.5 Architecture P0 gelée

> **M-01 — Architecture P0 gelée** : FTO favorable, standard radio validé, module caméra sélectionné, MCU retenu. **Go** → WP02+03+04 démarrent. **No-go** → réévaluation composants bloquants.

---

### WP02 — Hardware & Enclos

| Champ | Contenu |
|-------|---------|
| **Objectif** | Concevoir et fabriquer le premier prototype PCB fonctionnel en boîtier IP67 |
| **Durée** | 3 mois |
| **Dépendances** | M-01 |
| **Owner** | wildnexus-hardware-physical + wildnexus-camera-imaging + wildnexus-firmware-ulp |

**Tâches :**
- T02.1 — Schéma électronique : alimentation, rails caméra, IR pulsé, LPWAN, BLE, capteurs env.
- T02.2 — Layout PCB : chemin IR LED synchronisé, power gate, antenne
- T02.3 — CAO enclos : port optique, joint EPDM, fenêtre AR, fixation
- T02.4 — Fabrication PCB prototype (5 exemplaires)
- T02.5 — Assemblage et tests banc

**Livrables :** D02.1 Schémas électroniques (open hardware) · D02.2 Fichiers PCB (Gerber + BOM) · D02.3 Fichiers CAO enclos · D02.4 5 prototypes testés banc

> **M-02 — Prototype banc fonctionnel** : boot caméra < 600 ms, autonomie estimée ≥ 60 jours, transmission LPWAN opérationnelle. **Go** → WP05 EVT. **No-go** → itération hardware.

---

### WP03 — Firmware ULP

| Champ | Contenu |
|-------|---------|
| **Objectif** | Firmware P0 : veille, déclenchement, capture, IA binaire, transmission, OTA |
| **Durée** | 3 mois (parallèle WP02) |
| **Dépendances** | M-01 |
| **Owner** | wildnexus-firmware-ulp |

**Tâches :**
- T03.1 — Machine à états : sleep / wake / PIR / boot caméra / capture / inférence / transmit / sleep
- T03.2 — Pilote caméra MIPI + power gate synchronisé
- T03.3 — Gestion BMS + MPPT + undervoltage lockout hardware
- T03.4 — Interface BLE configuration terrain
- T03.5 — Mécanisme OTA

**Livrables :** D03.1 Firmware P0 (dépôt open source) · D03.2 Protocole communication LPWAN · D03.3 Procédure configuration BLE

---

### WP04 — Edge AI

| Champ | Contenu |
|-------|---------|
| **Objectif** | Entraîner, quantiser et valider le classificateur binaire embarqué |
| **Durée** | 2 mois (parallèle WP02/03) |
| **Dépendances** | M-01 (MCU retenu) |
| **Owner** | wildnexus-edge-ai-cv |

**Tâches :**
- T04.1 — Dataset images IR nocturnes faune belge
- T04.2 — Entraînement et quantisation modèle binaire
- T04.3 — Validation : taux détection, faux positifs, latence sur MCU cible
- T04.4 — Intégration firmware WP03

**Livrables :** D04.1 Dataset annoté (open data) · D04.2 Modèle quantisé + métriques · D04.3 Rapport validation AI

---

### WP05 — Validation terrain (EVT)

| Champ | Contenu |
|-------|---------|
| **Objectif** | Valider le prototype P0 en conditions réelles, 30 jours minimum, site belge |
| **Durée** | 2 mois |
| **Dépendances** | M-02 |
| **Owner** | JCH + wildnexus-scientific-advisor |

**Tâches :**
- T05.1 — Sélection et préparation site EVT
- T05.2 — Déploiement 3 nœuds (installation chronométrée, objectif < 30 min/nœud)
- T05.3 — Monitoring continu 30 jours
- T05.4 — Collecte et analyse données
- T05.5 — Rapport EVT + liste corrections

**Livrables :** D05.1 Rapport EVT · D05.2 Dataset terrain annoté · D05.3 Liste actions correctives

> **M-03 — EVT validé** : autonomie ≥ 60 jours extrapolée, faux positifs < seuil défini, aucune défaillance mécanique/étanchéité. **Go** → DVT + corrections. **No-go** → retour WP02/03.

---

### WP06 — Open source & Communauté

| Champ | Contenu |
|-------|---------|
| **Objectif** | Publier le socle open source et amorcer l'engagement communautaire dès P0 |
| **Durée** | Continu depuis M-01 |
| **Dépendances** | D01.2 (FTO favorable avant publication) |
| **Owner** | JCH + wildnexus-program-manager-system-architect |

**Tâches :**
- T06.1 — Création dépôt public : firmware, schémas, BOM, documentation
- T06.2 — Documentation contribution (CONTRIBUTING.md, interface capteur)
- T06.3 — Canal communautaire (forum, Discord, ou équivalent)
- T06.4 — Stratégie visibilité sociale ([[Miel]]) : EVT documenté comme contenu communautaire

**Livrables :** D06.1 Dépôt open source public · D06.2 Documentation contribution · D06.3 Canal communautaire actif

> **M-04 — Open source publié, communauté amorcée** : dépôt public, documentation lisible par un tiers, premier contributeur externe actif. **Go** → P1.

---

### Séquence des jalons P0

```
M-01 Architecture gelée
    ↓
M-02 Prototype banc fonctionnel  (WP02 + WP03 + WP04 en parallèle)
    ↓
M-03 EVT terrain validé  (WP05)
    ↓
M-04 Open source publié  (WP06)
    ↓
Décision entrée P1
```

---

## 11. Plan de validation

| Objectif | Critère de succès | Seuil | Méthode | Condition d'échec |
|----------|------------------|-------|---------|-------------------|
| OBJ-01 Autonomie | Courant moyen sur cycle complet | ≤ 33 mAh/jour | Mesure banc + extrapolation EVT | < 45 jours extrapolés → retour WP02/03 |
| OBJ-01 Latence | PIR trigger → image capturée | < 600 ms | Chronométrage 50 événements labo | > 800 ms sur > 10 % → refonte power gate |
| OBJ-01 Qualité image | Utilisable pour identification à 5 m | 70 % images jugées utilisables | 50 images EVT évaluées en aveugle | < 70 % → révision IR ou objectif |
| OBJ-02 Classificateur | Détection animaux / faux positifs | Détection > 90 % / FP < 15 % | Test sur dataset EVT annoté | FP > 30 % → réentraînement |
| OBJ-03 Étanchéité | Intégrité après immersion 30 min 1 m | Zéro infiltration | Test IEC 60529 IP67 sur 3 enclos | Infiltration → refonte joint |
| OBJ-03 Durée vie matériaux | Absence dégradation après 3 mois EVT | Pas de fissure/déformation | Inspection visuelle post-EVT | Dégradation → changement grade |
| OBJ-03 Installation solo | Déploiement par non-technicien | < 30 minutes/nœud | Test 3 profils non-techniciens | > 45 min ou erreur → révision doc |
| OBJ-04 Open source | Compilable par tiers | Compilation sans assistance sur 3 env. | Test 3 développeurs externes naïfs | Échec → révision documentation |
| OBJ-05 EVT | 3 nœuds actifs 30 jours continus | 0 défaillance critique, données ≥ 90 % | Log transmission + inspection J+30 | Perte > 20 % ou défaillance → M-03 bloqué |
| OBJ-14 Non-intrusion | Interventions terrain hors déploiement | 0 intervention non planifiée sur 30 jours | Log incidents + journal terrain | Intervention < J+15 → autonomie/firmware insuffisant |

### Validation standard LPWAN (T01.3)

| Critère | Seuil | Méthode |
|---------|-------|---------|
| Portée forêt dense | ≥ 1 km avec gateway unique | Mesure RSSI sur parcours forestier balisé |
| Consommation émission | Compatible 33 mAh/jour avec 48 événements/jour | Mesure courant pic + durée émission |
| Conformité EU868 | Duty cycle respecté | Vérification firmware + calcul charge réseau |

---

## 12. Registre des risques

*P = Probabilité (H/M/L) — I = Impact (H/M/L)*

### Risques techniques

| Risque | P | I | Mitigation | Fallback |
|--------|---|---|-----------|---------|
| Portée LPWAN insuffisante en forêt belge | M | H | Campagne RF terrain avant M-01 | Substitution standard ou gateway rapproché |
| Boot time caméra > 600 ms | M | H | Benchmark empirique T01.4 avant gel | Module alternatif ; warm-standby partiel |
| Autonomie < 60 jours conditions hivernales | M | H | Test LiFePO4 < 0°C avant EVT | Augmentation capacité batterie |
| Faux positifs PIR > 30 % terrain | M | M | Classificateur IA comme second filtre | Ajustement seuil + réentraînement |
| Infiltration enclos après 30 jours | L | H | Test IP67 systématique sur chaque lot | Refonte joint EPDM |
| Consommation IA > budget énergie événement | L | M | Profiling énergie modèle quantisé avant intégration | Réduction complexité modèle |

### Risques supply chain & ressources

| Risque | P | I | Mitigation | Fallback |
|--------|---|---|-----------|---------|
| Module caméra indisponible ou délai > 3 mois | L | H | Sourcing anticipé dès M-01 ; second fournisseur identifié | Module alternatif benchmarké en T01.4 |
| Composants LPWAN en rupture | M | M | Stock précaution sur composants critiques | Standard alternatif évalué en T01.3 |
| Dépassement budget WP02 | M | M | BOM chiffré avant fabrication | Réduction prototypes EVT |

### Risques timeline

| Risque | P | I | Mitigation | Fallback |
|--------|---|---|-----------|---------|
| WP02 et WP03 non synchronisés à M-02 | M | M | Points synchronisation hebdomadaires | Firmware sur dev board si PCB retardé |
| EVT retardé météo ou accès site | L | L | Site identifié et autorisé avant M-02 | Second site de secours |
| FTO révèle brevet bloquant | L | H | FTO lancé en parallèle dès WP01 J+1 | Contournement technique ou dépôt défensif |

### Risques externes & mission

| Risque | P | I | Mitigation | Fallback |
|--------|---|---|-----------|---------|
| Dévoiement militaire ou para-militaire | L | H | Clause d'exclusion dans le dispositif juridique retenu dès D06.1 ; [[Renard]] + validation JCH | Révocation licence ou rupture contractuelle ; action juridique |
| Appropriation open source refermée | M | M | Modèle de diffusion clarifié avant M-01 | Surveillance forks ; réaction communautaire |
| Absence adoption communautaire | M | M | Canal actif avant publication ; EVT documenté ([[Miel]]) | Réseau bêta-testeurs naturalistes ciblés |
| Concurrent direct open source avant M-04 | L | M | Publication anticipée dès FTO validé | Contribution au projet concurrent si supérieur |
| Non-conformité RGPD (capture de personnes) | M | H | NN-09 : détection + suppression embarquée avant transmission ; signalétique EVT ; avis [[Renard]] | Désactivation transmission images jusqu'à conformité documentée |
| Tension NN-02 / NN-05/06 non résolue avant publication | M | H | Arbitrage licence prioritaire avant M-01 | Publication différée jusqu'à arbitrage juridique documenté |

---

## 13. Budget et logique de ressources

### 13.1 Modèle de financement P0

WildNexus est intégralement autofinancé par JCHYTECH durant la phase P0, conformément à NN-08. Un investisseur peut être sollicité après validation DVT, sur la base d'un produit terrain démontré.

### 13.2 Logique de budget par work package

| WP | Catégorie | Poste dominant | Ordre de grandeur |
|----|-----------|----------------|------------------|
| WP01 | Études & conseil | FTO ([[Renard]] + cabinet) + benchmark | Moyen |
| WP02 | Hardware | Fabrication PCB + enclos prototype | Élevé |
| WP03 | Développement | Temps JCH + outillage firmware | Faible |
| WP04 | IA & données | Dataset + compute entraînement | Moyen |
| WP05 | Terrain | Déplacement + site EVT + mesure | Faible |
| WP06 | Communauté | Infrastructure dépôt + communication | Très faible |

*Les montants précis sont définis dans le budget opérationnel JCHYTECH — document séparé, non inclus dans la bible publique.*

> **Note v0.2** : La cible de 900 € TTC (NN-01) nécessite un modèle de coût lié pour être un engagement d'ingénierie plutôt qu'une valeur déclarative. Ce modèle sera produit après D02.2 (BOM WP02) et intégré en §13 v0.3 : BOM + assemblage + enclos + certification CE/RoHS + garantie + TVA + marge distribution + support.

### 13.3 Budget minimum pour atteindre M-03

Le jalon critique est M-03 (EVT validé) — premier moment où WildNexus peut démontrer sa valeur à un tiers avec des données terrain réelles. Le budget minimum couvre WP01 complet + WP02 (5 prototypes) + WP03 + WP04 + WP05 partiel. En dessous de ce seuil, le projet ne produit pas de preuve suffisante pour une conversation investisseur.

### 13.4 Ce qu'un investisseur post-POC débloque

| Investissement | Ce que cela accélère |
|---------------|---------------------|
| Industrialisation enclos (injection) | Réduction coût unitaire série, DVT propre |
| Dataset P1 (espèces, individus) | Classificateur espèces + reconnaissance individuelle |
| Ressource développement communauté | Animation WP06, documentation, premiers partenariats |
| Certification CE, RoHS | Condition de mise sur le marché européen |

---

## 14. Outputs attendus et impact

### 14.1 Outputs

| Output | Phase | Nature |
|--------|-------|--------|
| Prototype nœud caméra P0 validé terrain | P0 | Hardware + firmware |
| Socle open source publié | P0 | Dépôt public, licence ouverte |
| Dataset images IR faune belge annoté | P0 | Données ouvertes |
| Rapport EVT terrain | P0 | Document technique |
| Classificateur binaire embarqué quantisé | P0 | Modèle IA open source |
| Protocole communication événementielle LPWAN | P0 | Spécification ouverte |
| Classificateur d'espèces faune européenne | P1 | Modèle IA |
| Module reconnaissance individuelle + comportement | P1 | Modèle IA + interface |
| Nœud acoustique validé | P1 | Hardware + firmware |
| Pipeline export Camtrap-DP / GBIF | P1 | Software |

### 14.2 Outcomes

- Un naturaliste amateur déploie seul un réseau de monitoring sans compétence technique spécialisée
- Un gestionnaire de réserve suit la faune sans perturber les zones de tranquillité sur 6 mois continus
- Un chercheur exporte des données WildNexus vers GBIF sans retraitement manuel
- Un développeur tiers intègre un capteur additionnel sans impliquer l'équipe WildNexus

### 14.3 Impact

**Écologique** : réduction de la perturbation humaine dans les zones sensibles ; données de présence plus denses et continues pour les décisions de gestion et de restauration.

**Scientifique** : démocratisation du monitoring faunistique rigoureux à l'échelle du naturaliste individuel ; contribution aux bases de biodiversité par un nouveau réseau de contributeurs équipés.

**Communauté** : émergence d'un écosystème open source autour du monitoring faunistique distribué — capteurs additionnels, algorithmes, interfaces — développé par et pour naturalistes et makers.

**Marché** : démonstration qu'un produit ouvert, extensible et éthique peut occuper le segment intermédiaire entre le piège photo grand public et l'infrastructure institutionnelle, de façon viable commercialement sans sacrifier les valeurs du projet.

---

## 15. Conditions de sortie et critères de pivot

*Cette section protège le projet du biais du coût irrécupérable. Elle est écrite à froid, avant que l'investissement émotionnel et financier ne rende les mauvaises nouvelles difficiles à entendre.*

### 15.1 Conditions d'arrêt du projet

Le projet WildNexus est arrêté si l'une des conditions suivantes est atteinte :

- **Blocage FTO insurmontable** : brevet tiers bloquant sur un composant central, sans contournement technique viable ni licence compatible avec les valeurs du projet
- **Autonomie structurellement insuffisante** : après deux itérations hardware, l'autonomie mesurée ne peut dépasser 30 jours sans compromettre le format ou le prix au-delà de NN-01
- **Épuisement du budget avant M-03** sans résultat démontrable permettant d'ouvrir une conversation partenaire ou investisseur
- **Violation d'un non-négociable** : si une contrainte externe impose de franchir une ligne de §5, le projet s'arrête plutôt que de compromettre ses valeurs fondatrices

### 15.2 Critères de pivot

Un pivot radical est déclenché si :

- **Standard radio invalidé** : tous les standards LPWAN évalués sont insuffisants — pivot vers architecture hybride (cellulaire en zones couvertes, LPWAN en zones reculées)
- **IA binaire insuffisante** : le classificateur P0 ne réduit pas les faux positifs sous le seuil — pivot vers stockage local uniquement, IA reléguée en P1
- **Absence d'adoption communautaire** après 6 mois de publication — pivot vers réseau fermé de bêta-testeurs naturalistes, open source différé
- **Concurrent direct supérieur émergent** : évaluation d'une contribution au projet concurrent plutôt que de maintenir WildNexus en parallèle — la mission prime sur l'ego du projet

### 15.3 Ce qui ne constitue pas un motif de pivot

- Des délais sur le calendrier P0 : les jalons sont des cibles, pas des ultimatums
- Des difficultés techniques résolues par une itération supplémentaire
- L'absence d'investisseur après M-03 : le projet continue en autofinancement si les ressources le permettent
- Une demande partenaire incompatible avec les non-négociables : la demande est refusée, pas le projet

---

*Document fondateur WildNexus — DRAFT v0.2 — 2026-05-17*
*Consolidé par [[Dobby]] 🦉 — orchestration documentaire PKA_JCH*
*Propriétaire : Jean-Claude Havaux — JCHYTECH*

**Changelog v0.1 → v0.2 :**
- Autonomie : hiérarchie explicite des trois cibles (60j batterie / 30j EVT / 6 mois produit)
- Edge AI : claims corrigés — filtrage binaire P0, classification espèces P1
- NN-02 : tension open source / exclusions d'usage clarifiée ; terminologie publique conditionnée au modèle juridique réel
- NN-09 ajouté : privacy RGPD — personnes capturées
- NN-07 : hiérarchie autonomie explicitée
- §2.3 allégé (overlap avec §4.2 réduit)
- Claims "aucun / premier" softened — conditionnés à T01.1
- §8.6 ajouté : périmètre P0 (ce que P0 est / n'est pas)
- §8.7 ajouté : modèle de données minimum P0 (12 champs)
- §8.8 ajouté : sécurité système P0 (firmware signé, OTA chiffré, BLE auth, stockage)
- §9 : gouvernance IP recentrée sur [[Renard]] + conseil [[Pi]] externe si nécessaire
- §12 : 2 nouveaux risques (RGPD, tension licence)
- §13 : note modèle de coût lié au prix cible 900 €
- Table des matières et owners alignés sur les agents WildNexus cibles
*Prochaine révision v0.3 : après T01.1 (analyse concurrents), D01.2 (FTO/conseil [[Pi]]), T01.3 (RF terrain), D02.2 (BOM → modèle coût §13)*

# WildNexus — Protocole de lancement

**Version :** v0.5
**Date :** 2026-11-05
**Vérifié :** 2026-11-12 — P0 engineering repris (décision JCH), dégel confirmé au pilotage, gates de reprise à lever
**Statut :** REPRIS — P0 engineering (2026-11-11) ; dégel confirmé au pilotage le 2026-11-12 ; les travaux matériels restent soumis aux gates de reprise
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Pilotage :** [[Dobby]]

## 1. Intention

Ce document définit le comportement attendu de [[Dobby]] quand JCH active WildNexus : sources à lire, état réel, ordre de reprise, preuves attendues et points nécessitant un arbitrage.

Principe directeur :

> JCH doit voir les décisions, les risques et les preuves. [[Dobby]] absorbe le suivi, la coordination et la maintenance opérationnelle.

Un test sur ordinateur hôte n'est pas un test sur ESP32-S3. Une architecture acceptée n'est pas une performance mesurée. Une fiche produit n'est pas une annonce commerciale.

## 2. Sources de vérité

### 2.1 Fondation et décisions

- `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` — périmètre P0 v0.5 et matrice exigence → preuve.
- `00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md` — philosophie d'ingénierie.
- `HISTORIQUE/01_FOUNDATION/MASTER_ARCHITECTURE_WN.md` — vision initiale, à lire comme cadrage historique.
- `HISTORIQUE/01_FOUNDATION/wildnexus-founding-document-v0.2.md` — brouillon fondateur non validé, pas source d'état actuel.
- `02_DECISIONS/WILDNEXUS_ADR_INDEX.md` — 16 ADR rédigés : 13 acceptés, 1 accepté sous réserve (ADR-010), 2 proposés (ADR-006/011).
- ADR-015 n'est pas rédigé ; ADR-018 reste à produire avant les exigences terrain de synchronisation temporelle.

Ordre d'autorité en cas de contradiction : décision explicite JCH, non-négociables validés, ADR acceptés, documents de pilotage, SOP et skills. Toute contradiction de fond devient une décision documentée.

### 2.2 État et ingénierie

- `03_P0_ENGINEERING/PROTOCOLES/progress.md` — état des protocoles, sans déduire un succès d'un simple artefact.
- `03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/WP03_BUDGET-ENERGIE_ET_GATE-60J.md` — modèle énergétique à compléter par mesures.
- `03_P0_ENGINEERING/07_PROCUREMENT_BOM/` — BOM et stock à rapprocher des commandes.
- `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md` — enveloppe et projection provisoire.
- `firmware/` — structure ESP-IDF et modules avec tests hôte historiques ; validation matérielle non acquise.
- Plane `03_WILDNEXUS` et `JCH_Inbox/01_DASHBOARDS/kanban.html` — vues de pilotage à synchroniser à la reprise.

## 3. État actuel au 2026-11-05

### 3.1 Jalons

| Jalon | État réel |
|-------|-----------|
| M-01 — Cadrage architecture | Documentation initiale réalisée ; 16 ADR rédigés, mais plusieurs validations matérielles restent ouvertes |
| M-02 — Prototype banc fonctionnel | Repris (2026-11-11) : phases A→C faites ; D→E et validations SOP-06 à SOP-18 non terminées |
| M-03 — Prototype terrain | Non commencé ; dépend de M-02, ADR-010/018 et du boîtier |
| M-04 — Industrialisation/pré-séries | Non commencé ; DVT, conformité, coûts et industrialisation à planifier après M-03 |

Aucune date trimestrielle n'est conservée : la reprise sera planifiée à partir du signal de JCH et des prérequis disponibles.

### 3.2 Work packages

| WP | Contenu | État au 2026-11-05 |
|----|---------|--------------------|
| WP01 — Architecture & ADR | Scope, choix et preuves | Cadrage révisé ; pas une certification du produit |
| WP02 — Hardware nœud | Alimentation, capteurs, média et BOM | En pause ; références micros/PIR et schéma d'alimentation à vérifier |
| WP03 — Énergie & mesure | PPK2, modèle Wh, gate 60 jours | Phases A→C mesurées ; budget complet et scénarios non validés |
| WP04 — Firmware | Cycles, SD, LoRa, audio et IA | 37/37 tests hôte consignés en juillet ; pas de validation matérielle équivalente |
| WP05 — Connectivité | Radio, codec, réception et journal gateway | Codec hôte seulement ; radio non commandée et chaîne de bout en bout absente |
| WP06 — Boîtier & terrain | Étanchéité, fixation et EVT | En attente ; cible IP67 non validée |

### 3.3 Matériel et achats — dernier état connu à revalider

| Équipement | État consigné | Référence / précision |
|------------|---------------|----------------------|
| ESP32-S3-DevKitC-1 N16R8 ×2 | Reçu | Amazon MiMiU, 21,98 € |
| Nordic PPK2 | Reçu | Mouser #39411684 ; 83,57 € enregistré, HT/TTC à rapprocher ; ne pas le compter deux fois |
| Mouser #39492997 | Reçu | MEMS, IR, PIR, buck, BME688, SHT31, antennes — 128,20 € |
| ESP32-CAM OV2640 ×2 et cartes seules ×4 | Reçu | Environ 25 € pour les deux avec caméra ; autres montants à retrouver |
| OV5640 DVP M12 ×5 | Reçu | Camemake + AliExpress, environ 30 € dans le suivi visible |
| USB-C TTL FT232RL ×3 | Reçu | AZDelivery, 9 € |
| Miuzei Starter Kit | Reçu | 35 € dans le suivi visible |
| Micros MEMS | Reçus | Le stock/générateur mentionne des TDK ; interface et datasheet à confirmer avant de les déclarer compatibles I2S |
| PIR EKMB | Reçus | EKMB1203111 dans le générateur contre EKMB1303111 dans les documents : référence physique à relever |
| Carte microSD 128 GB | À confirmer / acheter | Environ 15 € dans la projection, non considérée comme reçue |
| Panier Mouser restant | À revalider avant commande | Environ 279 €, incluant radio et connectique ; prix et contenu peuvent avoir changé |

### 3.4 Budget provisoire

- Enveloppe ferme : **1 000 €**.
- Engagé global consigné dans l'ancien état : **environ 610 €**, à réconcilier avec les factures.
- Reliquat estimé : **environ 279 € + 15 €**.
- Projection provisoire : **environ 904 €** ; réserve théorique : **environ 96 €**.
- La projection dépasse le seuil interne d'arbitrage de 900 € : aucune nouvelle commande avant réconciliation et décision JCH.

Ces montants ne sont pas un total comptable certifié. Le sous-total des seules lignes visibles dédupliquées et l'écart à documenter figurent dans le budget P0.

## 4. Reprise au signal `go`

### 4.1 Contrôle initial

1. Lire `progress.md`, le scope lock, l'index ADR, le budget et le stock réel.
2. Rapprocher commandes, factures, montants HT/TTC et matériel physiquement disponible.
3. Vérifier que Plane et le kanban reflètent l'état repris ; synchroniser sans créer de doublons.
4. Replanifier les tâches avec des dépendances et des preuves, sans réutiliser les échéances dépassées de juillet.
5. Vérifier les datasheets et schémas avant toute alimentation ou soudure.

### 4.2 Ordre technique recommandé

1. **Sécurité électrique :** SOP-10 reste suspendue. Ne pas assembler de pack 4S2P L91 ni appliquer 3,3 V sur la broche 5 V avant validation ADR-005 et schéma complet.
2. **Références :** confirmer l'interface des micros TDK et la référence PIR ; adapter SOP-13, le BOM et le pinout si nécessaire.
3. **Socle banc :** reprendre phases D/E, SOP-06, CAM-01/02 et SOP-08/09 sur matériel identifié.
4. **Audio réel :** exécuter SOP-13 puis SOP-14/15 sur fichiers produits par le nœud ; SOP-17/18 ensuite.
5. **IA :** constituer le dataset et comparer les modèles compatibles ; CAM-03/SOP-11 mesurent le modèle retenu, sans imposer MobileNet-SSD.
6. **Connectivité :** commander seulement après arbitrage, exécuter SOP-07 et livrer la gateway P0 : réception, décodage caméra/spectral, journal et gestion des erreurs.
7. **Intégration :** mesurer le cycle complet en Wh, puis préparer boîtier et EVT ; aucune promesse de 60 jours ou IP67 avant preuve.

### 4.3 Preuves de clôture M-02

La matrice du scope lock v0.5 fait foi. En particulier :

- les tests hôte FW-02 à FW-05 ne ferment pas les tests matériels correspondants ;
- SOP-16 valide seulement le codec spectral sur hôte, pas la transmission LoRa ;
- la gateway doit avoir effectivement reçu et journalisé les deux types de paquets ;
- les clips doivent être lus depuis une carte SD alimentée par le nœud et testés dans les pipelines cibles ;
- le coût énergétique de l'IA, des IR, de la SD, de l'audio et des retransmissions doit être inclus.

## 5. Coordination et automatisation

[[Dobby]] coordonne les compétences nécessaires dans des sessions ou skills dédiés : firmware, hardware, radio, optique, bioacoustique, IA, données, budget et juridique. Les rôles d'équipe ne remplacent pas une revue indépendante ni une mesure.

À chaque reprise ou changement structurel :

- mettre à jour `progress.md`, ce fichier, le stock et le budget selon les preuves ;
- régénérer le BOM Excel uniquement depuis sa source active, après vérification du générateur ;
- tracer décision, propriétaire, blocage, preuve et prochaine action ;
- maintenir les documents commerciaux distincts des résultats techniques ;
- exécuter `graphify update .` après modification du projet.

## 6. Escalade à JCH

JCH arbitre les non-négociables, dépenses, compromis coût/délai/performance, usages sensibles, engagements juridiques et risques terrain. Les corrections mécaniques et la clarification de l'état réel ne nécessitent pas d'escalade.

### Décisions actées le 2026-11-05

- Firmware sous **MIT + politique éthique `ETHICS.md`** ; la portée juridique du texte éthique et les autres licences restent à documenter avant publication.
- Prix FIELD 149–179 € et marge 40 % **retirés provisoirement** jusqu'au BOM et au coût complet.

### Points encore ouverts

| Point | Pourquoi il reste ouvert |
|-------|--------------------------|
| Pack et régulateur | Tension maximale, pics, courant, rendement et câblage non validés |
| Micros et PIR | Références physiques/datasheets à rapprocher du stock |
| Optique nocturne | Lentille IR-corrigée et coût réel non consolidés |
| Radio et gateway | Contenu/prix du panier à revalider ; preuve de bout en bout absente |
| Budget | Engagé global de 610 € et projection de 904 € non encore rapprochés de toutes les factures |
| Licence et publication | Texte MIT/ETHICS, notices tierces, hardware/docs/modèles/données et revue juridique |
| Planning | Go donné le 2026-11-11 ; roadmap relative à produire |
| RGPD et terrain | Base légale, conservation, signalétique, droit d'accès et sécurité avant M-03 |

---

*Révision 2026-11-05 : état gelé explicite, comptage ADR corrigé, validations hôte distinguées du matériel, SOP-10 suspendue, gateway P0 ajoutée, budget provisoire dédupliqué et décisions licence/prix enregistrées.*
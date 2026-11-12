# ADR-010 — Sécurité, Chiffrement et RGPD Edge AI

**Date :** 2026-06-06
**Dernière mise à jour :** 2026-11-05 (cohérence transport, conservation humaine et benchmark IA)
**Statut :** accepté sous réserve — 2026-06-08
**Points de réserve :** diversification de clé par nœud (→ ADR-011), choix de licence éthique précis (→ [[Hermine]] + [[Renard]]), procédure droit d'accès RGPD (→ [[Renard]]), benchmark Edge AI réel (→ [[Forge]] + [[Nova]])
**Owner PKA :** [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]]
**Jalon :** M-02 Prototype banc (filtrage humain) · M-03 Firmware ULP (chiffrement SD)

## Contexte

WildNexus est un réseau d'observation déployé en milieu naturel ouvert. Il peut capturer accidentellement des silhouettes humaines (randonneurs, agents forestiers). Les captures peuvent être stockées sur carte SD locale ; LoRa ne transporte que des métadonnées et alertes, jamais les images ou les clips audio. L'objectif d'ouverture du code, dont la licence reste à finaliser, ne supprime ni les obligations RGPD ni les risques de détournement.

## Modèle de menace

| Niveau | Adversaire | Capacité | Risque principal |
|---|---|---|---|
| N1 — Opportuniste | Promeneur, cueilleur | Retrait physique carte SD, lecture sur PC | Vol d'images non chiffrées |
| N2 — Technique | Braconnier équipé, militant anti-surveillance | Extraction firmware, sniffing LoRa, flash malveillant | Neutralisation nœud, extraction données, injection firmware |
| N3 — Organisé | Exploitant forestier, agence | Attaque side-channel, provisioning frauduleux | Compromission flotte entière |

**P0 couvre N1 et N2.** N3 est hors scope P0 mais les décisions (diversification de clé, secure boot) limitent l'impact d'une compromission isolée.

## Décisions

### 1. Filtre humain embarqué (RGPD)

**Les silhouettes humaines doivent être détectées sur le nœud. Une image reconnue comme humaine ne déclenche pas d'alerte animale et n'est jamais transmise. En P0, aucune image n'est transmise par LoRa : seuls les métadonnées ADR-014 quittent le nœud par ce canal.**

- Localisation : traitement **Edge AI sur le nœud** (pas côté Base Nexus ni cloud).
- Résolution d'inférence : **VGA (640×480)** pour contourner les limites RAM de l'ESP32-S3 — la capture haute résolution 5 MP n'est conservée localement que selon la règle de rétention ci-dessous ; seule la version VGA est requise pour l'inférence.
- **Rétention par défaut :** si une personne est détectée, l'originale est supprimée après traitement, ou les personnes sont irréversiblement floutées avant toute conservation. Si le filtre ne détecte pas de personne, l'image peut être conservée sur la SD chiffrée selon la durée maximale documentée dans le manuel terrain. Un faux négatif reste possible : il faut donc protéger la SD et prévoir le droit d'accès, sans promettre qu'aucune image humaine ne sera jamais conservée.
- **Contrat IA :** la décision d'alerte reste binaire animal / non-animal ; la détection humaine est une classe de sécurité distincte et non une identification d'espèce.
- Modèle : FOMO, MobileNet-SSD ou équivalent quantisé INT8 compatible ESP32-S3 PSRAM. L'architecture est choisie après benchmark comparatif sur le matériel cible ; aucune latence inférieure à 100 ms n'est acquise.
- Critère de succès P0 : détection humaine > 90 % recall à 5 m (jour), > 80 % recall à 5 m (nuit IR), faux positifs < 5 % sur faune.
- **Réserve :** les benchmarks jour et nuit doivent être exécutés sur le matériel cible (ESP32-S3 + PSRAM) avec le modèle quantisé retenu avant fermeture M-02. Si la latence dépasse 2s ou si le recall nuit est < 80 %, déclencher la migration MCU (ADR-001).

**Trigger de migration MCU :** si le modèle de détection humaine s'avère trop lourd pour l'ESP32-S3 (latence > 2s ou OOM), cela devient un critère supplémentaire de migration vers RV1106 ou STM32N6 (NPU intégré).

### 2. Chiffrement des données SD

- Les images sur carte SD doivent être chiffrées au repos (AES-128 minimum).
- **Diversification de clé par nœud** : chaque nœud possède une clé de chiffrement unique, dérivée de son identité (serial MCU) combinée à un secret de provisioning injecté en usine ou au banc. La master key PKA n'est jamais embarquée sur les nœuds. Voir ADR-011 pour la procédure complète.
- Objectif : rendre les images illisibles si la carte SD est retirée physiquement du nœud, **et empêcher qu'un nœud compromis ne compromette les autres**.

### 3. Signature des firmwares

- Tout firmware OTA (si implémenté en P1) doit être signé par une clé privée PKA WildNexus.
- Le nœud vérifie la signature avant flash — firmware non signé = rejet.
- En P0 : secure boot ESP32-S3 activé, pas d'OTA, mise à jour câble uniquement.

### 4. Transmission LoRa — protection des métadonnées

- Les métadonnées transmises (horodatage, ID nœud, type d'événement, coordonnées si GPS) peuvent, par inférence, révéler des patterns de présence humaine (ex. « non-détection » répétée sur un sentier à heures fixes).
- **Décision :** les métadonnées transmises en P0 sont limitées au schéma ADR-014 (identifiant, horodatage, événement et données techniques nécessaires). Aucune image, aucun clip audio et aucune coordonnée GPS ne sont transmis. Les patterns temporels et techniques sont documentés comme risque résiduel P0. Le chiffrement de la payload LoRa complète est repoussé en P1 ; cette décision devra être réévaluée avant un déploiement sur site sensible.

### 5. Signalétique terrain et droit d'accès RGPD

- **Signalétique obligatoire** sur chaque nœud déployé : panneau physique ou gravure boîtier indiquant « Zone sous observation automatisée pour le suivi de la faune. Filtrage local des personnes ; aucune image transmise par LoRa. Des captures peuvent être conservées temporairement sur support chiffré. Contact : [adresse projet] ». Le texte définitif et la base légale doivent être validés avant M-03.
- **Procédure droit d'accès :** si un faux négatif du filtre humain laisse passer une image, une personne concernée peut exercer son droit d'accès RGPD. La procédure P0 (documentée dans le manuel terrain) prévoit : (1) extraction câblée de la SD par une personne autorisée, (2) vérification manuelle restreinte et journalisée des images du jour concerné, (3) suppression ou floutage dans les délais légaux applicables. Aucune copie non expurgiée ne doit être transmise. Le modèle de registre est à rédiger par [[Renard]] avant M-03.
- **Registre RGPD :** un registre minimal des traitements sera maintenu dans le dépôt WildNexus, listant : finalité, base légale à confirmer, durée maximale de conservation locale, mesures de sécurité et procédure de suppression. Aucun déploiement terrain n'est autorisé tant que ces champs sont incomplets.

### 6. Licence MIT et politique éthique

- **Décision JCH du 2026-11-05 :** le firmware est destiné à être publié sous licence MIT, accompagné d'un fichier `ETHICS.md` et d'une politique d'usage WildNexus.
- La licence MIT demeure une licence de copyright permissive compatible OSI. `ETHICS.md` exprime les usages que le projet refuse et sert de référence à ses partenariats ; il ne devient pas automatiquement une restriction de licence opposable à tout utilisateur en aval par le seul usage du code.
- Les exclusions militaires, de surveillance humaine et d'atteinte à la biodiversité sont reprises dans les contrats lorsque le projet a une relation contractuelle. Leur portée réelle sur les autres tiers doit être expliquée sans surpromesse.
- Le choix MIT ne fixe pas les licences du hardware, de la documentation, des modèles, des datasets ou de la marque. Ces objets, les notices tierces et les contributions exigent des règles distincts.
- **Réserve :** les textes MIT/ETHICS, la politique d'usage et leur articulation contractuelle doivent être relus par [[Hermine]] et [[Renard]], avec conseil externe si nécessaire, avant publication ou contrat.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Filtre Edge (nœud) | RGPD par design, pas de transmission de données sensibles | Contrainte RAM/CPU sur ESP32-S3 | **Retenu** |
| Filtre Base Nexus | Plus de puissance de calcul, modèle plus lourd | Exigerait un transfert d'images non filtrées vers la gateway et élargirait la surface de risque | Rejeté en P0 |
| Filtre cloud | Précision maximale | Données hors zone blanche, latence, privacy absente | Rejeté |
| Pas de filtre P0 | Simplicité | Risque RGPD réel dès premier déploiement | Rejeté |
| Clé unique tous nœuds | Provisioning simple | 1 nœud compromis = flotte entière | Rejeté → ADR-011 |
| Licence Hippocratic 3.0 seule | Clause éthique intégrée | Non OSI-compatible, adoption et articulation contractuelle plus difficiles | Non retenue |
| MIT sans politique éthique | OSI, adoption maximale | La mission et les refus d'usage du projet ne seraient pas explicités | Non retenue seule ; complétée par ETHICS.md |
| AGPLv3 + licence commerciale | Réciprocité copyleft et offre duale possibles | Autre modèle de gouvernance et de distribution | Écartée par la décision JCH du 2026-11-05 |

## Conséquences

- WP04 firmware doit intégrer le modèle de détection humaine dès M-02 (pas reportable en P1).
- WP02 hardware doit prévoir PSRAM suffisante (≥ 8 MB) pour l'inférence VGA.
- ADR-001 (MCU) : si ESP32-S3 échoue sur la contrainte filtre humain → trigger migration RV1106/STM32N6.
- ADR-003/014 : les métadonnées respectent le format accepté, sans coordonnées GPS. Les compteurs techniques en clair sont autorisés dans ce contrat et documentés comme risque résiduel ; le chiffrement de la payload LoRa complète est P1.
- ADR-005 (énergie) : le coût énergétique de l'inférence Edge AI doit être mesuré avec le modèle retenu, intégré au budget batterie cible de 60 jours et croisé avec le modèle d'autonomie avant clôture M-02. L'ancienne estimation de 300 mW pendant 2 s n'est pas une mesure.
- ADR-011 (provisioning) : définit la procédure de diversification de clé et le cycle de vie complet.
- Le chiffrement SD est un critère de validation M-03, pas M-02.
- La signalétique terrain et le registre RGPD minimal doivent être prêts avant premier déploiement terrain.
- La publication doit distinguer les permissions MIT des engagements éthiques du projet et des obligations propres aux contrats.

## Tests obligatoires avant acceptation (levée des réserves)

| Test | Critère |
|---|---|
| Détection humaine à 5 m (jour) | > 90 % recall, < 5 % faux positifs faune |
| Détection humaine à 5 m (nuit IR) | > 80 % recall |
| Latence inférence VGA sur ESP32-S3 | < 2 s par frame |
| Benchmark énergétique inférence Edge AI | impact mesuré sur budget 60 jours, intégré ADR-005 |
| Lecture carte SD chiffrée hors nœud | Fichiers illisibles sans clé |
| Diversification de clé | Clé nœud A ≠ clé nœud B, compromission A n'affecte pas B |
| Boot avec firmware non signé | Rejet du boot confirmé |
| Textes MIT, ETHICS et politique d'usage | Revue écrite [[Hermine]] + [[Renard]] ; permissions MIT et engagements éthiques distingués |

## Points de réserve — à résoudre avant fermeture M-02

| # | Point | Owner | Échéance |
|---|---|---|---|
| R1 | Diversification de clé et provisioning → ADR-011 | [[Castor]] + [[Forge]] | M-02 |
| R2 | Articulation de MIT, `ETHICS.md`, de la politique d'usage et des contrats | [[Hermine]] + [[Renard]] | Avant publication/contrat |
| R3 | Procédure droit d'accès RGPD + modèle registre | [[Renard]] | M-03 |
| R4 | Benchmark Edge AI réel sur ESP32-S3 (jour + nuit) | [[Forge]] + [[Nova]] | M-02 |
| R5 | Impact énergétique Edge AI croisé avec ADR-005 | [[Bruno]] + [[Forge]] | M-02 |
| R6 | Template signalétique terrain | [[Renard]] | M-03 |

## Voir aussi

- [[ADR-001-choix-mcu-p0]] — trigger migration MCU si filtre trop lourd
- [[ADR-003-choix-radio-lpwan-p0]] — format métadonnées LoRa, chiffrement payload P1
- [[ADR-005-energie-autonomie-p0]] — budget énergétique à croiser avec inférence Edge AI
- [[ADR-009-architecture-satellite-base-cloud]] — architecture transmission
- [[ADR-011-provisioning-cycle-de-vie-cles]] — provisioning et cycle de vie des clés
- [[WILDNEXUS_ENGINEERING_PHILOSOPHY]] — NN-09 Privacy by design

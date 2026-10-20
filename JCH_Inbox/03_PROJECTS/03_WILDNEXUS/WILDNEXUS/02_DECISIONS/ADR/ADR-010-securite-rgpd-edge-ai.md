# ADR-010 — Sécurité, Chiffrement et RGPD Edge AI

**Date :** 2026-06-06
**Dernière mise à jour :** 2026-06-08 (révision Pro — angles morts comblés)
**Statut :** accepté sous réserve — 2026-06-08
**Points de réserve :** diversification de clé par nœud (→ ADR-011), choix de licence éthique précis (→ [[Hermine]] + [[Renard]]), procédure droit d'accès RGPD (→ [[Renard]]), benchmark Edge AI réel (→ [[Forge]] + [[Nova]])
**Owner PKA :** [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]]
**Jalon :** M-02 Prototype banc (filtrage humain) · M-03 Firmware ULP (chiffrement SD)

## Contexte

WildNexus est un réseau d'observation déployé en milieu naturel ouvert. Il peut capturer accidentellement des silhouettes humaines (randonneurs, agents forestiers). Les images sont stockées sur carte SD locale et transmises via LoRa. Le projet est open source. Ces trois facteurs créent des obligations RGPD et des risques de détournement.

## Modèle de menace

| Niveau | Adversaire | Capacité | Risque principal |
|---|---|---|---|
| N1 — Opportuniste | Promeneur, cueilleur | Retrait physique carte SD, lecture sur PC | Vol d'images non chiffrées |
| N2 — Technique | Braconnier équipé, militant anti-surveillance | Extraction firmware, sniffing LoRa, flash malveillant | Neutralisation nœud, extraction données, injection firmware |
| N3 — Organisé | Exploitant forestier, agence | Attaque side-channel, provisioning frauduleux | Compromission flotte entière |

**P0 couvre N1 et N2.** N3 est hors scope P0 mais les décisions (diversification de clé, secure boot) limitent l'impact d'une compromission isolée.

## Décisions

### 1. Filtre humain embarqué (RGPD)

**Les silhouettes humaines doivent être détectées et supprimées/floutées avant toute transmission.**

- Localisation : traitement **Edge AI sur le nœud** (pas côté Base Nexus ni cloud).
- Résolution d'inférence : **VGA (640×480)** pour contourner les limites RAM de l'ESP32-S3 — la capture haute résolution (5 MP) est stockée localement, mais seule la version VGA est soumise au filtre avant transmission.
- Modèle cible : MobileNet-SSD ou équivalent quantisé INT8 compatible ESP32-S3 PSRAM.
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
- **Décision :** les métadonnées transmises en P0 se limitent à `id_nœud + type_événement + horodatage`. Pas de coordonnées GPS ni de compteur de détections en clair. Les patterns temporels sont acceptés comme risque résiduel P0 documenté. Le chiffrement de la payload LoRa complète est repoussé en P1 (contrainte duty cycle et taille paquet).

### 5. Signalétique terrain et droit d'accès RGPD

- **Signalétique obligatoire** sur chaque nœud déployé : panneau physique ou gravure boîtier indiquant « Zone sous observation automatisée à des fins de suivi de faune — traitement Edge, aucune image humaine conservée ni transmise. Contact : [adresse projet] ».
- **Procédure droit d'accès :** si un faux négatif du filtre humain laisse passer une image, une personne concernée peut exercer son droit d'accès RGPD. La procédure P0 (documentée dans le manuel terrain) prévoit : (1) extraction câblée de la SD, (2) vérification manuelle des images du jour concerné, (3) suppression ou floutage sous 30 jours. Le modèle de registre est à rédiger par [[Renard]] avant M-03.
- **Registre RGPD :** un registre minimal des traitements sera maintenu dans le dépôt WildNexus, listant : finalité, base légale (intérêt légitime — recherche scientifique), durée de conservation locale, mesures de sécurité.

### 6. Licence Ethical-Source

- **Décision révisée :** la licence doit être compatible avec l'écosystème open-source standard tout en excluant les usages militaires et de surveillance de masse.
- **Option retenue :** dual-license — MIT pour le code (compatible OSI, écosystème standard) + addendum éthique dans les termes d'utilisation du projet WildNexus (ETHICS.md à la racine du dépôt), contraignant pour tout utilisateur par simple usage.
- **Réserve :** la formulation exacte de l'addendum et sa portée juridique doivent être validées par [[Hermine]] (propriété intellectuelle) et [[Renard]] (droit des [[contrats]]) avant publication du dépôt public.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Filtre Edge (nœud) | RGPD par design, pas de transmission de données sensibles | Contrainte RAM/CPU sur ESP32-S3 | **Retenu** |
| Filtre Base Nexus | Plus de puissance de calcul, modèle plus lourd | Images humaines transmises en clair via LoRa — inacceptable RGPD | Rejeté |
| Filtre cloud | Précision maximale | Données hors zone blanche, latence, coût, privacy absente | Rejeté |
| Pas de filtre P0 | Simplicité | Risque RGPD réel dès premier déploiement | Rejeté |
| Clé unique tous nœuds | Provisioning simple | 1 nœud compromis = flotte entière | Rejeté → ADR-011 |
| Licence Hippocratic 3.0 seule | Clause éthique intégrée | Non OSI-compatible, bloque écosystème open-source | Rejeté → dual-license |
| Licence MIT seule | OSI, adoption maximale | Aucune protection contre usages militaires | Rejeté → dual-license |

## Conséquences

- WP03 firmware doit intégrer le modèle de détection humaine dès M-02 (pas reportable en P1).
- WP02 hardware doit prévoir PSRAM suffisante (≥ 8 MB) pour l'inférence VGA.
- ADR-001 (MCU) : si ESP32-S3 échoue sur la contrainte filtre humain → trigger migration RV1106/STM32N6.
- ADR-003 (radio LPWAN) : le format des métadonnées transmises doit exclure GPS et compteurs en clair. Le chiffrement payload complète LoRa est P1.
- ADR-005 (énergie) : le coût énergétique de l'inférence Edge AI (MobileNet-SSD, ~300 mW estimé pendant 2s par réveil) doit être intégré au budget batterie 60 jours et croisé avec le modèle d'autonomie avant M-02.
- ADR-011 (provisioning) : définit la procédure de diversification de clé et le cycle de vie complet.
- Le chiffrement SD est un critère de validation M-03, pas M-02.
- La signalétique terrain et le registre RGPD minimal doivent être prêts avant premier déploiement terrain.

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
| Licence duale validée | Avis écrit [[Hermine]] + [[Renard]] |

## Points de réserve — à résoudre avant fermeture M-02

| # | Point | Owner | Échéance |
|---|---|---|---|
| R1 | Diversification de clé et provisioning → ADR-011 | [[Castor]] + [[Forge]] | M-02 |
| R2 | Formulation exacte dual-license (MIT + ETHICS.md) | [[Hermine]] + [[Renard]] | M-02 |
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

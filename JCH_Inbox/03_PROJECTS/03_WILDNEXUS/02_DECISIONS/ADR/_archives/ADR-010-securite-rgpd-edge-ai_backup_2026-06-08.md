# ADR-010 — Sécurité, Chiffrement et RGPD Edge AI

**Date :** 2026-06-06
**Statut :** accepté — 2026-06-06 (contraintes validées par analyse NotebookLM)
**Owner PKA :** [[Castor]] + [[Forge]]
**Jalon :** M-02 Prototype banc (filtrage humain) · M-03 Firmware ULP (chiffrement SD)

## Contexte

WildNexus est un réseau d'observation déployé en milieu naturel ouvert. Il peut capturer accidentellement des silhouettes humaines (randonneurs, agents forestiers). Les images sont stockées sur carte SD locale et transmises via LoRa. Le projet est open source. Ces trois facteurs créent des obligations RGPD et des risques de détournement.

## Décisions

### 1. Filtre humain embarqué (RGPD)

**Les silhouettes humaines doivent être détectées et supprimées/floutées avant toute transmission.**

- Localisation : traitement **Edge AI sur le nœud** (pas côté Base Nexus ni cloud).
- Résolution d'inférence : **VGA (640×480)** pour contourner les limites RAM de l'ESP32-S3 — la capture haute résolution (5 MP) est stockée localement, mais seule la version VGA est soumise au filtre avant transmission.
- Modèle cible : MobileNet-SSD ou équivalent quantisé INT8 compatible ESP32-S3 PSRAM.
- Critère de succès P0 : détection humaine > 90 % à 5 m, faux positifs < 5 % sur faune.

**Trigger de migration MCU :** si le modèle de détection humaine s'avère trop lourd pour l'ESP32-S3 (latence > 2s ou OOM), cela devient un critère supplémentaire de migration vers RV1106 ou STM32N6 (NPU intégré).

### 2. Chiffrement des données SD

- Les images sur carte SD doivent être chiffrées au repos (AES-128 minimum).
- La clé de chiffrement est dérivée du serial MCU + secret provisioning (stocké en eFuse ou OTP).
- Objectif : rendre les images illisibles si la carte SD est retirée physiquement du nœud.

### 3. Signature des firmwares

- Tout firmware OTA (si implémenté en P1) doit être signé par une clé privée PKA WildNexus.
- Le nœud vérifie la signature avant flash — firmware non signé = rejet.
- En P0 : secure boot ESP32-S3 activé, pas d'OTA, mise à jour câble uniquement.

### 4. Licence Ethical-Source

- Le code source est publié sous licence excluant explicitement les usages militaires (surveillance de périmètre, ciblage).
- Mention obligatoire dans tout fork ou dérivé.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Filtre Edge (nœud) | RGPD par design, pas de transmission de données sensibles | Contrainte RAM/CPU sur ESP32-S3 | **Retenu** |
| Filtre Base Nexus | Plus de puissance de calcul, modèle plus lourd | Images humaines transmises en clair via LoRa — inacceptable RGPD | Rejeté |
| Filtre cloud | Précision maximale | Données hors zone blanche, latence, coût, privacy absente | Rejeté |
| Pas de filtre P0 | Simplicité | Risque RGPD réel dès premier déploiement | Rejeté |

## Conséquences

- WP03 firmware doit intégrer le modèle de détection humaine dès M-02 (pas reportable en P1).
- WP02 hardware doit prévoir PSRAM suffisante (≥ 8 MB) pour l'inférence VGA.
- ADR-001 (MCU) : si ESP32-S3 échoue sur la contrainte filtre humain → trigger migration RV1106/STM32N6.
- Le chiffrement SD est un critère de validation M-03, pas M-02.

## Tests obligatoires avant acceptation

| Test | Critère |
|---|---|
| Détection humaine à 5 m (jour) | > 90 % recall, < 5 % faux positifs faune |
| Détection humaine à 5 m (nuit IR) | > 80 % recall |
| Latence inférence VGA sur ESP32-S3 | < 2 s par frame |
| Lecture carte SD chiffrée hors nœud | Fichiers illisibles sans clé |
| Boot avec firmware non signé | Rejet du boot confirmé |

## Voir aussi

- [[ADR-001-choix-mcu-p0]] — trigger migration MCU si filtre trop lourd
- [[ADR-009-architecture-satellite-base-cloud]] — architecture transmission
- [[WILDNEXUS_ENGINEERING_PHILOSOPHY]] — NN-09 Privacy by design

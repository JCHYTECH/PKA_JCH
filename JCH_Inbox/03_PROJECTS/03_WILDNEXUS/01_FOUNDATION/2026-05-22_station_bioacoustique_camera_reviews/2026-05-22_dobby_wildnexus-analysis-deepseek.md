# Analyse Deepseek — WILDNEXUS : Station Bioacoustique & Caméra Hybride

**Date :** 2026-05-22  
**Auteur :** Dobby 🦉 (Orchestrator)  
**Contexte :** Revue critique de la fiche specs & BOM du prototype WILDNEXUS.

---

## 1. Synthèse de l'Architecture

L'approche bi-étagée est validée car elle respecte les contraintes de consommation énergétique en milieu isolé.

- **ESP32-S3 :** Gardien basse consommation (Always-on).
- **Pi Zero 2 W / CM4 :** Processeur média lourd (On-demand).
- **Connectivité :** LTE Cat-1 pour le cloud, WiFi local pour la maintenance.

---

## 2. Analyse Critique & Points de Vigilance

### A. La Latence de Réveil (Le maillon faible)
Le boot d'un Raspberry Pi Zero 2 (20-40s) est incompatible avec une capture réactive suite à un trigger sonore.
- **Solution préconisée :** Utiliser la PSRAM de l'ESP32-S3 comme buffer circulaire (10s d'audio permanent).
- **Transfert :** Transmettre ce buffer au Pi dès son réveil pour ne perdre aucune donnée pré-trigger.

### B. Fiabilité du Stockage
Les cartes SD sont fragiles face aux coupures d'alimentation.
- **Recommandation :** Système de fichiers en **Read-Only** (OverlayFS) pour l'OS du Pi.
- **Données :** Partition dédiée ou eMMC (sur CM4) pour les captures.

### C. Gestion Thermique et Condensation
Un boîtier IP65 fermé est un four en été et une boîte à buée en hiver.
- **Action :** Intégrer un évent de décompression (Pressure Compensation Plug) et des sachets de silice.
- **Dissipation :** Couplage thermique du Pi au châssis.

---

## 3. Améliorations Techniques du BOM

| Composant Suggéré | Fonction | Impact |
| :--- | :--- | :--- |
| **Filtre IR-CUT motorisé** | Correction colorimétrique jour/nuit | Indispensable |
| **Membrane ePTFE** | Protection micros MEMS sans perte dB | Critique étanchéité |
| **Batterie LiFePO4** | Sécurité thermique et longévité | Recommandé |
| **Super-capacité 4G** | Gestion des pics de courant (2A) | Stabilité système |

---

## 4. Recommandations Équipe (Orchestration)

1. **Chouette 🦉 (#25)** : Doit valider l'intégration mécanique des membranes acoustiques.
2. **Forge 🦦 (#12)** : Doit tester la communication ESP32-S3 <-> Pi Zero en mode "USB Gadget".
3. **Furet 🦡 (#03)** : Doit sourcer des boîtiers industriels "hackables" pour réduire le coût NRE.

---
*Document généré pour JCH — Système PKA_JCH.*

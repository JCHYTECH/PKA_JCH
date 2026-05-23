# Analyse de la fiche specs/BOM — Station bioacoustique/caméra hybride

**Date :** 2026-05-22  
**Auteur :** Dobby 🦉  
**Document analysé :** `JCH_Inbox/00_INBOX/fiche_specs_BOM_station_bioacoustique_camera.md`  
**Contexte :** briefs WildNexus du 2026-05-22 (multimodal reset, architecture satellite/base, matrice capteurs)  
**Spécialistes concernés :** Forge 🔨, Chouette 🦉, Furet 🦡, Castor 🦫, Clio 📚

---

## Ce qui est bon — à conserver

1. **Structure claire et actionnable.** Concept → architecture → specs → BOM → options → validation. C'est exactement le format qu'il faut pour un document de décision.

2. **Les 10 points critiques de validation (§7).** Excellente liste. La condensation, la stabilité modem 4G, le comportement solaire hiver belge, la robustesse microSD après coupure — ce sont les vrais risques terrain. Ne touche à rien ici.

3. **Modes opératoires bien définis** (normal / événement / maintenance). Le séquencement énergétique est juste.

4. **BOM chiffrée.** 499 € prototype, fourchette 450-550 €, options éco 320-380 €, pré-série 600-850 €. Les ordres de grandeur sont réalistes.

5. **Options économique et pré-série (§5-6).** Utile pour pitching et décisions budgétaires.

---

## Décalages avec la vision architecturale validée aujourd'hui

C'est le cœur de l'analyse. Les briefs de ce matin ont abouti à des recommandations qui recadrent plusieurs choix de la fiche.

### 1. Architecture : boîtier unique → satellites + base

La fiche décrit **un boîtier tout-en-un** (ESP32 + Pi + 4G + Cloud). Les 4 briefs d'aujourd'hui convergent vers une **architecture distribuée à 3 niveaux** :

| Niveau | Rôle | Hardware recommandé |
|---|---|---|
| Satellite Lite | Veille, PIR, audio léger, LoRa, stockage simple | STM32U5, Apollo510 |
| Satellite Smart | Caméra, audio riche, détection locale, préfiltrage IA | STM32N6, Rockchip RV1106 |
| Base Nexus | Stockage lourd, BirdNET-Go local, 4G/5G, dashboard | Pi 5, NXP i.MX 8M Plus |

**Impact sur la fiche :** le schéma du §2 est à refondre. Ce n'est pas un boîtier unique avec des sous-modules, c'est un **réseau de nœuds à rôles différenciés**. La BOM du §4 décrit en réalité… une Base Nexus compacte, pas un satellite.

**Recommandation :** ajouter une section « Architecture distribuée » avec les 3 profils, et faire 2 BOM distinctes (Satellite Smart prototype + Base Nexus prototype).

### 2. ESP32-S3 : le déclasser comme cerveau

La fiche place ESP32-S3 comme pilier central. Le verdict des briefs est sans ambiguïté :

> *« Garder ESP32 comme outil de prototype ou sous-module, mais ne plus le mettre au centre de WildNexus. »*

L'ESP32-S3 reste utile comme **contrôleur basse consommation** (veille, capteurs I2C, PIR, réveil). Mais pas comme ordonnanceur multimodal. STM32U5 et STM32N6 sont les alternatives sérieuses identifiées.

**Recommandation :** dans la BOM prototype, garder ESP32-S3 pour le proto rapide (c'est honnête), mais ajouter une colonne « Cible produit » avec STM32U5/N6.

### 3. BirdNET : cloud → local ou gateway

La fiche envoie tout vers un cloud BirdNET. Les briefs recommandent :

- **P0 : pas de BirdNET embarqué.** Juste capture audio + métadonnées.
- **P1 : BirdNET-Go sur la Base Nexus** (traitement local, pas cloud obligatoire).
- Cloud = option de synchronisation, pas dépendance.

**Recommandation :** revoir le schéma du §2 : la Base Nexus fait tourner BirdNET-Go en local. Le cloud devient un service de backup/sync/dashboard, pas le point de passage obligé.

### 4. Absence de LoRa dans le schéma de communication

La fiche mentionne WiFi local et 4G LTE, mais pas LoRa. Or LoRa est le lien recommandé entre satellites et base :

- Alerte événement
- Statut batterie
- Métadonnées
- Index fichiers
- Commande de réveil

**Recommandation :** ajouter LoRa/LoRaWAN dans le schéma du §2 entre ESP32 et Base, et dans la BOM.

### 5. Phasage P0-CAM / P0-AUDITIF / P1-FUSION absent

Le multimodal reset a défini un phasage clair :

- **P0-CAM :** preuve caméra autonome basse conso
- **P0-AUDITIF :** preuve audio minimale (capture + timestamp, pas classification)
- **P1-FUSION :** corrélation caméra + audio + environnement
- **P2-RESEAU :** écosystème distribué

La fiche mélange P0 et P1 sans distinguer les jalons.

**Recommandation :** ajouter une section « Phasage » avec ces 4 paliers.

---

## Améliorations ponctuelles sur la BOM et les specs

### Capteurs : sur-priorisation et angle mort

| Capteur | Statut fiche | Recommandation matrice capteurs | Action |
|---|---|---|---|
| AS7341 (spectral 11 canaux) | Inclus, 20 € | « Option faible priorité » — usage écologique non démontré pour la faune | **Retirer du prototype.** Réinjecter les 20 € ailleurs |
| BME688 (VOC/eCO₂) | Inclus | CO₂/VOC = « rejeter baseline » pour usage extérieur faune | Remplacer par BME280 (T/H/P, moins cher) ou garder BME688 pour T/H/P seule |
| Double micro | Inclus (2× MEMS) | P1/P2, pas Lite initial | Garder pour Smart, mais 1 micro suffit pour P0-AUDITIF |
| LoRa | Absent | Obligatoire si satellites | **Ajouter module LoRa**, ~15-20 € |
| IMU/accéléromètre | Absent | Recommandé système (anti-tamper, orientation) | Ajouter ~5 € |
| Capteur humidité interne | Absent | Obligatoire (détection fuite/condensation) | Le BME fait T/H, mais séparer T/H interne dédié |

### Points manquants dans la BOM

- **Module LoRa** (RFM95W ou équivalent) : ~15-20 €
- **Watchdog externe** : critique pour récupération plantage terrain, ~3 €
- **IMU/accéléromètre** : orientation, choc, anti-vol, ~5 €
- **Évent membrane** (mentionné au §3 mais pas dans la BOM) : ~8 €

### Points manquants dans les specs

1. **Licence BirdNET / BirdNET-Go.** Usage commercial → vérifier compatibilité licence CC BY-NC-SA 4.0 ou modèle Google. Bloquant si produit commercial.
2. **RGPD audio.** Capturer des voix humaines et conversations → politique à définir avant premier déploiement terrain. Pas optionnel en Europe.
3. **Politique anti-corruption microSD.** Les coupures d'alimentation corrompent les SD. Journalisation append-only + index séparé.
4. **Double microSD vs stockage unifié.** La fiche propose 2 SD (audio + média). En pratique, une SD industrielle unique avec partitionnement logique est plus fiable et moins chère.
5. **PIR comme déclencheur unique.** Les briefs suggèrent de tester le radar mmWave basse conso en complément (filtre végétation, détection sans chaleur).

---

## Synthèse des recommandations

### Structurelles (à faire avant proto)

1. Ajouter une section « Architecture distribuée satellites + base » avec 3 profils
2. Déclasser ESP32-S3 au rang de contrôleur basse conso, pas de cerveau
3. Ajouter LoRa au schéma de communication et à la BOM
4. Intégrer le phasage P0-CAM / P0-AUDITIF / P1-FUSION / P2-RESEAU
5. Déplacer BirdNET du cloud vers la Base Nexus (local), cloud = backup optionnel

### BOM

6. Retirer AS7341 (-20 €) — usage écologique non démontré
7. Remplacer BME688 par BME280 (-5 €) ou ne pas utiliser VOC/CO₂
8. Ajouter LoRa (+15-20 €), watchdog (+3 €), IMU (+5 €), évent membrane (+8 €) → impact net quasi nul
9. Unifier stockage sur 1 SD industrielle au lieu de 2

### Gouvernance

10. Vérifier licence BirdNET pour usage commercial
11. Ajouter une section RGPD audio
12. Ajouter politique anti-corruption stockage après coupure

---

*Analyse produite par Dobby 🦉 sur demande de JCH, basée sur les briefs WildNexus du 2026-05-22.*

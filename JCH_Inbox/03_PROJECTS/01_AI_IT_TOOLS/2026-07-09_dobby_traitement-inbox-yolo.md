# Traitement INBOX — Mode YOLO
> 2026-07-09 — Dobby 🦉
> 6 fichiers traités sans validation intermédiaire, sur demande explicite de JC.

---

## Fichiers traités

| # | Fichier original | Action | Destination |
|---|-------------------|--------|-------------|
| 1 | `CBE PC100 KIT & PC200 KIT instruction manual.pdf` | Déplacé | `03_PROJECTS/11_IOT/iot-van/ds300-tap/CBE-PC100-PC200-DS300-instruction-manual.pdf` |
| 2 | `CO2601-0223 (2).pdf` | Archivé | `07_TRAVELS/van technique/achat-van/archive/CO2601-0223_commande-stylevan-equinox4-170-4x4-15012026.pdf` |
| 3 | `IMG_4206.HEIC` | Rangé | `00_INBOX/_captures/2026-07-08/IMG_4206.HEIC` |
| 4-5 | `RE_ Vetalyx NOTE DE CADRAGE...body.txt` + `.eml` | Supprimés (doublons) | déjà archivés le 07/07 dans `08_VETALYX/strategy/2026-06-25_NOTE-CADRAGE_Vetalyx_Depinois_AWDN.*` — contenu identique octet pour octet (128 lignes, diff vide) |
| 6 | Dossier "Voici la synthèse complète..." | Déplacé + renommé | `07_TRAVELS/van technique/securite/camera-reolink-argus-magicam-lupo.md` |

**Résultat : `00_INBOX/` vide** (hors `.DS_Store` et le nouveau sous-dossier `_captures/`).

---

## Détail par fichier

### 1. Manuel CBE PC100/PC200/DS300 (13 pages, italien/anglais/allemand/français)
Documentation officielle du panneau de contrôle CBE et du boîtier de distribution DS300 — exactement le matériel du Westfalia Kelsey (« Lupo »). Confirme et enrichit `SPEC-DS300-TAP.md` :
- Détail complet des LED/boutons PC-100 et PC-200 (test batterie B1/B2, jauge eau, alarme 230V)
- **Fonction "Minimal Voltage Control"** : coupure auto des mains 12V si B2 < 10V, avec relance 1 min possible. Le frigo, les marches électriques et les circuits directs B2 sont exclus.
- **Sonde capacitive "SPE"** : alimentée 5V, retour 0-2,5V, rafraîchie toutes les 8s pour économiser l'énergie
- **DS-300** : détail des 12 fusibles (auvent 5A, pompe 10A, chauffage/chaudière 10A, éclairage A/B 20A, frigo 3 voies 30A, régulateur solaire 20A, marche électrique 25A, gaz 3A, D+ simulé 3A) + bridge AES + sortie D+ simulée pour marche électrique/frigo AES/vanne de vidange/antenne
→ **Action possible pour Araignée** : intégrer ces seuils de fusibles dans le firmware DS300-Tap comme limites de sécurité.

### 2. Commande CO2601-0223 — Stylevan Equinox 4
Devis/commande daté du **15 janvier 2026** pour un **Stylevan Equinox 4** (porteur Ford, 170ch A8, 4x4, gris Matter) — 91 138,67€ TTC. Ce modèle **n'a pas été retenu** : le van final acheté est le **Westfalia Kelsey** (« Lupo »), commandé le 30 juin 2026 chez Vanomobil pour 94 174,46€ TTC (cf. `fiche-technique-lupo-kelsey.md`). Document archivé comme trace de la phase de sélection, pas d'action requise.

### 3. IMG_4206.HEIC
Photo iPhone 17 Pro Max, 08/07/2026, GPS 50.564°N 5.614°E (zone Esneux/Tilff), altitude 261m. Aucune métadonnée de contenu (pas de légende/description). Rangée par date en attente de contexte — à trier si besoin.

### 4-5. Doublon Vetalyx Depinois
Fichiers strictement identiques (diff = vide, 128 lignes) à `2026-06-25_NOTE-CADRAGE_Vetalyx_Depinois_AWDN.md/.eml` déjà traités en session du 2026-07-07 (analyse complète livrée : `TEAM_Inbox/2026-07-07_dobby_analyse-note-cadrage-vetalyx-depinois.md`). Suppression pure, aucune perte d'information.

### 6. Configuration Reolink Argus MagiCam
Guide d'installation caméra dashcam/sécurité pour le Westfalia Kelsey — recoupe avec le projet caméras déjà exploré le 2026-07-04 (`07_ARCHIVES/inbox-2026-07-04-cameras-lupo/`, projet caméras ESP32+relais). Points clés extraits :
- **Alimentation** : brancher uniquement sur prise allume-cigare "après-contact" (ACC) du porteur Ford — jamais sur les prises cellule Westfalia (alimentation continue = décharge batterie + caméra bloquée en dashcam permanent)
- **Logique auto** : contact ON → mode dashcam continu (2K, ~1,35 Go/h) ; contact OFF → bascule batterie interne, mode détection de mouvement
- **Fixation** : aimant néodyme ⌀66mm + tige 1/4"-20, câble plat USB-C 3m sous tapis → montant portière passager → sortie sous joint bas de porte
- **Stockage** : microSD "High Endurance" (SanDisk/Samsung), 128 Go recommandé (~22 jours de dashcam, mode overwrite "Oldest")
→ **Concordance avec `securite-van-lupo.md`** : ce guide couvre l'usage "route" (dashcam), le doc sécurité existant couvre l'usage "bivouac" (Zigbee+HA). Complémentaires, pas redondants.

---

## Voir aussi
- [[SPEC-DS300-TAP]]
- [[securite-van-lupo]]
- [[fiche-technique-lupo-kelsey]]
- [[hardware-state]]

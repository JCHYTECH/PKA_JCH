---
date: 2026-11-06
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-06 — AirGuard Lupo ré-appairé et meuble-banquette v7

## Session — 15:45 — AirGuard Lupo ré-appairé et meuble-banquette v7

### Contexte
- Modèle : deepseek-v4
- Projet : 11_IOT + 07_TRAVELS (multi-projet)

### Résumé
Session Dobby multi-projet : ré-appairage à distance du capteur AirGuard Lupo (23 h de silence radio, LQI 56/255) ; refonte du meuble-banquette Lupo en aluminium T-slot (v7, sans tiroir) ; revue de la procédure WildNexus P0 (à jour, rien à modifier) ; correction du défaut recto-verso de l'Epson ET-8550.

### Actions
- **AirGuard Lupo** : diagnostic complet (HA API + Z2M database.db + logs) → silence radio 23 h, LQI 56/255. Ré-appairage à distance via Z2M/MQTT (permit-join + maintien bouton 5 s). Résultat LQI 255/255, mesures fraîches (18,8 °C / 66,1 % / 100 %). `hardware-state.md` mis à jour (cause racine : lien radio faible, distance).
- **Meuble-banquette v7** : refonte complète en profilé aluminium 2020 + Dibond 3 + HPL 12, dérivée de la réflexion ChatGPT « profilés alu 10×10 ». Sans tiroir → volets avant/arrière rabattables 90° (accès double sens) ; table = assise coulissante double sens sur coulisses Chambrelan D5DD. 4 fichiers créés (design, plan SVG, coupes xlsx, procédure) ; v5 bois + v6 archivés.
- **WildNexus P0** : revue — procédure (`progress.md`), processus de montage et ADR tous à jour (2026-11-05) et cohérents. Aucun changement requis. 3 déblocages identifiés : Panier Mouser ~279 € (LoRa), gates ADR-005 (batterie AA), datasheet micros TDK.
- **Epson ET-8550** : défaut recto-verso supprimé (`lpoptions -p ... -o Duplex=None`).
- **Accès ChatGPT** : récupéré le lien partagé « Profilés aluminium 10×10 » via l'API publique (`backend-api/share`).

### Décisions
- AirGuard Lupo : cause racine = lien radio faible (distance au coordinateur), pas un défaut capteur. À placer près du ZBDongle-E en installation finale.
- Meuble-banquette : profilé 2020 (pas MakerBeam 10×10, trop léger pour assise 80 kg) ; assise HPL 12 (insensible humidité, van inutilisé) ; Dibond 3 mm partout ; cubes 3 voies aux sommets ; table sur coulisses acier (pas la gorge seule, trop faible en porte-à-faux 30 cm).
- WildNexus : la procédure n'a pas besoin d'être modifiée — l'exécution est bloquée par le gel + panier Mouser non commandé.

### Prochaines étapes
- Meuble-banquette : prototyper le module A seul d'abord ; trancher la préhension des volets (plus tard, prise affleurante) ; confirmer la D5DD au fournisseur.
- WildNexus : au dégel — commander le Panier Mouser, lever les gates ADR-005, vérifier la datasheet des micros TDK.
- IOT : vérifier la réception du second ZBDongle-E (maison/serre).

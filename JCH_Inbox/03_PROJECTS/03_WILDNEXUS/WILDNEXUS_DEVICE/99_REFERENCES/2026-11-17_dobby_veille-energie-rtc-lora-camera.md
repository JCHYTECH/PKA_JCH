# Veille — Énergie, RTC, LoRa, caméra (points actionnables pour WILDNEXUS_DEVICE)

> Dobby 🦉 · 2026-11-17 · veille YouTube (9 derniers mois)
> Sources : transcripts `ultra-long-battery-life…` (Tech Dregs, oVrDZNoOu6s),
> `esp32-deep-sleep-explained…` (Rolling Bob, U5gBRJZVOBo),
> `how-to-send-sensor-data-over-lora…` (Shilleh, ET_vBzLNKu8),
> `esp32-s3-edge-ai-camera…` (IoT Journal, 554BfgEMc9A) — dans `99_REFERENCES/`
> **Statut :** référence à intégrer après levée des gates (gate 1 inventaire en cours).
> Aucun achat ni montage avant. Chiffres = dires des vidéastes, à confirmer au banc PPK2.

---

## 🔋 Énergie / ultra-low-power (le poste dominant P0)

**Chiffres bruts rapportés :**
- Radio Wi-Fi : RX ~95–100 mA · TX ~180–240 mA · deep sleep ~10 µA (timer).
- Boucle type « wake → mesure → envoi → sleep » : 100 mA pendant 2 s + 0,1 mA pendant 9m58
  → **0,43 mA moyen → ~192 jours (6 mois) sur 2000 mAh**.
- Un **capteur à 1 mA en continu** fait passer l'autonomie de **192 j → 58 j** (÷3).

**Piège n°1 — le dev board fuit :** même en deep sleep, la LED d'alim, le chip USB-série et le
régulateur du dev board restent alimentés. Le µC n'est qu'une partie de la conso réelle.
→ Mesurer le **système complet**, pas la datasheet du chip.

**Piste matérielle — RTC externe :** un RTC (ex. Epson RX-8130) + gestion d'alim dédiée peut
**÷50 à ÷100 la conso de sleep**, en réveillant le µC à heure fixe (horodatage offline, sortie
fréquence). À évaluer pour l'ULP WildNexus vs simple timer interne.

**Méthode :** persister l'état en **mémoire RTC** (survit au deep sleep) et en flash (survit au
power-off). Finir le travail le plus vite possible, dormir le reste du temps.

---

## 📡 Connectivité — LoRa (WILDMESH)

**Meshtastic = stack mesh prête à l'emploi** : firmware + CLI Python (`meshtastic`) + flasher web
(flasher.meshtastic.org). Canal privé + région + télémétrie. Portée de plusieurs km, sans
Wi-Fi/internet. Exemple de référence : BME280 (T°/H°/pression) en télémesure entre 2 nœuds.

→ **Recommandation** : tester Meshtastic avant de rebâtir un protocole LoRa maison. C'est le
chemin le plus court pour un mesh de capteurs WildNexus (le BME688 est déjà au BOM).

---

## 🎥 Caméra / edge AI (bring-up DEVICE)

- **ESP32-S3 obligatoire** : instructions vectorielles AI+DSP intégrées. L'ESP32 classique échoue
  sur l'inférence. (Cohérent avec le choix S3 acté.)
- **Résolution caméra = résolution d'entraînement** (ex. 96×96) — config `pixel_format` exacte.
- **Le mapping des pins caméra est la cause n°1 d'échec d'init** — spécifique à chaque board
  (FreeNove S3 WROOM, XIAO ESP32-S3 Sense…).
- **Matrice de dépannage** :
  - faux positifs → plus d'images d'entraînement variées (lumière/fond) ;
  - `camera init failed` → pins à corriger ;
  - OOM → baisser la résolution ou prendre un modèle plus petit.
- **MobileNet v2** (classification) / **FOMO** (détection à boxes) via Edge Impulse = voie la
  plus rapide. ⚠️ FOMO est sensible à la couleur/reflets → dataset soigné requis.

---

## Actions recommandées (post-gate)

1. **PPK2** : mesurer la conso réelle du dev board en deep sleep (avec LED/chip USB/régulateur)
   pour quantifier la fuite — pas seulement le µC.
2. **Évaluer le RTC externe** (RX-8130) : gain réel ÷50-100 sur notre architecture ULP cible.
3. **Bench Meshtastic** vs LoRa custom pour le mesh de capteurs.
4. **Documenter le mapping des pins** de la caméra choisie dès le bring-up (évite la cause n°1
   d'échec).

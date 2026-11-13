# Procédure — Relance du setup RPi 5 « JC home » (RPi Home)

> **Date :** 2026-11-11 | **Orchestré par :** Dobby 🦉 | **Projet :** 11_IOT
> **Objectif :** redémarrer l'instance Home Assistant du domicile (Esneux — maison + serre), après l'échec de boot constaté le 10/11.
> **Règle multi-terminal :** chaque commande est préfixée par sa machine cible — **[M5]** (Mac), **[RPi]** (RPi 5 « JC home »).

---

## Contexte (état réel)

| Date | Constat |
|------|---------|
| 2026-11-07 | HAOS 18.5 boote (avec ventilateur). Mosquitto OK, Zigbee2MQTT OK (dongle + réseau PANID `6699` + 3 devices reconnus : `vanne_serre`, `serre_temp_hum`, `LuxSerre`). **HA Core plante en boucle** (~30 min après onboarding, et après installation des add-ons). |
| 2026-11-10 | **RPi Home non joignable** (mDNS, scan IP/MAC, Tailscale, ports 8123/22 fermés) → HAOS ne boote plus. |

**Suspects HA Core (non tranchés) :**
1. Hardware RPi 5 défectueux (composant qui lâche sous charge).
2. Bug HAOS 18.5 / HA Core.

Éliminé au 07/11 : SD (2 cartes, lecture propre), image (boote), alim (27 W confirmée), chaleur (ventilateur ajouté).

---

## Décision clé

Re-flasher en **HAOS 18.3** (baseline validée sur Lupo, inclut le fix #5005) **plutôt que 18.5** → élimine directement le suspect « bug 18.5 ».
- Si le crash disparaît en 18.3 → la cause était la version 18.5.
- Si le crash persiste en 18.3 → hardware défectueux → échange du RPi 5 (garantie).

---

## Phase 0 — Diagnostic physique (vérité terrain)

Objectif : comprendre pourquoi le boot ne tient plus (07/11 il bootait, 10/11 plus).

- [ ] **Alimentation** : LED rouge et/ou verte sur le RPi 5 ? Alim officielle **27 W** (USB-C) bien branchée ?
- [ ] **microSD** : présente et bien enclenchée ? La retirer et la tester sur **[M5]** (lecture).
- [ ] **Ventilateur** : toujours en place et alimenté ? (la surchauffe a déjà corrompu HA une fois — sans ventilo, ça recommencera).
- [ ] **Ethernet** : câble branché pour le premier boot (plus fiable que Wi-Fi, évite les galères d'onboarding).

→ Mettre à jour `hardware-state.md` avec l'état constaté.

---

## Phase 1 — Flash HAOS 18.3 [M5]

Suivre **`SEQUENCE-FLASH-HAOS-18.3-2026-10-01.md`** (image `haos_rpi5-64-18.3.img.xz`).

Résumé des étapes :

```bash
# [M5]
cd /tmp
curl -L -o haos_rpi5-64-18.3.img.xz \
  https://github.com/home-assistant/operating-system/releases/download/18.3/haos_rpi5-64-18.3.img.xz

echo "e148a92595059d71c8bbf4c80d66fcb9166b647e10024641936316402863c60f  haos_rpi5-64-18.3.img.xz" | shasum -a 256 -c -
# Attendu : haos_rpi5-64-18.3.img.xz: OK

xz -d haos_rpi5-64-18.3.img.xz
diskutil list   # repérer la microSD → /dev/diskN
```

⚠️ **Vérifier DEUX FOIS le `/dev/diskN`** avant de flasher. Préférer **balenaEtcher** ou **Raspberry Pi Imager** (GUI, plus sûr que `dd`).

---

## Phase 2 — Premier boot + onboarding [RPi]

1. Insérer la microSD flashée, **SD seule** (aucun autre disque).
2. Brancher l'alim 27 W + Ethernet.
3. Attendre ~5 min, ouvrir `http://homeassistant.local:8123` (ou l'IP locale).
4. Créer le foyer **« JC home »**, compte `jc`.
5. **Désactiver l'auto-update immédiatement** : Settings → System → Updates → OFF.
6. Hostname : `jchome`.

---

## Phase 3 — Réinstaller la stack [RPi]

1. Add-on **Mosquitto** → installer + démarrer (port 1883).
2. Add-on **Zigbee2MQTT** → config :
   - `mqtt://core-mosquitto:1883`
   - device `/dev/ttyACM0`
   - adapter `ember`
   - → **Submit** + onboarding web.
3. Brancher le **Sonoff ZBDongle-E maison/serre** sur le RPi Home.
   ⚠️ *Le dongle maison/serre est documenté « branché sur M5 » au 06/11 — vérifier son emplacement physique avant cette étape.*
4. Vérifier que Z2M détecte le réseau Zigbee **PANID `6699`** et les 3 devices (`vanne_serre`, `serre_temp_hum`, `LuxSerre`) — ils restent appairés côté coordinateur.

---

## Phase 4 — Capturer les logs HA Core si crash (le point qui bloquait)

Le crash précédent était reproductible ~30 min après l'onboarding → surveiller cette fenêtre.

Deux voies, par ordre de simplicité :

- **A. Écran HDMI + clavier** sur le RPi (le plus simple) : la console affiche l'erreur au moment du crash.
- **B. SSH debug HAOS par clé USB** (port 22222, sans écran) : clé USB avec dossier `CONFIG/` + `authorized_keys`, puis `ssh root@<ip> -p 22222` → `journalctl` / logs Supervisor & Core.

→ Le log tranche entre **hardware** et **logiciel**.

---

## Phase 5 — Arbre de décision

| Situation | Verdict | Action |
|-----------|---------|--------|
| Boot + stack OK, pas de crash sur 24 h | Bug HAOS 18.5 | Résolu — rester en 18.3 |
| Crash reproductible en 18.3 | Hardware suspect | Lire logs (Phase 4) → échange RPi 5 |
| Boot ne tient pas du tout | Hardware (alim/SD/RPi) | Tester chaque composant séparément |

---

## Vigilance

1. **Auto-update HAOS : JAMAIS** — le bug 18.x revient à chaque montée de version non maîtrisée.
2. **SHA256 obligatoire** avant chaque flash.
3. **Retirer les autres disques** avant flash.
4. Mettre à jour `hardware-state.md` + `thread-iot.md` après chaque phase.

---

*Fichier maintenu par Dobby 🦉 — à mettre à jour après chaque phase.*

# Installation HAOS sur RPi 5 « JC home » — état et diagnostic

> Dobby 🦉 — 2026-11-07 — Projet 11_IOT

---

## 1. Intention

- Mettre en place une instance **Home Assistant dédiée au domicile** (Esneux), couvrant la **maison + la serre** du jardin.
- Nom du foyer : **« JC home »**.
- Support : **RPi 5 4 Go** (neuf, jamais utilisé) — remplace le HA Docker du M5 qui pilotait jusque-là la vanne + l'AirGuard serre + le LuxSerre.
- Logiciels cibles : **Mosquitto** (broker MQTT) + **Zigbee2MQTT** (coordination Zigbee).
- Objectif final : piloter la **vanne Sonoff** (ouvrir/fermer le robinet de la serre), l'**AirGuard serre** et le **LuxSerre**.
- Architecture visée : le RPi 5 « JC home » pilote maison/serre ; le RPi Lupo ne conserve que l'AirGuard Lupo.

---

## 2. Déroulé

1. Téléchargement de l'image officielle **HAOS 18.5 `rpi5-64`** (342 Mo compressé → 988 Mo décompressé). Taille conforme à GitHub.
2. Formatage d'une **SD 64 Go** + gravure de l'image.
3. **Premier boot** → onboarding → dashboard → **HA Core plante ~30 min après**.
4. Diagnostic : test de lecture SD (propre, 90 Mo/s), image (boote), alim (27 W confirmé).
5. **Surchauffe identifiée** (RPi 5 posé nu) → installation d'un **ventilateur**.
6. **Re-flash de la SD** (l'état HA avait été corrompu par les arrêts brutaux pendant la surchauffe).
7. Boot **stable** avec le ventilo → onboarding refait (« JC home », compte `jc`).
8. Installation de **Mosquitto broker** → **OK, en cours d'exécution**.
9. Installation de **Zigbee2MQTT** + configuration (`mqtt://core-mosquitto:1883`, `/dev/ttyACM0`, adapter `ember`) + **onboarding web (Submit)**.
10. Z2M a **détecté le dongle** et le **réseau Zigbee existant** (PANID `6699`) → la vanne, l'AirGuard serre et le LuxSerre sont **toujours appairés**.
11. **HA Core a re-planté** pendant/après l'installation des add-ons.

---

## 3. Résultat

### ✅ Ce qui fonctionne

- Le RPi 5 **boote et reste stable** (avec ventilateur) : ping OK, OS observer (`:4357`) répond 200 en continu.
- **Mosquitto** tourne (port 1883 ouvert).
- **Zigbee2MQTT** a démarré et **détecté le dongle + le réseau** : les 3 devices (vanne_serre, serre_temp_hum, LuxSerre) sont reconnus.
- Image HAOS **correcte**, SD **correcte**, alimentation **27 W correcte**, refroidissement **ajouté**.

### ❌ Ce qui ne fonctionne pas

- **HA Core** (interface web `:8123`) **plante de façon récurrente** : il démarre, fonctionne un temps, puis meurt **sans redémarrer**.
- Le crash survient de façon **reproductible** autour de l'installation/config des add-ons.

---

## 4. Où ça bute

**HA Core plante de façon récurrente, et la cause exacte est inconnue** (aucun log accessible à distance).

Éliminé jusqu'ici :
- ❌ la SD (2 cartes testées, lecture propre),
- ❌ l'image (elle boote correctement),
- ❌ l'alimentation (27 W officielle confirmée),
- ❌ la chaleur (ventilateur installé, le board tient désormais).

Suspects restants :
1. **Hardware RPi 5 défectueux** (un composant qui lâche sous charge).
2. **Bug HAOS 18.5 / HA Core** déclenché par l'installation des modules.

### Prochaine étape (pour trancher)

Lire les **logs de HA Core** — deux voies :
- **Écran HDMI + clavier** sur le RPi 5 (le plus simple ; la console affiche l'erreur).
- **SSH par clé USB** (port 22222, sans écran).

Selon le résultat :
- hardware défectueux → **échange du RPi 5** ;
- bug HAOS 18.5 → **essayer une autre version HAOS**.

---

## 5. Résolution — 2026-11-11

**Verdict : pas de plantage Core.** Le problème venait d'un mauvais diagnostic de port + la surchauffe d'origine (corrigée depuis par le ventilateur).

**Découvert via SSH debug (clé USB `CONFIG` + `authorized_keys` à la racine) :**
- HA Core tourne et répond **HTTP 200 sur le port 80** — pas 8123. Tous les contrôles « 8123 fermé → Core mort » visaient le mauvais port.
- Container `homeassistant` : `running`, `OOMKilled=false`, `ExitCode=0`, `RestartCount=0` → aucun crash matériel, pas de boucle.
- Core 2026.11.0, Supervisor 7.1.3, HAOS 18.5, watchdog actif.
- Le plantage du 07/11 = **surchauffe** (ventilateur installé depuis) + arrêts brutaux ayant corrompu la base sqlite (sessions « unfinished » dans les logs).

**Actions réalisées :**
- SSH debug permanent activé : `root@192.168.129.57 -p 22222` (clé id_ed25519 importée).
- Mot de passe du compte `jc` réinitialisé (`ha authentication reset`).
- Accès HA confirmé : `http://homeassistant.local` (port 80).

**Résolution Z2M (2026-11-11, plus tard dans la journée) :**
- L'option `serial` de l'addon était **figée sur `ttyACM0`** — l'API Supervisor 2026.10 refusait de la modifier (`extra keys not allowed`, seul `watchdog` accepté). Toute édition de fichier (`configuration.yaml`, `options.json`, `apps.json`) était écrasée par un override en variable d'environnement.
- **Fix : réinstallation de l'addon Z2M** (`ha apps uninstall` + `install`), qui a vidé les options `serial`/`mqtt` (`{}`), supprimant l'override fantôme. Le port est alors lu depuis `configuration.yaml` → `/dev/ttyUSB0`.
- Résultat : Z2M **healthy**, dongle reconnu, MQTT connecté, frontend :8099.

**Reste à faire :**
- ⚠️ **Re-appairer les 3 devices** (`vanne_serre`, `serre_temp_hum`, `LuxSerre`) : le réseau a été reformé (0 device joint) → permit join + bouton physique sur chaque device.
- Confirmer la stabilité de Core (24 h sans replantage).
- Option : remettre le port 80 → 8123 (standard HA).

---

## 6. Vérification post power-cycle — 2026-11-12

**Contexte :** JC a éteint/rebranché le RPi HOME pour l'installer dans une coque de protection. Ethernet oublié un temps (pensait que le WiFi suffirait — il n'est pas configuré).

**Verdict : RPi HOME OK.**
- Boot propre : 37 min d'uptime, charge 0.00, pas de crash.
- Core 2026.11.0 (HTTP 200 port 80), Supervisor `healthy`/`supported`, Mosquitto `started`.
- Dongle Sonoff détecté sur `/dev/ttyUSB0`.

**Point corrigé :** Z2M a redémarré en **état stale** après le power-cycle (logs figés à 00:04, frontend muet). Fix : `ha apps restart 45df7312_zigbee2mqtt` → démarrage propre, MQTT online, `serre_temp_hum` renvoie des mesures fraîches.

**Règles ajoutées (à respecter) :**
1. Après chaque coupure/reboot du RPi HOME → vérifier Z2M (`ha apps info` + logs), `restart` si stale.
2. Le frontend Z2M (8099) n'est pas exposé en direct — accès via ingress HA.
3. WiFi à configurer en secours si les capteurs sont trop loin (déplacement du RPi sans câble).

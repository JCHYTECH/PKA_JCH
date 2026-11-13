# Synthèse de session — RPi Home + Zigbee (2026-11-11)

> Dobby 🦉 — faits vérifiés + pièges à éviter. Projet 11_IOT.

---

## Faits (vérifiés, avec preuve)

### RPi Home — résolu
- **HA Core tourne sur le port 80**, pas 8123. Le « plantage » du 07/11 était un **faux diagnostic de port** : on testait 8123 alors que l'instance écoute sur 80 (`ha core info` → `port: 80`, `curl :80` → HTTP 200).
- Container `homeassistant` : `running`, `OOMKilled=false`, `ExitCode=0`, `RestartCount=0` → aucun crash matériel.
- **SSH debug permanent** activé : `root@192.168.129.57 -p 22222` (clé `id_ed25519` importée).
- Mot de passe `jc` réinitialisé (`ha authentication reset`).

### Zigbee2MQTT — réinstallé, healthy
- Dongle **Sonoff ZBDongle-E** détecté sur `/dev/ttyUSB0` (pas `ttyACM0`).
- L'option `serial` de l'addon était **figée sur `ttyACM0`** : l'API Supervisor 2026.10 refuse de la modifier (`extra keys not allowed`, seul `watchdog` est accepté).
- **Fix : réinstallation de l'addon** (`ha apps uninstall` + `install`) → options `serial`/`mqtt` vidées (`{}`) → le port est lu depuis `configuration.yaml` → `ttyUSB0`.
- Z2M : **Up (healthy)**, MQTT connecté, frontend :8099.

### serre_temp_hum — re-appairé
- Device `0xa4c1380f1ceaffff` (SONOFF SNZB-02DR2) rejoint, renommé `serre_temp_hum`.
- Mesures fraîches : **21,9 °C · 59,7 % · batterie 85 % · LQI 255**.

---

## Pièges à éviter (erreur → règle)

1. **Ne jamais conclure « Core mort » sur un port fermé.** Vérifier d'abord `ha core info` (le champ `port`) avant de diagnostiquer un plantage. (Coût ici : 4 jours de fausse piste.)

2. **Clé USB de debug HAOS : étiquette du volume = `CONFIG`** (pas un dossier), et `authorized_keys` **à la racine** du volume. Un dossier `CONFIG/` ou un fichier dedans ne fonctionne pas. Et il faut **redémarrer** pour que HAOS lise la clé (pas de hot-plug fiable).

3. **Ne pas bidouiller `apps.json`** (store interne du Supervisor) : les modifications directes sont écrasées par l'état mémoire du Supervisor, et un `kill` du Supervisor régénère le token. **Réinstaller l'addon** est le reset propre des options figées.

4. **Surveillance ping longue → `caffeinate -i`.** Le M5 s'est endormi pendant le relevé de 08:00 (réveil loggé à 08:21:19), ce qui a clairsemé la couverture — pas un bug du moniteur.

5. **Tâche de fond longue → `exec_shell background=true` ou `task_shell_start`.** Un `nohup ... &` dans une commande frontale est nettoyé à la fin de la commande (le relevé 1 h de 09:49 est mort, log à 0 octet).

---

## Reste à faire

- Re-appairer **`vanne_serre`** (Sonoff Smart Water Valve) + **`LuxSerre`** (Aqara Light Sensor T1) : permit join + bouton ~10 s + LED clignote.
- Confirmer stabilité Core sur 24 h.
- Option : remettre le port 80 → 8123 (standard).
- Lire le résultat du relevé 1 h box Proximus (`/tmp/box-monitor-1h-summary.json`).

*Fichiers à jour : `thread-iot.md`, `haos-rpi5-jchome-diagnostic.md`, `TTD.md`, `wiki/log.md`, `team.db` (memory_log), Daily note.*

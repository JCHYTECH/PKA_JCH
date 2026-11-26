# Résurrection du Karotz — 2026-11-09 (session complète)

> **Statut : ✅ SUCCÈS** — Karotz ressuscité avec miniil Karotz OS + miniil's OpenKarotz.
> **Résultat final** : lapin connecté (LED verte clignotante), interface web OpenKarotz opérationnelle sur `http://192.168.129.250`.

---

## Configuration finale (état stable à retenir)

- **Karotz** : IP fixe `192.168.129.250` · passerelle `192.168.128.1` (box Proximus) · masque `/23` (`255.255.254.0`) · DNS `8.8.8.8`.
- **WiFi dédié** : SSID « Karotz » émis par le **RUT240** (Teltonika) · chiffrement **WPA (TKIP)** · mode **802.11g** · canal 6.
- **Interface web** : `http://192.168.129.250` → Web `/api.html` · Mobile `/mui/index.html`.
- **Identifiants réseau** : voir `CONFIG-RESEAU-KAROTZ.md` (ne pas dupliquer les secrets ici).

---

## Les 6 problèmes rencontrés — et comment les éviter

1. **WPA2 ne marche pas.** Le Karotz ne supporte **pas le WPA2 seul** (confirmé noir sur blanc par miniil en commentaire du guide). Il faut **WPA (TKIP)** ou **WPA/WPA2 mixte**. ⚠️ À vérifier AVANT de flasher, sinon LED bleue bloquée.

2. **Mode 802.11n invisible.** En mode `11ng` le lapin ne voit pas le réseau (il reste en LED bleue, impossible de s'associer). Il faut forcer le mode **`11g`** (802.11g) sur l'AP.

3. **Clé USB laissée branchée.** Tant que la clé reste dans le lapin, **l'installation se relance à chaque démarrage** et, pire, elle **efface `/etc/inetd.conf`** (config du serveur web) juste après que le boot l'ait recopiée → le serveur web échoue. **Toujours retirer la clé après le flash.**

4. **Le serveur web ne démarre pas.** Le script de démarrage (`startup.sh`) peut se figer sur l'étape dbus. Correctif appliqué : lancer **`inetd` directement** dans `waitfornetwork.sh` (ligne `/sbin/inetd -f /usr/etc/inetd.conf &`), sans attendre l'étape qui bloque.

5. **Firmware corrompu après une coupure.** Une coupure réseau/alim a laissé le lapin avec une **MAC aléatoire** (au lieu de sa vraie `00:0E:8E:…`) + boot figé (LED rouge, muet, aucune tentative WiFi). Un **re-flash propre** a corrigé.

6. **Route par défaut du RUT240.** Le RUT240 routait par défaut via `wwan0` (modem mobile sans SIM). Pour le lapin (bridge L2) ça ne compte pas (il route lui-même via la box), mais noter que la box Proximus **bloque le ping vers elle-même** depuis le répéteur tout en **relayant** le trafic internet (8.8.8.8 répond).

---

## Procédure exacte qui a marché (référence rapide)

1. **Clé USB** FAT32 avec les fichiers miniil (`usbkey.zip`) + `waitfornetwork.sh` édité : IP/SSID/PWD corrects **+ la ligne `inetd`** (correctif problème n°4).
2. **RUT240** : WiFi « Karotz » en **WPA (TKIP)**, mode **11g**.
3. **Flash** : lapin éteint → insérer la clé → démarrer → installation vocale (orange/vert) → **retirer la clé** → redémarrer.
4. **Boot normal** → LED **verte clignotante** (démarrage complet) → serveur web sur le port 80.
5. **Navigateur** → `http://192.168.129.250` → bouton « Install Open Karotz » → ~2 min (téléchargement depuis `karotz.miniil.be`) → `F5`.

---

## Futur : autres jouets (Cozmo et consorts)

- JC envisage d'installer **d'autres robots/jouets** (ex. **Cozmo** d'Anki, évoqué dans une autre session).
- **Leçons réutilisables** pour tout nouvel objet connecté :
  - Vérifier la **compatibilité WiFi** (WPA vs WPA2, mode 802.11g/n) AVANT de tenter quoi que ce soit.
  - Repérer **où tourne le cerveau** : à bord vs déporté (Karotz = déporté sur M5/HA ; Cozmo = sur le téléphone appairé).
  - Repérer **comment on pilote l'objet** : flash USB + interface web (Karotz) vs SDK Python + app (Cozmo).
  - Repérer la **procédure de flash/appairage** et ses pièges (clé à retirer, ne pas éteindre pendant le flash, rester appairé).
  - Identifier le **serveur/interface web local** et comment il se lance (et ce qui l'empêche de démarrer).
  - Toujours **retirer le support de boot** après installation.
- **Cozmo** : fichier de travail créé → [`../cozmo-reborn/README.md`](../cozmo-reborn/README.md) (leçons transposées, PoC, verrous).

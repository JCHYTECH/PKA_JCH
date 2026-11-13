# Configuration réseau — Karotz Reborn

> Valeurs à coller dans `waitfornetwork.sh` (après avoir téléchargé `usbkey.zip` depuis miniil.be).
> ⚠️ Ce fichier contient le **mot de passe WiFi en clair** (nécessaire pour le Karotz). Garder ce dossier privé.

## Les 6 valeurs

| Champ | Valeur |
|---|---|
| IP (adresse du lapin) | `192.168.129.250` |
| DNS | `8.8.8.8` |
| GW (adresse de ta box) | `192.168.128.1` |
| NM (masque du réseau) | `255.255.254.0` |
| SSID (nom du réseau) | `Karotz` (réseau du RUT240, mode « ancien + récent ») |
| PWD (mot de passe) | `karotz2026` (simplifié — sans `!`, le vieux WiFi du lapin a du mal avec les caractères spéciaux) |

## Précisions

- **IP** : `192.168.129.250` est proposée libre (le Mac est en `.56`, le RPi van en `.16`). Si la box signale un conflit, prendre `.251`.
- **NM** : `255.255.254.0` = le vrai masque du réseau Proximus (détecté sur le Mac). Ne pas utiliser le `255.255.255.0` de l'exemple miniil, sinon le lapin ne routrait pas.
- **DNS** : `8.8.8.8` (Google) — c'est le plus simple.

## ⚠️ Blocage possible avant flash — la sécurité WiFi

Le Karotz ne lit que l'**ancien type de protection WiFi** (WPA), pas le récent (WPA2) seul. Vérifier avant de flasher :

1. Navigateur → `192.168.128.1` → se connecter (identifiants sur l'étiquette de la box).
2. Menu **Wi-Fi** → **Sécurité**.
3. Passer de « WPA2 » (récent seul) à « **WPA + WPA2** » (mixte).

Si ce réglage n'existe pas sur la box, il faudra un autre point d'accès (ou un vieux routeur) pour le Karotz.

## À faire ensuite

1. Télécharger `usbkey.zip` (lien « ICI » sur la page miniil.be).
2. Décompresser, éditer `waitfornetwork.sh` avec les 6 valeurs ci-dessus.
3. Formater la clé USB en FAT32, copier tous les fichiers.
4. Karotz éteint → insérer la clé → démarrer → laisser flasher (messages vocaux).

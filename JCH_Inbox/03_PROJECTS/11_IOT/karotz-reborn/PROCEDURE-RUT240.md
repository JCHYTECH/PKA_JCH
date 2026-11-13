# Procédure — RUT240 comme réseau dédié au Karotz

> Objectif : créer un **petit réseau WiFi « ancien + récent »** pour le lapin, branché sur ta box Proximus, pour que le lapin reste sur le **même réseau que Home Assistant**.
> Pourquoi : la box Proximus (Internet Box) ne se règle plus localement et ne permet probablement pas le mode « ancien + récent ».

## Prérequis (matériel)

- Le **RUT240** (en stock)
- Son **alimentation** (bloc 9–30 V fourni, ou PoE)
- **1 câble Ethernet** (pour relier RUT240 → box Proximus)
- Ton **Mac** pour la configuration initiale

---

## Étape 1 — Allumer et se connecter au RUT240

1. Branche l'alimentation du RUT240.
2. Connecte-toi à son **WiFi par défaut** (nom « `RUT240_XXXX` », mot de passe sur l'étiquette **dessous** le boîtier) — **ou** un câble Ethernet entre ton Mac et le **port LAN** du RUT240.
3. Navigateur → `192.168.1.1` → identifiants `admin` / `admin01`.
4. Au premier démarrage, il demande de **changer le mot de passe** → choisis-en un simple (ex. `karotz2026`).

## Étape 2 — Régler le WiFi « ancien + récent »

5. Menu **Network → Wireless** :
   - **Nom du réseau** : `Karotz`
   - **Sécurité** : choisis l'option **mixte** (souvent nommée « WPA/WPA2 » ou « WPA2/WPA ») — c'est le mode « ancien + récent » que le lapin comprend.
   - **Mot de passe** : `karotz2026` (exemple, mets ce que tu veux)
6. Enregistrer.

## Étape 3 — Relier le RUT240 à ta box (même réseau que HA)

7. Menu **Network → LAN** : **désactive le serveur d'adresses (DHCP)** du RUT240 — c'est la box Proximus qui doit distribuer les adresses (sinon conflit).
8. **Adresse du RUT240** → `192.168.129.2` (pour pouvoir l'administrer plus tard depuis ton Mac).
9. Enregistrer + **redémarrer** le RUT240.

## Étape 4 — Brancher

10. Câble Ethernet entre le **port LAN du RUT240** et un **port LAN de la box Proximus**.
11. Vérifie : le réseau **`Karotz`** apparaît, et un appareil qui s'y connecte reçoit une adresse `192.168.128.x` / `192.168.129.x` (la même plage que ton Mac en `.56`).

## Étape 5 — Configurer le lapin

12. Mets à jour `CONFIG-RESEAU-KAROTZ.md` :
    - SSID → `Karotz`
    - PWD → (le mot de passe du réseau Karotz)
    - **IP, GW, NM, DNS inchangés** (le lapin reste sur le même réseau, via le pont du RUT240)

---

*Note : les noms exacts des menus peuvent varier selon la version du firmware RUT240 (00.07.xx). Si l'option « mixte » n'apparaît pas dans la sécurité, dis-le-moi — on regardera la version.*

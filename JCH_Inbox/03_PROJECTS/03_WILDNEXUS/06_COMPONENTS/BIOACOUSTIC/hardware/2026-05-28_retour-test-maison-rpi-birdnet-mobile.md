# Retour test maison — RPi BirdNET-Pi + MF833U1 LTE

**Date :** 2026-05-28  
**Durée :** 2h13 (19:35 – 21:48)  
**Machine :** tkajch ([[Raspberry Pi 5]], BirdNET-Pi, [[Tailscale]] 100.84.45.93)  
**Testeur :** JCH + [[Dobby]]  
**Protocole :** Phase 1 (maison 2h) — powerbank, LTE uniquement, audio BOYA BY-MM1

---

## Résumé

Le modem MF833U1 LTE fonctionne parfaitement. L'interface BirdNET-Pi est accessible via [[Tailscale]]. L'autonomie powerbank est excellente (10/10 LED après 2h). Trois problèmes bloquants identifiés et corrigés. Le système tourne en continu, à laisser jusqu'à demain matin.

---

## Résultats par composant

### MF833U1 LTE — SUCCES

- Détection USB : `19d2:1706 ZTE DEMO Mobile Boardband`
- Interface `eth1`, IP `192.168.0.178/24`
- Route prioritaire configurée (metric 100 vs wlan0 metric 600)
- Ping 8.8.8.8 : 40-143ms
- DNS + ping google.com : 18-37ms

### [[Tailscale]] — SUCCES

- Mac : `100.108.55.44` (macbook-pro-de-jc-1)
- RPi : `100.84.45.93` (tkajch)
- Interface [[BirdNET]] accessible via `http://100.84.45.93`

### Powerbank Anker 20100 mAh / 72.36 Wh — SUCCES autonomie

- 10/10 LED après 2h+ de test
- ATTENTION : USB classique (pas PD) -> undervoltage chronique -> throttling

### Audio BOYA BY-MM1 — SUCCES

- Micro fonctionnel, [[BirdNET]] analyse en continu
- Détections confirmées : Merle noir, Buse variable, Pinson des arbres

---

## Problèmes identifiés et corrigés

### 1. Undervoltage chronique (NON CORRIGE, materiel)

- `throttled=0x50000`, ~15 episodes d'undervoltage dans dmesg
- Cause : port USB classique du powerbank (max 2.4A) insuffisant pour RPi 5 (demande 5V/5A)
- Conséquence : throttling CPU + reboot a 21:09
- **Action requise :** utiliser un cable et port USB-C PD (Power Delivery)

### 2. DB readonly "Database busy" (CORRIGE, permanent)

- Cause : conflit d'ownership WAL [[SQLite]] entre `jchavaux` (analyse [[Python]]) et `caddy` (serveur web)
- Fix applique :
  - `jchavaux` ajoute au groupe `caddy`
  - Repertoire scripts en setgid 2775
  - Override systemd : `Group=caddy` + `UMask=0002`
  - DB : `chown jchavaux:caddy`, `chmod 664`

### 3. Coordonnees GPS erronees (CORRIGE)

- Etaient : `51.1904 / 4.4294` (Anvers)
- Corrigees : `50.55 / 5.57` (Esneux-Tilff)

### 4. Documentation erronee (CORRIGE)

- Les docs referencaient le port 8080 pour l'interface
- Port correct : **80** (8080 = gotty, binde localhost uniquement)
- Fichiers mis a jour : `BIRDNET_PI_ACCESS.md`, `connexion RPI.md`

---

## Points de vigilance restants

- wlan0 s'est reconnecte automatiquement malgre le `disconnect` -> autoconnect pas totalement desactive
- Test LTE pur biaise par la reconnexion Wi-Fi

---

## Decisions

- Laisser tourner jusqu'au matin 2026-05-29 pour mesurer l'autonomie reelle complete
- Pour le test terrain 24h : **obligatoire cable USB-C PD** entre powerbank et RPi
- Le fix DB doit etre documente dans MEMORY.md comme procedure standard BirdNET-Pi

---

## Prochaine iteration

- Test terrain 24h avec cable USB-C PD
- Verifier que le fix DB tient apres un reboot a froid
- Desactiver definitivement l'autoconnect Wi-Fi avant test LTE pur

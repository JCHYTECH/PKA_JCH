# BirdNET-Pi - Acces local et reperes critiques

**Date de creation :** 2026-05-24  
**Derniere mise a jour :** 2026-06-03 — IP Tailscale active `100.66.110.60` observee, ancienne IP `100.84.45.93` inactive  
**Projet :** WildNexus / Bioacoustique  
**Machine :** [[Raspberry Pi]] BirdNET-Pi  
**Owner :** JCH  
**Regle :** ne pas stocker les mots de passe en clair dans PKA.

## Acces web BirdNET-Pi

### Port correct (valide 2026-05-28)

**L'interface BirdNET-Pi ecoute sur le port 80** (nginx integre).
Le port 8080 du RPi est `gotty` (terminal web), binde sur `127.0.0.1` uniquement — inaccessible depuis l'exterieur.
Ne pas utiliser `:8080` pour l'interface BirdNET-Pi sur cette machine.

```text
http://<ip ou hostname>       # port 80 — interface BirdNET-Pi
```

### URL canonique cible

URL fixe souhaitee :

```text
http://birdnetpi.local
```

Raison : les IP `172.20.10.x` du hotspot iPhone peuvent changer. Le nom `.local` via Avahi/Bonjour doit etre privilegie pour un acces stable depuis Safari iPhone et depuis Mac.

Plan de stabilisation :

1. ✅ fixer le hostname Raspberry a `birdnetpi` — fait 2026-05-29 (`hostnamectl set-hostname` + `preserve_hostname: true` dans cloud-init) ;
2. ✅ `avahi-daemon` actif et operationnel ;
3. utiliser `http://birdnetpi.local` comme URL principale (OK sur reseau local) ;
4. ✅ `192.168.1.48` reservation routeur maison — IP WiFi wlan0 ;
5. ✅ [[Tailscale]] actif : `100.66.110.60` — acces distant observe le 2026-06-03.

**Reseau — priorite (2026-05-29) :** WiFi maison (wlan0, metric 600) primaire, LTE dongle (eth1, metric 700) backup.

### [[Tailscale]] / Tailnet

Objectif si acces stable hors reseau local :

```text
http://birdnetpi.<tailnet>.ts.net
```

ou via IP [[Tailscale]] :

```text
http://100.x.y.z
```

IPs [[Tailscale]] observees le 2026-05-28 :

```text
MacBook-Pro-de-JC-1 : 100.108.55.44
iPhone 182 : 100.75.75.90
tkajch (Raspberry Pi BirdNET-Pi) : 100.84.45.93
```

Observation 2026-06-03 :

```text
rpi-pkajch (Raspberry Pi BirdNET-Pi) : 100.66.110.60 — ping Tailscale OK
ancienne IP 100.84.45.93 — no reply
SSH jchavaux@100.66.110.60 — hote joignable, authentification non interactive refusee (publickey,password)
```

URL Tailnet stable a tester pour BirdNET-Pi :

```text
http://100.66.110.60
```

Statut Mac observe le 2026-05-24 :

```text
Tailscale installe mais arrete sur le Mac : "Tailscale is stopped."
```

Verification a faire sur le Raspberry :

```bash
tailscale status
tailscale ip -4
hostname
```

Si [[Tailscale]] est absent du Raspberry :

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Ensuite activer/verifier MagicDNS dans la console [[Tailscale]], puis tester depuis iPhone :

```text
http://birdnetpi.<tailnet>.ts.net
```

### iPhone / Safari

Depuis l'iPhone, Safari peut acceder a l'interface BirdNET-Pi si l'iPhone et le Raspberry sont sur le meme reseau :

- meme Wi-Fi maison ;
- ou iPhone en hotspot et Raspberry connecte a ce hotspot.

URLs a tester pour l'interface et l'historique des detections :

```text
http://birdnetpi.local
http://192.168.1.48
http://192.168.1.48:8080
```

Dans l'interface BirdNET-Pi, chercher les entrees de type :

- `History`
- `Detections`
- `Charts`
- `Tools`

Si Safari affiche l'interface mais pas l'historique, verifier d'abord le port correct, puis le service web BirdNET-Pi.

### Reseau maison

Adresse probable reservee / fixe :

```text
192.168.1.48
```

URLs a tester :

```text
http://192.168.1.48
http://192.168.1.48
http://birdnetpi.local
```

Note 2026-05-28 : le port 80 est le port correct pour l'interface BirdNET-Pi. Le port 8080 de cette machine appartient a `gotty` (terminal web), binde sur localhost uniquement.

### Hotspot iPhone

Plage observee :

```text
172.20.10.x
```

Exemples traces :

```text
172.20.10.2
172.20.10.7
172.20.10.8
172.20.10.15
```

Historique Safari iPhone observe le 2026-05-24 :

```text
http://172.20.10.2/
http://172.20.10.7/
```

Commande de scan depuis le Mac si l'iPhone sert de hotspot :

```bash
for i in $(seq 1 20); do ping -c 1 -W 1 172.20.10.$i > /dev/null 2>&1 && echo "172.20.10.$i alive"; done
```

## Acces Tools BirdNET-Pi

Identifiant web Tools :

```text
birdnet
```

Mot de passe Tools :

```text
vide par defaut, sauf modification ulterieure
```

## Acces SSH [[Raspberry Pi]]

Utilisateur SSH actuel :

```text
jchavaux
```

Commandes :

```bash
ssh jchavaux@birdnetpi.local
ssh jchavaux@192.168.1.48
```

Mot de passe SSH :

```text
connu de JCH ; ne pas ecrire en clair dans PKA
```

## Modele [[BirdNET]] observe

Modele en place :

```text
BirdNET_GLOBAL_6K_V2.4_Model_FP16
```

Lecture :

- `GLOBAL` : modele mondial.
- `6K` : environ 6000 classes/especes.
- `V2.4` : generation du modele.
- 

## Commandes utiles

### Outil de diagnostic et réparation rapide ([[Dobby]] Tool)

J'ai installé un script sur le RPi pour diagnostiquer et réparer automatiquement les problèmes de base de données ("Database is busy") ou de services plantés.

**Lancer le diagnostic :**
```bash
ssh jchavaux@100.84.45.93 "/home/jchavaux/BirdNET-Pi/scripts/birdnet_check.sh"
```

**Lancer la réparation automatique :**
```bash
ssh jchavaux@100.84.45.93 "/home/jchavaux/BirdNET-Pi/scripts/birdnet_check.sh --repair"
```

### Verifier l'adresse IP du Raspberry :

```bash
hostname -I
```

Verifier le reseau Wi-Fi cote Raspberry :

```bash
nmcli device status
nmcli connection show
```

Verifier l'installation BirdNET-Pi :

```bash
cd ~/BirdNET-Pi
git remote get-url origin
git branch --show-current
git log -1 --oneline
```

Chercher le modele [[BirdNET]] :

```bash
find ~/BirdNET-Pi -iname '*model*' -o -iname '*BirdNET*'
```

## Changer la langue des noms d'especes

**Procedure validee 2026-05-30 :**

```bash
# 1. Modifier le parametre dans la config
sudo sed -i 's/^DATABASE_LANG=.*/DATABASE_LANG=fr/' /etc/birdnet/birdnet.conf

# 2. Regenere les labels (telecharge les noms francais)
cd /home/jchavaux/BirdNET-Pi/scripts && sudo -E ./install_language_label.sh

# 3. Redemarrer les services
sudo systemctl restart birdnet_analysis.service birdnet_log.service \
  birdnet_recording.service birdnet_stats.service chart_viewer.service \
  spectrogram_viewer.service
```

**Note :** les detections deja enregistrees gardent leur nom d'origine (anglais) dans `birds.db`. Seules les nouvelles detections utilisent la nouvelle langue apres redemarrage.

## EventNET — detection acoustique meteo (orage, pluie, vent)

**Installe le 2026-05-30.** YAMNet (AudioSet, 521 classes) en parallele de BirdNET sur le meme flux audio.

### Fonctionnement

- `eventnet.service` surveille les WAV produits par BirdNET dans `StreamData/` via inotify
- Chaque segment est analyse par YAMNet TFLite (modele ~4 Mo)
- Les evenements météo (score > 0.15) sont loggues dans `events.db`

### Classes detectees

| Classe | AudioSet ID |
|--------|-------------|
| Tonnerre | `/m/0ngt1` |
| Orage | `/m/0jbk` |
| Pluie | `/m/06mb1` |
| Pluie (surface) | `/t/dd00129` |
| Vent | `/m/03m9d0h` |
| Vent (micro) | `/m/0cj0r` |

### Commandes

```bash
# Statut du service
sudo systemctl status eventnet

# Voir les logs en direct
tail -f /home/jchavaux/BirdNET-Pi/eventnet/eventnet.log

# Stats des detections
/home/jchavaux/BirdNET-Pi/birdnet/bin/python3 /home/jchavaux/BirdNET-Pi/eventnet/eventnet_detect.py --stats

# Derniers evenements (SQLite direct)
sqlite3 /home/jchavaux/BirdNET-Pi/eventnet/events.db "SELECT timestamp,class_name_fr,score FROM events ORDER BY id DESC LIMIT 10;"
```

### Fichiers

```
/home/jchavaux/BirdNET-Pi/eventnet/
├── yamnet.tflite           # Modele YAMNet TFLite (~4 Mo)
├── yamnet_class_map.csv    # 521 classes AudioSet
├── eventnet_detect.py      # Script de detection
├── events.db               # Base SQLite des evenements
├── eventnet.log            # Logs du service
└── processed_files.txt     # Fichiers deja traites
```

### Script local PKA

`scripts/eventnet_detect.py` + `scripts/eventnet.service`

## Regle memoire [[Dobby]]

Toute nouvelle information d'acces BirdNET-Pi doit etre ajoutee ici :

- IP fixe ou reserve DHCP ;
- URL fonctionnelle ;
- port correct ;
- identifiant non sensible ;
- existence d'un secret sans le secret ;
- commande de verification qui a marche ;
- date de validation.

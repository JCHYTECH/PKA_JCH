---
type: protocol
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - [[BirdNET]]
  - raspberry-pi
  - bioacoustique
  - terrain
  - mobile
owner: "[[Chouette]]"
project: "[[WILDNEXUS]]"
---

# Protocole terrain 24 h — [[Raspberry Pi 5]] + BirdNET-Go mobile

## Objectif

Tester si un systeme mobile compose d'un [[Raspberry Pi 5]] avec [[BirdNET-Go]], d'un micro BOYA BY-MM1, d'un powerbank Anker 20100 mAh / 72.36 Wh et d'une connexion via iPhone peut fonctionner en continu dans un site riche en oiseaux et eloigne pendant une periode cible de 24 heures.

Le test doit mesurer :

- autonomie reelle ;
- stabilite BirdNET-Go ;
- stabilite audio ;
- stabilite reseau via hotspot iPhone ou connexion mobile ;
- capacite a consulter l'interface depuis iPhone ou MacBook ;
- qualite et quantite des detections [[BirdNET]].

## Hypothese a verifier

La batterie Anker 72.36 Wh peut ne pas suffire pour 24 h si le [[Raspberry Pi 5]], BirdNET-Go, l'audio USB et le reseau mobile consomment trop.

Le critere important du premier test n'est donc pas seulement "tenir 24 h", mais :

- mesurer la duree reelle ;
- identifier le maillon limitant ;
- verifier que la capture [[BirdNET]] reste propre jusqu'a extinction ou recuperation.

## Materiel

| Element | Role |
|---|---|
| [[Raspberry Pi 5]] | calcul BirdNET-Go |
| micro BOYA BY-MM1 | capture audio directionnelle |
| adaptateur audio USB UGREEN ou equivalent | entree micro vers [[Raspberry Pi]] |
| powerbank Anker 20100 mAh / 72.36 Wh | alimentation terrain |
| cable USB-C haute puissance | alimentation [[Raspberry Pi]] |
| iPhone | hotspot, consultation, secours terrain |
| MacBook | configuration et controle avant depart |
| boitier / protection pluie temporaire | protection terrain hors pluie directe |
| carte microSD suffisante | systeme + logs + captures [[BirdNET]] |
| option : MF833U1 LTE USB | connectivite mobile alternative ou complementaire |

## Architecture de test

```text
BOYA BY-MM1
  -> adaptateur audio USB
  -> Raspberry Pi 5
  -> BirdNET-Go
  -> reseau maison avant depart
  -> hotspot iPhone ou modem LTE en terrain
  -> consultation iPhone / MacBook

Powerbank Anker
  -> alimentation Raspberry Pi 5
  -> alimentation indirecte des peripheriques USB via Raspberry Pi
```

Important : si le modem MF833U1 est utilise, il doit rester connecte au [[Raspberry Pi]] pour les donnees. Si son alimentation est separee du powerbank, utiliser un hub USB alimente ou une solution equivalente. Une cle USB LTE ne peut pas communiquer avec le [[Raspberry Pi]] si elle est seulement branchee au powerbank.

## Cadrage WildNexus

Ce protocole concerne le banc mobile [[BirdNET-Go]] / bioacoustique. Il ne modifie pas l'architecture Satellite Lite P0 :

- Satellite Lite P0 : AA, frugal, local, [[LoRa]]/statuts/metadonnees.
- Banc [[BirdNET]] mobile : [[Raspberry Pi]], BirdNET-Go, powerbank, hotspot/LTE, test terrain 24 h.

## Phase 0 — Preparation maison

### 0.1 Verifier que BirdNET-Go tourne parfaitement sur le reseau maison

Depuis le MacBook ou l'iPhone connecte au Wi-Fi maison :

```text
http://birdnetpi.local
http://birdnetpi.local:8080
http://192.168.1.48
http://192.168.1.48:8080
```

Depuis le [[Raspberry Pi]] :

```bash
hostname
hostname -I
nmcli device status
docker ps
```

Si BirdNET-Go tourne comme service systemd plutot que [[Docker]] :

```bash
systemctl status birdnet-go
```

Si BirdNET-Pi est utilise sur cette machine :

```bash
cd ~/BirdNET-Pi
git branch --show-current
```

### 0.2 Verifier l'audio

Lister les peripheriques audio :

```bash
arecord -l
arecord -L
```

Faire un enregistrement court :

```bash
mkdir -p ~/birdnet-field-test
arecord -D plughw:1,0 -f S16_LE -r 48000 -c 1 -d 20 ~/birdnet-field-test/audio-test.wav
aplay ~/birdnet-field-test/audio-test.wav
```

Si `plughw:1,0` ne correspond pas a l'adaptateur USB, adapter selon `arecord -l`.

Controle attendu :

- signal audible ;
- pas de saturation evidente ;
- pas de craquements ;
- BirdNET-Go continue a recevoir l'audio apres test.

### 0.3 Verifier le hotspot iPhone

Sur iPhone :

1. Reglages.
2. Partage de connexion.
3. Activer "Autoriser les autres utilisateurs".
4. Activer "Maximiser la compatibilite".
5. Garder l'ecran sur cette page pendant le demarrage du [[Raspberry Pi]].

Sur [[Raspberry Pi]] :

```bash
nmcli dev wifi list
sudo nmcli dev wifi connect "NOM_HOTSPOT_IPHONE" password "MOT_DE_PASSE"
nmcli connection show
```

Ne pas stocker le mot de passe dans PKA.

Definir les priorites :

```bash
sudo nmcli connection modify "NOM_WIFI_MAISON" connection.autoconnect-priority 20
sudo nmcli connection modify "NOM_HOTSPOT_IPHONE" connection.autoconnect-priority 10
```

Test de bascule :

1. eteindre temporairement le Wi-Fi maison ou l'oublier seulement pour test ;
2. activer hotspot iPhone ;
3. redemarrer le [[Raspberry Pi]] ;
4. verifier que l'iPhone indique une connexion ;
5. ouvrir l'interface [[BirdNET]] depuis Safari.

### 0.4 Option : verifier [[Tailscale]]

Sur [[Raspberry Pi]] :

```bash
tailscale status
tailscale ip -4
```

Sur iPhone :

- ouvrir [[Tailscale]] ;
- verifier que le VPN est connecte ;
- tester l'URL ou l'IP [[Tailscale]] du [[Raspberry Pi]].

[[Tailscale]] est preferable pour eviter les changements d'IP du hotspot.

### 0.5 Option : verifier le modem MF833U1 LTE

Si le test utilise le MF833U1 :

```bash
lsusb
ip addr
nmcli device
dmesg | tail -80
```

Verifier :

- detection USB ;
- creation d'une interface reseau ;
- SIM et APN ;
- route Internet ;
- stabilite apres reboot ;
- coexistence avec l'adaptateur audio USB.

## Phase 1 — Test maison 2 heures

Avant toute sortie 24 h, faire un test complet a la maison pendant 2 heures.

### Configuration

- [[Raspberry Pi]] alimente par le powerbank.
- BOYA BY-MM1 branche via adaptateur audio USB.
- Reseau via hotspot iPhone ou MF833U1, pas Wi-Fi maison.
- BirdNET-Go lance et consultable.

### Releves au demarrage

```bash
date
hostname -I
nmcli device status
docker ps
vcgencmd measure_temp
uptime
df -h
```

Si disponible :

```bash
vcgencmd get_throttled
```

### Releves apres 30, 60 et 120 minutes

```bash
date
uptime
vcgencmd measure_temp
vcgencmd get_throttled
df -h
nmcli device status
dmesg | tail -40
```

Noter :

- pourcentage restant du powerbank ;
- acces interface [[BirdNET]] ;
- nombre de detections ;
- presence de coupures audio ;
- temperature ;
- erreurs reseau.

Critere de passage terrain : aucun reboot, interface accessible, audio stable, temperature acceptable, au moins 2 h continues.

## Phase 2 — Installation terrain

### Choix du site

Choisir un endroit :

- riche en oiseaux ;
- eloigne des routes et machines ;
- sans risque de vol evident ;
- hors pluie directe ;
- avec support stable pour le micro ;
- avec reception mobile suffisante si suivi distant requis.

### Placement micro

BOYA BY-MM1 :

- oriente vers la zone d'activite aviaire ;
- protege du vent direct ;
- eloigne du [[Raspberry Pi]] et du powerbank autant que le cable le permet ;
- pas enferme dans le meme boitier que le ventilateur du [[Raspberry Pi]] ;
- eviter contact direct avec branches, herbes ou surfaces vibrantes.

### Placement [[Raspberry Pi]] / powerbank

- placer dans une boite ou sac de protection vent/pluie, sans etouffer la ventilation ;
- laisser une circulation d'air minimale ;
- proteger les connexions USB ;
- eviter condensation directe ;
- sur-elever du sol ;
- eviter exposition solaire directe.

## Phase 3 — Demarrage terrain

1. Activer hotspot iPhone ou brancher le MF833U1.
2. Brancher le micro/adaptateur audio.
3. Brancher le [[Raspberry Pi]] au powerbank.
4. Attendre 2 minutes.
5. Verifier sur iPhone qu'une connexion est active.
6. Ouvrir [[BirdNET]] :

```text
http://birdnetpi.local:8080
http://100.84.45.93:8080
http://172.20.10.2:8080
```

7. Verifier les detections ou l'etat live.
8. Noter l'heure exacte de debut.

## Phase 4 — Suivi pendant 24 h

### Releves minimum

| Moment | Controle |
|---|---|
| T0 | demarrage, acces interface, audio, batterie |
| T+30 min | interface, temperature, detections |
| T+2 h | stabilite, batterie, reseau |
| T+6 h | si possible : interface, batterie |
| T+12 h | si possible : interface, batterie |
| T+24 h | recuperation, logs, etat final |

Si le site est vraiment eloigne et non visite pendant 24 h, faire au minimum :

- T0 complet ;
- T+24 recuperation complete.

### Journal terrain

Noter manuellement :

- lieu approximatif ;
- meteo ;
- vent ;
- pluie ;
- heure debut ;
- orientation micro ;
- reseau utilise ;
- niveau batterie initial ;
- niveau batterie a recuperation ;
- heure d'arret si le systeme est eteint ;
- observations oiseaux visibles/audibles.

## Phase 5 — Recuperation

Au retour :

```bash
date
uptime
hostname -I
docker ps
vcgencmd measure_temp
vcgencmd get_throttled
df -h
dmesg | tail -120
```

Exporter ou sauvegarder :

- logs BirdNET-Go ;
- detections ;
- extraits audio si disponibles ;
- captures d'ecran interface ;
- notes terrain.

Verifier :

- duree exacte avant extinction ou recuperation ;
- nombre total de detections ;
- distribution horaire ;
- coupures reseau ;
- coupures audio ;
- temperature maximale observee ;
- espace disque restant.

## Criteres de reussite

### Reussite complete

- 24 h de fonctionnement ;
- BirdNET-Go actif jusqu'a la recuperation ;
- audio stable ;
- reseau consultable au moins au demarrage et a la recuperation ;
- pas de reboot non desire ;
- donnees exploitables.

### Reussite partielle

- autonomie inferieure a 24 h mais superieure a 6 h ;
- donnees audio/detections exploitables ;
- cause probable identifiee : batterie, reseau, temperature, stockage ou audio.

### Echec utile

- systeme arrete avant 6 h ;
- mais logs suffisants pour identifier la cause.

## Risques et parades

| Risque | Cause probable | Parade |
|---|---|---|
| autonomie < 24 h | RPi 5 + [[BirdNET]] + LTE trop consommateurs | mesurer duree reelle, prevoir powerbank plus grand ou double alimentation |
| reboot | sous-alimentation ou cable faible | cable USB-C haute puissance, port powerbank haute sortie |
| audio absent | mauvais device ALSA | verifier `arecord -l`, figer device dans BirdNET-Go |
| bruit mecanique | micro trop proche du RPi/fan | eloigner micro, proteger du vent |
| perte hotspot | iPhone verrouille/eloigne/5 GHz instable | maximiser compatibilite, garder iPhone proche, [[Tailscale]] si possible |
| modem LTE instable | APN/SIM/driver/alimentation | test maison 2 h avant terrain |
| stockage plein | captures/logs trop volumineux | verifier `df -h`, limiter retention si necessaire |

## Donnees a produire apres test

Creer une note de retour :

```text
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/hardware/YYYY-MM-DD_retour-test-terrain-birdnet-mobile.md
```

Structure :

- contexte ;
- materiel ;
- lieu ;
- meteo ;
- duree ;
- reseau ;
- alimentation ;
- resultats [[BirdNET]] ;
- incidents ;
- decision prochaine iteration.

## Decision

Le test terrain 24 h est valide comme essai BirdNET-Go mobile. Il doit etre precede d'un test maison 2 h sur powerbank et reseau mobile/hotspot. Le resultat attendu est une mesure d'autonomie et de stabilite, pas une validation definitive du Satellite Lite P0.

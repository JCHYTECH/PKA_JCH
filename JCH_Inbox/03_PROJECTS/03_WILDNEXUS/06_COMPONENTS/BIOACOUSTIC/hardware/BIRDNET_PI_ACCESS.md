# BirdNET-Pi - Acces local et reperes critiques

**Date de creation :** 2026-05-24  
**Projet :** WildNexus / Bioacoustique  
**Machine :** Raspberry Pi BirdNET-Pi  
**Owner :** JCH  
**Regle :** ne pas stocker les mots de passe en clair dans PKA.

## Acces web BirdNET-Pi

### URL canonique cible

URL fixe souhaitee :

```text
http://birdnetpi.local
```

Raison : les IP `172.20.10.x` du hotspot iPhone peuvent changer. Le nom `.local` via Avahi/Bonjour doit etre privilegie pour un acces stable depuis Safari iPhone et depuis Mac.

Plan de stabilisation :

1. fixer le hostname Raspberry a `birdnetpi` ;
2. verifier/installer `avahi-daemon` ;
3. utiliser `http://birdnetpi.local` comme URL principale ;
4. conserver `192.168.1.48` comme reservation routeur maison ;
5. utiliser Tailscale/MagicDNS si une URL stable est requise hors reseau local.

### Tailscale / Tailnet

Objectif si acces stable hors reseau local :

```text
http://birdnetpi.<tailnet>.ts.net
```

ou via IP Tailscale :

```text
http://100.x.y.z
```

IPs Tailscale observees le 2026-05-24 :

```text
iPhone : 100.75.75.90
Raspberry Pi BirdNET-Pi : 100.84.45.93
```

URL Tailnet stable a tester pour BirdNET-Pi :

```text
http://100.84.45.93
http://100.84.45.93:8080
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

Si Tailscale est absent du Raspberry :

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Ensuite activer/verifier MagicDNS dans la console Tailscale, puis tester depuis iPhone :

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
http://192.168.1.48:8080
http://birdnetpi.local
```

Note : l'historique local contenait `http://192.168.1.48:8080`, ce qui indique que le port 8080 a deja ete utilise pour l'interface.

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

## Acces SSH Raspberry Pi

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

## Modele BirdNET observe

Modele en place :

```text
BirdNET_GLOBAL_6K_V2.4_Model_FP16
```

Lecture :

- `GLOBAL` : modele mondial.
- `6K` : environ 6000 classes/especes.
- `V2.4` : generation du modele.
- `FP16` : version demi-precision, plus legere pour Raspberry Pi.

## Commandes utiles

### Outil de diagnostic et réparation rapide (Dobby Tool)

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

Chercher le modele BirdNET :

```bash
find ~/BirdNET-Pi -iname '*model*' -o -iname '*BirdNET*'
```

## Regle memoire Dobby

Toute nouvelle information d'acces BirdNET-Pi doit etre ajoutee ici :

- IP fixe ou reserve DHCP ;
- URL fonctionnelle ;
- port correct ;
- identifiant non sensible ;
- existence d'un secret sans le secret ;
- commande de verification qui a marche ;
- date de validation.

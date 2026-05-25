# Connexion RPI BirdNET-Pi

**Date :** 2026-05-24  
**Machine :** Raspberry Pi BirdNET-Pi  
**Projet :** WildNexus / Bioacoustique  
**Regle securite :** ne pas ecrire le mot de passe en clair dans ce fichier.

## Informations connues

### Raspberry Pi

- Hostname cible : `birdnetpi`
- User SSH : `jchavaux`
- IP maison probable : `192.168.1.48`
- IP Tailscale RPI : `100.84.45.93`
- Modele BirdNET : `BirdNET_GLOBAL_6K_V2.4_Model_FP16`

### iPhone

- IP Tailscale iPhone : `100.75.75.90`
- Plage hotspot iPhone observee : `172.20.10.x`
- IPs hotspot deja vues : `172.20.10.2`, `172.20.10.7`, `172.20.10.8`, `172.20.10.15`

### BirdNET-Pi Tools

- Login Tools : `birdnet`
- Mot de passe Tools : vide par defaut, sauf modification ulterieure.

## Connexion depuis Mac

### 1. Ouvrir Terminal

Application a ouvrir sur Mac :

```text
Terminal
```

ou :

```text
Applications > Utilitaires > Terminal
```

### 2. Tester l'acces web depuis le navigateur Mac

Dans Safari ou Chrome sur Mac, essayer dans cet ordre :

```text
http://birdnetpi.local
http://192.168.1.48
http://192.168.1.48:8080
http://100.84.45.93
http://100.84.45.93:8080
```

### 3. Connexion SSH depuis Terminal Mac

Commande prioritaire si le Mac est sur le meme reseau local :

```bash
ssh jchavaux@birdnetpi.local
```

Si `.local` ne repond pas, utiliser l'IP maison :

```bash
ssh jchavaux@192.168.1.48
```

Si Tailscale est actif sur Mac et sur RPI :

```bash
ssh jchavaux@100.84.45.93
```

### 4. Verifier Tailscale sur Mac

Application a ouvrir sur Mac :

```text
Tailscale
```

Commande Terminal possible :

```bash
/Applications/Tailscale.app/Contents/MacOS/Tailscale status
```

Si Tailscale est arrete, le demarrer depuis l'application Tailscale Mac.

## Connexion depuis iPhone

### 1. Ouvrir Tailscale

Application a ouvrir sur iPhone :

```text
Tailscale
```

Verifier que l'iPhone est connecte au tailnet.

### 2. Ouvrir Safari

Application a ouvrir sur iPhone :

```text
Safari
```

Adresse stable a encoder en premier :

```text
http://100.84.45.93
```

Si rien ne repond :

```text
http://100.84.45.93:8080
```

### 3. Alternative iPhone sur reseau local ou hotspot

Si l'iPhone et le RPI sont sur le meme reseau local :

```text
http://birdnetpi.local
```

Si le RPI est connecte au hotspot iPhone, tester les IPs vues dans l'historique Safari :

```text
http://172.20.10.2/
http://172.20.10.7/
```

Attention : les IPs `172.20.10.x` peuvent changer a chaque reconnexion hotspot. Pour un acces stable, preferer Tailscale :

```text
http://100.84.45.93
```

## Commandes utiles sur le Raspberry Pi

Ces commandes sont a envoyer dans le terminal apres connexion SSH.

### Verifier l'adresse IP du RPI

```bash
hostname -I
```

### Verifier le nom de machine

```bash
hostname
```

### Fixer le hostname si necessaire

```bash
sudo hostnamectl set-hostname birdnetpi
sudo reboot
```

### Verifier le Wi-Fi

```bash
nmcli device status
nmcli connection show
```

### Verifier Tailscale sur le RPI

```bash
tailscale status
tailscale ip -4
```

### Installer Tailscale si absent

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

### Verifier BirdNET-Pi

```bash
cd ~/BirdNET-Pi
git remote get-url origin
git branch --show-current
git log -1 --oneline
```

### Chercher le modele BirdNET

```bash
find ~/BirdNET-Pi -iname '*model*' -o -iname '*BirdNET*'
```

## Ordre de diagnostic rapide

1. Sur iPhone, verifier que Tailscale est connecte.
2. Dans Safari iPhone, ouvrir `http://100.84.45.93`.
3. Si echec, tester `http://100.84.45.93:8080`.
4. Depuis Mac Terminal, tester `ssh jchavaux@100.84.45.93`.
5. Une fois connecte au RPI, lancer `tailscale status` et `hostname -I`.
6. Si Tailscale ne marche pas, revenir au reseau local : `http://birdnetpi.local` ou `http://192.168.1.48`.

## A ne pas oublier

- `birdnet` est le login de l'interface Tools, pas le user SSH.
- `jchavaux` est le user SSH du Raspberry Pi.
- Les IPs Tailscale `100.x.y.z` sont plus stables que les IPs hotspot `172.20.10.x`.
- Le mot de passe RPI est connu de JCH mais ne doit pas etre stocke ici en clair.

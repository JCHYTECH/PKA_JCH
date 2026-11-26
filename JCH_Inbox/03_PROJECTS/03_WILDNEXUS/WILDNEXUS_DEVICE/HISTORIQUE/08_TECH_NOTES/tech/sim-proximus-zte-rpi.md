Voici le contenu du fichier Markdown prêt à être téléchargé. Copiez le texte ci-dessous et enregistrez-le sous le nom `install_sim.md`.

```markdown
# Installation d'une carte SIM Proximus Pay&Go sur une clé ZTE MF833UI avec un Raspberry Pi

Procédure complète pour connecter le modem USB à Internet via le réseau mobile Proximus.

## 1. Vérifications préalables
- **Carte SIM activée** : la carte Pay&Go doit avoir du crédit et une option data active (ex. « Surf Pay&Go »).
- **Code PIN** : si la carte possède un code PIN, il est fortement conseillé de la désactiver au préalable depuis un téléphone (pour simplifier). Sinon, nous l'inclurons dans la configuration.
- **Modem débloqué** : la clé ZTE MF833UI doit être désimlockée (non liée à un autre opérateur).

## 2. Insertion de la carte SIM
- Ouvrez le capot de la clé, insérez la carte micro-SIM (utilisez un adaptateur si nécessaire) en respectant le sens indiqué.

## 3. Connexion au Raspberry Pi
- Branchez la clé sur un port USB disponible du Raspberry Pi (de préférence directement, sans hub non alimenté). Le voyant doit s'allumer.

## 4. Installation des paquets nécessaires
```bash
sudo apt update
sudo apt install usb-modeswitch usb-modeswitch-data ppp wvdial -y
```

## 5. Reconnaissance du modem (mode série)
La clé peut d'abord apparaître comme un lecteur CD-ROM virtuel. Le paquet `usb-modeswitch` la bascule automatiquement en mode modem.

Après installation, redémarrez udev ou le Raspberry Pi :
```bash
sudo systemctl restart udev
```
Débranchez puis rebranchez la clé et vérifiez les ports série :
```bash
ls /dev/ttyUSB*
```
Vous devriez voir plusieurs interfaces (`ttyUSB0`, `ttyUSB1`, `ttyUSB2`). Le port principal est généralement `/dev/ttyUSB0`.

Si rien n'apparaît, identifiez la clé avec `lsusb` et forcez le basculement :
```bash
lsusb   # Repérez l'ID 19d2:xxxx
sudo usb_modeswitch -v 19d2 -p VOTRE_ID -M "5553424312345678000000000000061b000000020000000000000000000000"
```
Remplacez `VOTRE_ID` par l'ID produit réel. Vérifiez ensuite `/dev/ttyUSB*`.

## 6. Script de connexion (chat)
Créez le fichier `/etc/chatscripts/proximus` :
```bash
sudo nano /etc/chatscripts/proximus
```
Contenu (ajustez le PIN si nécessaire) :
```
# Déverrouillage du PIN (supprimez la ligne si PIN désactivé)
# Remplacez 1111 par votre code PIN, sinon commentez ou supprimez la ligne
'' AT+CPIN=1111

# Configuration de l'APN Proximus
'' AT+CGDCONT=1,"IP","internet.proximus.be"

# Numéro à composer (standard 99#)
'' ATDT*99***1#

# Attente de connexion
CONNECT ''
```
Sauvegardez (`Ctrl+O`, `Ctrl+X`).

## 7. Fichier de configuration PPP
Créez `/etc/ppp/peers/proximus` :
```bash
sudo nano /etc/ppp/peers/proximus
```
Contenu :
```
/dev/ttyUSB0          # Adaptez si votre modem utilise un autre ttyUSBx
115200

lock
crtscts
modem
passive
noauth
debug

user ""
password ""

connect "/usr/sbin/chat -v -f /etc/chatscripts/proximus"

noipdefault
defaultroute
usepeerdns

lcp-echo-interval 30
lcp-echo-failure 3
```
Sauvegardez.

## 8. Lancement de la connexion
```bash
sudo pon proximus
```
Surveillez les logs :
```bash
tail -f /var/log/syslog
```

## 9. Vérification
```bash
ifconfig ppp0
ping -c 4 8.8.8.8
curl -I http://google.com
```
Si tout est bon, votre Raspberry Pi est connecté via la clé Proximus.

## 10. Arrêt de la connexion
```bash
sudo poff proximus
```

## 11. Connexion automatique au démarrage (optionnel)
Ajoutez dans `/etc/rc.local` avant la ligne `exit 0` :
```bash
pon proximus
```

## Dépannage rapide
- **Pas d'interface ttyUSB** : vérifiez `lsusb` et que `usb-modeswitch` est installé.
- **Erreur CHAP / authentification** : assurez-vous que `user ""` et `password ""` sont bien présents et vides dans le fichier peer.
- **Pas d'adresse IP** : consultez `tail -f /var/log/syslog | grep pppd`.
- **PIN requis** : modifiez le chat script avec votre code PIN ou désactivez-le sur un téléphone.

Bon surf !
```

Copiez ce bloc, collez-le dans un éditeur de texte et sauvegardez en `.md`.
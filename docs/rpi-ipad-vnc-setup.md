# Fiche d'installation — RPi vers iPad (RustDesk + SSH)

> Génére le 2026-06-04 par [[Dobby]] — MAJ 2026-06-05 : RustDesk ajouté
> RPi : `rpi-pkajch` (Tailscale 100.66.110.60) — hostname `PKAJCH`
> User : `jchavaux` — Password : `dobbydobby`
> OS : Debian 13 Trixie ARM64

---

## 1. Connexions

### Via Tailscale (de partout)
| Service | Host | Port |
|---------|------|------|
| SSH | `100.66.110.60` | 22 |
| VNC (x11vnc) | `100.66.110.60` | **5900** — pas de mot de passe, accès direct |

### Via WiFi local
| Service | Host | Port |
|---------|------|------|
| SSH | IP locale du RPi | 22 |
| RustDesk | IP locale du RPi | 21118 |
| VNC (ancien) | IP locale du RPi | 5901 |

> IP locale : `hostname -I` sur le RPi.

---

## 2. Apps iPad

### SSH (gratuit)
- **Termius** (gratuit) — App Store

### Remote desktop (recommandé)
- **RustDesk** (gratuit, open-source) — App Store. Recommandé.
  - Client iOS + serveur Linux/Windows/macOS
  - Chiffré, auto-hébergeable, pas de compte obligatoire
- **bVNC Free VNC Viewer** (gratuit, open-source) — alternative VNC si RustDesk ne convient pas

---

## 3. Installation du serveur RustDesk sur le RPi

```bash
# Télécharger la dernière version ARM64 pour Debian/RPi
wget https://github.com/rustdesk/rustdesk/releases/download/1.3.7/rustdesk-1.3.7-aarch64.deb
sudo dpkg -i rustdesk-1.3.7-aarch64.deb
sudo apt install -f   # corriger les dépendances si besoin

# Lancer le service
sudo systemctl enable --now rustdesk

# Vérifier
systemctl status rustdesk
```

> Si le RPi est headless (pas de bureau X), RustDesk fonctionne en mode `--service` uniquement.

### Désactiver VNC (optionnel, si RustDesk remplace)
```bash
sudo systemctl stop tigervnc
sudo systemctl disable tigervnc
```

---

## 4. Connexion depuis l'iPad

1. Ouvrir **RustDesk** sur l'iPad
2. Dans « Remote ID », entrer l'ID affiché par `rustdesk --get-id` sur le RPi
3. Dans « One-Time Password », entrer le mot de passe temporaire ou configurer un mot de passe fixe :

```bash
# Sur le RPi, définir un mot de passe permanent
rustdesk --password dobbydobby
```

4. La session s'ouvre — bureau headless du RPi visible sur l'iPad

### Alternative via Tailscale (si le relay RustDesk public ne suffit pas)
- RustDesk peut utiliser son propre serveur de relay (self-host)
- Sinon, RustDesk en peer-to-peer via Tailscale (Tailscale chiffre déjà le trafic)

---

## Annexe — VNC (ancienne méthode, conservée pour référence)

```bash
sudo apt install -y tigervnc-standalone-server tigervnc-common \
  openbox xterm xfonts-base xinit
```

Config `~/.vnc/xstartup` :
```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
openbox-session &
xterm &
wait
```

Service systemd `/etc/systemd/system/tigervnc.service` :
```ini
[Unit]
Description=TigerVNC server
After=syslog.target network.target

[Service]
Type=forking
User=jchavaux
ExecStart=/usr/bin/tigervncserver :1 -localhost no -geometry 1280x720
ExecStop=/usr/bin/tigervncserver -kill :1
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now tigervnc
```

### Commandes VNC
```bash
tigervncserver -list         # lister sessions
tigervncserver -kill :1      # arreter
tigervncserver :1 -localhost no -geometry 1280x720  # demarrer
sudo ss -tlnp | grep 5901    # verifier ecoute
tailscale ip -4              # IP Tailscale
```

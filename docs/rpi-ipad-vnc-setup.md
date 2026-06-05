# Fiche d'installation — RPi vers iPad (VNC + SSH)

> Genere le 2026-06-04 par [[Dobby]]
> RPi : `rpi-pkajch` (Tailscale 100.66.110.60) — hostname `PKAJCH`
> User : `jchavaux` — Password : `dobbydobby`
> OS : Debian 13 Trixie ARM64

---

## 1. Connexions

### Via Tailscale (de partout)
| Service | Host | Port |
|---------|------|------|
| SSH | `100.66.110.60` | 22 |
| VNC | `100.66.110.60` | 5901 |

### Via WiFi local
| Service | Host | Port |
|---------|------|------|
| SSH | IP locale du RPi | 22 |
| VNC | IP locale du RPi | 5901 |

> IP locale : `hostname -I` sur le RPi.

## 2. Apps iPad

- **Termius** (SSH) — App Store
- **VNC Viewer** (RealVNC) — App Store

## 3. Installation d'un nouveau RPi

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

Password VNC (identique SSH) : `dobbydobby`

## 4. Commandes

```bash
tigervncserver -list         # lister sessions
tigervncserver -kill :1      # arreter
tigervncserver :1 -localhost no -geometry 1280x720  # demarrer
sudo ss -tlnp | grep 5901    # verifier ecoute
tailscale ip -4              # IP Tailscale
```

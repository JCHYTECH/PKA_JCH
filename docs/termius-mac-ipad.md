# Fiche — Termius : Mac M5 vers iPad (SSH)

> Genere le 2026-06-04 par [[Dobby]]
> Mac M5 — user `jchavauxm5` — password `5444`

---

## 1. Pre-requis

### Sur le Mac M5
- Remote Login : System Settings > General > Sharing > Remote Login (ON)
- Tailscale installe (connexion depuis partout)

### Sur l'iPad
- **Termius** (App Store)

---

## 2. Connexion

### Via Tailscale (de partout)
| Champ | Valeur |
|-------|--------|
| Host | `100.108.55.44` |
| Port | `22` |
| Username | `jchavauxm5` |
| Password | `5444` |

### Via WiFi local (meme reseau)
| Champ | Valeur |
|-------|--------|
| Host | `192.168.129.14` |
| Port | `22` |
| Username | `jchavauxm5` |
| Password | `5444` |

---

## 3. Une fois connecte

```bash
cd ~/PKA_JCH
claude                    # Claude Code
dobby "ta question"       # Dobby via Qwen 3.7 Plus
dobby max "ta question"   # Dobby via Qwen 3.7 Max
qwen "ta question"        # Qwen 3.7 Plus
qwen max "ta question"    # Qwen 3.7 Max
ssh m1@100.73.212.110 ollama list   # verifier M1
```

Qwen lit directement la cle OpenRouter dans `~/.config/pka-jch/openrouter_key.txt`.

---

## 4. Depannage

**Connection refused :**
```bash
systemsetup -getremotelogin              # doit dire On
sudo launchctl kickstart -kp system/com.openssh.sshd   # relancer SSH
```

**Claude Code : erreur Keychain :**
```bash
source ~/.zshrc && claude
```

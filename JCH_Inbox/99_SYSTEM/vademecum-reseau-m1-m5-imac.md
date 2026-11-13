---
title: Vade-mecum — Réseau M1 / M5 / iMac
date: 2026-11-13
tags: [réseau, M1, M5, iMac, noVNC, SSH, Tailscale, Thunderbolt]
---

# Vade-mecum — Réseau M1 / M5 / iMac

> Référence pratique d'utilisation du trio de Macs. Mise à jour le 2026-11-13 (session consolidation réseau + durcissement).
> **Les mots de passe ne sont plus en clair** : ils sont dans le **Trousseau macOS** (voir §5).

---

## ⭐ En 30 secondes — pour la secrétaire

Cet iMac sert d'**écran** pour le Mac portable de JC (appelé « le M5 »). Tout se fait en **double-cliquant sur une icône du Bureau**.

- **Voir le Mac de JC** → double-cliquer sur `Voir-le-Mac.command`.
- **Voir les deux écrans du Mac côte à côte** → double-cliquer sur `Deux-ecrans.command`.

En cas de problème :

- L'image est figée ou coupée → recharger la page avec **⌘ + R**.
- Rien ne s'affiche → appeler JC (les mots de passe sont dans son app « Mots de passe », pas sur cette machine).

*Le reste de ce document est la référence technique de JC ; vous n'en avez pas besoin au quotidien.*

---

## 1. Les 3 machines

| Machine | Rôle | Hostname | User | IP Tailscale |
|---|---|---|---|---|
| **M5** (MacBook Pro M5) | Principal, orchestrateur PKA | `MacBook-Pro-de-JC.local` | `jchavauxm5` | `m5-jc` · 100.108.55.44 |
| **M1** (MacBook Pro 14" M1 Pro) | Secondaire / LLM (Ollama) | `MacBook-Pro-de-M1.local` | `m1` | `m1-llm` · 100.73.212.110 |
| **iMac** (27" 5K 2017) | Écran miroir des deux | `news-imac.local` | `new` | — (hors Tailscale) |

- Le **M5** porte le PKA_JCH, les ponts noVNC et les scripts de bascule d'écran.
- Le **M1** a sa dalle interne morte → il se pilote par VNC/noVNC ou SSH. Ollama y tourne (port 11434).
- L'**iMac** affiche l'écran du M5 **ou** du M1 dans Safari (noVNC).

---

## 2. Voir un écran sur l'iMac (miroir noVNC)

Deux ponts noVNC tournent sur le M5 (launchd, auto-start) :

- **Écran du M5** → `http://MacBook-Pro-de-JC.local:6080/vnc.html?autoconnect=1&password=<mdp>&resize=scale`
- **Écran du M1** → `http://MacBook-Pro-de-JC.local:6081/vnc.html?autoconnect=1&password=<mdp>&resize=scale`

`<mdp>` = mot de passe VNC legacy (voir §5). Astuce : enregistrer ces URL en favori Safari ou en `.webloc` sur le Bureau.

---

## 3. Basculer les écrans du M5

Le M5 a deux écrans : **interne** (Color LCD, 1512×982) + **LG Ultrawide** (3440×1440). noVNC montre le bureau étendu (les deux côte à côte) ; pour n'en voir qu'un :

| Action | Terminal du M5 | Depuis l'iMac (icône Bureau) |
|---|---|---|
| Écran interne seul (LG éteint) | `~/PKA_JCH/bin/m5-ecran-interne` | double-clic `Voir-le-Mac.command` |
| Les deux écrans (étendu) | `~/PKA_JCH/bin/m5-ecran-double` | double-clic `Deux-ecrans.command` |
| Écran LG seul (interne éteint) | — | fermer le capot du M5 (clamshell) |

> **Écran LG seul** : pas de commande native fiable. `displayplacer` peut éteindre l'interne mais le réactiver est buggé (il faut `sudo killall -HUP WindowServer`, déconnectant la session). Deux voies : le **clamshell** (fermer le capot — gratuit, natif, le M5 reste éveillé sur le LG car sur secteur) ou **Lunar Pro** (BlackOut, app payante, éteint l'interne par raccourci). Revenir du clamshell : ouvrir le capot puis `Voir-le-Mac` ou `Deux-ecrans`.
> Si l'image noVNC ne se réajuste pas après un changement : recharger la page.

---

## 4. SSH entre machines

| Sens | Commande | Auth |
|---|---|---|
| M5 → iMac | `ssh new@news-imac.local` | clé (sans mot de passe) |
| iMac → M5 | `ssh jchavauxm5@MacBook-Pro-de-JC.local` | clé (sans mot de passe) |
| M5 → M1 | `ssh m1@MacBook-Pro-de-M1.local` | clé `~/.ssh/id_ed25519` |
| M1 ↔ M5 (Thunderbolt) | `ssh m1@10.0.0.2` | clé |

Clés : M5 `~/.ssh/id_ed25519` ; iMac (compte `new`) `~/.ssh/id_ed25519` (générée le 13/11). Le Remote Login (SSH) est actif sur M5 et iMac.

---

## 5. Mots de passe — Trousseau (plus de clair)

Tous les mots de passe machines sont dans l'app **Mots de passe** (Trousseau macOS), plus dans les fichiers texte.

| Libellé Trousseau | Contenu |
|---|---|
| `PKA M1 session` | mot de passe de session M1 (`m1`) |
| `PKA VNC legacy` | mot de passe VNC M5 + M1 |
| `PKA iMac new` | compte iMac `new` |

Récupérer un secret :

```bash
security find-generic-password -s "PKA VNC legacy" -w
```

`JCH_PRIVATE/credentials-central.md` ne contient plus que des pointeurs `🔑 Keychain <libellé>` + les clés API (fichier `~/.config/pka-jch/api_keys`, chmod 0600).

---

## 6. Tailscale

| Nœud | IP | Machine |
|---|---|---|
| `lupo` | 100.106.152.118 | RPi 5 van (HA) |
| `m5-jc` | 100.108.55.44 | Mac M5 |
| `m1-llm` | 100.73.212.110 | Mac M1 (Ollama) |
| `iphone182` | 100.75.75.90 | iPhone |
| `ipad-pro-12-9-gen-4` | 100.94.181.65 | iPad |

L'iMac n'est **pas** sur Tailscale. ⏳ ACL à poser (reporté 13/11 — voir TTD infra).

---

## 7. Thunderbolt M1 ↔ M5 (résumé)

Lien 40 Gb/s : M5 = `10.0.0.1`, M1 = `10.0.0.2`. Détail complet : `thunderbolt-m1-m5-mode-emploi.md` (SMB ~400 MB/s, SSH ~280 MB/s, backup auto toutes les 4 h via `com.pka.backup-m1`).

---

## 8. Dépannage rapide

- **noVNC affiche une demande user+password** : le pont doit servir le type 2 (VNC), pas le type 30 (Apple RD). Correctif déjà appliqué dans `_local/novnc/core/rfb.js`.
- **Le LG ne revient pas après `m5-ecran-interne`** : `~/PKA_JCH/bin/m5-ecran-double`.
- **Mot de passe oublié** : `security find-generic-password -s "<libellé>" -w`.
- **L'iMac ne joint pas le M5 en SSH** : vérifier Remote Login (Réglages Système → Partage → « Connexion à distance ») et la clé de l'iMac dans `~/.ssh/authorized_keys` du M5.

---

*Référence générée par Dobby 🦉 le 2026-11-13. Sources : MEMORY.md, credentials-central.md, thunderbolt-m1-m5-mode-emploi.md, `tailscale status`.*

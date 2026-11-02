# Accès à Lupo (Home Assistant) depuis iPhone / iPad

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Objet :** guide d'accès à l'instance HA « Lupo » (RPi 5 van) depuis iOS.
> **Secrets :** voir `JCH_PRIVATE/credentials-central.md` (ne pas recopier ici).

---

## 1. Pré-requis — deux apps

| App | Rôle | Store |
|-----|------|-------|
| **Tailscale** | VPN maillé → accès à distance | App Store |
| **Home Assistant Companion** | Interface HA officielle | App Store |

**Installation unique :**
1. **Tailscale** → connexion avec le compte `jc.havaux@`. Une fois connecté, `lupo` apparaît comme machine du réseau privé.
2. **Companion** → à la première ouverture, renseigner l'URL du serveur (voir §2).

---

## 2. URLs selon la situation

| Situation | URL |
|-----------|-----|
| **À la maison** (même Wi-Fi) | `http://192.168.129.16:8123` (ou `http://lupo.local:8123`) |
| **À distance** (via Tailscale) | `https://100.106.152.118:8123` |
| **Dans le van** (hors réseau) | Wi-Fi du van `VanLife_Network` → puis `http://192.168.129.16:8123` |

**Login :** `jchavaux` / (mot de passe dans `credentials-central.md`)

---

## 3. Configuration Companion (recommandée)

Dans l'app → **Settings → Companion app** :

- **Internal URL** : `http://192.168.129.16:8123` (Wi-Fi local)
- **External URL** : `https://100.106.152.118:8123` (Tailscale)

→ L'app bascule automatiquement selon le réseau. C'est la config la plus confortable.

---

## 4. Certificat auto-signé (⚠️ normal)

L'URL Tailscale est en `https://` avec un **certificat auto-signé** (HA OS). Safari/Companion affichera un avertissement la première fois → **« Continuer quand même »**. Ce n'est pas une erreur de sécurité : le réseau Tailscale est privé.

---

## 5. Accès rapide sans app

Ouvrir **Safari** → `http://192.168.129.16:8123` (maison) ou `https://100.106.152.118:8123` (distance, Tailscale actif).

L'interface HA se charge en **PWA** → possible de l'ajouter à l'écran d'accueil (Share → « Sur l'écran d'accueil »).

---

## 6. En résumé

> **Tailscale + Companion**, avec l'URL locale (`192.168.129.16`) en interne et l'URL Tailscale (`100.106.152.118`) en externe → Lupo accessible partout.

---

## 7. Accès SSH (optionnel, depuis iPad)

Voir `docs/termius-mac-ipad.md` pour l'accès SSH/terminal via Termius.

```bash
ssh root@192.168.129.16 -p 22222 -i ~/.ssh/id_ed25519      # local
ssh root@100.106.152.118 -p 22222 -i ~/.ssh/id_ed25519     # Tailscale
```

---

*Fichier maintenu par Dobby 🦉 — à mettre à jour si l'IP/l'URL change.*

# Accès mobile au dashboard PKA (iPhone / iPad) — Tailscale, lecture seule

> Dernière mise à jour : 2026-09-14
> Contexte : consulter les lieux DÉCOUVERTES (et le hub PKA) depuis iPhone/iPad,
> en lecture seule. Les écritures, l'intégration de screenshots et l'admin restent
> réservées au Mac (M5).

---

## Objectif / périmètre

- **Mobile (iPhone, iPad) → consultation uniquement.** Toute écriture est refusée (`403`).
- **Mac (M5) → accès complet** (lecture + écriture, sans token).

## Prérequis

- [Tailscale](https://tailscale.com) installé **et connecté** sur le Mac, l'iPhone et l'iPad.
- Le serveur `scripts/dashboard_server.py` tourne (launchd) sur le port `8787`, hôte `0.0.0.0`.
- Tous les appareils sont sur le même tailnet (même compte).

## Références réseau

| Élément | Valeur |
|---------|--------|
| IP Tailscale du Mac | `100.108.55.44` |
| Nom d'hôte Tailscale (MagicDNS) | `m5-jc` |
| Port | `8787` |

Pour retrouver l'IP actuelle du Mac :

```bash
tailscale ip -4
```

> L'IP `100.x` est stable tant que le nœud n'est pas réinitialisé. Si elle change,
> remplacer `100.108.55.44` dans les URLs ci-dessous.

---

## 1. Vérifier la connexion Tailscale

Sur le Mac :

```bash
tailscale status
```

L'iPhone (`iphone182`) et l'iPad doivent apparaître. S'ils sont `offline`,
ouvrir l'app Tailscale sur l'appareil pour le reconnecter.

## 2. URL d'accès

```
http://100.108.55.44:8787/decouvertes.html
```

Ou, si MagicDNS est actif :

```
http://m5-jc:8787/decouvertes.html
```

Le hub complet est accessible à la racine : `http://100.108.55.44:8787/hub.html`.

## 3. Déverrouillage par token (première fois, puis tous les 30 jours)

Au premier accès depuis un appareil mobile, le serveur redirige vers une page
« Dobby Live » (déverrouillage). Saisir le token du dashboard.

### Récupérer le token

Le token est stocké dans un fichier sécurisé sur le Mac (`chmod 600`) :

```bash
cat ~/.codex/memories/pka-jch/dashboard_token.txt
```

### Connexion en un clic (recommandé pour créer un signet)

Depuis le Mac, générer l'URL de connexion :

```bash
TOKEN=$(cat ~/.codex/memories/pka-jch/dashboard_token.txt)
echo "http://100.108.55.44:8787/?token=$TOKEN"
```

Ouvrir cette URL sur l'iPhone/iPad : le serveur valide le token, dépose un cookie
de session, puis redirige vers l'URL nettoyée (sans le secret dans la barre d'adresse).

## 4. Ajouter à l'écran d'accueil (iPhone / iPad)

1. Ouvrir l'URL dans Safari.
2. Bouton Partager → « Sur l'écran d'accueil ».
3. L'icône ouvre le dashboard comme une app.

---

## Comment fonctionne le verrou (rappel)

- **Requête locale** (`127.0.0.1`, `::1`, `localhost`) → autorisée d'office, pas de token.
- **Requête distante** (Tailscale, LAN) → token exigé (`?token=...` ou cookie `pka_token`).
- Le cookie est `HttpOnly`, `SameSite=Lax`, durée de vie **30 jours** (`Max-Age=2592000`).
- **Garde lecture seule** : même déverrouillé, un appareil distant ne peut que `GET`.
  Toute écriture (`POST`) → `403 « Lecture seule depuis un appareil distant »`.

## Gestion du service (sur le Mac)

```bash
bin/dashboardctl.sh status    # état + URL
bin/dashboardctl.sh restart   # redémarrer (après un changement de plist/code)
bin/dashboardctl.sh start
bin/dashboardctl.sh stop
```

## Dépannage

- **iPad « offline »** : ouvrir l'app Tailscale sur l'iPad, se reconnecter.
- **Redirection vers « Dobby Live »** : normal = il faut saisir le token (ou le cookie a expiré après 30 jours).
- **Port injoignable** : vérifier que le service tourne — `bin/dashboardctl.sh status`.
- **`Connection refused`** : le Mac est éteint/en veille, ou Tailscale déconnecté — vérifier `tailscale status`.

## Sécurité

- Le token est un secret personnel : **ne pas le commiter**, ne pas le partager.
- Il vit uniquement dans `~/.codex/memories/pka-jch/dashboard_token.txt` (permissions `600`).
- En écoutant sur `0.0.0.0`, le port est aussi visible sur le WiFi local ; le token
  et le garde lecture seule protègent l'accès distant.

# 📡 M1 ↔ M5 — Connexion depuis l'étranger

> Mode d'emploi grand débutant.  
> Mis à jour : 2026-10-27 (outillage `bin/m1-wake` + `bin/m1-rearm`, diagnostic panne 20 j)

---

## Le problème

Tu as **deux Mac** :

| Machine | Où elle est | Ce qu'elle fait |
|---------|-------------|----------------|
| **M1** (MacBook Pro 14" M1, capot fermé) | Chez toi (Belgique) | Tourne Ollama, fait tourner les scripts, accessible 24h/24 |
| **M5** | Avec toi (voyage) | Ta machine pour travailler (DeepSeek TUI, etc.) |

Tu veux pouvoir **utiliser M1 depuis M5** quand tu es à l'étranger — pour lui envoyer des tâches, utiliser Ollama, ou simplement SSH.

---

## Ce qu'il te faut

- ✅ Une **box internet** chez toi (M1 y est branché)
- ✅ **Tailscale** installé sur les deux machines (déjà fait)
- ✅ M1 **branché au secteur** (pas sur batterie)
- ✅ M1 réglé pour **ne jamais s'endormir** (déjà fait)

---

## Étape 1 — Avant de partir (vérifications)

Connecte-toi sur M1 **une dernière fois avant de quitter la maison** :

```bash
ssh m1@100.73.212.110
```

### 1a. Vérifie que M1 ne s'endort pas

```bash
pmset -g | grep -E 'sleep|standby|hibernate'
```

Tu dois voir :

```
 sleep               0
 standby             0
 hibernatemode       0
```

Si ce n'est pas le cas, corrige :

```bash
sudo pmset -a standby 0 hibernatemode 0 sleep 0
```

### 1b. Vérifie que Tailscale tourne

```bash
tailscale status
```

Tu dois voir une ligne avec **100.73.212.110** (M1 lui-même).

Si pas de résultat :

```bash
sudo tailscale up
```

### 1c. Vérifie qu'Ollama répond

```bash
curl http://127.0.0.1:11434/api/tags
```

Tu dois voir une liste de modèles (gemma4, qwen3.6, etc.).

### 1d. Lance un réveil automatique (optionnel mais conseillé)

Même avec `sleep 0`, certains redémarrages système peuvent figer la machine. Pour être tranquille :

```bash
sudo pmset repeat wake MTWRFSU 08:00:00
```

Ça réveille M1 **tous les jours à 8h**. Si jamais il s'est mis en veille pour une raison inconnue, il se réveillera tout seul.

---

## Étape 2 — Pendant le voyage

### 2a. Vérifie que tout est joignable

Depuis M5 (où que tu sois dans le monde) :

```bash
tailscale status
```

Tu dois voir M1 en ligne :

```
100.73.212.110  m1         macOS    -
```

Si M1 n'apparaît pas :
- Vérifie que M1 est **branché** et que ta **box internet chez toi fonctionne**
- Tailscale passe par des **relais DERP** automatiquement si la connexion directe ne marche pas (hôtel, aéroport, etc.). Ça peut prendre quelques secondes.
- Si ça ne revient pas → ton Internet chez toi est probablement coupé.

### 2b. Connecte-toi à M1

```bash
ssh m1@100.73.212.110
```

Ça marche de n'importe où, tant que les deux machines ont Internet et Tailscale.

### 2c. Utilise Ollama à distance

Depuis M5, tu peux utiliser les modèles qui tournent sur M1 :

```bash
curl http://100.73.212.110:11434/api/tags
```

Si tu veux lancer une requête à un modèle :

```bash
curl http://100.73.212.110:11434/api/generate \
  -d '{"model": "gemma4:latest", "prompt": "Bonjour !"}'
```

---

## Étape 3 — En cas de problème

| Problème | Cause possible | Solution |
|----------|---------------|----------|
| `ssh: connect to host 100.73.212.110 port 22: Operation timed out` | M1 éteint ou box sans internet | Attends le retour du courant. Si c'est juste un reboot de box, Tailscale reconnecte automatiquement en ~30s |
| `tailscale status` ne montre que M5 | Tailscale perdu sur M1 | Si M1 a redémarré, Tailscale ne se lance pas automatiquement → besoin de quelqu'un sur place pour `sudo tailscale up` |
| `curl: (7) Failed to connect` | Ollama arrêté | SSH sur M1 et `ollama serve` |
| Connexion très lente | Le relais DERP est loin (Asie → Europe) | C'est normal. Le débit sera limité, mais le SSH et les petites requêtes Ollama passent |

### Solution de secours : la multiprise connectée

Si M1 plante et que personne n'est chez toi pour le redémarrer, une **smart plug** (Kasa, Tapo, etc.) peut couper le courant à distance puis le remettre.

**Condition :** il faut que M1 soit configuré pour **démarrer automatiquement au retour du courant** (c'est le cas par défaut sur les Mac récents, mais à vérifier dans Préférences Système > Démarrage).

---

## Rappel visuel

```
🌍 TOI (M5) À L'ÉTRANGER
      │
      │  tailscale
      │  (DERP relay si nécessaire)
      │
      v
🏠 CHEZ TOI
   │
   ├── Box Internet (doit marcher)
   │       │
   │   tailscale up
   │       │
   ├── M1 (branché, réveillé)
   │       │
   │   ollama serve
   │       │
   │   ssh (port 22)
   │
   └── Smart Plug (optionnel)
```

---

## Commandes utiles (résumé)

| Ce que tu veux faire | Commande |
|----------------------|----------|
| Voir si M1 est joignable | `tailscale status` |
| Se connecter à M1 | `ssh m1@100.73.212.110` |
| Lister les modèles Ollama sur M1 | `curl http://100.73.212.110:11434/api/tags` |
| Empêcher M1 de dormir | `sudo pmset -a standby 0 hibernatemode 0 sleep 0` |
| Réveil automatique quotidien | `sudo pmset repeat wake MTWRFSU 08:00:00` |

---

## Outillage 2026-10-27 — réveil et réarmement

Deux scripts, à utiliser dans cet ordre.

### 1. `bin/m1-wake` — tenter le réveil

```bash
bin/m1-wake                 # WoL + attente 120 s + scan LAN
bin/m1-wake --timeout 300   # patience accrue
bin/m1-wake --scan-only     # ne réveille rien, cherche M1 sur le LAN
```

La MAC est lue dans `_local/m1-mac`, `$M1_MAC` ou `--mac`. Récupère-la dans les
baux DHCP de la box si le fichier n'existe pas.

**Limite structurelle :** M1 est un **MacBook Pro 14" M1**, donc **sans port
Ethernet**. Le Wake-on-LAN ne s'applique pas — il n'y a pas de NIC filaire à
réveiller. `bin/m1-wake` sert désormais à **détecter** la machine (Bonjour,
LAN, Tailscale) et à confirmer son retour, pas à la sortir de veille.

### 2. `bin/m1-rearm` — durcir après le retour

```bash
bin/m1-rearm --check     # lecture seule
bin/m1-rearm --dry-run   # affiche le script distant
bin/m1-rearm             # applique (sudo demandé sur M1)
```

Applique :

- `pmset -a sleep 0 standby 0 hibernatemode 0 autopoweroff 0 powernap 0 womp 1 autorestart 1`
  → jamais de veille, **Wake-on-LAN activé**, **redémarrage automatique après coupure**
- `pmset repeat wake MTWRFSU 07:30:00` → réveil planifié quotidien
- reconnexion Tailscale si hors ligne, relance Ollama si muet
- enregistre la MAC de M1 dans `_local/m1-mac`

### Diagnostic du 2026-10-27 (panne de 20 jours)

| Constat | Preuve |
|---|---|
| M1 absent de Tailscale | `tailscale status` → `m1-llm … offline, last seen 20d ago` |
| M1 absent du LAN | scan TCP 22/11434/5900 sur 192.168.128.0/23 → seuls M5 et un vieux dropbear (192.168.129.5) |
| M1 absent en mDNS | aucun `m1-llm.local`, seul « MacBook Pro de JC » |
| MAC inconnue | aucun enregistrement dans le repo → WoL impossible sans elle |

Conclusion : M1 est un **portable refermé**. Capot fermé = veille profonde,
Wi-Fi coupé, Tailscale et mDNS muets. Aucun outil logiciel ne réveille un
portable refermé — d'où l'échec de la session précédente.

### Correctif durable recommandé

1. `bin/m1-rearm` dès que M1 est joignable — inclut `pmset -a disablesleep 1`,
   indispensable sur un portable pour rester éveillé **capot fermé**.
2. Garder M1 **sur secteur en permanence** ; un portable sur batterie finit
   toujours par s'endormir ou s'éteindre.
3. Réglages Système → **Batterie → alimentation secteur** :
   « Empêcher la mise en veille automatique » + « Réveiller pour l'accès réseau ».
4. Optionnel : **prise connectée** (Tapo/Kasa) sur l'alim, combinée à
   `autorestart 1` → redémarrage à froid pilotable à distance.

### Ce qui ne réveille PAS un portable refermé

| Tentative | Résultat |
|---|---|
| WoL (magic packet) | ✗ aucune NIC filaire sur un MacBook Pro 14" |
| Câble USB entre M5 et M1 | ✗ ne transporte pas d'IP (vérifié 2026-10-27) |
| Câble Ethernet direct | ✗ impossible sans adaptateur USB-C→Ethernet |
| Attendre | ✗ la veille profonde ne rend pas la main au réseau |

La seule sortie d'une veille profonde non planifiée : **ouvrir le capot**.

---

## Voie sans routeur — lien direct Ethernet (2026-10-27)

> ⚠️ **Non applicable à M1** : MacBook Pro 14" M1 = aucun port RJ45.
> Conservé pour mémoire — utile si un adaptateur USB-C→Ethernet est branché un jour.
> Les ports `en4/en5/en6` du M5 sont des interfaces internes Apple ; le seul
> Ethernet réel est `en7` (« USB 10/100/1000 LAN » via le dock).

À utiliser quand la box ne distribue pas de bail DHCP et que M1 est donc
invisible sur le LAN (adresse auto-attribuée en 169.254.x.x).

1. Débrancher le câble Ethernet de M1 du routeur, le brancher **directement**
   sur le port Ethernet du dock / adaptateur USB-C de M5.
2. Attendre ~15 s. Les deux machines s'auto-attribuent une adresse link-local
   (169.254.x.x) — aucun DHCP nécessaire.
3. Bonjour/mDNS fonctionne sur ce lien : M1 s'annonce en `m1-llm.local`.

```bash
# M5 — vérifier que le lien est monté
ifconfig en4 | grep 'inet '          # en4/en5/en6 = ports du dock
bin/m1-wake --scan-only              # teste Tailscale + Bonjour + LAN
ssh m1@m1-llm.local                  # doit répondre
```

4. Réarmer M1 par ce lien (Tailscale est inutile ici) :

```bash
M1_HOST=m1-llm.local bin/m1-rearm
```

5. Rebrancher ensuite M1 sur le routeur : `womp 1` et `autorestart 1` sont
   désormais armés, la machine retrouvera son bail et Tailscale tout seul.

**Pourquoi ça marche :** mDNS est multicast sur le lien local, il ne dépend
d'aucun serveur. C'est la seule voie qui reste quand le routage est en panne.

---

## Piège — un câble USB entre deux Mac ne crée pas de réseau

Vérifié le 2026-10-27 : câble USB-C/USB-A entre M1 et M5 → aucun lien.
`system_profiler SPThunderboltDataType` → `Status: No device connected`,
`bridge0` reste `inactive`.

Seuls deux transports créent un lien IP entre deux Mac :

| Transport | Ce qui se monte | Condition |
|---|---|---|
| Câble **Thunderbolt 3/4 / USB4** | `bridge0` (Thunderbolt Bridge) + adresse 169.254.x.x | câble TB actif des deux côtés |
| Câble **Ethernet** | interface `enX` + link-local si pas de DHCP | ports RJ45 ou adaptateurs USB-C→Ethernet |

Un câble USB « data » ou « charge » ne transporte pas d'IP. Le clavier éclairé
prouve seulement que M1 est sous tension, pas qu'il est joignable.

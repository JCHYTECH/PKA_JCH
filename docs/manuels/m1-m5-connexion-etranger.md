# 📡 M1 ↔ M5 — Connexion depuis l'étranger

> Mode d'emploi grand débutant.  
> Mis à jour : 2026-06-09

---

## Le problème

Tu as **deux Mac** :

| Machine | Où elle est | Ce qu'elle fait |
|---------|-------------|----------------|
| **M1** (headless) | Chez toi (Belgique) | Tourne Ollama, fait tourner les scripts, accessible 24h/24 |
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

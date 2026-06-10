# PKA DÉCOUVERTES — Mode d'emploi

> Dernière mise à jour : 2026-06-09

## C'est quoi ?

Un pipeline qui transforme les messages d'un **groupe Telegram** en **fiches de lieux à visiter**.

**Exemple :** tu vois un château sur Instagram → tu fais une capture d'écran → tu l'envoies dans le groupe Telegram DÉCOUVERTES → 2 minutes plus tard, une fiche complète existe avec GPS, accès van, restos à proximité, réserves naturelles autour.

---

## Comment ça marche (vue d'ensemble)

```
📱 Tu envoies un message dans le groupe Telegram DÉCOUVERTES
         ↓
🤖 Le bot Telegram le capture automatiquement (24h/24)
         ↓
📁 Le message est sauvegardé dans raw/ + mis en file d'attente dans queue/
         ↓
🧠 Tu lances l'analyzer (manuellement) → il identifie le lieu
         ↓
📝 Une fiche Markdown est créée dans drafts/
         ↓
✅ Tu valides la fiche → tu la déplaces dans validated_places/
```

---

## Pour les membres du groupe Telegram

### Ce que tu peux envoyer

| Type | Exemple | Ce que le bot capture |
|------|---------|----------------------|
| **Photo** | Photo d'un monument | L'image + légende éventuelle |
| **Capture d'écran** | Screenshot Instagram, Google Maps | L'image + texte visible |
| **Lien** | URL d'un article, Facebook, blog | Le lien + le texte qui l'accompagne |
| **Texte** | "Château de Beynac, Dordogne" | Le texte brut |
| **Coordonnées GPS** | 44.8404, 1.1453 | Le texte |

### Ce qu'il ne faut PAS faire
- Envoyer des messages de discussion ("OK", "merci", "on y va quand ?") → l'analyzer les ignorera automatiquement
- Envoyer des liens Facebook sans description → l'analyzer ne peut pas lire Facebook

### Conseil
Ajoute toujours **un petit texte** avec ta photo ou ton lien. Même juste le nom du lieu. Ça aide l'analyzer à identifier.

---

## Pour l'administrateur (JCH)

### 1. Démarrer le collecteur (une fois par session)

Le collecteur écoute le groupe Telegram 24h/24. À lancer dans un terminal dédié :

```bash
cd ~/PKA_JCH/scripts/decouvertes-collector
source venv/bin/activate
python3 collector.py
```

**Ne pas fermer ce terminal.** Le collecteur tourne en permanence.

Pour l'arrêter : `Ctrl+C` dans ce terminal.

⚠️ **Une seule instance à la fois.** Si tu vois une erreur `Conflict`, fais :
```bash
pkill -f collector.py
sleep 2
python3 collector.py
```

### 2. Lancer l'analyse (quand tu veux)

L'analyzer traite tous les messages en attente dans `queue/` :

```bash
cd ~/PKA_JCH/scripts/decouvertes-collector
source venv/bin/activate

# Analyse rapide (Claude Haiku, ~0.01€ par message)
python3 analyzer.py

# Analyse cascade (qwen3.5 local → Haiku → Sonnet → Opus, plus fiable)
python3 analyzer.py --cascade

# Traiter seulement les 5 premiers messages
python3 analyzer.py --limit 5

# Forcer un modèle spécifique
python3 analyzer.py --model sonnet
```

**Quand lancer ?** Une fois par jour, ou après avoir reçu plusieurs messages dans le groupe.

### 3. Valider les fiches

Les fiches générées sont dans :
```
JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/drafts/
```

Pour chaque fiche :
1. Ouvre le fichier `.md` dans Obsidian
2. Vérifie : nom du lieu, GPS, photo, scores (photo/nature/patrimoine)
3. Si c'est bon → déplace dans `validated_places/`
4. Si incorrect → supprime ou corrige

### 4. Vérifier que tout va bien

```bash
# Le collecteur tourne ?
ps aux | grep collector.py

# Y a-t-il des messages en attente ?
ls JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/queue/

# Combien de fiches générées ?
ls JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/drafts/

# Le log est-il propre ?
tail -5 JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/logs/collector.log
```

---

## Structure des dossiers

| Dossier | Contenu | Qui écrit |
|---------|---------|-----------|
| `raw/text/` | Messages texte bruts | collector.py (auto) |
| `raw/images/` | Photos et screenshots | collector.py (auto) |
| `raw/links/` | Liens extraits | collector.py (auto) |
| `raw/metadata/` | Métadonnées JSON | collector.py (auto) |
| `queue/` | Files d'attente (copie des métadonnées) | collector.py → analyzer.py |
| `drafts/` | Fiches Markdown générées | analyzer.py (auto) |
| `validated_places/` | Fiches validées manuellement | Toi (JCH) |
| `logs/` | Logs du collecteur (rotation auto 1 Mo) | collector.py (auto) |
| `reports/` | Rapports HTML interactifs (carte + restos) | analyzer.py (auto) |
| `maps/` | Cartes HTML des lieux | analyzer.py (auto) |

---

## Que contient une fiche ?

Exemple d'une fiche générée dans `drafts/` :

```markdown
---
type: lieu_a_visiter
status: validated
source: telegram
pays: France
region: Pyrénées-Atlantiques
ville: Oloron-Sainte-Marie
nom_lieu: Oloron-Sainte-Marie
gps: "43.1922408, -0.6115586"
interet_photo: 5
interet_nature: 1
interet_patrimoine: 5
confidence: 0.95
---

# Oloron-Sainte-Marie

## Résumé
Cathédrale UNESCO, maisons à colombages, Béarn...

## Pourquoi visiter
...

## Accès minivan (2m hauteur · 5m longueur)
Parking Jeanne-d'Albret (gratuit, hauteur 2,3m)...

## Localisation
GPS + lien Google Maps

## Rapport complet
Lien vers le rapport HTML avec carte interactive
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| "DECOUVERTES_TOKEN manquant" | Vérifier `JCH_PRIVATE/decouvertes.env` — le token doit être sur UNE SEULE ligne : `DECOUVERTES_TOKEN=890...` |
| "Conflict" au démarrage | `pkill -f collector.py` puis relancer |
| Le bot ne reçoit plus rien | Vérifier que le token n'a pas été révoqué (BotFather) |
| L'analyzer ne trouve rien | `queue/` est peut-être vide ou les statuts sont `"skipped"` au lieu de `"pending"` — vérifier avec `cat queue/*.json \| grep analysis_status` |
| Le log est énorme | Normalement rotation automatique à 1 Mo. Si dépassé, purger : `echo "" > logs/collector.log` |
| Token visible dans le log | Ne devrait plus arriver (TokenMaskFilter). Si oui, redémarrer le collector. |

---

## Secrets et sécurité

- Les tokens et clés API sont dans `JCH_PRIVATE/decouvertes.env` (protégé par `.gitignore`)
- Le fichier `scripts/decouvertes-collector/.env` ne contient **aucun secret** (juste PKA_ROOT)
- `scripts/decouvertes-collector/.env.example` est le template pour les nouveaux contributeurs
- Le token est automatiquement masqué (`***TOKEN***`) dans les logs
- Rotation des logs : 1 Mo maximum, 3 backups

# 🐶 Dobby — Bot Telegram PKA
## Guide d'installation complet

> **Prérequis :** Tu as déjà un bot Telegram créé (via @BotFather) avec son token et ton user ID.  
> **Durée estimée :** 15 minutes.

---

## Ce que tu vas installer

Un service qui tourne en arrière-plan sur ton Mac et te permet de parler à Dobby via Telegram :
- Messages texte → Dobby répond
- Messages vocaux → transcription automatique → Dobby répond
- Photos → analyse visuelle → Dobby répond

---

## Étape 0 — Récupérer ton User ID Telegram

Tu as besoin de ton **User ID numérique** Telegram (différent de ton nom d'utilisateur).

1. Sur Telegram, cherche le bot `@userinfobot`
2. Envoie-lui `/start`
3. Il te répond avec ton ID numérique (ex: `123456789`)
4. Note ce nombre — tu en as besoin à l'étape 2

---

## Étape 1 — Récupérer une clé OpenAI (pour la voix)

> Si tu ne veux pas utiliser les messages vocaux, saute cette étape.

1. Va sur [platform.openai.com](https://platform.openai.com)
2. Crée un compte ou connecte-toi
3. Menu gauche → **API Keys** → **Create new secret key**
4. Copie la clé (commence par `sk-`)
5. Note-la — elle n'est visible qu'une fois

> **Coût voix :** Whisper coûte $0.006/minute audio. Pour un usage personnel, compte €1-2/mois max.

---

## Étape 2 — Créer le fichier .env

C'est le fichier qui contient tes clés secrètes. Il ne doit jamais être partagé.

Ouvre le Terminal et tape :

```bash
cd /Users/jchavauxm5/PKA_JCH/scripts/telegram-bot
cp .env.example .env
open -e .env
```

L'éditeur TextEdit s'ouvre. Remplace chaque valeur :

```
TELEGRAM_TOKEN=      ← ton token BotFather (ex: 7123456789:AAH...)
TELEGRAM_USER_ID=    ← ton user ID numérique (ex: 123456789)
ANTHROPIC_API_KEY=   ← ta clé Anthropic (ex: sk-ant-api03-...)
OPENAI_API_KEY=      ← ta clé OpenAI (ex: sk-proj-...) — optionnel si pas de voix
PKA_ROOT=            ← laisser tel quel : /Users/jchavauxm5/PKA_JCH
```

Sauvegarde et ferme TextEdit.

**⚠️ Vérifie** qu'il n'y a pas d'espace avant ou après le `=` et pas de guillemets autour des valeurs.

---

## Étape 3 — Lancer l'installation

Dans le Terminal :

```bash
cd /Users/jchavauxm5/PKA_JCH/scripts/telegram-bot
bash install.sh
```

Le script fait automatiquement :
1. Vérifie que Python est installé
2. Crée un environnement virtuel isolé (`venv/`)
3. Installe toutes les bibliothèques nécessaires
4. Vérifie ton fichier `.env`
5. Crée le service de démarrage automatique
6. Démarre Dobby

Si tu vois ✅ **Dobby est en ligne !** → c'est bon.

---

## Étape 4 — Tester

1. Ouvre Telegram
2. Trouve ton bot (celui que tu as créé avec @BotFather)
3. Envoie `/start`
4. Dobby doit répondre : "🐶 Dobby en ligne. Parle — je t'écoute."

Test voix :
- Envoie un message vocal → Dobby transcrit et répond

Test photo :
- Envoie une photo (avec ou sans légende) → Dobby analyse

---

## Commandes disponibles

| Commande | Action |
|----------|--------|
| `/start` | Démarrer / vérifier que Dobby tourne |
| `/status` | État du système PKA (membres actifs, contexte) |
| `/clear` | Effacer l'historique de conversation |
| `/help` | Afficher l'aide |

---

## Gestion du service (après installation)

### Vérifier que Dobby tourne
```bash
launchctl list | grep dobby
```
Si une ligne apparaît → il tourne. Si rien → il est arrêté.

### Voir les logs en temps réel
```bash
tail -f /Users/jchavauxm5/PKA_JCH/scripts/telegram-bot/dobby.log
```
Très utile pour déboguer. `Ctrl+C` pour quitter.

### Arrêter Dobby
```bash
launchctl unload ~/Library/LaunchAgents/com.pka.dobby.plist
```

### Redémarrer Dobby
```bash
launchctl kickstart -k gui/$(id -u)/com.pka.dobby
```

### Désinstaller complètement
```bash
launchctl unload ~/Library/LaunchAgents/com.pka.dobby.plist
rm ~/Library/LaunchAgents/com.pka.dobby.plist
```

---

## Structure des fichiers

```
telegram-bot/
├── bot.py              ← code principal du bot
├── dobby_context.py    ← personnalité et contexte PKA de Dobby
├── requirements.txt    ← bibliothèques Python nécessaires
├── install.sh          ← script d'installation (à lancer une fois)
├── .env                ← tes clés secrètes (ne jamais partager)
├── .env.example        ← modèle du fichier .env
├── venv/               ← environnement Python isolé (créé par install.sh)
├── conversation.db     ← historique des conversations (créé au démarrage)
└── dobby.log           ← logs du bot (créé au démarrage)
```

---

## Comportement automatique

- **Au démarrage du Mac** → Dobby démarre automatiquement
- **Si Dobby plante** → il redémarre automatiquement après 10 secondes
- **Quand le Mac dort** → les messages arrivent en attente, traités au réveil
- **Historique** → les 20 derniers échanges sont conservés entre sessions

---

## Problèmes courants

### "Erreur Claude" dans la réponse
→ Vérifie que `ANTHROPIC_API_KEY` est correct dans `.env`  
→ Vérifie que tu as du crédit sur ton compte Anthropic

### "Transcription non disponible"
→ `OPENAI_API_KEY` manquant ou incorrect dans `.env`

### Le bot ne répond pas du tout
→ Lance `tail -f dobby.log` et regarde le message d'erreur  
→ Le plus souvent : `TELEGRAM_TOKEN` incorrect

### "Accès refusé" dans les logs
→ Quelqu'un d'autre a trouvé ton bot et essaie d'écrire  
→ C'est normal — seul ton `TELEGRAM_USER_ID` est autorisé

### Le service ne démarre pas après reboot
```bash
launchctl load ~/Library/LaunchAgents/com.pka.dobby.plist
```

---

## Mettre à jour le contexte PKA (équipe, projets)

Quand l'équipe évolue ou qu'un projet change de statut :

1. Ouvre `dobby_context.py`
2. Modifie la section correspondante dans `SYSTEM_PROMPT`
3. Redémarre Dobby :
```bash
launchctl kickstart -k gui/$(id -u)/com.pka.dobby
```

---

*Installé par Forge · PKA JCH · 2026-05-10*

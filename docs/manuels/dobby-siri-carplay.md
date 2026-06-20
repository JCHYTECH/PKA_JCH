# Dobby via Siri & CarPlay — Mode d'emploi

> **Objectif :** parler à Dobby 🦉 en mains libres, en voiture (CarPlay) ou n'importe où via Siri.
> **Date :** 2026-06-20
> **Statut :** prêt à déployer

---

## Pourquoi ce guide

L'app Telegram sur CarPlay ne permet pas l'envoi de messages vocaux — uniquement l'écoute.  
Le bot Telegram (pipeline STT/TTS Gemini) n'est donc pas accessible en voiture.

**Solution :** un Raccourci iOS qui :
1. Capture ta voix
2. L'envoie à l'API Moonshot (Kimi K2.7) avec le system prompt complet de Dobby
3. Lit la réponse à voix haute via Siri

---

## Prérequis

| Élément | État |
|---------|-------|
| iPhone avec iOS 18+ | ✅ |
| Clé API Moonshot (`~/.config/pka-jch/kimi_key.txt`) | ✅ |
| Crédits Kimi K2.7 actifs | ✅ |
| Fichiers système PKA accessibles (Dropbox, iCloud, ou copie manuelle) | ⚠️ À faire |

---

## Étape 1 — Préparer le system prompt Dobby

Dobby a besoin de son contexte pour fonctionner. On crée un fichier unique qui fusionne les 4 fichiers système.

**Sur M5, dans PKA_JCH :**
```bash
cd ~/PKA_JCH
cat KIMI.md SOUL.md USER.md MEMORY.md > /tmp/dobby-system-prompt.txt
```

Le fichier `dobby-system-prompt.txt` fait environ 30-40 KB. Il contient :
- `KIMI.md` — identité, règles, projets actifs
- `SOUL.md` — personnalité Dobby, règles comportementales
- `USER.md` — profil JC, setup technique
- `MEMORY.md` — historique PKA complet

**Transférer ce fichier sur l'iPhone :**
- Option A : AirDrop → l'enregistrer dans Fichiers > Raccourcis
- Option B : iCloud Drive → `Raccourcis/dobby-system-prompt.txt`
- Option C : Dropbox → accessible depuis l'app Raccourcis

> ⚠️ **À refaire** après chaque mise à jour de MEMORY.md ou SOUL.md (~1×/semaine).  
> Le fichier ne se synchronise pas automatiquement.

---

## Étape 2 — Récupérer la clé API Kimi

```bash
cat ~/.config/pka-jch/kimi_key.txt
```

Copier la clé (commence par `sk-`).  
À entrer dans le Raccourci à l'étape suivante.

> 🔒 Cette clé sera stockée en clair dans le raccourci.  
> Le raccourci est privé sur ton iPhone — personne d'autre n'y a accès.  
> Pour plus de sécurité : stocker la clé dans le Trousseau iCloud et la lire via l'action « Récupérer le mot de passe ».

---

## Étape 3 — Créer le Raccourci « Dobby »

Ouvrir l'app **Raccourcis** sur l'iPhone.

### 3.1 Créer un nouveau raccourci

- Appuyer sur **+** (haut à droite)
- Nom : **Dobby**
- Icône : 🦉
- Activer « Afficher sur Apple Watch » (optionnel)
- Activer « Siri » — phrase : *« Dis Siri, Dobby »*

### 3.2 Ajouter les actions (dans l'ordre)

#### Action 1 — Dicter du texte
```
Action : « Dicter du texte »
Langue : Français
Arrêter après : Après une pause
```
→ Stocke la transcription dans `Texte dicté`

#### Action 2 — Lire le system prompt
```
Action : « Fichier »
Fichier : dobby-system-prompt.txt
```
→ Stocke le contenu dans `Fichier`

#### Action 3 — Appeler l'API Kimi (via « Obtenir le contenu de l'URL »)
```
Action : « Obtenir le contenu de l'URL »
URL : https://api.moonshot.ai/v1/chat/completions
Méthode : POST
En-têtes :
  - Authorization : Bearer sk-ta_clé_api_kimi
  - Content-Type : application/json
Corps de la requête : JSON
```

Dans le corps JSON :
```json
{
  "model": "kimi-k2.7-code",
  "messages": [
    {"role": "system", "content": "[Fichier]"},
    {"role": "user", "content": "[Texte dicté]"}
  ],
  "max_tokens": 500,
  "temperature": 0.7
}
```

> **Note :** remplacer `[Fichier]` et `[Texte dicté]` par les variables des actions 1 et 2.  
> Dans Raccourcis, toucher longuement le champ → « Insérer une variable » → choisir la variable.

#### Action 4 — Extraire la réponse
```
Action : « Obtenir la valeur du dictionnaire »
Dictionnaire : [Résultat de l'URL]
Clé : choices.0.message.content
```
→ Stocke dans `Réponse Dobby`

#### Action 5 — Lire la réponse à voix haute
```
Action : « Énoncer le texte »
Texte : [Réponse Dobby]
Langue : Français
Voix : Siri (ou une voix française améliorée)
Attendre la fin : OUI
```

### 3.3 Résumé du flux

```
🎤 Dicter → 📄 Charger KIMI+SOUL+USER+MEMORY → 🌐 API Moonshot → 📥 Extraire réponse → 🔊 Énoncer
```

---

## Étape 4 — Tester

1. Dire « Dis Siri, Dobby » (ou lancer le raccourci manuellement)
2. Parler après le bip
3. Attendre ~3-8 secondes (latence API Kimi)
4. Siri lit la réponse

**Premier test recommandé :** *« Dobby, qui es-tu ? »*  
Réponse attendue : *« Je suis Dobby 🦉 — ton orchestrateur PKA... »*

---

## Étape 5 — CarPlay

Le raccourci fonctionne automatiquement en CarPlay :

1. Maintenir le bouton vocal au volant → Siri s'active
2. Dire « Dobby » → le raccourci se lance
3. Parler normalement
4. La réponse est lue via les haut-parleurs du véhicule

> ℹ️ CarPlay utilise le micro du véhicule — qualité audio généralement bonne.  
> Pas besoin de toucher l'iPhone.

---

## Dépannage

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| « J'ai besoin d'une app pour ça » | Raccourci pas nommé « Dobby » | Renommer le raccourci |
| Erreur 401 | Clé API invalide | Vérifier la clé dans `~/.config/pka-jch/kimi_key.txt` |
| Réponse absurde | System prompt pas chargé | Vérifier que `dobby-system-prompt.txt` est accessible dans Fichiers |
| Latence > 10s | Réseau faible | Vérifier la connexion cellulaire |
| Siri coupe la réponse | `Attendre la fin` non activé | Action « Énoncer » → activer « Attendre la fin » |
| Coût excessif | `max_tokens` trop élevé | Réduire à 300-400 tokens pour l'usage vocal |

---

## Coût estimé

| Modèle | Input (system prompt) | Output (réponse) | Coût par interaction |
|--------|----------------------|-------------------|---------------------|
| kimi-k2.7-code | ~25K tokens × $0.6/M | ~300 tokens × $1.8/M | ~$0.02 |

Soit environ **2 centimes par question**. Avec $5 de crédit → ~250 interactions.

> 📊 Le system prompt (KIMI+SOUL+USER+MEMORY) compte ~25 000 tokens. C'est le principal coût.  
> Si le crédit baisse vite, envisager de réduire MEMORY.md à l'essentiel pour le raccourci.

---

## Améliorations futures

- [ ] **Trousseau iCloud** — stocker la clé API dans le Trousseau plutôt qu'en clair
- [ ] **TTS OpenAI** — voix « Nova » plus naturelle que Siri ($0.015/1K car.)
- [ ] **Mise à jour auto** — script qui pousse `dobby-system-prompt.txt` vers iCloud après chaque `/save`
- [ ] **Contexte conversation** — sauvegarder les derniers échanges pour des réponses contextuelles
- [ ] **Mode push-to-talk** — Raccourci qui reste actif pour une conversation continue

---

*Guide rédigé par Dobby 🦉 — à déployer quand tu veux. Le Raccourci prend ~5 minutes à créer.*

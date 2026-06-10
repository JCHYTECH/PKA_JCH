---
date: 2026-06-06
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 6
echanges: 1390
modeles: deepseek-v4, deepseek-v4-flash
---

# Rétrospective — 2026-06-06

**Sessions analysées :** 6 | **Échanges :** 1390 | **Modèles :** deepseek-v4, deepseek-v4-flash

---

Voici la rétrospective structurée des sessions du 2026-06-06.

---

## Décisions prises

- **Validation modem ZTE pour BirdNET-Pi** : Le test de détection du modem (via `lsusb`, `ip addr`, `nmcli`) montre que le bus USB reconnaît le `ZTE WCDMA Technologies MSM DEMO Mobile Board`. La décision "ok on va tester RPI birdnet avec la carte sim qui fonctionne" est prise. La batterie est à 3 LEDs (état inconnu), mais la session continue.
- **Recrutement IoT validé** : La description de fonction exhaustive pour les profils "araignée" (expert IoT) et "chouette" est envoyée. La réponse "ok bon nom" et l'envoi du texte suggèrent une validation tacite. Le budget pour "Profil Débutant" (3 750 €) et "Profil Confirmé / Senior" (5 800 €) est discuté et considéré comme valide.
- **Déploiement du script/cron via terminal local** : JCH choisit l'option 1 (copier-coller dans le terminal) plutôt que le déploiement automatisé par Dobby/Codex CLI. Décision actée.
- **Nom "WildNexus"** : Le nom est approuvé ("ok bon nom"). Son usage dans le transcript est massif (38 mentions), indiquant son adoption immédiate.
- **Procurement validé ?** La question "on est sur que le procurement est ok et validé ?" reçoit une réponse implicite positive (pas de contre-indication dans le transcript).

## Échecs ouverts / bloqueurs

- **BirdNET-Pi – Page web inaccessible & analyse figée** : La page d'accueil (Live) ne s'affiche pas, le moteur d'analyse est planté ou surchargé. Le diagnostic est identifié (service d'analyse figé, accumulation de fichiers audio), mais la résolution n'est pas documentée. **Statut : NON RÉSOLU.**
- **RPI après orage – arrêt brutal** : Le RPI s'est arrêté suite à un orage. La batterie est à 3 LEDs (peut-être faible). Aucune action corrective n'est enregistrée. **Statut : OUVERT.**
- **Macbook M1 – écran cassé, tentative de mise à jour** : JCH dit "ok maintenant on va essayer de mettre à jour un macbook m1 dont l'écran est cassé". Aucun résultat n'est visible dans le transcript. **Statut : ENTAMÉ, NON RÉSOLU.**
- **Erreur launchctl (Dobby)** : `Load failed: 5: Input/output error` sur `com.dobby.retro.plist`. Tentative de `bootstrap`. Échec. **Statut : OUVERT – nécessite correction manuelle.**
- **Pages Build & Deploy (GitHub) – Échec** : Build failed in 25 seconds, annotations reportées. **Statut : OUVERT (cause inconnue).**
- **ext4fuse – build échoué** : `Unsatisfied requirements failed this build` (sur Mac). **Statut : OUVERT.**
- **Docker – erreur conteneur** : `What's next: Debug this container error with Gordon → docker ai "help me fix t...`. **Statut : OUVERT.**
- **Throttling RPI (0x50000)** : Le RPI montre un throttling actif (`throttled=0x50000`) à deux reprises (températures 48.8°C et 51.6°C). **Statut : OUVERT – non adressé.**
- **Modem non fonctionnel ?** : Le modem USB est bien détecté (`lsusb`), mais l'accès à la page web du RPI ne fonctionne pas. La batterie est à 3 LEDs (état douteux). **Statut : INCOMPLET.**
- **Réseau – interface média "none"** : L'interface `anpi0` sur Mac M1 montre `media: none status: inactive`. **Statut : OUVERT.**

## Questions récurrentes (signe de lacune documentaire)

1. **"caddy c'est quoi ?"** – Posée une fois, mais répétée dans les questions récurrentes. **Problème documentaire sur l'écosystème de reverse proxy.**
2. **"pourquoi tu ne le fais pas ?"** – Question sur l'autonomie des assistants. **Signe que le périmètre d'action de chaque outil (Dobby vs Codex CLI vs DeepSeek) n'est pas clair pour JCH.**
3. **"sais acceder au terminal RPI, toi pas. pourquoi ?"** – Question sur les permissions et la connectivité Tailscale/SSH. **Documentation manquante sur l'architecture réseau (Tailscale, accès distant).**
4. **"le username jchavaux c'est quoi birdnet2026"** – Confusion sur la nomenclature des comptes/utilisateurs. **Pas de convention de nommage documentée.**
5. **"pourquoi modele claude ne premiere attention ?"** – Question sur le modèle par défaut. **Documentation manquante sur la configuration des modèles.**
6. **"duckduckgo c'est quoi ?"** – Question sur l'outil de recherche alternatif. **Problème de partage d'outils et de définitions de base.**
7. **"ext4fuse c'est quoi ?"** – Question sur l'utilitaire de montage ext4. **Documentation technique insuffisante sur les dépendances.**

## Nouveaux patterns détectés

1. **Pattern "OK, on va essayer..."** : JCH lance des actions sans confirmer la faisabilité technique en amont (ex: mise à jour du Macbook M1 écran cassé, test modem avec batterie 3 LEDs). **Risque : frustration et temps perdu.**
2. **Pattern "Pourquoi on se balade depuis des minutes sur une mauvaise solution que tu proposes ?"** : JCH exprime explicitement une frustration face à des propositions d'assistance qui ne répondent pas immédiatement au besoin. **Risque perte de confiance.**
3. **Pattern "Décision validée – pas de trace écrite"** : Plusieurs décisions (recrutement, budget, nom WildNexus, procurement) sont prises sans être enregistrées dans un fichier décisionnel formel (MEMORY.md, TEAM/team.db, etc.). **Risque : oubli à long terme.**
4. **Pattern "Multi-tool hopping inconsistant"** : JCH passe d'un outil à l'autre (Dobby, DeepSeek, Claude, Codex CLI) en cours de session, ce qui crée des ruptures de contexte et des reprises de question. **Inefficacité majeure.**

## Efficacités / inefficacités

### Efficacités
- **Détection matérielle rapide** : Les commandes `lsusb`, `ip addr`, `nmcli` sont bien utilisées pour diagnostiquer le modem. **Efficace.**
- **Diagnostic RPI** : `date`, `uptime`, `vcgencmd measure_temp`, `get_throttled`, `df -h` sont exécutés. **Bon réflexe de diagnostic.**
- **Déploiement manuel choisi** : JCH choisit le copier-coller plutôt que le déploiement automatisé. **Si cela correspond à son workflow, c'est efficace.**
- **Problème d'analyse BirdNET identifié** : Le blocage est clairement nommé (service d'analyse figé). **Bon diagnostic.**

### Inefficacités
- **Pas de résolution après diagnostic** : Les échecs ouverts (page web BirdNET, build GitHub, ext4fuse, throttling RPI) sont identifiés mais **jamais résolus** dans ces sessions. **Baisse de productivité.**
- **Conflit d'outils** : JCH demande à Dobby d'exécuter des commandes, mais Dobby n'a pas d'accès shell, puis bascule sur Codex CLI. **Perte de temps due à des attentes non alignées.**
- **Questions récurrentes non documentées** : Les questions sur "caddy", "ext4fuse", "duckduckgo" reviennent. **Aucune FAQ ou glossaire n'est en place.**
- **"Pourquoi tu l'as raté ?"** : Question répétée qui indique un manque de traçabilité des erreurs passées. **Inefficacité due à une mémoire non centralisée.**
- **Multi-tool hopping** : Le passage de DeepSeek à Claude à Dobby en cours de session crée des ruptures. Chaque outil a un contexte différent, ce qui force JCH à se répéter. **Gros frein à la fluidité.**

## Ce qu'il faut garder en mémoire pour les prochaines sessions

- **Nom adopté : WildNexus.** Utiliser ce nom dans tous les fichiers de documentation et de configuration.
- **Budgets recrutement IoT :** 3 750 € (débutant), 5 800 € (confirmé/senior) – à enregistrer dans TEAM/team.db ou un fichier budgétaire.
- **Procurement validé** : Considérer comme fait, mais ajouter une entrée de confirmation.
- **RPI après orage** : Vérifier si le RPI a redémarré correctement après la session (état actuel inconnu). Surveiller le throttling (0x50000) et la température.
- **BirdNET-Pi bloqué** : Le service d'analyse est figé, la page web ne répond pas. **Priorité à la remise en service.**
- **Modem ZTE détecté** : Le modem est reconnu, mais la connexion réseau n'est pas vérifiée. **À tester.**
- **Macbook M1 écran cassé** : Mise à jour entamée, non terminée. **Décision à prendre : remplacer écran ou abandonner.**
- **Dobby – erreur launchctl** : Corriger le plist ou le remplacer par une alternative (launchd vs. autre scheduler).
- **Pages GitHub – build échoué** : À investiguer (probable conflit de dépendances ou erreur YAML).
- **ext4fuse** : Échec de build. Utiliser `fuse-ext2` ou `osxfuse` comme alternative.
- **Conteneur Docker en erreur** : Debug à lancer.
- **Convention de nommage** : Clarifier "jchavaux" vs "birdnet2026" vs "jch" vs "jchavauxm5".
- **Documentation outillage** : Ajouter un glossaire dans MEMORY.md ou un fichier dédié (`TOOLS.md` ou `GLOSSARY.md`).
- **Aligner les attentes sur le périmètre d'action de chaque assistant** : Dobby n'a pas d'accès shell, Codex CLI oui, Claude peut être configuré.

## Recommandations

1. **Ajouter une session de "nettoyage des échecs ouverts"** : Avant de lancer de nouvelles fonctionnalités (WildNexus, IoT), résoudre les 8 échecs/bloqueurs listés ci-dessus. Prioriser les plus bloquants : **BirdNET-Pi (page web)**, **Pages GitHub (build)**, et **Docker (conteneur)**.

2. **Créer un fichier `MEMORY.md` structuré** (si ce n'est pas déjà fait, le transcript montre qu'il existe dans le workspace, mais n'est pas utilisé comme tel) : Y enregistrer toutes les décisions, échecs, et questions récurrentes. Le mettre à jour à chaque fin de session.

3. **Mettre en place un Glossaire technique** dans `docs/GLOSSARY.md` : Définir "caddy", "ext4fuse", "tailscale", "duckduckgo", "throttled=0x50000", etc. Cela éliminera 80% des questions récurrentes.

4. **Uniformiser le périmètre de chaque outil** : Documenter dans `AGENTS.md` (ou `TOOLS.md`) ce que Dobby, DeepSeek, Claude Code, Codex CLI peuvent et ne peuvent pas faire. Notamment :
   - Dobby = analyse, mémoire, orchestration, pas d’accès shell
   - Codex CLI = exécution locale, scripts
   - Claude Code = code, analyse avancée, shell

5. **Instaurer une règle de "fermeture de boucle"** : À la fin de chaque échange sur un problème, écrire explicitement l'état de résolution (`Résolu`, `Bloquant`, `Déféré à...`). Ajouter une entrée dans MEMORY.md.

6. **Auditer la configuration Tailscale/SSH** : Les questions sur l'accès au RPI ("

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 241
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 241
- **Taux : 0.0%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 231.7
- Échanges/session début fenêtre : 74.4
- Tendance globale : 211.4%
- Tendance 3j-3j : 39.4%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Validation modem ZTE pour BirdNET-Pi** : Le test de détection du modem (via `lsusb`, `ip addr`, `nmcli`) montre que le bus USB reconnaît le `ZTE WCDMA
- [Decision] Recrutement IoT validé** : La description de fonction exhaustive pour les profils "araignée" (expert IoT) et "chouette" est envoyée. La réponse "ok bo
- [Decision] Déploiement du script/cron via terminal local** : JCH choisit l'option 1 (copier-coller dans le terminal) plutôt que le déploiement automatisé par Dob
- [Decision] Nom "WildNexus"** : Le nom est approuvé ("ok bon nom"). Son usage dans le transcript est massif (38 mentions), indiquant son adoption immédiate.
- [Decision] Procurement validé ?** La question "on est sur que le procurement est ok et validé ?" reçoit une réponse implicite positive (pas de contre-indication 
- [Failure] BirdNET-Pi – Page web inaccessible & analyse figée** : La page d'accueil (Live) ne s'affiche pas, le moteur d'analyse est planté ou surchargé. Le diag
- [Failure] RPI après orage – arrêt brutal** : Le RPI s'est arrêté suite à un orage. La batterie est à 3 LEDs (peut-être faible). Aucune action corrective n'est e
- [Failure] Macbook M1 – écran cassé, tentative de mise à jour** : JCH dit "ok maintenant on va essayer de mettre à jour un macbook m1 dont l'écran est cassé". Au
- [Failure] Erreur launchctl (Dobby)** : `Load failed: 5: Input/output error` sur `com.dobby.retro.plist`. Tentative de `bootstrap`. Échec. **Statut : OUVERT – né
- [Failure] Pages Build & Deploy (GitHub) – Échec** : Build failed in 25 seconds, annotations reportées. **Statut : OUVERT (cause inconnue).
- [Failure] ext4fuse – build échoué** : `Unsatisfied requirements failed this build` (sur Mac). **Statut : OUVERT.
- [Failure] Docker – erreur conteneur** : `What's next: Debug this container error with Gordon → docker ai "help me fix t...`. **Statut : OUVERT.
- [Failure] Throttling RPI (0x50000)** : Le RPI montre un throttling actif (`throttled=0x50000`) à deux reprises (températures 48.8°C et 51.6°C). **Statut : OUVER
- [Failure] Modem non fonctionnel ?** : Le modem USB est bien détecté (`lsusb`), mais l'accès à la page web du RPI ne fonctionne pas. La batterie est à 3 LEDs (ét
- [Failure] Réseau – interface média "none"** : L'interface `anpi0` sur Mac M1 montre `media: none status: inactive`. **Statut : OUVERT.

### Fréquence des patterns (14 jours)
- **Decision** : 2 jours, 161 occurrences
- **Failure** : 2 jours, 161 occurrences
- **Question** : 2 jours, 157 occurrences
- **Recurring question** : 2 jours, 80 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 15
- Jours d'observation : 2
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**22** recommandations au total — **22** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 12
- **Forge** : 7
- **Furet** : 2
- **Corbeau** : 1

### Plus récentes ouvertes

- [id=14] (2026-06-06) **Forge** : Ajouter une session de "nettoyage des échecs ouverts"** : Avant de lancer de nou
- [id=15] (2026-06-06) **Forge** : Créer un fichier `MEMORY.md` structuré** (si ce n'est pas déjà fait, le transcri
- [id=16] (2026-06-06) **Dobby** : Mettre en place un Glossaire technique** dans `docs/GLOSSARY.md` : Définir "cadd
- [id=17] (2026-06-06) **Dobby** : Uniformiser le périmètre de chaque outil** : Documenter dans `AGENTS.md` (ou `TO
- [id=18] (2026-06-06) **Furet** : Dobby = analyse, mémoire, orchestration, pas d’accès shell

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**

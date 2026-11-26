---
date: 2026-09-25
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1051
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-25

**Sessions analysées :** 2 | **Échanges :** 1051 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA - 2026-09-25

## Décisions prises

- **Approche interrogative avant action** : Poser des questions polies aux utilisateurs/partenaires pour comprendre avant d'implémenter (pattern récurrent, jamais formalisé jusqu'à présent).
- **Choix du niveau iPhone disponible** : Sélectionner le niveau d'API/SDK existant sur iOS plutôt que de demander une installation manuelle unitaire.
- **Abandon de la fixation individuelle de facteurs** : Ne pas exiger la fixation manuelle de paramètres ; créer une forme sphérique par défaut (décision d'arrêt : "on tourne en rond").
- **Documentation forcée** : Créer un fichier `.md` pour documenter la situation actuelle et les échecs.
- **Finalisation des fiches validées** : Marquer comme complètes et passer à la phase suivante.
- **Migration vers les screenshots inbox** : Basculer le flux de travail vers `inbox/sites` pour les captures d'écran.
- **Procedure spots de stationnement** : Créer une procédure dédiée pour les fiches "spots" (parking/stationnement).
- **Escalade partenaire Alain Bosseloir** : Reporter certaines décisions après discussion avec le partenaire stratégique.
- **Essai de solution** : Approuver une tentative ("oui on va essayer") sans préjugé du résultat.

**Verdict** : Beaucoup de micro-décisions, peu de décisions stratégiques formalisées. Trop de "on va" sans trace écrite de *pourquoi*.

---

## Échecs ouverts / bloqueurs

### Critiques
1. **AppManager.install bloqué** → `duplicate_os_install`  
   État : Système non-sain, installation dupliquée détectée. Action : Diagnostic + amélioration de la procédure requise.

2. **Connexion sécurisée échouée** → SSL/TLS handshake failure  
   État : Bloqueur réseau non isolé. Probable : certificat expiré, configuration TLS cassée.

3. **Erreur SQUASHFS superblock** → `/mnt: fsconfig() failed`  
   État : Partition NVMe (nvme0n1p5) corrompue ou mal montée. Impossible d'accéder au système de fichiers. **BLOCKER MATÉRIEL**.

4. **Authentification Google Keyword défaillante** → Username/pass non fonctionnels  
   État : Credentials périmés ou API révoquée. Impact : Impossible de récupérer des données de mots-clés.

5. **Erreur 404 sur endpoint inconnu**  
   État : Endpoint disparu ou URL malformée. Pas d'URL citée → diagnostic impossible.

6. **Vanroll Test ne retourne plus de données**  
   État : Requête récurrente mais non résolue. Besoin d'investigation sur l'API Vanroll.

7. **Terminal RPi inaccessible** → Raison non documentée  
   État : Blocage SSH/réseau ou service arrêté. Récurrent et non investigué.

8. **Fiches Dante vides** → Cause inconnue  
   État : Défaut global probable ou cas exceptionnel ? À différencier.

### Stale issues
- Lupo reporté au 31 août (?) → Pas de clarté sur le status actuel.
- M5 vs Lupo/Assiette vs Esneux/iPhone : Quelle est la différence d'instance HA ? Non documentée.

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Implication |
|----------|-----------|------------|
| "Pourquoi tu ne peux pas travailler dans le terminal RPi ?" | 2x | Procédure SSH/accès non formalisée |
| "C'est quoi le ZH ?" | 1x relevée, probablement plus | Terminologie métier manquante |
| "C'est quoi L(M) ?" | 1x | Format/notation non documentée |
| "C'est quoi les states files ?" | 1x | Concept Home Assistant non vulgarisé |
| "Pourquoi vanroll test ne donne plus de données ?" | 2x+ | Pas de run-book de dépannage |
| "Comment faire en sorte que tu gardes en mémoire les procédures ?" | 1x relevée | Architecture de mémoire/prompting insuffisante |
| "TTL 24h, comment l'utiliser avec fluidité en HTML ?" | 1x | Documentation intégration API incomplète |
| "Quelle est la différence entre instance Lupo/Assiette et Esneux/iPhone ?" | 1x | Cartographie des instances HA absent |
| "Est-ce que cette instruction existe et si oui pourquoi ne l'a-t-elle pas été exécutée ?" | 1x | Traçabilité des exécutions (audit trail) manquante |

**Verdict** : 9 catégories de questions fondamentales sans réponse stable. Chacune génère de la friction à chaque session. **C'est du travail répété**.

---

## Nouveaux patterns détectés

1. **Bifurcation non-fermée sur expertise externe**  
   JCH interroge un expert externes, reçoit un commentaire détaillé sur LLM + Ollama pour RPi 5, mais la session continue sans validation/implémentation claire du conseil.  
   → Pattern : Expert advice → inintégré.

2. **Mélange projet/infra/ops dans même session**  
   - Vetalyx (projet Belgique, levée chinoise 40%, droit des sociétés)
   - Lupo/Assiette (infrastructure RPi 5 + NVMe + batterie)
   - Home Assistant (orchestration temps-réel)  
   - Screenshots inbox (workflow doc)  
   
   Zéro séparation contexte → Switching tax énorme.

3. **Grep/shell comme outil de dépannage par défaut**  
   JCH + Claude = composition automatique de `grep_files`, `exec_shell`, `read_file`, `list_dir`.  
   Utile mais : **pas d'archivage des diagnostics effectués**. À chaque nouveau problème, diagnostic from scratch.

4. **Escalade partenaire comme blocage tacite**  
   "Je vais en discuter avec Alain Bosseloir et je te reviens" = fin de sujet sans deadline ni trace.  
   → Décisions floues, follow-up jamais garanti.

5. **Inbox/Sites comme hub central improvisé**  
   Screenshots, fiches, procédures tous convergeant vers `JCH_Inbox/00_INBOX/` et dérivés.  
   Pas de taxonomie claire → risque de perte/doublon.

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Claude + grep/shell combo** : Récupération rapide d'infos d'infra (IPs, configs, fichiers).
- **Escalade expert (Alain)** : Reconnaître quand consulter au lieu de boucler.
- **Arrêt volontaire ("on tourne en rond")** : Éviter l'impasse infinie.
- **Multi-outil orchestration** : DeepSeek TUI + Claude Code + Codex CLI = flexibilité.

### ❌ Inefficacités
- **Redémarrage diagnostic à chaque session** : Zéro capitalisation d'investigation.
- **Mélange contexte projet/infra** : Switching tax ~30-40% par session.
- **Questions récurrentes non documentées** : Même lacune investigée 5+ fois.
- **Fiches vides (Dante)** : Pas de validation de données upstream.
- **État Lupo flou** : "Reporté 31 août" → Est-ce fait ? Bloqué ? Annulé ?
- **TTL 24h sans pattern d'usage** : Info donnée, pas d'appliqué.
- **Escalade partenaire sans deadline** : Suspension ouverte, aucune prise en charge asynchrone.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Critiques à résoudre avant poursuite
1. **Partition NVMe corrompue (nvme0n1p5 SQUASHFS)** → Besoin recréation/repair urgent. Lupo est blind jusqu'à fix.
2. **Terminal RPi inaccessible** → Tester SSH, vérifier firewall, check service. Diagnostic complet manquant.
3. **Fiches Dante vides** → Différencier bug global vs cas isolé. Impact : validation qualité de Vetalyx.

### 🟠 À intégrer en priorité
4. **Terminologie formalisée** : ZH, L(M), states files, TTL usage patterns → Mini-glossaire dans AGENTS.md.
5. **Cartographie instances HA** : Lupo/Assiette vs Esneux/iPhone vs M5. Schéma network + rôles.
6. **Procédure accès RPi** : SSH config, creds, fallback. Codifier plutôt que redéboguer.

### 🟡 À documenter
7. **Diagnostic archive** : Chaque `exec_shell` + `grep_files` → sauvegarde dans `JCH_Inbox/DIAGNOSTICS/` avec timestamp.
8. **Follow-up partenaire Alain** : Créer ticket explicite avec deadline (format : `WAITING_ON_ALAIN_BOSSELOIR_DUE_YYYY-MM-DD`).
9. **Vetalyx legal + tech** : Séparer sessions projet / infra. Trop de context-switch.

### 🟢 À réutiliser
10. **Expert review + integration loop** : Avis reçu d'expert sur LLM Ollama → exécuter plan recommandé, tracer dans CLAUDE.md.

---

## Recommandations

### Immédiat (< 24h)
1. **Créer diagnostic.md** (template) pour capturer les outputs `exec_shell` + analyses. Stocker systématiquement.
2. **Fix NVMe Lupo** : Reproduire erreur SQUASHFS, tenter mount avec options alternates ou recréer partition. Critique.
3. **Audit Vanroll API** : Vérifier endpoint, auth, rate limits. Une requête, une exécution, une trace.

### Court terme (1 semaine)
4. **Glossaire technique** : ZH, L(M), states files, TTL patterns, Vetalyx market terms → Fichier `GLOSSARY.md` dans `wiki/`.
5. **Cartographie HA instances** : Fichier YAML ou markdown avec :
   - Nom instance, IP locale, rôle (main/backup/dev), config manager, status.
   - Différences M5 vs Lupo vs Esneux.
6. **Run-book RPi access** : Doc procédurale complète : SSH config, creds (from `JCH_PRIVATE/credentials-central.md`), fallback (VNC, serial).

### Moyen terme (2-3 semaines)
7. **Séparation contexte PKA** : 
   - Sessions **Projets** (Vetalyx legal, produits, market) → Lundi/mercredi.
   - Sessions **Infra** (RPi, HA, network) → Mardi/jeudi.
   - Buffer workflows (inbox, screenshots) → Async.
8.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 25
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 25
- **Taux : 0.0%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 194.1
- Échanges/session début fenêtre : 74.4
- Tendance globale : 160.9%
- Tendance 3j-3j : 443.5%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Approche interrogative avant action** : Poser des questions polies aux utilisateurs/partenaires pour comprendre avant d'implémenter (pattern récurrent
- [Decision] Choix du niveau iPhone disponible** : Sélectionner le niveau d'API/SDK existant sur iOS plutôt que de demander une installation manuelle unitaire.
- [Decision] Abandon de la fixation individuelle de facteurs** : Ne pas exiger la fixation manuelle de paramètres ; créer une forme sphérique par défaut (décision 
- [Decision] Documentation forcée** : Créer un fichier `.md` pour documenter la situation actuelle et les échecs.
- [Decision] Finalisation des fiches validées** : Marquer comme complètes et passer à la phase suivante.
- [Decision] Migration vers les screenshots inbox** : Basculer le flux de travail vers `inbox/sites` pour les captures d'écran.
- [Decision] Procedure spots de stationnement** : Créer une procédure dédiée pour les fiches "spots" (parking/stationnement).
- [Decision] Escalade partenaire Alain Bosseloir** : Reporter certaines décisions après discussion avec le partenaire stratégique.
- [Decision] Essai de solution** : Approuver une tentative ("oui on va essayer") sans préjugé du résultat.
- [Decision] : Beaucoup de micro-décisions, peu de décisions stratégiques formalisées. Trop de "on va" sans trace écrite de *pourquoi*.
- [Failure] → `duplicate_os_install`
- [Failure] → SSL/TLS handshake failure
- [Failure] → `/mnt: fsconfig() failed`
- [Failure] → Username/pass non fonctionnels
- [Failure] État : Endpoint disparu ou URL malformée. Pas d'URL citée → diagnostic impossible.
- [Failure] État : Requête récurrente mais non résolue. Besoin d'investigation sur l'API Vanroll.
- [Failure] → Raison non documentée
- [Failure] AppManager.install bloqué** → `duplicate_os_install`
- [Failure] Connexion sécurisée échouée** → SSL/TLS handshake failure
- [Failure] Erreur SQUASHFS superblock** → `/mnt: fsconfig() failed`
- [Failure] Authentification Google Keyword défaillante** → Username/pass non fonctionnels
- [Failure] Erreur 404 sur endpoint inconnu
- [Failure] Vanroll Test ne retourne plus de données
- [Failure] Terminal RPi inaccessible** → Raison non documentée
- [Failure] Fiches Dante vides** → Cause inconnue

### Fréquence des patterns (14 jours)
- **Failure** : 2 jours, 14 occurrences
- **Question** : 2 jours, 13 occurrences
- **Recurring question** : 2 jours, 11 occurrences
- **Decision** : 1 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 25
- Jours d'observation : 2
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**413** recommandations au total — **413** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 369
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5

### Plus récentes ouvertes

- [id=411] (2026-09-25) **Furet** : Créer diagnostic.md** (template) pour capturer les outputs `exec_shell` + analys
- [id=412] (2026-09-25) **Dobby** : Fix NVMe Lupo** : Reproduire erreur SQUASHFS, tenter mount avec options alternat
- [id=413] (2026-09-25) **Dobby** : Audit Vanroll API** : Vérifier endpoint, auth, rate limits. Une requête, une exé
- [id=398] (2026-09-09) **Dobby** : Immédiat (avant session suivante)
- [id=399] (2026-09-09) **Dobby** : Déclarer Lupo-RPI morte

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

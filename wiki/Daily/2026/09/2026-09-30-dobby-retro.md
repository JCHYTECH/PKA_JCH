---
date: 2026-09-30
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1044
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-30

**Sessions analysées :** 2 | **Échanges :** 1044 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Session 2026-09-30 — Dobby PKA

## Décisions prises

1. **Test en live du système LUPO-RPI** : "on va tester en life et je te reviens"
   - Décision de valider la configuration matérielle sur le terrain avant itération suivante
   - Implique : redémarrage du LUPO-RPI seul pour validation de bootstrap complet

2. **Documentation des fiches vides** : Création de fichiers `.md` pour tracer les échecs
   - Formalisation de la procédure de documention post-mortem
   - Engagement : expliquer la situation, l'échec actuel et les pistes testées

3. **Escalade Vetalyx Belgique** : Discussion avec partenaire Alain Bosseloir
   - Contexte : entrée du capital chinois (40% via DIaho) sans personnel chinois opérationnel
   - Question reportée : obligation déclarative vs. structure légale

4. **Attente positionnement des autres parties** : "P2 on va attendre la position des autres"
   - Suspension délibérée de décisions multi-parties en attente de feedback

5. **Recherche infrastructure Ombrie** : Lancement d'une requête de recherche sur locations exotiques
   - Rattachement au projet VETALYX (expansion géographique)

---

## Échecs ouverts / bloqueurs

### Critiques (système bloqué)

| Bloqueur | Impact | Statut |
|----------|--------|--------|
| **RPi 5 : blocage phase d'initialisation matérielle** | Impossible de booter le système ; hardware apparemment détecté mais pas de progression | Ouvert — nécessite debug de la séquence HAT/SSD NVMe |
| **Home Assistant : erreur `duplicate_os_install`** | `AppManager.install` bloqué ; détecte instance HA fantôme sur même réseau/disque | Ouvert — cause probable : restauration de sauvegarde sans cleanup réseau |
| **Authentification Google Keyword : credentials invalides** | Username/password venant de Google Keyword ne fonctionne pas | Ouvert — à investiguer : expiration token / mauvaise source |

### Secondaires (dégradés)

- **LUPO hardware presque complet** : reste à ajouter SD "endurance" + silent blocs RPi (planning : 31 août, décalé)
- **Secure connection failure** : erreur SSL/TLS non contextualisée dans le transcript
- **Fiches de projet vides** (Dante) : pas de cause identifiée ; pattern systémique inconnu

---

## Questions récurrentes (signe de lacunes documentaires)

### Top 5 — Inefficacité cognitive

1. **"C'est quoi la synthèse de lecture propre ?"** (appears 2x)
   - **Lacune** : pas de définition partagée d'une "synthèse" ; variabilité d'interprétation
   - **Recommandation** : créer glossaire projet dans `CLAUDE.md` ou `AGENTS.md`

2. **"L(M)" et notation technique récurrente**
   - **Lacune** : notations abrégées non documentées
   - Exemple : `L(M)` = ? ; `ZH` = ? ; distinction 4-roues vs petit + avant/arrière

3. **Différence `LUPO/assiette` vs `Esneux/iPhone` — c'est l'instance HA ?**
   - **Lacune** : topologie du système pas clairement documentée
   - Implique confusion : architectures locales vs. instances de supervision vs. déploiements
   - **Coût** : chaque clarification = round-trip dialog

4. **"Pourquoi vanroll test ne donne plus de données ?"**
   - Suggère monitoring/alerting insuffisant
   - Pas de SOP pour diagnostic de « perte de signal »

5. **"State files" (LUPO, 31 août)** + **"Pourquoi le tiroir 25-26 cm ?"**
   - Documentation hardware/logique matériel inexistante
   - Raisonnement implicite non partagé (contrainte mécanique / électrique / UX)

---

## Nouveaux patterns détectés

### 1. **Multi-contexte mélangés dans une session**
- Infrastructure IoT (RPI, LUPO, HA)
- Juridique/compliance (Vetalyx Belgique, Chinese capital ownership)
- Recherche géographique (Ombrie)
- LLM optimization (Ollama, quantization Q4_K_M)

⚠️ **Signal** : JCH jongle entre domaines sans cloisonnement. Risque de décision hâtive ou d'oubli.

### 2. **Expertise externe importée mais non consolidée**
- "J'ai interrogé un expert qui me donne ceci..." (Modèles LLM pour RPi 5)
- Knowledge en vrac, non intégré à AGENTS.md / workflow
- Questions post-expert = JCH doit réapprendre à chaque session

### 3. **Procédures verbales → fiction documentaire**
- "Met moi le chemin des fichiers à encore validé ?"
- "Rappelle-moi si on avait aussi [feature X]"
- **Implication** : mémoire partagée intra-session seulement. Inter-session = régression.

### 4. **Erreurs d'ordre de magnitude non capturées**
- "Observe l'importance de ton erreur : un facteur 3. Cela peut tuer une décision sur un projet"
- Pas de trace post-mortem → risque de répétition
- Besoin : formulaire structuré "Leçons apprises + seuil d'escalade"

### 5. **Accumulation de cas d'usage HA mal isolés**
- Duplicate OS install
- TTL 24h + HTML button avec state
- Config permanente vs. instance active
- **Diagnostic** : HA = black box pour JCH ; besoin d'une SOP/runbook centralisé

---

## Efficacités / Inefficacités

### ⚡ Efficacités observées

| Aspect | Evidence |
|--------|----------|
| **Réactivité escalade** | Décision "on va discuter avec Alain" vs. débat interne = fast-track décision multi-parties |
| **Triage clair** | "Fiches validées finalise" → acceptation de sous-tâches isolées |
| **Test en conditions réelles** | "On va tester en life" = pragmatisme ; évite cycles de spec infinies |
| **Utilisation multi-outil appropriée** | DeepSeek pour debug infra, Claude pour stratégie/docs, Codex pour CLI |

### 🔴 Inefficacités critiques

| Aspect | Coût estimé | Cause racine |
|--------|-------------|--------------|
| **Répétition Q-R sur definitions (synthèse, L(M), ZH)** | 15-20 min/session × 2+ répétitions | Pas de glossaire centralisé ; notation projet non normed |
| **Escalade tardive de bloqueurs matériel** | Unknown (RPi 5 stuck depuis ?) | Pas de SLA/escalation timeline ; on "tourne en rond" |
| **Fiches vides (Dante) = analyse reactive** | 10-15 min debug | Pas de validation schema a priori ; découverte tardive |
| **Credentials invalides Google Keyword** | Bloqueur direct | Pas de secret rotation / audit trail |
| **Contexte switch mental** | 30+ min (Vetalyx Belg → IoT → LLM optimization) | Working set trop large pour une session |

### 🔁 Pattern inefficace : "Tourne en rond"

Mention explicite : **"on va arreter là. on tourne en rond"**
- Signe : absence de decision point claire / critères de go/no-go
- Symptôme : itération sans feedback externe (attente du "test en life")
- Remède : créer **decision matrix** (go/no-go + escalation owners)

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Priorités critiques

1. **LUPO-RPI blocage initialisation**
   - État : En test "live" depuis ~2026-09-30
   - Action requise : Feedback post-test + analyse SSD/HAT si blocage persiste
   - Owner : JCH (test), escalade → expert hardware si >3 jours sans progression
   - Risque : Cascade sur calendrier LUPO final

2. **Home Assistant duplicate_os_install**
   - Cause probable : Instance fantôme post-restauration sauvegarde
   - Remedy : Network scan + UUID check disques ; cleanup si nécessaire
   - Owner : Dobby/system admin
   - Lié à : Vetalyx infra → priorité haute

3. **Google Keyword credentials expiration**
   - Impact : Blocage accès automation secrets
   - Action : Audit secret rotation policy + refresh credentials
   - Owner : JCH PRIVATE
   - Dépendance : aucune (isolé) mais marque hygiene technique

### 📋 Documentation urgente

| Artefact | Contenu | Audience |
|----------|---------|----------|
| **GLOSSAIRE_PROJET.md** | Synthèse de lecture, L(M), ZH, state files, LUPO/assiette vs HA instance, etc. | Team + Dobby |
| **HA_RUNBOOK.md** | Procédures : backup/restore sans duplicate_os, TTL config, state management | JCH + Renard (ops) |
| **VETALYX_TOPOLOGIE.md** | Architectures : locations, instances, IP ranges, configurations par site | Renard (lead) |
| **POST_MORTEM_TEMPLATE.md** | Facteur 3 error → leçons, seuil escalade, owner | Team |

### 🔄 Processus à installer

1. **Pre-session : Context narrow**
   - Agenda par domaine (IoT / Legal / Infra) avec time-box
   - Évite context switch pathologique

2. **Intra-session : Decision checkpoint**
   - Toutes les 30 min : "Décision prise ? Escalade ? Défer ?"
   - Empêche "tourner en rond"

3. **Post-session : Action items → Wiki**
   - Status pour chaque bloqueur (open/awaiting/resolved)
   - Owner + deadline explicite

4. **Notation technique standardisée**
   - Exporter liste de notations de AGENTS.md/CLAUDE.md
   - Passer dans un formulaire de validation avant utilisation cross-context

---

## Recommandations

### Immédiat (48h)

1. ✅ **Capture résultat test LUPO-RPI en live**
   - Fichier : `JCH_Inbox/03_PROJECTS/11_IOT/LUPO/2026-09-30_test-results.md`
   - Format : Test observations + go/no-go + next steps

2. ✅ **Démarrer cleanup HA duplicate_os**
   - Scan réseau : `arp -a | grep -E "(192.168|M5|RPi)"`
   - Check UUIDs disques + backup logs
   - Créer SOP : "Restore HA cleanly"

3. ✅ **Créer GLOSSAIRE_PROJET.md**
   - 5 définitions min : synthèse, L(M), ZH, state files, LUPO/assiette
   

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 29
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 26
- **Taux : 10.3%**

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

- [Decision] : "on va tester en life et je te reviens
- [Decision] Décision de valider la configuration matérielle sur le terrain avant itération suivante
- [Decision] Implique : redémarrage du LUPO-RPI seul pour validation de bootstrap complet
- [Decision] : Création de fichiers `.md` pour tracer les échecs
- [Decision] Formalisation de la procédure de documention post-mortem
- [Decision] Engagement : expliquer la situation, l'échec actuel et les pistes testées
- [Decision] : Discussion avec partenaire Alain Bosseloir
- [Decision] Contexte : entrée du capital chinois (40% via DIaho) sans personnel chinois opérationnel
- [Decision] Question reportée : obligation déclarative vs. structure légale
- [Decision] : "P2 on va attendre la position des autres
- [Decision] Suspension délibérée de décisions multi-parties en attente de feedback
- [Decision] : Lancement d'une requête de recherche sur locations exotiques
- [Decision] Rattachement au projet VETALYX (expansion géographique)
- [Decision] Test en live du système LUPO-RPI** : "on va tester en life et je te reviens
- [Decision] Documentation des fiches vides** : Création de fichiers `.md` pour tracer les échecs
- [Decision] Escalade Vetalyx Belgique** : Discussion avec partenaire Alain Bosseloir
- [Decision] Attente positionnement des autres parties** : "P2 on va attendre la position des autres
- [Decision] Recherche infrastructure Ombrie** : Lancement d'une requête de recherche sur locations exotiques
- [Failure] | Impossible de booter le système ; hardware apparemment détecté mais pas de progression | Ouvert — nécessite debug de la séquence HAT/SSD NVMe |
- [Failure] | `AppManager.install` bloqué ; détecte instance HA fantôme sur même réseau/disque | Ouvert — cause probable : restauration de sauvegarde sans cleanup
- [Failure] | Username/password venant de Google Keyword ne fonctionne pas | Ouvert — à investiguer : expiration token / mauvaise source |

### Fréquence des patterns (14 jours)
- **Recurring question** : 5 jours, 15 occurrences
- **Failure** : 4 jours, 14 occurrences
- **Question** : 4 jours, 18 occurrences
- **Decision** : 3 jours, 27 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 21
- Jours d'observation : 6
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**449** recommandations au total — **449** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 404
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=441] (2026-09-30) **Dobby** : ✅ **Capture résultat test LUPO-RPI en live
- [id=442] (2026-09-30) **Dobby** : Fichier : `JCH_Inbox/03_PROJECTS/11_IOT/LUPO/2026-09-30_test-results.md`
- [id=443] (2026-09-30) **Dobby** : Format : Test observations + go/no-go + next steps
- [id=444] (2026-09-30) **Dobby** : ✅ **Démarrer cleanup HA duplicate_os
- [id=445] (2026-09-30) **Dobby** : Scan réseau : `arp -a | grep -E "(192.168|M5|RPi)"`

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

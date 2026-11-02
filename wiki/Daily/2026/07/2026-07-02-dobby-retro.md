---
date: 2026-07-02
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1283
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-02

**Sessions analysées :** 4 | **Échanges :** 1283 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS JCH - 2026-07-02

## Décisions prises

1. **Migration vers OpenRouter** : abandon de l'achat de crédits Claude/DeepSeek individuels → centralisation via OpenRouter pour réduire la gestion des clés API
2. **Déploiement HA + Zigbee** : arrêt du M5, basculement sur Home Assistant avec dongle Zigbee comme hub domotique
3. **Choix du broker MQTT** : question ouverte mais pas finalisée ("je choisis quel mqtt ?")
4. **Synchronisation Vetalyx** : départ prévu 25/07 à 15:00 depuis Namu, travail sur l'analyse marché Chine documentée
5. **Gestion des projets bioacoustiques** : décision de créer un fork dédié pour isoler les travaux sur les plantes

**⚠️ Problème détecté** : plusieurs décisions sont restées partiellement articulées ou sans validation finale (MQTT non tranché, OpenRouter partiellement intégré)

---

## Échecs ouverts / bloqueurs

### 🔴 Critiques
1. **Crash Outlook + restauration incomplète** : perte de contexte, travail partiellement perdu, sans plan de secours visible
2. **Fonction launcher OpenRouter dysfonctionnelle** : erreur après clic, utilisateur bloqué sur l'utilisation en VS Code
3. **Arduino CLI installation échouée** : lien documenté mais exécution non aboutie
4. **Erreur 6683 récurrente** : non expliquée, requiert clarification technique
5. **Traceback Python** : script `/Users/jchavauxm5/PKA_JCH/...` en erreur, débuggage inachevé

### 🟡 Secondaires
1. **Installation HACS incomplète** : demande restée sans résolution ("comment installer tout cela")
2. **Références produits AliExpress non validées** : liens fournis sans vérification si compatible avec ESP32-S3 + OV5640
3. **Sauvegarde travail "plantes"** : signalée comme nécessaire mais non exécutée avant fork

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Interprétation |
|----------|-----------|----------------|
| `.venv` c'est quoi ? / `.env` vs `.venv` | 3× | **Lacune majeure** : virtualenv Python non documenté pour l'équipe |
| Harness, c'est quoi ? | 2× | Concept technique (test harness ?) jamais clarifié |
| Memory nudge ? | 2× | Jargon système Dobby opaque pour JCH |
| Comment connecter VS Code à OpenRouter ? | 2× | **Blocage UX** : workflow non standardisé |
| Terminal VS Code vs terminal natif ? | 2× | Confusion shells/environnements non adressée |
| Comment intégrer Apple Notes au PKA ? | 2× | Processus d'ingestion data incomplet |
| X1201-C1 : quel composant exactement ? | 1× | Documentation matériel manquante (SSD connector ?) |

**Recommandation immédiate** : créer un `FAQ_ONBOARDING.md` avec glossaire (`.venv`, harness, nudge, MQTT basics)

---

## Nouveaux patterns détectés

### 1. **Mode "Question-Réponse sans Closure"**
JCH pose une question, reçoit une réponse, ne valide pas, continue. Exemple : "je choisis quel mqtt ?" → pas de décision tracée → revient implicitement plus tard.

**Impact** : accumulation de décisions semi-faites, plus tard = rediscussions.

### 2. **Alternance outils sans transition claire**
- Deepseek TUI → Claude Code → Codex CLI → OpenRouter
- Chaque switch sans documenter **pourquoi** (contexte insuffisant ? limitation détectée ?)
- Travaux fragmentés entre outils → perte de continuité

### 3. **Documentation "in-flight" incomplète**
- Transcripts de recherche Kimi 2.5 sur PKA système non sauvegardés formellement
- Analyses pharmaceutiques (Virbac, hydrocortisone) en réponses libres, pas de `.md` final
- Résultat : même info re-demandée 3 sessions plus tard

### 4. **Projets actifs trop nombreux** (12 simultanés)
- 4 en "plein régime", 4 en cours, 4 en veille
- JCH jongle sans système de priorité visible
- Symptôme : "je vais le faire manuellement" (frustration, abandon d'automatisation)

### 5. **Dépendance matérielle mal cartographiée**
- ESP32-S3 + OV5640 : constraints techniques complexes, documentées en réponse, pas en schéma préalable
- M5 arrêté/relancé plusieurs fois
- RPi/RPI/Raspberry Pi utilisés de manière interchangée (typos ?) → imprécision

---

## Efficacités / inefficacités

### ✅ Forces
1. **Dobby capture bien les patterns** : 1283 échanges synthétisés en structure cohérente
2. **Utilisation multi-modèle pertinente** : DeepSeek pour code, Claude pour analyse, Deepseek TUI comme orchestrateur → choix rationnel
3. **PKA système ~18 Go maintenu** : infrastructure lourde mais stable (health-check RED ≠ down complet)
4. **Équipe DB robuste** : 32 membres (31 spécialistes + Dobby) → scaling possible

### ❌ Frictions majeures
1. **Pas d'issue tracking** : décisions en dialogue libre, aucune traçabilité type GitHub Issues
2. **Contexte oublié entre sessions** : JCH doit re-demander "comment OpenRouter VS Code" → memory nudge insuffisant
3. **Code snippets générés jamais sauvegardés** : solutions (Arduino CLI, MQTT config) perdues après session
4. **Absence de runbooks** : "je vais le faire manuellement" revient trop souvent (Outlook, HACS, launcher)
5. **Nomenclature instable** : DeepSeek-TUI = CodeWhale (renommage non annoncé ?), M5/ESP32 confused, RPi/RPI typos

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Contexte actif (à restaurer immédiatement)
- **OpenRouter partiellement intégré** : launcher non fonctionnel → priorité FIX avant de l'utiliser largement
- **Migration HA/Zigbee en cours** : M5 arrêté, validation de la config manquante
- **Vetalyx marché Chine** : départ 25/07, analyse à finaliser avant cette date
- **Travail "plantes"** : fork du projet bioacoustique à créer (blocage fork = blocage commit)

### 📋 Dettes techniques
1. Erreur 6683 (MQTT ? OpenRouter ?) non expliquée
2. Arduino CLI installation incomplete
3. HACS setup à terminer
4. Outlook crash recovery : vérifier perte données
5. Traceback Python dans PKA_JCH (quel script ?)

### 🗂️ Références projet
- **Entités clés** : Wildnexus (19 mentions), Vetalyx (25 mentions), Home Assistant (13)
- **Machines** : M1 (26 mentions = machine dev principale), M5 (29 mentions = ancien hub ?), RPi (18, en déploiement)
- **Modèles actifs** : deepseek-v4, deepseek-v4-pro

### 💾 Données à préserver
- Analyse Kimi 2.5 du PKA système (18 Go, 12 projets, dérives 🔴)
- Recherches pharma (Virbac, Cortavance, Easotic)
- Constraints ESP32-S3 + OV5640 (24-pin DVP, GPIO limités)
- Config HA + Zigbee (dongle model ? pinouts ?)

---

## Recommandations

### 🚨 URGENT (avant session suivante)

1. **Fixer OpenRouter launcher** → tester en VS Code, valider UX
2. **Documenter erreur 6683** → grep logs, identifier source (MQTT ? API ?)
3. **Créer `DECISIONS.md`** : matrice (Date | Sujet | Décision | Statut | Propriétaire | Deadline)
   - Exemple : `2026-07-02 | MQTT broker | ? | OPEN | JCH | 2026-07-05`
4. **Sauvegarder snippets session** :
   - Code Arduino CLI (complet)
   - Config HACS
   - OpenRouter integration (VS Code)
   - Tout dans `docs/solutions/`

### 📖 SHORT TERM (1-2 sessions)

5. **Créer `FAQ_ONBOARDING.md`** avec glossaire :
   ```
   - .venv : dossier virtualenv Python, isolé par projet
   - .env : fichier secrets (clés API), à .gitignore
   - Harness : framework de test (Arduino ? pytest ?)
   - Memory nudge : rappel IA de contexte passé (Dobby feature)
   - MQTT : protocole IoT pub/sub (remplace HTTP pour HA)
   ```

6. **Standardiser nomenclature** :
   - DeepSeek-TUI **OU** CodeWhale ? (choisir + annoncer)
   - ESP32 vs M5 vs RPi : matrice comparatif dans wiki
   - Utiliser issue labels : `[BLOCKED]`, `[WAITING]`, `[DECISION]`

7. **Implémenter runbooks** pour tâches répétées :
   - `runbook/HACS_install.md`
   - `runbook/OUTLOOK_restore.md`
   - `runbook/OPENROUTER_setup.md`

### 🔄 MEDIUM TERM (3-4 sessions)

8. **Prioriser projets** : 12 actifs = trop. Créer matrice impact/effort, garder ~4 prioritaires
9. **Intégrer Apple Notes → PKA** : script d'ingestion (curl vers API Notes ?)
10. **Auto-close décisions non finalisées** : "MQTT : décision par 2026-07-08, sinon PostgreSQL par défaut"
11. **Audit matériel** : valider compatibilité ESP32-S3 + OV5640 avant commande, générer schéma pinout

### 🤖 DOBBY SYSTEM

12. **Améliorer memory nudge** :
    - Ajouter auto-inject au début de session : "Contexte restauré : OpenRouter launcher broken, Vetalyx deadline 25/07, plantes fork pending"
    - Tracker "unresolved" en rouge visible

13. **Monitorer health-check faux positifs** : 🔴 RED causé par bruits → réduire seuil ou filtrer

---

## Verdict final

**État du système PKA JCH : Fonctionnel mais Désorganisé**

✅ **Capacités techniques présentes** (multi-modèles, infrastructure 18 Go, équipe 32)  
❌ **Processus fragile** (pas de

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 40
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 38
- **Taux : 5.0%**

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

- [Decision] : abandon de l'achat de crédits Claude/DeepSeek individuels → centralisation via OpenRouter pour réduire la gestion des clés API
- [Decision] : arrêt du M5, basculement sur Home Assistant avec dongle Zigbee comme hub domotique
- [Decision] : question ouverte mais pas finalisée ("je choisis quel mqtt ?")
- [Decision] : départ prévu 25/07 à 15:00 depuis Namu, travail sur l'analyse marché Chine documentée
- [Decision] : décision de créer un fork dédié pour isoler les travaux sur les plantes
- [Decision] : plusieurs décisions sont restées partiellement articulées ou sans validation finale (MQTT non tranché, OpenRouter partiellement intégré)
- [Decision] Migration vers OpenRouter** : abandon de l'achat de crédits Claude/DeepSeek individuels → centralisation via OpenRouter pour réduire la gestion des cl
- [Decision] Déploiement HA + Zigbee** : arrêt du M5, basculement sur Home Assistant avec dongle Zigbee comme hub domotique
- [Decision] Choix du broker MQTT** : question ouverte mais pas finalisée ("je choisis quel mqtt ?")
- [Decision] Synchronisation Vetalyx** : départ prévu 25/07 à 15:00 depuis Namu, travail sur l'analyse marché Chine documentée
- [Decision] Gestion des projets bioacoustiques** : décision de créer un fork dédié pour isoler les travaux sur les plantes
- [Failure] : perte de contexte, travail partiellement perdu, sans plan de secours visible
- [Failure] : erreur après clic, utilisateur bloqué sur l'utilisation en VS Code
- [Failure] : lien documenté mais exécution non aboutie
- [Failure] : non expliquée, requiert clarification technique
- [Failure] : script `/Users/jchavauxm5/PKA_JCH/...` en erreur, débuggage inachevé
- [Failure] Crash Outlook + restauration incomplète** : perte de contexte, travail partiellement perdu, sans plan de secours visible
- [Failure] Fonction launcher OpenRouter dysfonctionnelle** : erreur après clic, utilisateur bloqué sur l'utilisation en VS Code
- [Failure] Arduino CLI installation échouée** : lien documenté mais exécution non aboutie
- [Failure] Erreur 6683 récurrente** : non expliquée, requiert clarification technique
- [Failure] Traceback Python** : script `/Users/jchavauxm5/PKA_JCH/...` en erreur, débuggage inachevé

### Fréquence des patterns (14 jours)
- **Failure** : 7 jours, 47 occurrences
- **Decision** : 6 jours, 39 occurrences
- **Question** : 6 jours, 23 occurrences
- **Recurring question** : 6 jours, 22 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 21
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**191** recommandations au total — **191** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 159
- **Forge** : 27
- **Corbeau** : 3
- **Furet** : 2

### Plus récentes ouvertes

- [id=184] (2026-07-02) **Dobby** : Fixer OpenRouter launcher** → tester en VS Code, valider UX
- [id=185] (2026-07-02) **Dobby** : Documenter erreur 6683** → grep logs, identifier source (MQTT ? API ?)
- [id=186] (2026-07-02) **Dobby** : Créer `DECISIONS.md`** : matrice (Date | Sujet | Décision | Statut | Propriétair
- [id=187] (2026-07-02) **Dobby** : Exemple : `2026-07-02 | MQTT broker | ? | OPEN | JCH | 2026-07-05`
- [id=188] (2026-07-02) **Dobby** : Sauvegarder snippets session** :

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🔴 $1.06 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $1.06**

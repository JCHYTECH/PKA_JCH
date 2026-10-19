---
date: 2026-10-01
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1198
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-01

**Sessions analysées :** 3 | **Échanges :** 1198 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 Rétrospective PKA - Sessions du 2026-10-01

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| Approche progressive pour LUPO | Poser des questions polies avant action | En cours |
| Fiches validées finalisées | Clôture des templates de fiches | ✅ Fermé |
| Simulations avant déploiement | Tester en environnement contrôlé avant production | Pending validation |
| Procédure "fiches spots" | Créer un mécanisme de parking des données non-fixables | À définir |
| Test en live après simulations | Valider sur environnement réel | Planifié |
| Discussion avec Alain Bosseloir | Escalade stratégique pour décisions complexes | À scheduler |
| Créer fichier .md de synthèse | Documenter les points de rotation circulaire | ✅ À générer |

**Problème détecté** : Les décisions sont très fragmentées et manquent de propriétaire explicite. 7 décisions en 3 sessions = 2.3/session. Très peu ont des dates cibles claires.

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent le travail)
1. **Conflit d'instances Home Assistant**
   - Erreur : `duplicate_os_install` / présence d'instance fantôme
   - Impact : `AppManager.install` bloqué, système "unhealthy"
   - Cause probable : Restauration de sauvegarde sans nettoyage des UUID/identifiants
   - Action requise : Scanner le réseau pour détecter instances dupliquées + nettoyer les UUID disque

2. **API Key manquante en HA**
   - Erreur : "API key required" pour le module `cap`
   - Contexte : Van à niveau "off", CAP non fonctionnel
   - Impact : Authentification cassée, bloque les tests

3. **PSU/HAT Geekworm mal configuré**
   - Paramètre incorrect : `PSU_MAX_CURRENT=5000` suspecté
   - Impact : Risque de shutdown inopiné, alimentation instable
   - À vérifier : Datasheet vs. config réelle

### Importants (ralentissent)
4. **LUPO matériel incomplet**
   - Manque : SD endurance + silent blocs RPi
   - Délai : Reporté au 31 août (deadline déjà passée?)
   - Impact : Prototype non itérable

5. **Fiche Dante vide**
   - Symptôme : Une fiche de spécification sans contenu
   - Question ouverte : Bug systémique ou cas isolé?
   - Risque : Incohérence dans la base de fiches

6. **Credentials Google mal intégrées**
   - Erreur : Username/password de Google Keyword ne fonctionnent pas
   - Contexte : Authentification multi-source (Google Auth vs. local)
   - À clarifier : Quel provider utiliser pour Mosquitto?

---

## Questions récurrentes (signe de lacune documentaire)

### Très fréquentes (>3 mentions)
| Question | Fréquence | Indice du problème |
|----------|-----------|-------------------|
| "C'est quoi la synthèse de lecture propre?" | 2× | **Pas de définition formelle, concept flottant** |
| "État des fiches nécessitant review?" | Implicite | **Pas de dashboard/liste centralisée des fiches** |
| "Pourquoi cette erreur HA?" | Itérative | **Modèle mental incomplet de l'infra HA** |
| État de LUPO / architecture matérielle | 4× | **Pas de single source of truth pour le hardware** |
| "Quelle est la différence Lupo/Assiette vs Esneux/iPhone?" | 1× clair | **Instances HA confondues, manque de naming convention** |
| "Qu'est-ce que state files?" | 1× | **Concept HA non intégré** |
| "C'est quoi L(M)?" / "C'est quoi ZH?" | 2× | **Notation non documentée** |

### Problème structurel
**Ces questions reviennent parce que :**
- Pas de glossaire partagé
- Pas de diagramme d'architecture HA actualisé
- Pas de matrice des instances/deployments
- Documentation éparpillée entre Markdown, HA UI, et mémoire

---

## Nouveaux patterns détectés

### Pattern 1 : "Tourne en rond"
JCH reconnaît explicitement : *"on va arreter là. on tourne en rond"*
- Symptôme : Cycles itératifs sans convergence (3 questions → 3 réponses → 3 nouvelles questions)
- Causes : 
  - Manque de définitions amont
  - Pas de critères d'arrêt clairs
  - Contexte fragmenté entre outils

### Pattern 2 : Escalade à la demande
- Les décisions complexes (VETALYX capital, statut légal) → remontées à Alain Bosseloir ou partenaires
- **Bon signe** : reconnaissance des limites
- **Mauvais signe** : Pas de processus d'escalade formalisé (timing flou)

### Pattern 3 : Multi-outils sans synchronisation
Sessions alternent : DeepSeek → Claude Code → Codex CLI
- Chaque session a son propre working set
- Contexte HA fragmenté entre DeepSeek et Claude (cf. extraits confus)
- **Inefficacité** : Résumé local de patterns est lui-même garbled (voir "P2 on va attendre", "P3 = abadvices")

### Pattern 4 : Décisions "en suspens infini"
- "Je te reviens" (4×)
- "On va tester en live" (sans date)
- "Termine pour le moment" = pause, pas fermeture
- **Risque** : Oublis, dégradation de priorité

### Pattern 5 : Erreur 3× en impact décisionnel
JCH cite : *"un facteur 3. cela peut tuer une decision sur un projet"*
- Clair signal : Besoin de validation numérique, pas de "eyeballing"
- Recommandation implicite : Logs de test + métriques = obligatoires

---

## Efficacités / Inefficacités

### ✅ Efficacités
| Pratique | Evidence |
|----------|----------|
| **Consultation d'experts** | Commentaire expert LLM sur Pi 5 bien intégré |
| **Reconnaissance des impasses** | "On tourne en rond" → génère action (fichier .md) |
| **Escalade appropriée** | VETALYX legal → UCM (société de conseil) |
| **Simulation avant prod** | Pattern de testing intentionnel |
| **Questions directes** | JCH pose des questions clairement articulées |

### ❌ Inefficacités
| Pratique | Impact | Sévérité |
|----------|--------|----------|
| **Pas de criteria d'arrêt** | Sessions prolongées sans resolution claire | Haute |
| **Contexte fragmenté** | Résumé local est garbled (cf. "P2 on va attendre P3 = abadvices") | Haute |
| **Pas de single source of truth** | Questions répétées sur architecture HA | Moyenne |
| **Timing flou des escalades** | "Je vais discuter avec Alain" = 0 deadline | Moyenne |
| **Fiches vides (Dante)** | Détecté mais pas root-cause | Basse |
| **Notation non documentée** | L(M), ZH, "synthèse propre" flottent | Basse |

### Ratio
- **Efficacité globale** : ~55% (beaucoup d'intention, mais exécution fragmentée)
- **Taux de résolution** : ~35% (la plupart des sujets restent "en suspens")

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Architecture HA (critique)
- **Instances actuelles** :
  - `lupo/assiette` (RPi 5, 8GB, SSD NVMe + HAT Geekworm)
  - `esneux/iphone` (conflit? autre instance?)
  - Erreur `duplicate_os_install` suggère doublons cachés
- **Problème immédiat** : UUID/identifiants en conflit → nettoyer avant de continuer

### LUPO état réel
- Matériel : Incomplet (SD endurance + silent blocs manquent)
- Deadline : 31 août = **DÉPASSÉE**
- SLM sur Ollama recommandé (quantisé Q4_K_M, pas de full models)

### VETALYX (juridique)
- 40% capital via DIaho (Chine)
- Capital = 10.000€
- **Question ouverte** : Déclaration obligatoire des actionnaires chinois? UCM a répondu (voir extraits)
- **Action** : Relire réponse UCM, formellement documenter la position légale

### Authentification multi-source
- Google Keyword credentials ≠ Mosquitto credentials
- API key manquante en HA (module CAP)
- **Pattern** : Auth fragmentation, à consolider

### Notation/Vocabulaire
- "Synthèse de lecture propre" = **à définir formellement**
- "L(M)" = **à définir**
- "ZH" = **à définir**
- "State files" (HA) = **à documenter**

### Working set prioritaire
- `/JCH_Inbox/03_PROJECTS/08_VETALYX/` (juridique + ops)
- `/JCH_Inbox/03_PROJECTS/11_IOT/` (HA, LUPO, archis)
- `JCH_PRIVATE/credentials-central.md` (auth consolidation)

---

## Recommandations

### 🔴 URGENT (cette semaine)

1. **Nettoyer la polution HA**
   ```
   ACTION: Identifier toutes les instances HA sur le réseau (scanner ARP)
   THEN: Documenter UUID/MAC de chaque instance
   THEN: Supprimer les doublons, nettoyer les sauvegardes orphelines
   OWNER: JCH + expert infra
   DEADLINE: J+3
   ```

2. **Créer matrice instances HA**
   ```markdown
   | Nom | IP | UUID | Rôle | RPi/M5 | État |
   |-----|----|----|------|--------|------|
   | lupo/assiette | ?.?.?.? | xxx | production | RPi 5 8GB | à vérifier |
   | esneux/iphone | ?.?.?.? | yyy | ??? | ??? | ??? |
   ```
   OWNER: JCH
   DEADLINE: J+1

3. **Résoudre API key CAP**
   - Où devrait vivre cette clé? (vault? env?)
   - Format attendu?
   - OWNER: Renard (HA expert mentionné)
   - DEADLINE: J+2

### 🟠 HIGH PRIORITY (cette semaine)

4. **Créer glossaire partagé** (fichier `.md`)
   ```
   - "Synthèse de lecture propre" = [DÉFINITION]
   - "L

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 31
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 29
- **Taux : 6.5%**

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

- [Decision] : Les décisions sont très fragmentées et manquent de propriétaire explicite. 7 décisions en 3 sessions = 2.3/session. Très peu ont des dates cibles cl
- [Failure] Erreur : `duplicate_os_install` / présence d'instance fantôme
- [Failure] Impact : `AppManager.install` bloqué, système "unhealthy
- [Failure] Cause probable : Restauration de sauvegarde sans nettoyage des UUID/identifiants
- [Failure] Action requise : Scanner le réseau pour détecter instances dupliquées + nettoyer les UUID disque
- [Failure] Erreur : "API key required" pour le module `cap`
- [Failure] Contexte : Van à niveau "off", CAP non fonctionnel
- [Failure] Impact : Authentification cassée, bloque les tests
- [Failure] Paramètre incorrect : `PSU_MAX_CURRENT=5000` suspecté
- [Failure] Impact : Risque de shutdown inopiné, alimentation instable
- [Failure] À vérifier : Datasheet vs. config réelle
- [Failure] Conflit d'instances Home Assistant
- [Failure] API Key manquante en HA
- [Failure] PSU/HAT Geekworm mal configuré

### Fréquence des patterns (14 jours)
- **Failure** : 5 jours, 18 occurrences
- **Recurring question** : 5 jours, 15 occurrences
- **Decision** : 4 jours, 27 occurrences
- **Question** : 4 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 14
- Jours d'observation : 7
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**455** recommandations au total — **455** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 410
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=450] (2026-10-01) **Dobby** : Nettoyer la polution HA
- [id=451] (2026-10-01) **Dobby** : Créer matrice instances HA
- [id=452] (2026-10-01) **Dobby** : Résoudre API key CAP
- [id=453] (2026-10-01) **Dobby** : Où devrait vivre cette clé? (vault? env?)
- [id=454] (2026-10-01) **Dobby** : Format attendu?

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

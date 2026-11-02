---
date: 2026-07-13
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1096
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-13

**Sessions analysées :** 2 | **Échanges :** 1096 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective des Sessions du 2026-07-13 - Projet PKA

## Décisions prises

### Infrastructure & Configuration
- **Migration OpenRouter pour Kimi** : abandon des appels directs, passage exclusif par OpenRouter pour standardiser les points d'entrée API
- **Nettoyage PKA confirmé** : suppression des `.bak-*`, vérification des `.DS_Store` restants (8 identifiés), archivage des `session_*.json`
- **Aenova validé comme partenaire CDMO** : 8 sites industriels approuvés pour produits vétérinaires, expertise confirmée pour formulation hydrocortisone aceponate
- **Démarrage en isolation du Lupo-RPi** : reboot sans dépendances externes pour diagnostiquer les points d'entrée

### Outils & Modèles LLM
- **SLM + Ollama pour Raspberry Pi 5 (8 Go)** : recommandation d'expert reçue, modèles quantisés Q4_K_M préconisés
- **Déplacement des ressources plantes vers fork bioacoustique** : création fork projet requise, transfert documenté en attente
- **Memory nudge system** : référencé en standard mais JAMAIS expliqué à l'utilisateur (voir section questions récurrentes)

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent le travail)
1. **Whisper ne fonctionne pas dans VSCode** 
   - Symptôme : erreur non identifiée lors appel fonction
   - Contexte : exécution depuis IDE vs terminal
   - Status : investigation en cours, aucune conclusion

2. **OpenRouter launcher dysfonctionnel**
   - Symptôme : fonction de lancement ne s'exécute pas après clic
   - Erreur affichée : non documentée précisément
   - Impact : interface VS Code inutilisable pour sélection modèles

3. **Accès terminal RPi bloqué**
   - JCH ne peut pas atteindre le shell RPi malgré demandes répétées
   - Alternatives proposées : aucune (situation créant frustration)
   - Dependencies : connaissance réseau RPi insuffisante

### Matériels/Système
4. **Flash Home Assistant OS interrompu**
   - Erreur : `haos_rpi5-15.1.img: No such file or directory`
   - Cause : téléchargement 404 (lien mort ou incomplet)
   - Tentative : `dd` command, récupération image échouée

5. **Conflit UUID Home Assistant détecté**
   - Message d'erreur : ancienne instance détectée sur même réseau/disque
   - Cause probable : clonage disque ou restauration sauvegarde antérieure
   - Résolution : nécessite diagnostic réseau, pas encore effectué

6. **team.db inaccessible**
   - Raison citée : permissions ou chemin invalide
   - Fréquence : question posée 2x
   - Statut : AUCUNE réponse documentée

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Lacune sous-jacente |
|----------|-----------|-------------------|
| `memory nudge c'est quoi ?` | 3x | Concept jamais expliqué, assumé connu |
| `comment utiliser openrouter dans VSCode ?` | 2x | Aucune doc interface VS Code + openrouter |
| `pourquoi (.env) en début de path ?` | 2x | Variables d'environnement mal documentées |
| `whisper ne fonctionne pas, pourquoi ?` | 2x | Pas de guide VSCode vs Terminal distinction |
| `pourquoi pas accès terminal RPi ?` | 3x | Réseau/SSH non documenté, troubleshooting absent |
| `team.db pourquoi inaccessible ?` | 2x | **Jamais répondu explicitement** |
| `c'est quoi le X1201-C1 ?` | 1x | Spécification matérielle manquante |
| `comment bootstrap GM 5.2 identique ?` | 1x | Processus d'uniformisation non défini |
| `pourquoi ça boot ? / pourquoi il boot ?` | 2x | Langage imprécis → confusion logique de démarrage |

**Verdict** : Ces questions révèlent 3 domaines non documentés :
1. Architecture système (RPi SSH, réseau, paths)
2. Interfaces outils (VSCode + OpenRouter, Whisper)
3. Concepts PKA (memory nudge, team.db, bootstrap uniformisé)

---

## Nouveaux patterns détectés

### Pattern 1 : Tunnel de confusion terminal vs IDE
JCH demande régulièrement si une commande terminal fonctionne identiquement dans VSCode. Aucune réponse structurée donnée. Signe d'une ligne floue entre exécution locale, tunnel SSH, et virtualisation.

### Pattern 2 : Réseau RPi = zone d'ombre totale
- Accès terminal RPi bloqué
- Diagnostic SSH absent
- Fallback sur alternatives non proposé
- **Résultat** : productivité gelée, questions répétées = frustration croissante

### Pattern 3 : Décisions pharmacie/vétérinaire dispersées
Trois documents reçus (Virbac, Aenova, CDMO) sans synthèse unifiée. JCH reconstitue le puzzle manuellement. Pas de KB centralisée pour Vetalyx.

### Pattern 4 : Cleanup PKA sans vérification d'impact
Suppression en cours (`.bak-*`, `.DS_Store`) avec commandes `dd` lancées sur images disque. Aucun backup confirmé avant. Risque opérationnel élevé.

### Pattern 5 : Multi-projet en même session
En même jour : Vetalyx (pharma), wildnexus (bio), Home Assistant (IoT), bioacoustique (fork), tout sans contexte switching documenté. ADHD-friendly ? Non.

---

## Efficacités / Inefficacités

### ✅ Efficacités conservées
- **Expert consultation réflexe** : JCH interroge experts externes (Kimi 2.5 analyse PKA, expert RPi/LLM), améliore décisions qualitatives
- **Validation multi-source** : Aenova confirmé par expertise, modèles LLM recommandés par consultant compétent
- **Décisions rapides** : choix OpenRouter validé, migration décidée sans délai
- **Dobby actif** : orchestration mémoire fonctionne, patterns capturés régulièrement

### ❌ Inefficacités graves
1. **Accumulation non-résolue** : 9 questions récurrentes non répondues = 3-4h temps utilisateur perdu (estimation)
2. **Dépendance Dobby > documentation** : JCH s'appuie sur memory system plutôt que KB écrite → fragile si session décalée
3. **Diagnostic incomplet** : erreurs système (Whisper, OpenRouter, Home Assistant UUID) laissées "en attente"
4. **Contexte switching sans garde-fou** : passage Vetalyx → Home Assistant → bioacoustique → GM 5.2 en 1 session, aucun recap
5. **SSH/Réseau RPi = terrain miné** : plusieurs tentatives échouées, aucun diagnostic posé, frustration bâtit
6. **Langage imprécis** : "pourquoi ça boot ?", "pourquoi il boot ?" → interprétation nécessaire à chaque fois
7. **Cleanup sous stress** : suppression fichiers + flash disque simultanés = risque de perte données

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Projets actifs (état 2026-07-13)
- **Vetalyx** : CDMO sélectionné (Aenova), formulation hydrocortisone aceponate en cours, référence fabricants (Virbac) centralisée
- **wildnexus** : bioacoustique fork en création (transfert ressources plantes en attente)
- **Home Assistant Lupo-RPi** : UUID conflict detected, image flash interrompue, redémarrage isolé planifié
- **PKA** : 18 Go, 12 projets actifs, nettoyage en cours (`.bak-*`, `.DS_Store`)

### Infrastructure décisionnelle
- **OpenRouter** : passage confirmé, launcher VSCode dysfonctionnel (to-do)
- **Raspberry Pi 5 (8 Go)** : SLM + Ollama Q4_K_M = config recommandée par expert
- **GM 5.2** : bootstrap uniformisation = demande en attente

### Points de friction bloquants
1. Terminal RPi **toujours inaccessible** → diagnostic SSH URGENT
2. **team.db inaccessible** → réponse manquante, relancer
3. **Whisper dans VSCode** → isoler terminal vs IDE, reproduire
4. **OpenRouter launcher** → error handling manquant
5. **Home Assistant UUID** → deux instances détectées, diagnostic réseau requis

### Concepts mal expliqués (créer mini-docs)
- `memory nudge` : définition + use case
- Variables d'environnement + `.env` path prefix
- VSCode terminal vs terminal local distinction
- SSH connectivity RPi troubleshooting

---

## Recommandations

### 🔴 URGENT (Bloque productivité)
1. **Diagnostic SSH Lupo-RPi ce jour**
   - Test connectivité : `ssh user@rpi_ip`
   - Fallback sur accès physique si nécessaire
   - Document : "RPi Access Troubleshooting" pour future sessions
   - Freinage : JCH perd ~20 min/question sur ce sujet

2. **Répondre team.db question directement**
   - Créer doc : permissions, chemin exact, how-to access
   - Ajouter à mémoire : raison inaccessibilité + solution

3. **Isoler Whisper VSCode bug**
   - Reproduire : exact terminal, exact commande, capture erreur complète
   - Vérifier : PATH, locale warnings (vu dans logs: `LC_CTYPE=UTF-8`)
   - Documenter : VSCode vs Terminal execution model

### 🟠 HAUTE (Cette semaine)
4. **Créer doc "Quick Start : OpenRouter + VS Code"**
   - Sélection modèles interface
   - Launcher fixing (error catching)
   - Exemple : "lancer Kimi 2.5 depuis VSCode en 3 clicks"

5. **Synthèse Vetalyx centralisée**
   - Fusionner Virbac + Aenova + CDMO requirements en 1 page
   - Ajouter : timeline fabrication, coûts estimés, next steps
   - Purpose : arrêter recherche dispersée, accélérer décision

6. **Backup avant cleanup PKA**
   - Vérifier : `.bak-*` files = vraiment dups ?
   - Checksum 3-4 fichiers clés avant suppression
   - Archive `session_*.json` complets (potential memory loss)

7. **Unifyer "pourquoi il boot ?" / "pourquoi ça boot ?"**
   - Clarifier : demande diagnostic vs demande explication ?
   - Template réponse : « Tu veux savoir [1] si le démarrage est anormal OU [2] pourquoi techniquement il reboote ? »

### 🟡 

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 57
- Résolus automatiquement : 19
- Résolus manuellement : 0
- Encore ouverts : 38
- **Taux : 33.3%**

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

- [Decision] Migration OpenRouter pour Kimi** : abandon des appels directs, passage exclusif par OpenRouter pour standardiser les points d'entrée API
- [Decision] Nettoyage PKA confirmé** : suppression des `.bak-*`, vérification des `.DS_Store` restants (8 identifiés), archivage des `session_*.json`
- [Decision] Aenova validé comme partenaire CDMO** : 8 sites industriels approuvés pour produits vétérinaires, expertise confirmée pour formulation hydrocortisone 
- [Decision] Démarrage en isolation du Lupo-RPi** : reboot sans dépendances externes pour diagnostiquer les points d'entrée
- [Failure] Symptôme : erreur non identifiée lors appel fonction
- [Failure] Contexte : exécution depuis IDE vs terminal
- [Failure] Status : investigation en cours, aucune conclusion
- [Failure] Symptôme : fonction de lancement ne s'exécute pas après clic
- [Failure] Erreur affichée : non documentée précisément
- [Failure] Impact : interface VS Code inutilisable pour sélection modèles
- [Failure] JCH ne peut pas atteindre le shell RPi malgré demandes répétées
- [Failure] Alternatives proposées : aucune (situation créant frustration)
- [Failure] Dependencies : connaissance réseau RPi insuffisante
- [Failure] Whisper ne fonctionne pas dans VSCode
- [Failure] OpenRouter launcher dysfonctionnel
- [Failure] Accès terminal RPi bloqué

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 35 occurrences
- **Question** : 9 jours, 27 occurrences
- **Failure** : 8 jours, 47 occurrences
- **Recurring question** : 7 jours, 24 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 11
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**265** recommandations au total — **265** ouvertes — **0** en cours — **0** terminées

⚠️ 234 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 227
- **Forge** : 31
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=254] (2026-07-13) **Dobby** : Diagnostic SSH Lupo-RPi ce jour
- [id=255] (2026-07-13) **Dobby** : Test connectivité : `ssh user@rpi_ip`
- [id=256] (2026-07-13) **Dobby** : Fallback sur accès physique si nécessaire
- [id=257] (2026-07-13) **Dobby** : Document : "RPi Access Troubleshooting" pour future sessions
- [id=258] (2026-07-13) **Dobby** : Freinage : JCH perd ~20 min/question sur ce sujet

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $24.94 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $24.94**

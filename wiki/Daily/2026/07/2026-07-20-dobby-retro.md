---
date: 2026-07-20
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1059
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-20

**Sessions analysées :** 2 | **Échanges :** 1059 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-07-20

## Décisions prises

1. **Transfert de contexte sur modèle étendu** : Face à des problèmes complexes, décision de transférer vers un modèle plus développé (probablement Claude) pour meilleure capacité de raisonnement.

2. **Validation et mise à jour documentaire** : Ensemble de fichiers à mettre à jour après décisions ; formalisation de notification aux stakeholders.

3. **Configuration Aenova** : Reconnaissance que Aenova dispose de 8 sites industriels approuvés pour vétérinaire, expertise validée comme point d'entrée stratégique (projet Vetalyx).

4. **Gestion iPhone/niveau disponible** : Décision de fonctionner au niveau disponible sur iPhone plutôt que d'optimiser, avec envoi configuré.

5. **Mise en mémoire de tests réels** : Enregistrement de configuration pour tests matériel prévus "dans quelques jours" (pas de date fixée).

6. **Retour à lupo-rpi setup** : Décision de figer la configuration du Raspberry Pi lupo après exploration des problèmes hardware.

7. **Facteur forme sphérique** : Design decision de ne pas demander aux utilisateurs une fixation manuelle une à une, mais d'utiliser format sphérique.

8. **Pivot vers Vetalyx** : Redirection de priorité vers projet Vetalyx suite à sollicitation chinoise identifiée.

---

## Échecs ouverts / bloqueurs

### CRITIQUES

- **Ctrl+C non fonctionnel sur RPi** : Bloqueur sur interaction terminal, affect productivité de debugging.
  
- **AppManager.install bloqué** : Erreur système `duplicate_os_install` avec message "system is not healthy". Indique installation OS corrompue ou conflictuelle sur lupo-rpi.

- **Whisper ne fonctionne pas dans VS Code** : Problème de dépendances audio/I2S non résolu. Context manquant : pourquoi VS Code vs terminal natif ?

- **Accès terminal RPi inaccessible** : JCH demande itérativement pourquoi Dobby n'a pas accès. Problème SSH ou permission non documenté.

- **Fichier HAO corrompu** : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory` - image d'installation introuvable ou chemin malformé.

- **team.db inaccessible** : Base de données verrouillée ou permissions incorrectes. Cause inconnue, impact sur projet non clair.

- **404 non identifié** : Référence vague à un "404" sans contexte d'URL. À clarifier.

### TECHNIQUE

- **Erreur de facteur 3x observée** : JCH note "une erreur : un facteur 3. cela peut tuer une decision sur un projet" → calcul/mesure avec divergence majeure non tracée. Quelle variable ? Quel test ?

- **Problème alimentation HAT/PSU** : `PSU_MAX_CURRENT=5000` relevé sans contexte de solution. Limit insuffisante ? Oscillation de power ?

- **Composants en backorder Mouser** : MEMS microphone, IR emitter, motion sensor tous en backorder → délai de 3-4 semaines probable sur livraison. Impact sur M5 ou WildNexus assembly.

- **Conflits Home Assistant** : Détection d'instance dupliquée ou UUID partagés. Symptôme : installation OS fragmentée (clonage de disque, UUID non unique).

- **Locale Debian invalide** : Warning `LC_CTYPE=UTF-8, LC_ALL=` sur lupo-rpi → can affect package management et internationalization.

---

## Questions récurrentes (signe de lacune documentaire)

1. **"Pourquoi tu n'as pas accès au terminal RPi ?"** (répétée 3x)
   - Dobby ne peut pas expliquer restriction SSH/permissions.
   - **À documenter** : accès terminal, modèle d'authentification, restrictions système.

2. **"Whisper ne fonctionne pas ; vérifie pourquoi on est dans VS Code"**
   - Confusion sur contexte d'exécution (VS Code vs terminal natif).
   - **À documenter** : environnement d'exécution pour audio/I2S, dépendances.

3. **"Pourquoi il boot ?"** (incomplète, contexte perdu)
   - Probable : "Pourquoi ça reboot ?" ou "Pourquoi ça ne boot pas ?"
   - **À clarifier** : comportement au démarrage lupo-rpi.

4. **"Comment faire en sorte qu'il ait le même bootstrap ?"** (gm 5.2 vs M5)
   - Proces d'initialisation M5 vs autre device flou.
   - **À documenter** : bootstrap procedure, variations par device.

5. **"C'est quoi l'avant vs l'arrière [4 roues/chassis] ?"**
   - Orientation physique du robot/device pas intuitive ou non documentée.
   - **À documenter** : schéma physique orientation, conventions.

---

## Nouveaux patterns détectés

### PATTERNS POSITIFS

- **Multi-expert intake** : JCH consulte des experts externes (pharmacie, hardware) et intègre leurs recommandations directement dans workflow. Efficace pour validation.

- **Transfert contextuel fluide** : Passage entre DeepSeek → Claude intelligent basé sur complexité. Utilisation d'outils appropriés.

- **Test-driven decision** : "Ok mets cela en mémoire car on va faire des tests en réel" → décisions validées empiriquement, pas théoriques.

### PATTERNS NÉGATIFS

- **Documentation décentralisée** : Recommandations LLM (SLM/Ollama/Q4_K_M) mentionnées mais pas intégrées dans playbook central. Risque de duplication.

- **Debugging itératif sans trace** : Erreurs (ctrl+c, AppManager, Whisper) posées puis abandonnées sans root cause document. Dobby redécouvre même problème.

- **Scope creep silencieux** : 3 projets actifs (WildNexus, Home Assistant, Vetalyx) avec priorités fluides. Vetalyx "une société chinoise me demande" → décision de pivot sans planification.

- **Hardware inventory fragmenté** : Listes Mouser (microphones, inductors, sensors) sans mapping à projet/deadline. 8 composants en backorder → risque d'arrêt assembly.

- **Contexte technique perdu** : Extraits de transcript mélangeant français/anglais, tronqués (erreurs syntaxe). Difficulté pour Dobby de reconstituer intent.

---

## Efficacités / inefficacités

### EFFICACE ✅

- **Décisions rapides** : "Fais le 1", "ok on va essayer" → pas de réunion-paralysie.
- **Expertise externe intégrée** : Consultant pharmaco + hardware expert → validation rapide design.
- **Outils polyvalents** : DeepSeek + Claude + exec_shell combinés → investigation technique robuste.

### INEFFICACE ❌

- **Boucles de debugging répétées** : Ctrl+C, whisper, terminal RPi reviennent 3-4x sans résolution.
- **Absence de issue tracker** : Bloqueurs éparpillés dans transcript, pas de board/backlog centralisé.
- **Composants en backorder** : Pas de contingency planning, risque d'arrêt physique.
- **Communication asynchrone fragmentée** : Dobby pose questions, JCH répond partiellement (contexte tronqué), confusion persiste.
- **Pas de arborescence décision** : Vetalyx pivot décidé sans documenter impact sur WildNexus/Home Assistant timeline.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

1. **lupo-rpi est en état fragile** : AppManager bloqué, instance OS dupliquée détectée, Ctrl+C inopérant. Besoin d'une **réinstallation propre** (HAOS 15.1 image valide + verification UUID unique).

2. **Accès terminal est un préalable** : Multiple questions "pourquoi pas d'accès RPi". Fixer SSH keys, permissions, firewall AVANT prochaine session.

3. **Whisper audio chaîne incertaine** : I2S dependencies, VS Code context, microphone hardware → nécessite audit complet stack audio.

4. **Vetalyx est nouveau pivot stratégique** : "une société chinoise" implique timeline serré, validation réglementaire pharma (CDMO, EU-GMP). Clarifier scope vs WildNexus.

5. **8 composants en backorder** : Mouser backlog impacte M5 assembly. Obtenir dates livraison, identifier substituts ou staging sans.

6. **Bootstrap M5 vs autres devices diverge** : "gm 5.2 comment faire en sorte qu'il ait le même bootstrap" → procédure standardisée manquante. À créer playbook unifiée.

7. **Facteur 3 observé non tracé** : "une erreur : facteur 3. cela peut tuer une decision" - quelle mesure ? Quel test ? Relancer investigation avec précision.

8. **Locale Debian manquante** : lupo-rpi warning `LC_CTYPE=UTF-8` → corriger avec `dpkg-reconfigure locales`. Peut affecter compilation/packaging.

---

## Recommandations

### IMMÉDIAT (24-48h)

1. **Créer issue tracker centralisé** : Dobby + JCH trient bloqueurs actuels (Ctrl+C, AppManager, whisper, terminal access) → board priorité/status.

2. **Auditer accès terminal RPi** : Tester SSH depuis M1/M5, valider keys, firewall rules. Documenter dans `JCH_PRIVATE/credentials-central.md`.

3. **Récupérer image HAOS valide** : Vérifier chemin `haos_rpi5-15.1.img`, re-flasher SD avec dd proprement, valider boot unique (UUID).

4. **Clarifier Vetalyx timeline** : Société chinoise = deadline ? Scope pharma complet vs POC ? Réallocuer ressources WildNexus.

5. **Auditer hardware backorder** : Contact Mouser, obtenir ETA 8 composants, identifier plan B (substituts, staged assembly, vendor alternatif).

### COURT TERME (1-2 semaines)

6. **Créer playbook bootstrap unifié** : Documenter procédure M5, M1, RPi5 side-by-side (env variables, configs, test first-boot).

7. **Isoler stack audio Whisper** : Créer test harness I2S/microphone sans VS Code. Valider dépendances. Documenter config.

8. **Quantifier "facteur 3"** : Relancer test précis, tracer mesure exacte, documenter écart → décision pharma robuste.

9. **Mettre en mémoire partagée** : Intégrer recommendations LLM (SLM/Ollama/Q4_K_M pour RPi5 8Go) dans `JCH_Inbox/04_PILOTAGE_STRATEGIQUE`.

### MOYEN TERME (3+ semaines)

10. **Standup async quotidien** : Dobby envoie briefing texte (3 bloqu

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 39
- Résolus automatiquement : 11
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 28.2%**

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

- [Decision] : Face à des problèmes complexes, décision de transférer vers un modèle plus développé (probablement Claude) pour meilleure capacité de raisonnement.
- [Decision] : Ensemble de fichiers à mettre à jour après décisions ; formalisation de notification aux stakeholders.
- [Decision] : Reconnaissance que Aenova dispose de 8 sites industriels approuvés pour vétérinaire, expertise validée comme point d'entrée stratégique (projet Veta
- [Decision] : Décision de fonctionner au niveau disponible sur iPhone plutôt que d'optimiser, avec envoi configuré.
- [Decision] : Enregistrement de configuration pour tests matériel prévus "dans quelques jours" (pas de date fixée).
- [Decision] : Décision de figer la configuration du Raspberry Pi lupo après exploration des problèmes hardware.
- [Decision] : Design decision de ne pas demander aux utilisateurs une fixation manuelle une à une, mais d'utiliser format sphérique.
- [Decision] : Redirection de priorité vers projet Vetalyx suite à sollicitation chinoise identifiée.
- [Decision] Transfert de contexte sur modèle étendu** : Face à des problèmes complexes, décision de transférer vers un modèle plus développé (probablement Claude)
- [Decision] Validation et mise à jour documentaire** : Ensemble de fichiers à mettre à jour après décisions ; formalisation de notification aux stakeholders.
- [Decision] Configuration Aenova** : Reconnaissance que Aenova dispose de 8 sites industriels approuvés pour vétérinaire, expertise validée comme point d'entrée s
- [Decision] Gestion iPhone/niveau disponible** : Décision de fonctionner au niveau disponible sur iPhone plutôt que d'optimiser, avec envoi configuré.
- [Decision] Mise en mémoire de tests réels** : Enregistrement de configuration pour tests matériel prévus "dans quelques jours" (pas de date fixée).
- [Decision] Retour à lupo-rpi setup** : Décision de figer la configuration du Raspberry Pi lupo après exploration des problèmes hardware.
- [Decision] Facteur forme sphérique** : Design decision de ne pas demander aux utilisateurs une fixation manuelle une à une, mais d'utiliser format sphérique.
- [Decision] Pivot vers Vetalyx** : Redirection de priorité vers projet Vetalyx suite à sollicitation chinoise identifiée.
- [Failure] Ctrl+C non fonctionnel sur RPi** : Bloqueur sur interaction terminal, affect productivité de debugging.
- [Failure] AppManager.install bloqué** : Erreur système `duplicate_os_install` avec message "system is not healthy". Indique installation OS corrompue ou conflic
- [Failure] Whisper ne fonctionne pas dans VS Code** : Problème de dépendances audio/I2S non résolu. Context manquant : pourquoi VS Code vs terminal natif ?
- [Failure] Accès terminal RPi inaccessible** : JCH demande itérativement pourquoi Dobby n'a pas accès. Problème SSH ou permission non documenté.
- [Failure] Fichier HAO corrompu** : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory` - image d'installation introuvable ou chemin malformé.
- [Failure] team.db inaccessible** : Base de données verrouillée ou permissions incorrectes. Cause inconnue, impact sur projet non clair.
- [Failure] 404 non identifié** : Référence vague à un "404" sans contexte d'URL. À clarifier.

### Fréquence des patterns (14 jours)
- **Failure** : 9 jours, 54 occurrences
- **Decision** : 8 jours, 35 occurrences
- **Question** : 7 jours, 20 occurrences
- **Recurring question** : 6 jours, 20 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 23
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**319** recommandations au total — **319** ouvertes — **0** en cours — **0** terminées

⚠️ 253 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 277
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 4

### Plus récentes ouvertes

- [id=315] (2026-07-20) **Dobby** : Créer issue tracker centralisé** : Dobby + JCH trient bloqueurs actuels (Ctrl+C,
- [id=316] (2026-07-20) **Dobby** : Auditer accès terminal RPi** : Tester SSH depuis M1/M5, valider keys, firewall r
- [id=317] (2026-07-20) **Dobby** : Récupérer image HAOS valide** : Vérifier chemin `haos_rpi5-15.1.img`, re-flasher
- [id=318] (2026-07-20) **Dobby** : Clarifier Vetalyx timeline** : Société chinoise = deadline ? Scope pharma comple
- [id=319] (2026-07-20) **Dobby** : Auditer hardware backorder** : Contact Mouser, obtenir ETA 8 composants, identif

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

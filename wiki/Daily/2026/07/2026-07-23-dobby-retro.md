---
date: 2026-07-23
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1114
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-23

**Sessions analysées :** 2 | **Échanges :** 1114 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Session 2026-07-23 | JCH & Assistants

## Décisions prises

1. **Arrêt itération de documentation** → Créer fichier `.md` consolidé plutôt que continuer en boucle
2. **Validation déploiement Lupo-RPi** → Relance seule pour vérifier redémarrage complet (`100% validé`)
3. **Passage vers modèle LLM optimisé** → Migration de la configuration IA sur Raspberry Pi 5 vers SLM légers + Ollama (formats Q4_K_M GGUF)
4. **Tests réels en production** → Planification tests hardware dans "quelques jours" → mémoriser cette baseline
5. **Validation mise à jour fichiers** → Tous les fichiers utiles synchro, équipe notifiée
6. **Stratégie déploiement firmware** → Rejet de l'approche "fixer une à une" → **solution sphere/facteur form** (non détaillée, à documenter)

**Problème critique** : Les décisions sont validées oralement mais **rarement documentées en temps réel**. Aucune trace écrite de la "sphere" ou du modèle LLM choisi pour RPi5.

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent production)
- **Duplicate OS install** → Home Assistant détecte 2 instances HA actives sur réseau/disque (sauvegarde + clonage ?)
  - Cause probable : restauration résente sans cleanup UUID
  - Status : Non résolu, en attente diagnostique
  
- **RPi5 bloquée au boot hardware** → Reste stuck phase init matériel (CPU ? thermal ? GPU ?)
  - Tentative : `dd` image HAOS 64-bit → **fichier manquant** (`haos_rpi5-15.1.img` not found)
  - Téléchargement en cours → timeouts récurrents (347 MB incomplet)
  - Status : À relancer avec `haos_rpi5-64-18.1.img` ?
  
- **SSH/Terminal RPi inaccessible** → Ctrl+C ne fonctionne pas, connexion reste "Broken pipe"
  - Impact : Impossible debugging matériel/OS
  - Status : Diagnostic en suspens

### Secondaires (dégradent UX)
- **Whisper non fonctionnel** → Vérifié dans VSCode, raison racine inconnue
- **Ctrl+M affiche 'm'** → Interface/keybinding cassé (VSCode ou terminal ?)
- **Vanroll test retourne 0 données** → À investiguer (source données ?)
- **Locale Debian UTF-8 invalide** → Message warning répété, UX dégradée

---

## Questions récurrentes (signe de lacune documentaire)

1. **"Quelle est la différence entre lupo/assiette et esneux/iphone ?"**
   - Posée 2x → Hypothèse : différence d'instance HA, de HAT hardware, ou de configuration réseau
   - **Lacune** : Pas de mapping entités machine ↔ config HA
   
2. **"Pourquoi tu n'as pas accès au terminal RPi ?"**
   - Posée itérativement → Personne ne comprend le diagnostic SSH/permissions
   - **Lacune** : Pas de run-book SSH troubleshooting

3. **"Pourquoi il boot ?"**
   - Formulation flou, répété → Confusion sur état matériel / OS / image
   - **Lacune** : Pas de state diagram ou checklist boot sequence RPi5

4. **"Pourquoi vanroll test ne donne plus de données ?"**
   - Posée 2x → Source de données non documentée, dépendances opaques
   - **Lacune** : Pas d'architecture données / data flow

5. **"Avant/arrière 4 roues vs petit truc ?"**
   - Contexte perdu → Probablement hardware physique (robot mobile ? caméra ?)
   - **Lacune** : Pas d'inventaire matériel avec photos/specs

---

## Nouveaux patterns détectés

### Pattern 1 : "Cercle de documentation"
- Décisions prises → orales → validation → pas d'écriture → question répétée 2-3 jours plus tard
- Symptôme : "ok mets à jour les fichiers utiles" (vague, jamais vérifié)

### Pattern 2 : "Migration incompète LLM"
- Décision : Passer Ollama + SLM quantisés sur RPi5
- Réalité : Configuration IA consommée depuis extraits expert, **zéro implémentation trackée**
- Risk : Dans 3 jours, oubli du choix modèle (Phi ? TinyLlama ? Qwen ?)

### Pattern 3 : "Hardware vs Software confusion"
- Erreur `duplicate_os_install` interprétée comme soft → possiblement **2 disques physiques** branchés
- Test : Lupo-RPi "relancé seul" pour vérification, mais **aucune diagnostique préalable**

### Pattern 4 : "Outils multi-canaux sans sync"
- Claude Code + DeepSeek TUI + Codex CLI → même context → divergence (fichiers manipulés séquentiellement, risque overwrite)
- Aucun lock ou journal de chkpt

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Expertise hardware multipiste** : Expert consulté, doc qualité reçue (SLM/Ollama recommandations précises)
- **Validation rapide** : Décision "100% validé" → confiance élevée
- **Multi-outils opportuniste** : Recherche Mouser + grep distantes combinées quand bloqué

### ❌ Inefficacités
- **Debugging aveugle** : RPi5 "bloquée au boot" → zéro information système (dmesg, kernel panic log, serial console)
  - Coût : 3-4 itérations avant accès SSH, puis abandon
  
- **Image système manquante** : Script télécharge `haos_rpi5-15.1.img`, cherche `haos_rpi5-64-18.1.img`
  - Coût : Perte 30 min, retry timeout
  
- **Terminal inopérant** : SSH rpi bloqué → migration en aveugle vers diagnostic réseau M5
  - Coût : Perte contexte hardware, distraction
  
- **Questions "résumées" mal transmises** : Problème résumé par IA → transfert modèle plus développé → perte détails originaux
  - Coût : Re-diagnostique depuis zéro

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Baseline matériel & config
```
LUPO-RPi config (à valider) :
- Host : lupo-rpi.local | 2a02:a03f:a10d:4501:25fb:e5xx
- OS : Home Assistant OS (tentative HAOS 64-18.1)
- Kernel : 6.18.34-rpt-rpi-2712 (si boot réussi)
- Locale : UTF-8 manquant → `sudo dpkg-reconfigure locales`
- Instance HA : "assiette" (probablement, vs "iphone"/esneux)

TESTS PRODUCTION PRÉVUS : "quelques jours" (~2026-07-25 à 27)
- Configuration LLM : Ollama + SLM Q4_K_M (modèle TBD : recommandations expert reçues)
- Vérification facteur form : Approche "sphere" (design non documenté)
```

### Systèmes en attente de diagnostique
```
🔴 BLOQUANT : RPi5 stuck boot → serial console log ?
🟡 CONCERNANT : duplicate_os_install error → UUID conflict resolution
🟡 CONCERNANT : SSH broken pipe + Ctrl+C non fonctionnel → permutations réseau/auth
🟢 À DOCUMENTER : Whisper VSCode, Vanroll data source, avant/arrière hardware
```

### Lacunes critiques pour prochaines sessions
1. **Pas de run-book SSH** → créer template diagnostique RPi
2. **Pas de data flow doc** → Vanroll test source/sink
3. **Pas d'inventaire matériel** → "4 roues" vs petit truc indéfinis
4. **Pas de mapping instance HA** : lupo/assiette vs esneux/iphone
5. **Pas de git pour décisions** → décisions.md avec timestamps + statut

---

## Recommandations

### 🎯 Court terme (avant tests produc)

1. **Créer `BLOCKER_SUMMARY.md`** (1 page)
   - [ ] RPi5 boot failure : tentative serial console log ou reset firmware
   - [ ] SSH access : vérifier réseau, auth, hostname lupo-rpi.local
   - [ ] Duplicate OS : identifier les 2 disques/UUID, cleanup
   - [ ] Valider image HAOS téléchargeable (18.1 vs 15.1)
   
2. **Documenter décisions LLM immédiatement**
   - [ ] Fixer modèle SLM (Phi-2 ? TinyLlama-1.1B ?)
   - [ ] Écrite Ollama run command pour RPi5 (8GB, NVMe, Geekworm HAT)
   - [ ] Valider Q4_K_M quantization sur cette config
   
3. **Clarifier "facteur form sphere"**
   - [ ] Qui ? Quoi ? Pourquoi ? (design doc 0.5 page min)
   - [ ] Si composant hardware → specs, fournisseur, prix
   
4. **Déverrouiller accès SSH RPi5**
   - [ ] Serial console sur UART (si disponible) OU
   - [ ] Reset réseau (reboot depuis source d'alimentation) OU
   - [ ] Swap disque NVMe pour diagnostique

### 📋 Moyen terme (avant prochaine session)

5. **Créer registry entités**
   ```
   # machines.yaml
   lupo-rpi:
     hostname: lupo-rpi.local
     ha_instance: assiette
     storage: SSD NVMe
     battery: Geekworm HAT
     ha_version: 18.1
   esneux-iphone:
     hostname: esneux-iphone.local
     ha_instance: iphone
     # ...
   ```

6. **Documenter data flow Vanroll**
   - Source données : ?
   - Test exécution : où ?
   - Pourquoi zéro données maintenant ?

7. **Créer checklist SSH debug**
   - Résolveur DNS (avahi ?)
   - Clés SSH installées ?
   - Firewall/port 22 ouvert ?
   - HA system healthy ?

8. **Sync multi-outils**
   - Désigner un "état de référence" (ex: claude-main branch)
   - Logs alternatifs avec outil + timestamp
   - Pas de manipulation disque parallèle

### 🚀 Long terme

9. **Archiver expert comments** dans `docs/expert-llm-rpi5.md`
   - Citer source, date, contexte
   - Lier à décisions prises

10. **Créer PKA-specific template**
    

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 32
- Résolus automatiquement : 9
- Résolus manuellement : 0
- Encore ouverts : 23
- **Taux : 28.1%**

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

- [Decision] → Créer fichier `.md` consolidé plutôt que continuer en boucle
- [Decision] → Relance seule pour vérifier redémarrage complet (`100% validé`)
- [Decision] → Migration de la configuration IA sur Raspberry Pi 5 vers SLM légers + Ollama (formats Q4_K_M GGUF)
- [Decision] → Planification tests hardware dans "quelques jours" → mémoriser cette baseline
- [Decision] → Tous les fichiers utiles synchro, équipe notifiée
- [Decision] → Rejet de l'approche "fixer une à une" → **solution sphere/facteur form** (non détaillée, à documenter)
- [Decision] : Les décisions sont validées oralement mais **rarement documentées en temps réel**. Aucune trace écrite de la "sphere" ou du modèle LLM choisi pour R
- [Decision] Arrêt itération de documentation** → Créer fichier `.md` consolidé plutôt que continuer en boucle
- [Decision] Validation déploiement Lupo-RPi** → Relance seule pour vérifier redémarrage complet (`100% validé`)
- [Decision] Passage vers modèle LLM optimisé** → Migration de la configuration IA sur Raspberry Pi 5 vers SLM légers + Ollama (formats Q4_K_M GGUF)
- [Decision] Tests réels en production** → Planification tests hardware dans "quelques jours" → mémoriser cette baseline
- [Decision] Validation mise à jour fichiers** → Tous les fichiers utiles synchro, équipe notifiée
- [Decision] Stratégie déploiement firmware** → Rejet de l'approche "fixer une à une" → **solution sphere/facteur form** (non détaillée, à documenter)
- [Failure] Duplicate OS install** → Home Assistant détecte 2 instances HA actives sur réseau/disque (sauvegarde + clonage ?)
- [Failure] Cause probable : restauration résente sans cleanup UUID
- [Failure] Status : Non résolu, en attente diagnostique
- [Failure] RPi5 bloquée au boot hardware** → Reste stuck phase init matériel (CPU ? thermal ? GPU ?)
- [Failure] Tentative : `dd` image HAOS 64-bit → **fichier manquant** (`haos_rpi5-15.1.img` not found)
- [Failure] Téléchargement en cours → timeouts récurrents (347 MB incomplet)
- [Failure] Status : À relancer avec `haos_rpi5-64-18.1.img` ?
- [Failure] SSH/Terminal RPi inaccessible** → Ctrl+C ne fonctionne pas, connexion reste "Broken pipe
- [Failure] Impact : Impossible debugging matériel/OS
- [Failure] Status : Diagnostic en suspens

### Fréquence des patterns (14 jours)
- **Decision** : 8 jours, 28 occurrences
- **Failure** : 7 jours, 45 occurrences
- **Question** : 5 jours, 17 occurrences
- **Recurring question** : 4 jours, 12 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 23
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**345** recommandations au total — **345** ouvertes — **0** en cours — **0** terminées

⚠️ 274 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 303
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 4

### Plus récentes ouvertes

- [id=330] (2026-07-23) **Dobby** : Créer `BLOCKER_SUMMARY.md`** (1 page)
- [id=331] (2026-07-23) **Dobby** :  ] RPi5 boot failure : tentative serial console log ou reset firmware
- [id=332] (2026-07-23) **Dobby** :  ] SSH access : vérifier réseau, auth, hostname lupo-rpi.local
- [id=333] (2026-07-23) **Dobby** :  ] Duplicate OS : identifier les 2 disques/UUID, cleanup
- [id=334] (2026-07-23) **Dobby** :  ] Valider image HAOS téléchargeable (18.1 vs 15.1)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

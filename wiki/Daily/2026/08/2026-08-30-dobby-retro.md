---
date: 2026-08-30
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1113
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-30

**Sessions analysées :** 3 | **Échanges :** 1113 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🔍 RÉTROSPECTIVE SESSION 2026-08-30 - Dobby Analysis Report

## 📋 Décisions prises

- **Traitement des SKIPs par batch de 10** : passage à un traitement par lot plutôt qu'unitaire (décision de scalabilité)
- **Facteur form en sphère** : ne pas demander aux utilisateurs de fixer les paramètres unitairement (UX simplification)
- **Tests en environnement réel** : déploiement en production imminence (quelques jours) → mise en mémoire requise
- **Fiches validées finalisées** : clôture d'un cycle de validation
- **Redémarrage isolé lupo-rpi** : tentative de diagnostic en mode minimal (test de boot autonome)
- **Arrêt de la session** : création d'un fichier `.md` pour documenter et éviter les boucles

---

## 🚨 Échecs ouverts / Bloqueurs critiques

### Niveau P0 (Bloquant)
- **RPi5 gelé à l'initialisation matérielle** : système reste bloqué en début de phase de boot hardware
  - `Ctrl+C` inefficace sur RPI
  - Aucun accès terminal possible en état courant
  - **Symptôme** : "tout est bloqué"

### Niveau P1 (Sérieux)
- **Téléchargement HAOS échoué (404)** : 
  - Fichier `haos_rpi5-15.1.img` introuvable (`dd: failed to open`)
  - Lien GitHub cassé ou expiré
  - Tentatives de retry sans succès (Connection timed out)
  
- **Conflit d'instances Home Assistant** : 
  - Ancienne instance encore active en arrière-plan
  - UUID dupliqué ou restauration de sauvegarde mal finalisée
  - Bloque la nouvelle initialisation

- **Accès réseau lupo-rpi perdu** : 
  - SSH déconnexions fréquentes (`Broken pipe`)
  - Impossible d'accéder au terminal pour diagnostiquer

### Niveau P2 (À clarifier)
- **Erreur facteur 3 observée** : JCH souligne l'impact : "un facteur 3 peut tuer une décision sur un projet"
  - Contexte flou, type d'erreur non précisé
  - Potentiellement lié aux calculs LLM ou au dimensionnement RPi

---

## ❓ Questions récurrentes (Lacunes documentaires identifiées)

### Pattern 1 : Procédures non centralisées
**Question récurrente** : "comment faire en sorte que tu gardes en mémoire les procedures pour pouvoir lancer via un nom ?"
- Les procédures existent dans Inbox/Telegram mais pas indexées
- Pas de registry accessible des commandes nommées
- **Action requise** : créer un fichier `procedures-index.md` avec alias

### Pattern 2 : Différences architecturales confuses
**Questions** : 
- "quelle est la différence entre lupo/assiette et esneux/iphone ? c'est l'instance HA ?"
- "on avec les 4 roues un autre plus petit c'est quoi et ce serait bien de connaitre l'avant de l'arriere"

- **Diagnostic** : la taxonomie des machines n'est pas claire
- Lupo, Assiette, Esneux, iPhone = noms de déploiements flous
- Pas de diagramme d'architecture centralisé
- **Action requise** : créer `ARCHITECTURE.md` avec schéma machines/rôles

### Pattern 3 : Paramètres système mal documentés
**Questions non résolues** :
- "c'est quoi le ZH ?"
- "il indique L(M) c'est quoi ?"
- "lupo reporté au 31 aout. c'est quoi les states files ?"
- "TTL 24h. comment utiliser cela avec fluidité. est ce que par exemple dans un html on peut mettre un bouton"

- **Diagnostic** : jargon interne sans définition
- Paramètres HA/Home Assistant non expliqués
- **Action requise** : glossaire `GLOSSAIRE-PKA.md`

### Pattern 4 : Accès RPi bloqué
**Questions répétées** :
- "pourquoi tu n'as pas accès au terminal rpi ?" (3x)
- "pourquoi il boot ?"
- "en attendant pourquoi tu ne peux pas travailler dans le terminal RPI ?"

- **Diagnostic** : Dobby ne peut pas diagnostiquer sans accès, JCH teste en parallèle
- État du matériel inconnu de l'assistant
- **Action requise** : procédure de diagnostic RPi fallback (UART serial, LED status, etc.)

---

## 🔄 Nouveaux patterns détectés

1. **Approche iterative-mais-sans-mémoire** : JCH teste, rapporte partiellement, oublie contexte entre sessions
   - Même questions posées 2-3 fois en 1 session
   - Réponses antérieures non consultées

2. **Mix outils sans orchestration** : Claude, DeepSeek, Ollama, Docker, Tailscale utilisés en parallèle
   - Pas de flux d'information clair
   - Chaque outil isole ses résultats

3. **Priorités non rankées** : 
   - Vetalyx (affaires Chine/Belgique) mentionné brièvement
   - Home Assistant critique bloquée
   - Wildnexus en arrière-plan
   - Aucune priorisation explicite

4. **Documentations externes brutes copié-collées** : 
   - Expert LLM/RPi5 inséré sans synthèse
   - Credentials/IPs sensibles mélangées au flux
   - Pas de structuration

---

## ⚙️ Efficacités / Inefficacités

### ❌ Inefficacités majeures
| Inefficacité | Impact | Fréquence |
|---|---|---|
| Redondance questions | 3-4 réitérations mêmes questions | Haute |
| Pas d'index procédures | Perte temps recherche | Élevée |
| Contexte RPi opaque | Diagnostic aveugle | Critique |
| Mix outils sans sync | Duplication d'effort | Moyenne |
| Bruit documentaire | Credentials/logs mélangés | Haute |

### ✅ Efficacités conservées
- **Batch processing decision** : bon jugement scalabilité (skip par 10 vs. unitaire)
- **Testing in-life** : approche pragmatique validation réelle
- **Isolation lupo-rpi** : stratégie de diagnostic pertinente
- **Dobby memory** : JCH demande explicitement mémorisation pour décisions futures

---

## 💾 Ce qu'il faut garder en mémoire pour les prochaines sessions

### État critique du matériel
```
RPi5 (lupo-rpi.local)
├─ État: GELÉ à phase init hardware
├─ Symptoms: Aucun terminal accessible, Ctrl+C inopérant
├─ Cause probable: Conflit instance HA OR image HAOS corrompue (404)
├─ Action test: "reallume le lupo-rpi seul pour voir si tout redemarre"
└─ Dépend de: Succès téléchargement haos_rpi5-15.1.img VALIDE
```

### Décisions en attente de feedback
- ✋ **Traitement batch SKIPs** → en test, feedback "dans quelques jours"
- ✋ **Facteur form sphère** → bon travail validé, test en-life imminent
- ✋ **Fiches validées** → finalisées, state stable

### Détails réseau oubliés
- M5, lupo-rpi, assiette, esneux = machines nommées mais rôles flous
- Mosquitto/Docker-compose utilisé mais config éparpillée
- Tailscale en use but connectivity lupo-rpi intermittent

### Vetalyx (Belgique/Chine) - contexte juridique
- Société DIaho (Chine) entre au capital 40%, €10k total
- Pas de personnes physiques chinoises en ops/management
- Déclaration statut d'actionnaire → confirmation UCM Belgique requise

---

## 🎯 Recommandations

### 🔴 URGENT (< 24h)

1. **Débloquer lupo-rpi physiquement**
   ```
   - Essayer UART serial console (GPIO 14/15 + USB-TTL)
   - Ou : redémarrage forcé (couper alimentation, attendre 30s, relancer)
   - Ou : Teensy/PICO re-flash via carte mère directe
   - **Mettre en place Dobby callback** : "quand RPi respond, me notifier"
   ```

2. **Récupérer image HAOS valide**
   ```
   - Vérifier mirror GitHub officiel (ne pas trust lien expiré)
   - Télécharger version 18.1+ (pas 15.1)
   - Checksum SHA256 avant dd
   - **Stocker URL en SECURE**: JCH_PRIVATE/haos-downloads.md
   ```

3. **Résoudre conflit HA instances**
   ```
   - Lister tous les UUID/machine-id du réseau
   - Supprimer ancienne config si retrouvée
   - Référence: section "Conflit réseau" du transcript JCH
   ```

### 🟠 IMPORTANT (24-72h)

4. **Centraliser architecture & taxonomie**
   - Créer `ARCHITECTURE.md` :
     ```
     # Topologie PKA JCH
     - lupo-rpi.local (Raspberry Pi 5, 8Go, SSD NVMe) → Role: Home Assistant OS
     - M5 → Role: ?
     - assiette → Role: ?
     - esneux/iphone → Role: ?
     
     Diagramme réseau + Tailscale routing
     ```

5. **Indexer procédures nommées**
   - Créer `PROCEDURES-INDEX.md` :
     ```
     ## test-rpi-boot
     ssh jchavaux@lupo-rpi.local && systemctl status
     
     ## deploy-batch-skip
     ... (décrire le traitement batch de 10)
     
     ## restart-ha-clean
     ...
     ```
   - Dobby: maintenir index à jour

6. **Glossaire technique**
   - Créer `GLOSSAIRE-PKA.md` avec entrées manquantes:
     - ZH = ?
     - L(M) = ?
     - states files (Home Assistant) = ?
     - TTL 24h = time-to-live cache?
     - Assiette = hardware? container?

### 🟡 STRUCTUREL (cette semaine)

7. **Séparer signal du bruit documentaire**
   - Clips de credentials/IPs → `JCH_PRIVATE/credentials-central.md` uniquement
   - Logs → `JCH_PRIVATE/logs/` + archivage
   - Décisions/context → `JCH_Inbox/` + index Dobby

8. **Mettre en place flux de priorisation**
   - Session début: rank P0/P1/P2 explicitement
   - Dobby:

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 26
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 26
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

*Aucun nouveau pattern découvert par le LLM aujourd'hui.*

### Fréquence des patterns (14 jours)
- **Question** : 3 jours, 18 occurrences
- **Decision** : 2 jours, 17 occurrences
- **Failure** : 2 jours, 18 occurrences
- **Recurring question** : 2 jours, 13 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 0
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**397** recommandations au total — **397** ouvertes — **0** en cours — **0** terminées

⚠️ 397 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 354
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=383] (2026-08-18) **Dobby** : Re-flash lupo-rpi** :
- [id=384] (2026-08-18) **Dobby** : Télécharger `haos_rpi5-64-18.1.img.xz` complet (mirror ou USB).
- [id=385] (2026-08-18) **Dobby** : Brûler sur SD avec `balena-etcher` + vérification checksum.
- [id=386] (2026-08-18) **Dobby** : Brancher RPi5 seule (pas d'autres périphériques) et log les premier 5 min de boo
- [id=387] (2026-08-18) **Dobby** : Documenter first error → ouvrir issue.

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**

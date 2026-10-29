---
date: 2026-07-03
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 5
echanges: 1214
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-03

**Sessions analysées :** 5 | **Échanges :** 1214 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE DOBBY - Sessions 2026-07-02/03

## Décisions prises

- ✅ **Migration vers OpenRouter** : Abandon de Claude Code + Codex CLI (coûts/friction). OpenRouter devient le hub unique pour les modèles LLM.
- ✅ **Validation ESP32** : Après tests, l'ESP32 (modèle précis TBD) confirmé pour WildLens/WildNexus. Décision d'achat en attente du modèle exact.
- ✅ **Utilisation de HA (Home Assistant) + dongle Zigbee** : Remplacement du M5 pour la domotique. Intégration HACS validée comme carrefour Sonoff/IoT.
- ✅ **Sauvegarde travaux plantes** : Tous les outputs marqués "validé" doivent être sauvegardés formellement (plant analysis workstream).
- ✅ **Photo WildLens documentée** : Canon EOS R10 + RF 200-800mm, couple + poussin confirmé (référence 112.jpg).

---

## Échecs ouverts / bloqueurs

### 🔴 **Critiques**
1. **Upload ESP32 bloqué** : Erreurs récurrentes `no upload port provided` + `connection timeout` + `upstream connect error`. **Cause probable** : configuration de port série défaillante ou driver USB manquant. Non résolu, workaround manuel en place.
2. **Erreur 6683** : Référence à un code d'erreur jamais explicitée. Contexte perdu (probablement liaison sérielle ou Modbus). **À investiguer d'urgence**.
3. **Source Meter (Output OFF, Mode Source Meter, 5000 mV)** : JCH ne trouve pas où configurer cela → UI non documentée ou mauvais outil utilisé.

### 🟡 **Mineurs mais persistants**
4. **Crash Outlook + remise en place nécessaire** : Impact sur continuité. Aucune migration vers solution robuste (notes Apple citées mais non exploitées).
5. **Camera aliexpress non confirmée** : Lien produit 1005005710463218 référencé mais pas de spec validée. Risque : mauvaise pièce commandée.

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Nombre de fois | Lacune sous-jacente |
|----------|----------------|-------------------|
| C'est quoi `(.venv)` au début du path ? | 2x | **Environnements virtuels Python jamais expliqués formellement** |
| Comment accéder à Apple Notes depuis les assistants ? | 2x | **Système d'intégration mémoire externalisée inexistant** |
| C'est quoi `(.env)` ? | 1x | Confusion avec `.venv` - même lacune |
| Comment installer HACS et configurer HA ? | 1x | **Absence de guide d'setup Home Assistant dans PKA** |
| Comment utiliser OpenRouter dans VS Code ? Choisir un modèle ? | 1x | **Documentation OpenRouter-VSCode manquante** |
| C'est quoi "memory nudge" ? | 1x | **Terme interne non défini (probablement feature Dobby mal nommée)** |
| C'est quoi "harness" ? | 2x | **Contexte hardware absent (harness = connectique/câblage ?)** |
| C'est quoi le X1201-C1 et SSD ? | 1x | **Reference matérielle opaque, pas d'inventory centralisé** |
| Différence commande terminal VSCode vs terminal système ? | 1x | **Confusion environnement terminal** |
| Comment travailler plus logique/pro + accès recherches ? | 1x | **Processus PKA non formalisé pour l'utilisateur** |

**Impact** : Ces questions reviennent car la **documentation PKA est fragmentée** (dispersée entre AGENTS.md, CLAUDE.md, MEMORY.md, et wiki). Aucun onboarding centralisé.

---

## Nouveaux patterns détectés

### 📊 **Patterns de travail**
1. **Recherche documentaire ad-hoc** : JCH coupe/colle de sources externes (Virbac, datasheets, Mouser, AliExpress) sans contexte. Les assistants les traitent isolément → perte de chaîne décisionnelle.
2. **Décisions implicites** : "on va attendre", "validé à 100%", "ca marche pas" sans état formalisé. Dobby déduit mais ne confirme pas.
3. **Multi-contexte simultané** : WildLens + WildNexus + pharmacie vétérinaire + domotique HA en parallèle. Pas de cloisonnement. Risque : mélange des specs.
4. **Intégration outil chaotique** : DeepSeek TUI → Claude Code → Codex CLI → OpenRouter. Chaque outil est un îlot. Pas de workflow unifié.
5. **Hardware empirique** : Tests répétés sans doc préalable (ESP32-S3 vs OV5640, pinout, GPIO). Approche essai-erreur coûteuse.

### 🎯 **Nouvelles métriques PKA détectées**
- **"Pointeurs multi-modèles : 12 dérives 🔴"** → Système en drift. 12 références de modèles LLM non synchronisées.
- **"Health-check auto : RED"** → Nombreux faux positifs non nettoyés.
- **Git : 1,92 Go de pack (binaires)** → Historique pollué. À nettoyer.

---

## Efficacités / inefficacités

### ⚡ **INEFFICACITÉS flagrantes**

| Inefficacité | Impact | Cause |
|--------------|--------|-------|
| Questions sans réponse formalisée → reposées X fois | Perte 2-3h/semaine | Pas de FAQ/KB centralisée |
| Upload ESP32 échoue à chaque session | Blocage 1-2h | Config port non persistée + driver issue |
| Recherche doc manuelle (AliExpress, Mouser, datasheets) | Friction cogn. | Pas d'intégration API → copié-collé manuel |
| Crash Outlook mid-session | Perte contexte | Aucune résilience PKA (MEMORY.md local seulement) |
| Multi-outils (DeepSeek, Claude, OpenRouter) | Friction d'adoption | Pas d'alias unifiés ni workflow template |
| Contexte WildLens dispersé (camera spec, pinout ESP32, HA config) | Décisions isolées | Pas de STATE document centralisé par projet |

### ✅ **EFFICACITÉS conservées**

| Efficacité | Raison | À maintenir |
|------------|--------|------------|
| Dobby extrait patterns automatiquement | 55+ mentions = système détecté JCH. Feedback quasi-temps-réel | Garder extraction locale + reporting |
| Validation explicite ("validé 100%") | Marque clairement les snapshots | Formaliser en YAML/JSON decision log |
| OpenRouter comme hub unique | Coûts prévisibles, pas de friction achat | Documenter setup VSCode + modèle selection |
| HA + Zigbee choisi pour domotique | Écosystème stable, HACS well-supported | Créer guide setup TBD |
| DeepSeek-v4 pour analyse complexe | Utilisé 80% du temps, bon rappel | Garder comme modèle principal |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 **État critique à persister**

```markdown
### WildLens/WildNexus
- **Camera** : Canon EOS R10 + RF 200-800mm (CONFIRMÉ)
- **Microcontroller** : ESP32 (modèle exact TBD, après achat test)
- **Camera module** : OV5640 DVP 24-pin (NO DIRECT PLUG - custom pinout required)
- **Blocker** : Upload port error - need USB driver check + port config persistence

### Hardware State
- **M5** : ARRÊTÉ (remplacé par HA)
- **HA + Zigbee dongle** : ACTIF, HACS TBD
- **Camera AliExpress 1005005710463218** : NOT YET VALIDATED
- **Parts backorder** : MMICT5848 (mics), VSLB3940 (IR 940nm), EKMB1203111 (motion)

### Erreurs Non Résolues
- Code erreur 6683 : contexte perdu, à re-investiguer
- Source Meter config (5000 mV, Output OFF) : UI location unknown
- ESP32 upload port : intermittent, needs systematic debug

### Décisions Pending
- ESP32 model final selection (before AliExpress purchase)
- HACS/HA complete setup guide (who does this?)
- Pharmaceutical CDMO supplier search (Virbac vs alternatives)

### Contextes Parallèles
1. WildLens (35x mentions) = wildlife camera + AI
2. WildNexus (11x) = (unclear scope?)
3. ARTEON (8x) = (pharmaceutical formulation?)
4. Vetalyx (7x) = (veterinary product?)
5. Domotique HA = separate thread
```

### 📌 **Signaux faibles à monitorer**
- **12 model drifts** dans PKA → risque de divergence. Dobby doit weekly sync.
- **Faux positifs health-check** → détox Git + mémoire stale dans MEMORY.md.
- **1,92 Go pack** → Git refactor obligatoire avant prochaine sprint.

---

## Recommandations

### 🎯 **IMMÉDIAT (avant prochaine session)**

1. **Créer `/wiki/FAQ-RECURRENTES.md`** : Répondre aux 9 questions qui reviennent
   - `.venv` vs `.env` (Python virtual env expliqué simplement)
   - "Memory nudge" = function Dobby pour poke PKA (clarifier terme)
   - "Harness" = connectique/câblage hardware (définir lexique)
   - OpenRouter setup dans VSCode (pas de doc = confusion)
   - HACS installation guide (lien + steps)

2. **Créer `PKA/DECISIONS.yaml`** : Log structuré des validations
   ```yaml
   session: 2026-07-03
   decisions:
     - id: ESP32-model
       status: pending
       note: "Attendre achat pour confirmation"
     - id: HA-Zigbee-migration
       status: validated
       decision_date: 2026-07-03
       next_action: "HACS setup guide"
   ```

3. **Créer `PKA/ERROR-LOG.md`** : Tracker erreurs non résolues
   ```markdown
   ## Erreur 6683
   - Status: OPEN
   - Occurrences: 1+ (contexte perdu)
   - Suspected: Modbus/serial link issue
   - Action: Re-reproduce in next session, capture full stack

   ## ESP32 Upload Port
   - Status: OPEN (workaround manual)
   - Blockers: USB driver? Port config?
   - Action: Debug checklist + port persistence script
   ```

4. **Établir UNIQUE tool alias** : Éviter dérive multi-outils
   - `openrouter` =

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 41
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 39
- **Taux : 4.9%**

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

- [Decision] ✅ **Migration vers OpenRouter** : Abandon de Claude Code + Codex CLI (coûts/friction). OpenRouter devient le hub unique pour les modèles LLM.
- [Decision] ✅ **Validation ESP32** : Après tests, l'ESP32 (modèle précis TBD) confirmé pour WildLens/WildNexus. Décision d'achat en attente du modèle exact.
- [Decision] ✅ **Utilisation de HA (Home Assistant) + dongle Zigbee** : Remplacement du M5 pour la domotique. Intégration HACS validée comme carrefour Sonoff/IoT.
- [Decision] ✅ **Sauvegarde travaux plantes** : Tous les outputs marqués "validé" doivent être sauvegardés formellement (plant analysis workstream).
- [Decision] ✅ **Photo WildLens documentée** : Canon EOS R10 + RF 200-800mm, couple + poussin confirmé (référence 112.jpg).
- [Failure] 1. **Upload ESP32 bloqué** : Erreurs récurrentes `no upload port provided` + `connection timeout` + `upstream connect error`. **Cause probable** : con
- [Failure] : Référence à un code d'erreur jamais explicitée. Contexte perdu (probablement liaison sérielle ou Modbus). **À investiguer d'urgence**.
- [Failure] : JCH ne trouve pas où configurer cela → UI non documentée ou mauvais outil utilisé.
- [Failure] Upload ESP32 bloqué** : Erreurs récurrentes `no upload port provided` + `connection timeout` + `upstream connect error`. **Cause probable** : configur
- [Failure] Erreur 6683** : Référence à un code d'erreur jamais explicitée. Contexte perdu (probablement liaison sérielle ou Modbus). **À investiguer d'urgence**.
- [Failure] Source Meter (Output OFF, Mode Source Meter, 5000 mV)** : JCH ne trouve pas où configurer cela → UI non documentée ou mauvais outil utilisé.

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 41 occurrences
- **Failure** : 6 jours, 38 occurrences
- **Question** : 6 jours, 22 occurrences
- **Recurring question** : 5 jours, 21 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 11
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**208** recommandations au total — **208** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 174
- **Forge** : 28
- **Corbeau** : 4
- **Furet** : 2

### Plus récentes ouvertes

- [id=192] (2026-07-03) **Corbeau** : 1. **Créer `/wiki/FAQ-RECURRENTES.md`** : Répondre aux 9 questions qui reviennen
- [id=193] (2026-07-03) **Dobby** : `.venv` vs `.env` (Python virtual env expliqué simplement)
- [id=194] (2026-07-03) **Dobby** : Memory nudge" = function Dobby pour poke PKA (clarifier terme)
- [id=195] (2026-07-03) **Dobby** : Harness" = connectique/câblage hardware (définir lexique)
- [id=196] (2026-07-03) **Dobby** : OpenRouter setup dans VSCode (pas de doc = confusion)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $14.94 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $14.94**

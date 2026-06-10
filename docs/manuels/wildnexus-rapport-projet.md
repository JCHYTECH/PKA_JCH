# 📡 WildNexus — Rapport projet pour responsable

**Date :** 2026-06-09  
**Rédigé par :** [[Dobby]] 🦉 (PKA Orchestrator)  
**Auteur du projet :** Jean-Claude Havaux (JCH) — concepteur, chef de projet  
**Contact :** Liège, Belgique — consul honoraire de Malaisie, Master Zoologie ULiège

---

## 1. Qu'est-ce que WildNexus ?

Un **nœud caméra autonome** qui reste 60 jours dans la nature sans intervention humaine. Il capture des images (jour + nuit infrarouge), de l'audio court, détecte les animaux avec un filtre embarqué, et envoie une alerte par radio LoRa quand il voit quelque chose.

**Ce n'est PAS un piège photo.** C'est une plateforme modulaire qui, plus tard, pourra faire de la bioacoustique, de la reconnaissance d'espèces, et former un réseau de stations connectées. Mais la phase P0 reste strictement sur le nœud caméra.

---

## 2. Où en est le projet ?

**Statut :** M-01 (Architecture gelée) — atteint  
**Prochaine étape :** M-02 (Prototype banc fonctionnel)

### Jalons

| Jalon | Date cible | Statut | Signification |
|-------|-----------|--------|--------------|
| M-01 Architecture gelée | 2026-05-23 | ✅ **Atteint** | Tous les composants sont choisis et documentés : MCU, caméra, radio, stockage, énergie, boîtier |
| M-02 Prototype banc | En cours | 🔴 **Chemin critique** | Protocole de validation : intégration ESP32-S3 + OV5640 + LoRa + microSD, benchmark Edge AI, tests de fiabilité. **Pass M-02 = système complet fonctionnel sur table** |
| M-03 EVT terrain | À définir | 🔴 À venir | 30 jours dans la nature pour valider l'autonomie réelle, la fiabilité, la qualité des données |
| M-04 Publication | À définir | 🔴 À venir | Documentation + code source publié |

---

## 3. Architecture P0 (décisions validées)

Le système est composé de 3 sous-ensembles, documentés par des ADR (Architecture Decision Records) :

### Cerveau : ESP32-S3
- Microcontrôleur basse consommation
- Gère la capture, le filtre IA, le stockage, la radio
- ADR-001

### Caméra : OV5640 + infrarouge
- 5 MP, jour/nuit
- Filtre animal/non-animal embarqué (Edge AI sur ESP32-S3)
- ADR-002, ADR-007

### Radio : LoRa P2P EU868
- Longue portée (jusqu'à 10-15 km line-of-sight)
- Basse consommation
- Envoie métadonnées et alertes (pas les images complètes)
- ADR-003

### Stockage : microSD industrielle
- Les images restent sur la carte SD
- Seule une alerte + métadonnées part en radio
- ADR-004

### Énergie : 8 piles AA + régulateur
- Autonomie cible : 60 jours
- Pas de panneau solaire en P0 (trop de complexité)
- ADR-005

### Boîtier : IP67
- Étanche, montable sur arbre/poteau
- ADR-006 (encore en rédaction)

### Architecture globale
- **Satellite** (le nœud terrain) → **Base locale** (RPi à proximité, optionnel) → **Cloud**
- ADR-009

---

## 4. Budget

| Poste | Estimation |
|-------|-----------|
| Composants (16 pièces) | ~736 € |
| Prototypage, tests, outillage | ~200 € |
| **Total P0** | **~1 000 €** |

---

## 5. Équipe terrain (qui fait quoi)

| Rôle | Agent PKA | Responsabilité |
|------|-----------|----------------|
| Architecture firmware | [[Forge]] 🦦 | Firmware ESP32-S3, stack LPWAN, intégration |
| Base de données & stockage | [[Castor]] 🦫 | Schéma données, microSD, métadonnées |
| Caméra & Edge AI | [[Nova]] 🦋 | Choix optique, benchmark IA embarquée, test image |
| Radio & terrain | [[Chouette]] 🦉 | Montage terrain, test radio, boîtier |
| Photo & qualité | [[Lynx]] 🐆 | Qualité image, post-traitement |
| Budget & supply | [[Bruno]] 🐻 | Composants, fournisseurs, alternatives |
| Juridique & licence | [[Renard]] 🦊 | RGPD, licence duale (MIT + ETHICS.md) |
| Propriété intellectuelle | [[Hermine]] ⬜ | Brevets, FTO (Freedom to Operate) |
| IoT transverse | [[Araignée]] 🕷️ | Interface avec projet IoT van |
| Protocoles, câblage | Fourmi 🐜 | Banc de test, mesures, PPK2 |

---

## 6. Travail restant avant M-02

### ⛔️ Bloquant — chemin critique M-02
- [ ] **🔴 Benchmark Edge AI ESP32-S3** — test filtre animal/non-animal sur cible réelle, mesure temps d'inférence ([[Forge]] + [[Nova]]). **C'est le chemin critique de M-02**
- [ ] **🔴 Impact énergétique Edge AI** — mesure via PPK2, vérification cible 60 jours autonomie ([[Bruno]] + [[Forge]]). Sans ce chiffre, M-02 n'est pas valide
- [ ] **🔴 ADR-012 (stratégie de test)** — définit le protocole de validation M-02 : ordre des tests, critères de passage, outils (PPK2, mire optique, simulateur LoRa)
- [ ] **🔴 ADR-013 (format payload LoRa)** — sans ce format, rien à transmettre ni à tester sur banc

### 🟡 En cours (non bloquant M-02)
- [ ] ADR-006 (boîtier IP67) — nécessaire pour M-03 terrain, pas pour M-02 laboratoire
- [ ] ADR-011 (provisioning clés) — sécurité, nécessaire pour M-03
- [ ] Dual-license (MIT + ETHICS) — en attente [[Renard]] + [[Hermine]]
- [ ] Template signalétique terrain — en attente [[Renard]]

### Fait
- [x] 11 ADR rédigés et validés
- [x] Budget cadré
- [x] Registre fournisseurs avec alternatives
- [x] Glossaire pour nouveaux entrants
- [x] Périmètre P0 verrouillé (scope lock)
- [x] 48 tâches dans Plane (PKA Kanban)

---

## 7. Risques principaux

| Risque | Niveau | Mitigation |
|--------|--------|------------|
| Undervoltage ESP32-S3 | ⚠️ | Alim stabilisée, test PPK2 |
| Corruption microSD | ⚠️ | Carte industrielle, filesystem adapté |
| **Performance Edge AI insuffisante** | 🔴 **Chemin critique M-02** | Benchmark ESP32-S3 prioritaire ; si >3s/trame → revoir architecture |
| Portée LoRa insuffisante | 🟡 | Test terrain avant déploiement final |
| Dérive de périmètre P0 | 🟢 | Scope lock documenté et rappelé |

---

## 8. En résumé

```
M-01 gelé   →   M-02 prototype   →   M-03 terrain   →   M-04 publication
✅ atteint       🔴 en préparation    🔴 TBD             🔴 TBD
```

WildNexus est un projet bien cadré, avec une architecture documentée, une équipe assignée, et un budget maîtrisé. Le premier prototype sur table (M-02) est l'étape critique suivante — assembler et faire fonctionner l'ESP32-S3 + caméra + radio + stockage pour la première fois.

---

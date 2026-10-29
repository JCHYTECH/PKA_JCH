# Arbor Analysis — WildNexus Product Line
> Dobby 🦉 — Protocole Arbor OBSERVE → IDEATE → DECIDE
> 2026-06-19 — Suite à la réorganisation structurelle

---

## PHASE 1 : OBSERVE — État actuel du master WildNexus

### Sources analysées
- `MASTER_ARCHITECTURE_WN.md` (706 lignes) — phases P0/P1/P2, variantes BASIC/ADVANCED
- `wildnexus-founding-document-v0.2.md` (831 lignes) — vision, non-négociables, budget
- `WILDNEXUS_P0_SCOPE_LOCK.md` — verrou de périmètre
- `wildnexus-usage-matrix.md` — cas d'usage par persona
- 14 ADRs — décisions architecturales
- `05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md` — logigramme multi-étages
- `etat-projets.md` — statut actuel (🟡 firmware, deadline 30/06)

### Ce qui est déjà défini

| Phase | Contenu | Statut |
|-------|---------|--------|
| **P0** | Nœud caméra autonome : capture jour/nuit, détection événementielle, filtre animal/non-animal, LoRa événementiel, stockage local, config smartphone, autonomie 60j (AA L91), IP67 | En cours — M-02 prototype banc |
| **P1** | Bioacoustique, IA embarquée, reconnaissance espèces, synchronisation multi-capteurs, gateways locales, exports scientifiques | Deferred |
| **P2** | Architecture plugins, API publique, SDK, réseau collaboratif, cloud scientifique, orchestration multi-sites | Future |

### Bottlenecks identifiés

1. **Pas de produit intermédiaire entre P0 (MVP) et P1 (ADVANCED)** — le gap est trop large. Un naturaliste qui adopte le MVP n'a pas de chemin d'upgrade incrémental.
2. **Bioacoustique absorbée par WildNexus** — extraite en NEXUS_ACOUSTIC (19/06), mais le lien produit n'est pas défini : est-ce un module hardware ? un produit standalone ? un add-on ?
3. **Pas de définition de « flagship »** — la vision « infrastructure autonome distribuée » est claire, mais le produit qui l'incarne ne l'est pas.
4. **Monétisation absente** — usage-matrix définit les personas, pas les modèles économiques par produit.
5. **Pas de différentiation claire entre les produits** — qu'est-ce qui fait qu'un utilisateur achète ADVANCED plutôt que BASIC ?

---

## PHASE 2 : IDEATE — Hypothèses de ligne produit

### Hypothèse A : Ligne 5 produits (MVP → BASIC → ADVANCED → PRO → NEXUS)

**Mécanisme :** Définir 5 produits distincts avec des gaps incrémentaux, chacun débloquant un nouveau cas d'usage.

| Produit | Phase | Hardware | Intelligence | Connectivité | Prix cible |
|---------|-------|----------|-------------|-------------|------------|
| **MVP** | P0 | ESP32-S3 + OV5640 + PIR + AA 6× | Binaire (animal/non-animal) | LoRa P2P (alertes) | ~80-120€ |
| **BASIC** | P0+ | MVP industrialisé (PCB pro, enclosure IP67) | Binaire optimisé | LoRa P2P + config BTLE | ~150-200€ |
| **ADVANCED** | P1 | BASIC + micro MEMS + LiFePO4 + petit panneau solaire | Espèces (FOMO/EdgeImpulse) + acoustique | LoRaWAN + gateway locale | ~300-400€ |
| **PRO** | P1+ | ADVANCED + LTE + capteurs env (T/H/P) + GPS | Multi-taxons + corrélation | LTE + WiFi + cloud | ~500-700€ |
| **NEXUS** | P2 | PRO × N en réseau maillé | Orchestration multi-capteurs + edge→cloud | LoRa mesh + LTE + WiFi + API | Station ~400€ + cloud |

**Histoire causale :** Chaque produit débloque un nouveau persona (naturaliste amateur → association → réserve naturelle → chercheur → réseau collaboratif). Le gap entre chaque produit est un saut de connectivité ou d'intelligence, pas un redesign complet.

**Critère de succès :** Un utilisateur BASIC peut upgrader vers ADVANCED en ajoutant un module et en flashant un firmware. Pas besoin de racheter le boîtier.

### Hypothèse B : Modularité hardware dès BASIC

**Mécanisme :** Le BASIC n'est pas un produit figé mais une plateforme modulaire avec 3 slots d'extension (capteur, radio, stockage). L'ADVANCED = BASIC + module acoustique + module solaire. Le PRO = ADVANCED + module LTE.

**Histoire causale :** La vision fondatrice insiste sur la modularité. La rendre physique (slots) plutôt que logicielle (plugins) fidélise l'utilisateur et réduit les SKU.

**Risque :** Complexité mécanique (connecteurs IP67, compatibilité électromagnétique). Coût du boîtier modulaire plus élevé.

### Hypothèse C : Deux lignes parallèles — FIELD et STATION

**Mécanisme :** Plutôt qu'une gamme linéaire, deux familles :
- **FIELD** : nœuds terrain ultra low-power (AA, binaire, LoRa) — déployables en nombre
- **STATION** : nœuds haute capacité (solaire, IA, LTE, bioacoustique) — 1 par site, fait gateway pour les FIELD

**Histoire causale :** La Master Architecture définit déjà une hiérarchie « satellite → gateway ». Un FIELD déployé à 20 exemplaires + 1 STATION par site = couverture dense à coût contrôlé.

### Hypothèse D : NEXUS_ACOUSTIC comme produit standalone + module WildNexus

**Mécanisme :** NEXUS_ACOUSTIC n'est pas qu'un sous-projet — c'est un produit autonome (station bioacoustique RPi + BirdNET) qui peut aussi se vendre comme module additionnel pour WildNexus ADVANCED.

**Histoire causale :** Le marché « monitoring acoustique » existe déjà (BirdWeather PUC, AudioMoth, Swift). NEXUS_ACOUSTIC y entre avec un positionnement ouvert et scientifique, puis se greffe sur WildNexus pour la corrélation multimodale.

---

## PHASE 3 : DECIDE — Ligne produit recommandée

### Décision : Hypothèse A + C + D combinées

**Ligne FIELD (nœuds terrain) :**

| # | Produit | Description | Prix | Marché |
|---|---------|-------------|------|--------|
| F1 | **WildNexus FIELD** | Nœud caméra autonome AA, PIR, binaire, LoRa, SD, IP67 | ~150€ | Naturalistes, associations |
| F2 | **WildNexus FIELD+** | F1 + micro acoustique + solaire LiFePO4 | ~300€ | Réserves, chercheurs terrain |

**Ligne STATION (gateway + intelligence) :**

| # | Produit | Description | Prix | Marché |
|---|---------|-------------|------|--------|
| S1 | **WildNexus STATION** | Gateway LoRa→WiFi/LTE + dashboard local + stockage | ~400€ | Gestionnaires de site |
| S2 | **WildNexus STATION+** | S1 + IA espèces (multi-taxons) + corrélation | ~700€ | Chercheurs, labs |

**Produit standalone :**

| # | Produit | Description | Prix | Marché |
|---|---------|-------------|------|--------|
| A1 | **Nexus Acoustic** | Station bioacoustique RPi + BirdNET + API | ~250€ | Bioacousticiens, ornithologues |

**Chemin d'adoption naturel :**
```
Naturaliste amateur → FIELD ×1 (découvre)
                    → FIELD ×3 + STATION ×1 (couvre son terrain)
                    → FIELD+ ×1 + STATION+ ×1 (passe en mode recherche)
                    → Nexus Acoustic ×1 (ajoute la bioacoustique)
```

### Pourquoi cette structure

1. **Sépare le matériel de terrain (FIELD, pas cher, déployable en nombre) des stations (STATION, plus chères, 1 par site)** — chaque produit a une raison d'être distincte.
2. **Pas de « flagship qui fait tout »** — le flagship WildNexus, c'est le RÉSEAU FIELD + STATION, pas un produit unique. La valeur est dans le système.
3. **NEXUS_ACOUSTIC est standalone** — ne force pas l'achat d'une caméra pour faire de la bioacoustique. Marché distinct.
4. **Prix croissants, gaps franchissables** — FIELD → FIELD+ (ajout module), pas de rachat complet.

### Prochaines étapes

1. Valider cette ligne produit avec JCH
2. Intégrer dans le Master Architecture (section 4 actuelle → ligne produit détaillée)
3. Créer une fiche produit par variante (specs, BOM, prix, marché)
4. Mettre à jour `wildnexus-usage-matrix.md` avec les nouveaux personas
5. Roadmap : FIELD MVP livré P0 → FIELD+ et STATION en P1 → Nexus Acoustic indépendant

---

*Analyse Arbor : OBSERVE (Master Architecture + Scope Lock + 14 ADRs) → IDEATE (4 hypothèses de ligne produit) → DECIDE (FIELD/STATION + Nexus Acoustic).*

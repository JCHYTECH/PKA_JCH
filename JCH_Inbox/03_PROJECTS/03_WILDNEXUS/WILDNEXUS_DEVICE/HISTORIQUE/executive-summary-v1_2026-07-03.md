# WildNexus — Executive Summary

> Document externe — investisseurs, partenaires, banquiers.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**WildNexus est un réseau de caméras-pièges autonomes à intelligence embarquée qui identifie et cartographie la faune en temps réel, sans infrastructure cloud.**

---

## Le problème

Les caméras-pièges traditionnelles capturent des milliers d'images — 90% de faux déclenchements (vent, végétation). Un chercheur ou un gestionnaire de réserve passe des **heures à trier manuellement**. Résultat : les données exploitables arrivent trop tard, ou jamais.

---

## Notre solution

Un nœud autonome (ESP32-S3 + caméra + IA embarquée + LoRa) qui :
- **Capture** — déclenchement intelligent (PIR + analyse IA locale)
- **Filtre** — classification embarquée (espèce, comportement)
- **Transmet** — radio longue portée LoRa (5-15 km), zéro abonnement cellulaire
- **Alimente** — panneau solaire intégré, autonomie multi-saisons

Les données remontent à une **Station** locale (Raspberry Pi) qui consolide et expose l'information via un dashboard.

---

## Le marché

- **Marché primaire** : réserves naturelles, parcs nationaux, associations de protection (France : 350+ réserves, 11 parcs nationaux)
- **Marché secondaire** : recherche académique (écologie, éthologie, bioacoustique)
- **Budget typique** : 5 000-50 000€ par site de suivi faune
- **Concurrence** : Reconyx, Bushnell (caméras classiques, pas d'IA), Arducam (modules, pas de système intégré)
- **Différenciation** : IA embarquée + LoRa + solaire = **zéro intervention humaine après installation**

---

## Gamme produit

| Produit | Prix cible | Phase | Description |
|---------|-----------|-------|-------------|
| **WildNexus FIELD** | 149-179€ | P0 (2026) | Nœud caméra-piège IA + LoRa + solaire |
| **WildNexus FIELD+** | 299-349€ | P1 (2027) | Multi-capteurs (caméra + micro + météo) |
| **WildNexus STATION** | 249-299€ | P1 | Hub local de réception et dashboard |
| **WildNexus STATION+** | 599-799€ | P1+ | Station renforcée multi-nœuds |
| **Nexus Acoustic** | 249-299€ | P1 | Station bioacoustique (chauves-souris, insectes, oiseaux) |

---

## Modèle économique

- **Vente matériel** : 149-799€ par unité (marge estimée 45-55%)
- **Licence logicielle** : dual-licensing (open source gratuit pour usage non commercial, licence payante pour usage professionnel/gouvernemental)
- **Marché cible an 3** : 5 000 unités/an → CA matériel ~1M€ + licences

---

## Roadmap

| Phase | Période | Jalon |
|-------|---------|-------|
| **M-01** | ✅ Complété | Architecture gelée |
| **M-02** | Q3 2026 | Prototype banc — test harness caméra (15 juillet) |
| **M-03** | Q4 2026 | EVT validé — prototype terrain |
| **M-04** | Q1 2027 | Publication open source + pré-séries |

---

## Propriété intellectuelle

- Marque « WildNexus » déposée (JCHYTECH)
- Hardware open source (CERN OHL v2)
- Logiciel dual-license (AGPL v3 / licence commerciale)
- Brevets : analyse FTO en cours

---

## L'équipe

- **Jean-Claude Havaux** — Fondateur, zoologiste (ULiège), photographe naturaliste
- **PKA_JCH** — Équipe de 31 spécialistes IA pilotée par Dobby 🦉 (orchestrateur IA)

---

## Budget actuel

- **Dépensé à date** : ~280€ (composants prototype M-02)
- **À commander** : ~279€ (panier Mouser — LoRa + connectique)
- **Budget total P0** : 1 000€

---

*Document destiné à un public externe. Version détaillée : `01_FOUNDATION/wildnexus-founding-document-v0.2.md`*

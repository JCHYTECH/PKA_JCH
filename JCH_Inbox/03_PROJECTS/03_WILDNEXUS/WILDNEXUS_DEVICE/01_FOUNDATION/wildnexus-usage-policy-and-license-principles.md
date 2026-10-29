# WildNexus — Usage Policy And License Principles

**Version :** v0.2  
**Date :** 2026-06-30  
**Statut :** Draft de travail — aligné avec ADR-010 §6  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Owner juridique :** [[Renard]]  

## 1. Purpose

Ce document fixe les principes directeurs de la future licence et de la politique d'usage WildNexus.

Il ne remplace pas le texte juridique final. Il sert de base de cadrage pour :
- la rédaction de la licence cœur
- la politique d'usage opposable aux tiers
- les contrats partenaires et commerciaux
- la cohérence entre la communication publique et la réalité juridique

## 2. Core Position — Dual-License (aligné ADR-010 §6)

> **Décision ADR-010 §6 (révisée 2026-06-08) :** WildNexus adopte un modèle **dual-license** :
> - **MIT** pour le code (compatible OSI, écosystème open-source standard)
> - **ETHICS.md** (addendum éthique) à la racine du dépôt, contraignant pour tout utilisateur par simple usage

Ce modèle remplace la position initiale `source-available / ethical-source` qui n'était pas compatible OSI.

Le projet assume donc une position claire :
- publication du code sous licence MIT (ouverte, OSI-compatible)
- addendum éthique ETHICS.md interdisant certains usages (militaire, surveillance, anti-environnemental)
- interdiction explicite de certains usages et secteurs dans les termes d'utilisation

> ⚠️ La formulation exacte de l'addendum ETHICS.md et sa portée juridique doivent être validées par [[Hermine]] (propriété intellectuelle) et [[Renard]] (droit des contrats) avant publication du dépôt public (M-04).

## 3. What Must Stay Open In Practice

Même sous licence MIT + ETHICS.md, WildNexus doit rester effectivement inspectable et contributif.

Le socle doit donc garantir :
- accès public au code source cœur
- accès public aux schémas matériels et à la BOM de référence
- documentation de build, flash et reproduction
- historique de versions et changements traçables
- possibilité de proposer des contributions externes
- documentation claire des interfaces d'extension

Le projet ne doit pas recréer une fermeture de fait par :
- dépendances binaires opaques non justifiées
- documentation volontairement insuffisante
- verrouillage artificiel du hardware
- clauses de contribution dissuasives ou incohérentes

## 4. Explicitly Forbidden Uses

Les usages ci-dessous doivent être interdits explicitement dans ETHICS.md et repris dans les documents contractuels associés.

### 4.1 Military and Paramilitary

Interdits :
- détection de drones
- surveillance de périmètre défensif ou offensif
- reconnaissance de terrain à finalité militaire
- aide à la planification tactique
- intégration dans un système de défense, de police militarisée ou d'armement

### 4.2 Anti-Environmental Or Harmful Uses

Interdits :
- braconnage
- repérage de la faune à des fins de destruction ou de capture non conforme
- exploitation extractive utilisant WildNexus pour contourner des protections environnementales
- surveillance destinée à faciliter des activités contraires à la restauration ou à la protection de la biodiversité

### 4.3 Misuse Of Human Data

Interdits sauf base légale explicite et cadre contractuel spécifique :
- exploitation d'images de personnes à des fins de surveillance générale
- profilage humain
- reconnaissance faciale
- transmission ou vente de données humaines capturées incidentellement

## 5. Conditionally Allowed Uses

Certains usages peuvent être permis mais seulement sous conditions documentées.

Exemples :
- recherche académique ou institutionnelle
- déploiement par ONG, réserves, communes, associations
- intégration par un partenaire commercial aligné avec la mission
- adaptation technique à un autre contexte écologique

Conditions minimales :
- respect intégral des exclusions d'usage
- conservation des mentions de provenance et des notices applicables
- absence de fermeture artificielle du socle partagé
- respect des obligations RGPD et terrain

## 6. Relationship Between License And Contracts

Le dispositif WildNexus doit fonctionner en couches cohérentes :

1. **Licence cœur (MIT)**
Elle porte la publication du code et la compatibilité OSI.

2. **ETHICS.md (addendum éthique)**
Elle porte les exclusions d'usage principales (militaire, surveillance, anti-environnemental).

3. **Politique d'usage**
Elle explicite les cas interdits, sensibles ou ambigus avec des exemples concrets.

4. **Contrats commerciaux et partenaires**
Ils reprennent les exclusions, les obligations de conformité, la gestion des données et les conditions de marque/distribution.

5. **Politique de marque et de communication**
Elle évite qu'un tiers se présente abusivement comme représentant WildNexus ou comme compatible sans validation.

## 7. Public Terminology Rules

La communication publique doit rester juridiquement cohérente.

Formulations à privilégier :
- `open source` (code sous MIT)
- `licence MIT + addendum éthique`
- `code et schémas publiés`
- `auditable`
- `contributif`
- `licence avec exclusions d'usage éthiques`

Formulations à éviter :
- `OSI-approved` seul (sans mentionner ETHICS.md)
- `open hardware` au sens strict si la licence contient des restrictions de domaine
- `source-available` (réservé aux licences non-OSI — remplacé par MIT depuis ADR-010 §6)

## 8. Governance

### 8.1 Decision Owner

[[Renard]] pilote :
- la rédaction de ETHICS.md
- la politique d'usage
- les clauses contractuelles partenaires et commerciaux
- l'alignement avec les obligations RGPD et terrain

### 8.2 External Counsel

Un conseil IP/juridique externe peut être mobilisé pour :
- valider la robustesse des clauses
- articuler licence, politique d'usage et contrats
- analyser les sujets brevets/FTO
- limiter les contradictions entre ambition éthique et opposabilité réelle

### 8.3 JCH Validation

Les éléments suivants exigent validation explicite JCH :
- définition finale des usages interdits
- niveau d'ouverture permis aux tiers
- politique commerciale associée
- texte final de ETHICS.md ou du dispositif principal

## 9. Immediate Drafting Outputs

Les prochains livrables juridiques à produire sont :
- un texte court de `ETHICS.md` (addendum éthique)
- une première `usage policy` formalisée
- une matrice `allowed / forbidden / conditional` (déjà existante — cf. `wildnexus-usage-matrix.md`)
- une note de terminologie publique pour cohérence communication/juridique

## 10. Non-Negotiable Integrity Check

Tout texte final devra respecter simultanément ces quatre conditions :
- WildNexus reste techniquement publiable et auditable
- les exclusions d'usage sont explicites et assumées
- la terminologie publique n'est pas trompeuse
- la mission biodiversité prime sur l'optimisation commerciale

---

*Mis à jour v0.2 le 2026-06-30 — alignement avec ADR-010 §6 (dual-license MIT + ETHICS.md), terminologie corrigée.*

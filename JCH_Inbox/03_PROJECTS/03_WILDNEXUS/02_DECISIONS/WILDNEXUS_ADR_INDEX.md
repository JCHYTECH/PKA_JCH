# WildNexus — ADR Index

**Version :** v0.2  
**Date :** 2026-05-18  
**Statut :** Ouvert  
**Owner :** Dobby + Forge  

## 1. Objet

Les ADR documentent les décisions techniques qui structurent P0. Chaque ADR doit expliquer le contexte, la décision, les alternatives et les conséquences.

## 2. ADR à produire pour M-01

| ADR | Sujet | Owner PKA | Agent WildNexus | Statut |
|---|---|---|---|---|
| [ADR-001](ADR/ADR-001-choix-mcu-p0.md) | Choix MCU P0 | Castor + Forge | `wildnexus-firmware-ulp` | **Accepté** |
| [ADR-002](ADR/ADR-002-choix-camera-ir-p0.md) | Choix caméra / IR P0 | Nova + Lynx | `wildnexus-camera-imaging` | **Accepté** |
| [ADR-003](ADR/ADR-003-choix-radio-lpwan-p0.md) | Choix radio / LPWAN P0 | Forge + Chouette | `wildnexus-rf-propagation` | **Accepté** |
| ADR-004 | Stockage local | Castor + Forge | `wildnexus-firmware-ulp` | À produire |
| [ADR-005](ADR/ADR-005-energie-autonomie-p0.md) | Énergie et autonomie P0 | Bruno + Chouette | `wildnexus-hardware-physical` | Proposé |
| [ADR-006](ADR/ADR-006-boitier-ip67-montage-terrain.md) | Boîtier IP67 et montage terrain | Chouette | `wildnexus-hardware-physical` | Proposé |
| ADR-007 | Détection événementielle | Nova + Forge | `wildnexus-edge-ai-cv` | À produire |
| ADR-008 | Interface capteurs extensible | Castor | `wildnexus-program-manager-system-architect` | À produire |

## 3. Template ADR

```markdown
# ADR-XXX — Titre

**Date :** YYYY-MM-DD
**Statut :** proposé / accepté / remplacé
**Owner :** spécialiste PKA
**Agent WildNexus :** agent

## Contexte

## Décision

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|

## Conséquences

## Critère de révision
```

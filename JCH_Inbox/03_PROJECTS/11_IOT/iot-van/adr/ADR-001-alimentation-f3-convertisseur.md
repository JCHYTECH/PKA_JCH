# ADR-001 — Alimentation RPi 5 sur circuit F3 DS300

**Date :** 2026-06-04
**Statut :** proposé
**Owner PKA :** [[Chouette]] + [[Forge]]
**Jalon :** Phase 2 — Installation van

## Contexte

Le RPi 5 doit être alimenté en 5.1V / 5A stable depuis la batterie cellule du van. Le circuit électrique d'origine est centralisé par le CBE DS300.

Trois options d'alimentation étaient envisageables :
- Bloc secteur 230V → double conversion AC/DC + DC/DC, perte énergétique, dépendant de l'onduleur
- Branchement direct batterie → simple mais nécessite perçage et câble longue distance
- Dérivation sur circuit fusible existant → pas de perçage, pas de coupe de fil d'origine

## Décision

**Alimenter le RPi 5 via un porte-fusible dérivateur (add-a-circuit) sur le circuit F3 (10A — Prises 12V) du CBE DS300**, avec un fusible dédié de 5A, un interrupteur 12V, et un convertisseur DC-DC 12V→5V USB-C PD 5A.

Le fil de masse est raccordé au goujon de masse -B2 du DS300 (pas au châssis Ford — colles structurelles isolantes).

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| Porte-fusible F3 + DC-DC | Pas de modification irréversible ; réversible en 5 min ; pas de perçage | Nécessite confirmer que F3 n'est pas saturé par les prises 12V existantes | **Retenu** |
| Branchement direct batterie via fusible dédié | Tension stable, circuit dédié | Perçage cloison, câble plus long, modifie le faisceau d'origine | Écarté — non-réversible |
| Bloc secteur 230V | Simple, déjà au van | Double conversion (230V→12V→5V), perte 20-30%, dépend de l'onduleur | Écarté — inefficace |
| Alimentation via prise allume-cigares | Aucune modification | Connecteur instable sur route, pas de fusible dédié, partage avec d'autres usages | Écarté — fiabilité |

## Conséquences

- ✅ Garantie préservée — aucun fil d'origine coupé, tout est dérivable
- ✅ Réversible en moins de 5 minutes
- ✅ Fusible dédié 5A dimensionné pour RPi 5 (pic 5A = 25W, max théorique)
- ✅ Convertisseur DC-DC certifié isolé évite les boucles de masse
- ⚠️ F3 alimente aussi les prises 12V existantes — vérifier que la charge cumulée reste < 10A
- ⚠️ Le câble USB-C PD 5A avec e-mark est obligatoire — sans lui, undervoltage chronique

## Critère de révision

Revoir si le RPi 5 subit des reboots ou une tension mesurée < 4.9V en charge. Alternative : passer sur F3 direct avec un convertisseur plus puissant (5.2V / 5A).

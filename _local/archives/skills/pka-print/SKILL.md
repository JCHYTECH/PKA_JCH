---
name: pka-print
description: Imprimer un document sur l'imprimante EPSON ET-8550 (ou autre) via CUPS — conversion propre en PDF (pandoc + xelatex, gestion CJK) puis impression. Déclencher sur "imprime", "print", "imprime le brouillon", "imprime ce document".
---

# Skill — pka-print

Impression CUPS fiable depuis le M5. Le point dur est la **conversion** : imprimer un `.md`/`.txt` brut via `lp` produit une page blanche (le filtre texte de CUPS ne gère pas l'UTF-8/CJK). Ce skill passe par un **PDF propre** (pandoc + xelatex) avant d'imprimer.

## Déclencheur
- « imprime <fichier> », « print », « imprime le brouillon », « imprime ce document »
- « imprime <fichier> en recto-verso », « imprime en 2 exemplaires »

## Procédure
1. `bin/pka-print <fichier>` — imprime **recto seul** sur l'EPSON (défaut)
2. `bin/pka-print <fichier> --duplex` — recto-verso
3. `bin/pka-print <fichier> --copies 2` — plusieurs exemplaires
4. `bin/pka-print <fichier> --dry-run` — convertit sans imprimer (vérification avant envoi)
5. `bin/pka-print --list` — lister les imprimantes disponibles

## Formats supportés
- `.md`, `.txt`, `.docx`, `.html`, `.odt` → convertis en PDF (pandoc + **xelatex**, police CJK `PingFang SC`)
- `.pdf` → imprimé directement

## Notes
- **Recto seul par défaut** (`lp -o sides=one-sided`) — l'EPSON imprime sinon en recto-verso.
- Imprimante par défaut : **EPSON ET-8550** (résolue via `lpstat -d` ; `--printer` pour la Canon).
- Glyphes non rendus par Helvetica nettoyés automatiquement (🦉, →, ↔).
- Marge 2,5 cm, police Helvetica.

## Voir aussi
- `pandoc` + `xelatex` (prérequis : tous deux installés sur le M5)
- `lpstat -p` / `lpstat -d` pour lister les imprimantes et la défaut

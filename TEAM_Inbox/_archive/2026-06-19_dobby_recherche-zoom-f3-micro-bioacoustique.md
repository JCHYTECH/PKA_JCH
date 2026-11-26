# Setup Bioacoustique Pro — Zoom F3 + micro externe
> Recherche pour PKA-JCH / InsectNet
> 2026-06-19 par Dobby 🦉

---

## Zoom F3 — L'enregistreur

| Spécification | Valeur | Pourquoi ça compte |
|---------------|--------|--------------------|
| Format | 32-bit float WAV | **Pas besoin de régler le gain** — impossible de saturer. Un grillon à 50 cm ou un coup de vent, tout est capté sans écrêtage. |
| Fréquence max | 192 kHz | Capture jusqu'à 96 kHz → couvre l'ultrason des chauves-souris et des sauterelles haute fréquence |
| Préamplis | 2× XLR, bruit −127 dBu | 127 dB de rapport signal/bruit — le bruit du préampli est plus bas que le bruit ambiant d'une forêt la nuit |
| Alimentation fantôme | +24V / +48V switchable | Alimente les micros électret professionnels (LOM, Sennheiser, Avisoft) |
| Poids | 170g | Moins lourd qu'un iPhone |
| Autonomie | 2×AA (~8h) ou USB-C | Une nuit complète d'enregistrement |
| Prix | ~200-250€ | |

### Pourquoi 32-bit float change tout

Avec un enregistreur classique (16 ou 24-bit), tu dois régler le gain AVANT d'enregistrer. Trop bas → le signal est noyé dans le bruit. Trop haut → saturation. Avec le 32-bit float, le gain est virtuel — tu ajustes en post-production. C'est comme photographier en RAW au lieu de JPEG. Pour la bioacoustique de terrain où un grillon peut chanter à 50 cm puis s'arrêter net, c'est révolutionnaire.

---

## Microphones recommandés (3 niveaux)

### Niveau 1 — LOM MikroUši Pro (~180€)

| Spécification | Valeur |
|---------------|--------|
| Type | Électret omnidirectionnel, paire stéréo appairée |
| Réponse en fréquence | 20 Hz – 60+ kHz |
| Diamètre | 6.8 mm (minuscule — se camoufle dans l'herbe) |
| Alimentation | Phantom +48V (fourni par le Zoom F3) |
| Sensibilité | Très élevée — conçu pour les sons faibles |
| Bruit propre | Exceptionnellement bas |

**Pour :** léger, discret, couvre l'ultrason, stéréo naturelle. Le choix des field recordists et bioacousticiens européens.

### Niveau 2 — Avisoft CM16/CMPA (~400€)

| Spécification | Valeur |
|---------------|--------|
| Type | Condensateur à polarisation permanente |
| Réponse en fréquence | 2 kHz – 150 kHz |
| Particularité | Conçu **spécifiquement** pour la bioacoustique |
| Bruit propre | Très bas, optimisé pour les signaux faibles |

**Pour :** la référence scientifique. Utilisé dans les publications académiques. Si tu veux publier les données InsectNet, c'est le standard.

### Niveau 3 — Sennheiser MKH 8020 (~1200€)

| Spécification | Valeur |
|---------------|--------|
| Type | Condensateur RF |
| Réponse en fréquence | 10 Hz – 60 kHz |
| Bruit propre | 10 dBA (parmi les plus bas au monde) |
| Robustesse | Insensible à l'humidité (condensation) |

**Pour :** l'excellence absolue. Prix élevé mais insensible à l'humidité — crucial pour l'enregistrement nocturne en prairie où la rosée tue les micros électret.

---

## Budget total

| Configuration | Enregistreur | Micro | Total |
|--------------|-------------|-------|-------|
| **Essentiel** | Zoom F3 (220€) | LOM MikroUši Pro (180€) | **~400€** |
| **Scientifique** | Zoom F3 (220€) | Avisoft CM16 (400€) | **~620€** |
| **Pro** | Zoom F3 (220€) | Sennheiser MKH 8020 (1200€) | **~1420€** |

---

## Comparaison avec l'iPhone

| Critère | iPhone 17 Pro Max | Zoom F3 + LOM |
|---------|-------------------|---------------|
| Format | AAC compressé | WAV 32-bit float |
| Gain | Automatique (imprévisible) | Pas de gain — 32-bit float |
| Fréquence max | 24 kHz (48 kHz SR) | 96 kHz (192 kHz SR) |
| Bruit de fond (2-8 kHz) | −1 dB | −10 dB estimé |
| Dynamique utile | ~50 dB | >120 dB |
| Stéréo | Oui (4 micros intégrés) | Oui (2 micros externes séparables) |
| Séparation spatiale | Fixe (espacement iPhone) | Variable (tu écartes les micros comme tu veux) |
| Robustesse humidité | Faible | Micros électret = sensibles ; MKH 8020 = immunisé |
| Prix | Déjà dans ta poche | ~400€ |

---

## Recommandation pour InsectNet

La config **Essentiel (Zoom F3 + LOM MikroUši Pro, ~400€)** est le sweet spot. Elle te permet de :
- Capturer en 192 kHz → couvrir les sauterelles ultrasoniques que l'iPhone ne capte pas
- Placer les micros près du sol sans toucher l'enregistreur (les 2 micros sont sur câble, le F3 reste dans ta poche)
- Faire de la vraie stéréo spatiale avec espacement contrôlé (bien meilleur que l'iPhone pour l'identification individuelle)
- Ne jamais saturer même si le grillon se met à chanter juste devant le micro

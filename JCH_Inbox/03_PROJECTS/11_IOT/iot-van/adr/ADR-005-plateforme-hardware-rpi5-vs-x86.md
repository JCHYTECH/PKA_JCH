# ADR-005 — Plateforme hardware : RPi 5 armuré vs x86 industrialisé

**Date :** 2026-06-21
**Statut :** accepté
**Owner PKA :** [[Dobby]] + [[Forge]]
**Jalon :** Phase 1 — Prototype banc maison

## Contexte

Le projet IOT Vanlife prévoit un serveur Home Assistant embarqué dans le Stylevan Equinox 4. La plateforme doit fonctionner en environnement véhicule : vibrations, chocs, variations de température (−10°C à +50°C), humidité, alimentation 12V batterie cellule, autonomie électrique critique (150 Ah LiFePO4, 300W solaire).

Le guide existant (`rpi-vanlife-guide-complet.md`) documente un RPi 4/5 avec SSD obligatoire. JC a soulevé la question des alternatives x86 industrialisées (Protectli, Zimaboard) pour gagner en résilience physique sans travail de montage.

## Décision

**RPi 5 (4 Go) avec durcissement complet**, selon l'architecture suivante :

| Couche | Composant | Coût |
|--------|-----------|------|
| Compute | Raspberry Pi 5, 4 Go | ~55€ |
| Stockage | NVMe HAT officiel + SSD M.2 128 Go | ~45€ |
| Refroidissement | Boîtier Argon ONE (ventilateur PWM, passif aluminium) | ~25€ |
| Alimentation | DC-DC isolé 12V→5V USB-C PD 5A + TVS + fusible PTC | ~15€ |
| Vibrations | Silentblocs M3 + standoffs silicone | ~5€ |
| Humidité | Conformal coating MG Chemicals 422B | ~15€ |
| Backup | Carte microSD 32 Go avec image HA de secours | ~5€ |
| **Total** | | **~165€** |

**Plan de résilience complémentaire :**
- Carte SD de secours préinstallée — swap en 30 secondes (vs 5-10 jours pour remplacer un mini-PC x86)
- Backup automatique de la config HA → Pi maison via Tailscale
- Zigbee autonome — bindings directs capteurs→actionneurs, indépendants de HA
- Hardware watchdog activé (`/dev/watchdog` + systemd)
- OverlayFS read-only sur la partition système

## Alternatives considérées

| Option | Pour | Contre | Verdict |
|--------|------|--------|---------|
| **RPi 5 armuré** | Écosystème HA natif, guide existant (462 lignes), 4W idle, remplaçable partout en Europe en 1h, backup SD 30s | Plage température 0-50°C, assemblage manuel 40 min | **Retenu** |
| **RPi CM5 + carrier board** | eMMC onboard (pas de SD), 12V natif, GPIO vissé | Même plage température que Pi 5, écosystème moins standard, ~80€ | Écarté — gain marginal vs Pi 5 |
| **Protectli VP2420** | −20 à 60°C, 12V natif, x86 fanless, 4 ports GbE | 10W idle (×2.5 Pi), 280€, indisponible en magasin physique, backup complexe | Écarté — conso et logistique |
| **Zimaboard 832** | 12V natif, 8W idle, x86, SATA, ~200€ | 0-50°C comme le Pi, Celeron N3450 daté, pas de GPIO | Écarté — pas de gain température |
| **Intel NUC / Beelink** | x86 standard, prix compétitif | 0-40°C (pire que Pi), ventilateur audible, pas industrialisé | Écarté — plage température insuffisante |
| **Compulab fitlet2** | −40 à 85°C, 12V, passif, grade industriel | 400€, conso ~8W idle, délai livraison, overkill | Écarté — hors budget |
| **Advantech / Kontron** | Vrai grade automobile, rail DIN, certifié | 500-600€, encombrant, délai, totalement disproportionné | Écarté — hors périmètre vanlife |

### Analyse détaillée du trade-off RPi 5 vs Protectli

| Critère | RPi 5 armuré | Protectli VP2420 | Écart |
|---------|-------------|------------------|-------|
| Coût | 165€ | 280€ | +115€ (70%) |
| Conso idle | 4W | 10W | ×2.5 — critique sur batterie |
| Autonomie 7j off-grid | 672 Wh (37% batterie) | 1680 Wh (93% batterie) | Risque frigo coupé en hiver |
| Fiabilité physique | 90% risques couverts | 95% couverts | +5% marginal |
| Remplacement terrain | 1h, n'importe où en Europe | 5-10 jours livraison | Risque immobilisation |
| Écosystème HA | Natif, guide documenté | Supporté, friction install | Temps d'adaptation |
| Backup | Carte SD swap 30s | Pas d'équivalent simple | Résilience effective |
| Montage actif | 40 min | 15 min (install OS) | 25 min d'écart |
| Bruit | Passif (ventilateur >60°C) | Fanless | Équivalent |

## Conséquences

- ✅ Capitalisation sur le guide `rpi-vanlife-guide-complet.md` existant — aucune réécriture
- ✅ Budget maîtrisé : 165€ vs 900€ d'enveloppe totale projet → 18% du budget
- ✅ Conso électrique 4W idle — viable 7 jours off-grid sans soleil
- ✅ Plan B actif — carte SD de secours + backup Tailscale automatique
- ⚠️ Le conformal coating doit être appliqué avant la première mise sous tension
- ⚠️ La résistance chauffante 5W est nécessaire si le van stationne en dessous de 0°C prolongé
- ⚠️ La ventilation de l'Argon ONE doit être testée — vérifier que le flux d'air ne crée pas d'aspiration de poussière en environnement van
- ⚠️ À réception du matériel : mesurer la conso réelle idle + load avec PPK2 (banc M-02 WildNexus), valider l'autonomie théorique
- ✅ **2026-06-22 : Geekworm X1201 UPS + boîtier X1201-C1 réceptionnés.** Ajoute une couche UPS 18650 au RPi 5 — maintient l'alimentation pendant les transitions batterie et permet un shutdown propre. Sert aussi pour NEXUS_ACOUSTIC (station BirdNET-Go terrain).

## Critère de révision

Revoir cette décision si :
- Le RPi 5 subit plus de 2 pannes matérielles en 12 mois d'usage van
- La consommation réelle mesurée dépasse 8W idle
- La température interne du van descend régulièrement sous −5°C (stationnement hivernal prolongé)
- Home Assistant annonce la fin du support ARM (peu probable)

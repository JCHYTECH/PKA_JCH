# ADR-003 — Stockage système : SSD NVMe obligatoire

**Date :** 2026-06-04
**Statut :** proposé
**Owner PKA :** [[Forge]]
**Jalon :** Phase 1 — Setup base
**Source :** Leçon directe WildNexus — corruption microSD chronique sur RPi 5

## Contexte

Le RPi 5 doit fonctionner 24h/24 dans un environnement de van :
- Vibrations permanentes (route, ralentisseurs, faux plats)
- Coupures électriques possibles (déconnexion batterie, passage à la pompe)
- Cycles d'écriture continus (logs HA, base de données SQLite, sauvegardes)

La microSD est le stockage par défaut du RPi, mais elle est notoirement fragile : corruption après coupure, dégradation des cellules NAND en écriture intensive, délogement sous vibration.

WildNexus a documenté cet échec (retour test maison RPi 5, 2026-05-28) : une microSD Samsung EVO Plus 128 Go est devenue illisible après 3 cycles de coupure intempestive.

## Décision

**Boot et système sur SSD NVMe M.2 impérativement.** Pas de microSD pour le système — la carte SD ne sert que pour le firmware du RPi (bootloader EEPROM, à jour en NVMe boot).

Configuration retenue :
- SSD NVMe M.2 128 Go (Samsung / WD)
- HAT adaptateur Pimoroni NVMe Base (compatible RPi 5, PCIe 2.0 ×1)
- HA OS flashé directement sur le SSD (Raspberry Pi Imager)

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| **SSD NVMe M.2** | +10× endurance microSD ; résistant vibrations ; connexion PCIe stable ; boot natif RPi 5 | Coût additionnel ~45 € (SSD + HAT) | **Retenu** |
| microSD Samsung EVO Plus | Zéro coût supplémentaire | Corruption documentée WildNexus sous coupure ; pas de tolérance vibration | Rejeté — leçon WildNexus |
| SSD USB 3.0 externe | Aucun HAT requis ; plug & play | Encombrement (boîtier + câble USB) ; risque déconnexion sur route ; moins rapide que NVMe | Écarté — encombrement |
| Clé USB 3.0 haute endurance | Pas de HAT, pas cher, discret | Endurance inférieure au NVMe ; dépend de la qualité du contrôleur USB | Écarté — fiabilité |

## Conséquences

- ✅ Résistance aux vibrations : SSD soudé au HAT, pas de connecteur mobile
- ✅ Endurance NVMe : typiquement 150-300 TBW, soit 10-20× une microSD grand public
- ✅ Boot natif RPi 5 : NVMe amorcé directement (périphérique PCIe)
- ✅ Coût total SSD + HAT : ~45 € (20 € SSD + 25 € Pimoroni)
- ✅ Compatible HA OS : le RPi Imager flashe directement sur le SSD via adaptateur USB

- ⚠️ Nécessite de mettre à jour le bootloader RPi 5 pour NVMe boot (rpi-eeprom -> latest)
- ⚠️ Occupation du connecteur PCIe — plus de place pour un HAT supplémentaire (mais les capteurs passent par USB/Zigbee)
- ⚠️ Message d'erreur au premier boot si bootloader non à jour

## Critère de révision

Si le SSD tombe en panne dans les 2 ans, examiner un SSD avec TBW plus élevé (Samsung 990 Pro, WD SN850X). Si le HAT Pimoroni n'est plus fabriqué, remplacer par Waveshare NVMe HAT (compatible RPi 5).

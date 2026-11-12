# Procurement IoT — Registre des acquisitions

> **Date création :** 2026-06-23
> **Dernière consolidation :** 2026-11-05
> **Projets :** 11_IOT (van, serre, maison) + NEXUS_ACOUSTIC + WILDNEXUS (base station)

---

## Besoins non commandés — consolidation au 2026-11-05

| Besoin | Contenu / base de prix | État |
|---|---|---|
| **Lot P1 van** | 10 articles : contacts, température frigo SNZB-02P, mouvement, fuite, vibration, contrôleur et ruban LED | **~121 € estimés au 01/10** ; température frigo bien incluse ; prix courants à revalider |
| **Mopeka Pro Check** | Niveau gaz, bouteille acier | **P3, ~45 € historiques**, hors P1 |
| **Geekworm X1200** | UPS RPi 5, 5,1 V/5 A, deux 18650, jauge I²C | **~50–70 € historiques, non vérifiés** ; prix courant non obtenu ; compatibilité avec le boîtier X1201-C1 à confirmer |
| **DC-DC USB-C PD 5 A** | Conversion alimentation van exigée par ADR-001 | Modèle et prix à établir |
| **Silentblocs M3 ×4** | Fixation anti-vibration du RPi | ~5 € dans un ancien panier ; prix courant à vérifier |
| **Coating MG Chemicals 422B** | Protection conforme de la carte | Anciennes estimations divergentes (~5 € / ~15 €) ; aucun montant courant retenu |

**Aucun total final de reste à payer n'est calculé** : plusieurs prix sont anciens ou manquants. Aucun achat n'a été effectué dans cette passe.

Le [wiki constructeur X1200](https://wiki.geekworm.com/X1200) confirme la sortie 5,1 V/5 A et la jauge I²C. Il associe le X1200 au boîtier **X1200-C1** et le X1201 au **X1201-C1** : la compatibilité du boîtier déjà reçu doit être vérifiée. La même documentation décrit le X1205 avec deux accus **21700**, alors que le stock IOT mentionne des 18650 ; identifier physiquement la carte et les accus avant toute commande ou tout montage.

Référence détaillée : `../iot-van/LISTE-CAPTEURS-ZIGBEE-2026-10-01.md`.

---

## Commande #1 — PV PI (Solar Power Manager RPi)

| Champ | Valeur |
|-------|-------|
| **Produit** | PV PI — PhotoVoltaic Pi HAT |
| **Fabricant** | AutoEcology (Melbourne, Australie) |
| **Créateur** | Luke Ditria (@lukeditria) |
| **Site** | https://www.auto-ecology.com/store/p/pvpi-byg2d |
| **Date commande** | 2026-06-23 |
| **Prix** | **150 AUD** (~90 €) |
| **Fenêtre pré-commande** | Jusqu'au 5 juillet 2026 |
| **Fabrication** | ~1 mois après clôture pré-commandes |
| **Livraison estimée** | **Mi-août 2026** (rappel : 15 août) |
| **Statut** | ✅ REÇU — 1er juillet 2026 (avance 6 semaines sur prévision) |

### Spécifications

- HAT Raspberry Pi 40-pin stackable
- Charge LiFePO4 12V jusqu'à 10A
- Entrée solaire 12-50V VOC avec MPPT
- RTC + watchdog + auto-reboot
- UART (pins 14, 15)
- Firmware + PV Pi Manager open source
- XT30 connecteurs (solaire + batterie)
- Livré avec : header stackable, standoffs, vis, câbles XT30

### Projets cibles

| Projet | Usage |
|--------|-------|
| **IoT van** 🔴 | Alimentation solaire RPi 5 autonome off-grid |
| **IoT serre** 🟡 | Monitoring serre Esneux 24/7 sur batterie |
| **WILDNEXUS** 🟢 | Base Nexus RPi autonome terrain |
| **NEXUS_ACOUSTIC** 🟢 | Station bioacoustique RPi outdoor |

### Notes

- Batterie LiFePO4 12V et panneau solaire à acquérir séparément
- Kit complet estimé : batterie 40-80€ + panneau 30-60€ → total ~200-250€
- PV Pi Manager open source : à cloner et tester dès réception
- Chaîne YouTube Luke Ditria : https://youtube.com/@lukeditria

---

## Commande #2 — Sonoff ZBDongle-E (maison + serre)

| Champ | Valeur |
|-------|-------|
| **Produit** | Sonoff ZBDongle-E — EFR32MG21, coordinateur Zigbee |
| **Site** | https://www.amazon.com.be/dp/B0B6P22YJC |
| **Date commande** | 2026-11-05 |
| **Prix** | Non renseigné |
| **Livraison estimée** | **2026-11-06** |
| **Statut** | ⏳ COMMANDÉ |
| **Projet cible** | 11_IOT — maison + serre |

Le premier ZBDongle-E est détecté sur le RPi `lupo` et reste affecté au van. Le second coordinateur est destiné à une installation fixe maison + serre ; son affectation au M5 ou à un autre hub sera confirmée à réception. Un seul dongle est actuellement détecté sur le RPi, dont Zigbee2MQTT est arrêté après une déconnexion/reconnexion USB.

---

*Généré par Dobby 🦉 — 2026-06-23 ; consolidé le 2026-11-05.*

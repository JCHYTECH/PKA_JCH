# Topic — Zigbee (IOT / Domotique)

> Living document maintenu par Dobby 🦉 — **mémoire détaillée du sous-thème Zigbee**.
> **Dernière mise à jour** : 2026-11-06
> **Projet** : IOT — vue d'ensemble dans `thread-iot.md`
> **Statut** : 🟡 actif (coordinateurs opérationnels, 2 capteurs à ré-appairer)

---

## Contexte du topic

Le réseau Zigbee PKA couvre deux zones distinctes : le **van Lupo** (coordinateur sur le RPi, canal 11) et la **maison/serre** (coordinateur sur le M5, canal 15, temporaire en attendant un RPi dédié). Deux dongles Sonoff ZBDongle-E.

## État détaillé

| Axe | Statut | Détail confirmé |
|-----|--------|-----------------|
| ZBDongle-E — Lupo (van) | 🟢 | Coordinateur van, canal 11. Port noyau `3-2` (déplacé le 05/11), Z2M actif + MQTT connecté. |
| ZBDongle-E — M5 (maison/serre) | 🟢 | Reçu 06/11, branché M5. Pont série `serial_bridge.py` v4 relancé, Z2M up (EmberZNet 7.4.4, canal 15). **Temporaire** en attendant un RPi dédié. |
| AirGuard Lupo (SNZB-02UL E-Ink) | 🟢 | Ré-appairé 06/11 (force-remove + permit-join + bouton). LQI 56 → **255/255**. Mesures fraîches 18,8 °C / 66,1 %. Cause racine : lien radio faible (distance). |
| AirGuard Serre (SNZB-02DR2) | 🟢 | Ré-appairé du Lupo vers le **M5** 06/11 (canal 15). Mesures fraîches 20,5 °C / 64,8 % / batterie 89 %, LQI 255/255. |
| Valve d'eau (Sonoff SWV) | 🔴 | **Périmée** (dernier contact juillet). À ré-appairer sur le M5 — à localiser physiquement. |
| LuxSerre (Aqara T1 luminosité) | 🔴 | **Périmé** (dernier contact juillet). À ré-appairer sur le M5 — à localiser physiquement. |

## Décisions du topic

- [2026-11-06] Second ZBDongle-E affecté au **M5 temporairement** (le M1 étant en décommission, le M5 voyageant) — RPi dédié permanent à prévoir.
- [2026-11-06] AirGuard Lupo : cause racine = **distance au coordinateur** (LQI 56), pas un défaut capteur. À placer près du dongle en installation finale.
- [2026-11-06] Bascule serre Lupo → M5 : force-remove + permit-join + appui bouton (procédure validée 2×).

## TTD — Pending

- [ ] **P1 · — · (Dobby)** Ré-appairer la valve d'eau + LuxSerre sur le M5 (attendre que JC les localise).
- [ ] **P2 · — · (JC)** Provisionner un RPi dédié permanent pour remplacer le M5 (maison/serre).

## TTD — Done

- [x] 2026-11-06 · AirGuard Lupo ré-appairé → LQI 255/255, mesures fraîches.
- [x] 2026-11-06 · AirGuard Serre ré-appairé Lupo → M5 → mesures fraîches.
- [x] 2026-11-06 · Second ZBDongle-E branché M5, pont série v4 relancé, Z2M opérationnel.

## Historique

| Date | Résumé |
|------|--------|
| 2026-11-06 | Ré-appairage AirGuard Lupo (distance) + bascule serre vers M5 (dongle reçu). Valve + LuxSerre identifiés périmés. |

## Liens

- Hardware : `../../04_PILOTAGE_STRATEGIQUE/hardware-state.md`
- Appairage : `iot-van/PROCEDURE-APPAIRAGE-ZIGBEE-2026-10-05.md`
- Hub Esneux : `_shared/hub-esneux.md`

---

*Topic lié depuis `thread-iot.md`. Les états confirmés priment sur les cibles. Charger ce fichier quand on travaille sur le Zigbee (plutôt que tout le thread).*

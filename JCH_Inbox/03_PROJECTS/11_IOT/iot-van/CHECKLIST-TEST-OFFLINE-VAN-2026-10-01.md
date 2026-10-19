# Checklist de test — Scénarios offline Van (Lupo)

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Phase :** 4 de la procédure de réactivation (`PROCEDURE-REACTIVATION-IOT-VAN-2026-10-01.md`)
> **Prérequis :** HA OS 18.3 opérationnel sur banc (Phase 2 terminée), hostname `lupo`, auto-update OFF.
> **Légende :** `[ ]` à tester · `🔒` bloqué (matériel manquant) · `✅` validé · `❌` échec (à documenter)

---

## 0. Pré-requis système

- [ ] HA « Healthy » (pas de `duplicate_os_install`, pas d'erreur de boot)
- [ ] Auto-update **OFF** (Settings → System → Updates)
- [ ] Hostname = `lupo`
- [ ] Backup HA fait et téléchargé sur le [M5] (fichier `.tar`)
- [ ] Accès SSH/Terminal fonctionnel (add-on Terminal & SSH)

## 1. Alarme — sécurité

- [ ] Capteur de portes Zigbee appairé et visible dans HA 🔒 (capteurs à commander)
- [ ] Ouverture d'une porte → changement d'état immédiat dans HA (< 2 s)
- [ ] Scénario « Alarme armée » : intrusion → notification + alarme locale
- [ ] Scénario « Désarmé » : ouverture sans déclenchement
- [ ] L'alarme fonctionne **sans internet** (mode autonome) ✅/❌
- [ ] Reolink Argus MagiCam : flux visible + détection mouvement → alerte 🔒/à tester

## 2. Frigo — température

- [ ] Capteur T°/H° (SNZB-02DR2) appairé, placé dans le frigo
- [ ] Température relevée et remontée dans HA
- [ ] Seuil haut/bas configuré → alerte si hors plage
- [ ] Alerte frigo **sans internet** (notification locale, pas cloud) ✅/❌
- [ ] Historique de température lisible (graphique)

## 3. Alimentation — UPS X1205 + batterie

- [ ] Coupure de l'alim USB-C → le RPi **reste sous tension** (accus 18650)
- [ ] HA détecte le passage sur batterie (entité UPS/battery)
- [ ] Retour secteur → bascule propre (pas de reboot sauvage)
- [ ] PV PI HAT : panneau solaire branché → charge la batterie 🔒 (câblage van)
- [ ] Autonomie accus testée (durée estimée en van à l'arrêt)

## 4. Cuves — niveau liquide

- [ ] Capteurs XKC-Y25-V (×4) câblés via relais/ADC → lus dans HA 🔒
- [ ] Niveau eau propre / eaux grises remonté correctement
- [ ] Seuil bas → alerte « cuve à vidanger / à remplir »
- [ ] Lecture stable (pas de valeurs fantômes sur la route)

## 5. CAN bus — WiCAN Pro

- [ ] WiCAN Pro branché sur l'OBD → connecté au HA
- [ ] Les 17+ entités véhicule remontent (vitesse, RPM, batterie, portes, pneus)
- [ ] Batterie véhicule : SOC / courant / tension lisibles
- [ ] Mode stationnement : deep sleep < 1 mA (pas de risque batterie)

## 6. Connectivité offline / Tailscale

- [ ] HA joignable en **local** (http://lupo.local:8123 ou IP locale)
- [ ] Scénarios critiques tournent **sans internet** (test en coupant le Wi-Fi du RPi)
- [ ] Tailscale : HA joignable depuis l'iPhone à distance ✅/❌
- [ ] Redémarrage propre → HA revient seul (pas de blocage)

---

## Résultat de campagne

| Section | Statut | Notes |
|---------|--------|-------|
| 0. Pré-requis | ⬜ | |
| 1. Alarme | ⬜ | 🔒 capteurs portes à commander |
| 2. Frigo | ⬜ | |
| 3. Alimentation | ⬜ | 🔒 PV PI = câblage van |
| 4. Cuves | ⬜ | 🔒 câblage capteurs |
| 5. CAN bus | ⬜ | |
| 6. Connectivité | ⬜ | |

**Go/no-go installation van :** validé si les sections 0, 2, 3 (partiel), 6 sont ✅ et que les scénarios critiques tournent en offline.

---

*Checklist générée par Dobby 🦉 — à cocher au fur et à mesure, avec trace des échecs (`❌`) dans le diagnostic.*

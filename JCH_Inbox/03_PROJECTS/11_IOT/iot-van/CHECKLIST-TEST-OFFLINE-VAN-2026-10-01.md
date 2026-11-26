# Checklist de test — Scénarios offline Van (Lupo)

> **Création :** 2026-10-01 · **Recadrage documentaire :** 2026-11-05 · Dobby 🦉
> **État :** campagne de tests non exécutée ; aucune case n'est validée par cette révision.
> **Références :** `OPERATIONS-CAN-OBD.md` et `../thread-iot.md`.
> **Légende :** `[ ]` à tester · `🔒` bloqué · `✅` validé sur preuve · `❌` échec à documenter

---

## 0. Prérequis système

- [ ] HA « Healthy » et « Supported » au moment du test ; dernier contrôle distant conforme le 05/11.
- [ ] Auto-update **sélectif** vérifié : Supervisor + modules automatiques ; HAOS/Core manuels. Ne pas appliquer l'ancienne consigne « tout désactiver ».
- [ ] Hostname = `lupo`.
- [ ] Sauvegarde HA récente et copie externe vérifiée ; la sauvegarde locale `c38337a2` du 05/11 ne prouve pas une copie sur M5.
- [ ] Accès SSH/Terminal fonctionnel ; port SSH observé `22222`.
- [ ] Zigbee2MQTT restauré après l'incident USB du 05/11 et mesures des AirGuard effectivement disponibles.
- [ ] RPi installé dans son environnement de test ; au 05/11, il est encore au bureau sur le Wi-Fi maison.

## 1. Alarme — sécurité

- [ ] Capteurs de portes Zigbee du lot P1 reçus, appairés et visibles dans HA 🔒 (non commandés au 05/11).
- [ ] Ouverture d'une porte → changement d'état mesuré dans HA.
- [ ] Scénario « Alarme armée » : intrusion → notification + alarme locale.
- [ ] Scénario « Désarmé » : ouverture sans déclenchement.
- [ ] L'alarme fonctionne **sans Internet** (mode autonome) ✅/❌.
- [ ] Reolink Argus MagiCam : flux visible + détection mouvement → alerte 🔒/à tester.

## 2. Températures — cellule et frigo

- [ ] **AirGuard Lupo = SNZB-02UL**, déjà appairé, mesure la cellule et remonte effectivement dans HA.
- [ ] **SNZB-02P frigo** reçu, appairé et placé dans le frigo 🔒 (article P1 non commandé au 05/11).
- [ ] Ne pas utiliser le **SNZB-02DR2 AirGuard Serre** comme capteur frigo : il est affecté à la serre.
- [ ] Seuils haut/bas du frigo configurés → alerte si hors plage.
- [ ] Alerte frigo **sans Internet** ✅/❌.
- [ ] Historique de température lisible (graphique).

## 3. Alimentation — UPS et batteries

- [ ] Identifier physiquement la carte X1205 et le format de ses accus avant montage : documentation constructeur 21700, stock historique 18650.
- [ ] Vérifier la compatibilité du boîtier X1201-C1 avant tout remplacement envisagé par un X1200.
- [ ] Valider la chaîne DC-DC USB-C PD 5 A et mesurer tension/throttling en charge.
- [ ] Coupure contrôlée de l'alimentation → le RPi reste sous tension.
- [ ] HA détecte le passage sur batterie (entité UPS/battery réellement disponible).
- [ ] Retour d'alimentation → bascule propre, sans reboot sauvage.
- [ ] Autonomie mesurée et consommation documentée ; aucune autonomie déduite de la seule capacité nominale.
- [ ] PV PI HAT : panneau et batterie compatibles câblés → charge vérifiée 🔒.

## 4. Cuves — niveau liquide

- [ ] Capteurs XKC-Y25-V (×4) câblés selon une interface validée → lus dans HA 🔒.
- [ ] Niveau eau propre / eaux grises comparé au niveau réel.
- [ ] Seuil bas → alerte « cuve à vidanger / à remplir ».
- [ ] Lecture stable (pas de valeurs fantômes sur la route).
- [ ] Aucun flash ESPHome avant correction du conflit GPIO8 du DS300 Tap, si ce montage est utilisé.

## 5. CAN bus — WiCAN Pro

- [ ] RUT240 alimenté, réseau local du van établi et RPi relié par Ethernet 🔒 (intervention locale).
- [ ] Montage WiCAN/Exosfer inspecté ; fonctions de l'antivol conservées.
- [ ] WiCAN Pro connecté au réseau local et publications MQTT observées.
- [ ] Appareil WiCAN et entités réelles découverts dans HA ; aucun appareil/entité CAN au 05/11.
- [ ] PIDs disponibles comparés au véhicule ; les 17+ entités restent une cible, pas un critère à falsifier.
- [ ] Batterie véhicule : SOC/courant/tension validés uniquement si exposés par le véhicule.
- [ ] Veille profonde `<1 mA` mesurée ; réveil périodique et effet sur les ECU contrôlés.
- [ ] Consommation de stationnement mesurée et cutoff testé ; ne pas conclure « sans risque batterie » par principe.

## 6. Connectivité offline / Tailscale

- [ ] HA joignable en **local** par son adresse réelle sur le réseau du van.
- [ ] Scénarios critiques testés **sans Internet**, en coupant la WAN/SIM plutôt que le LAN nécessaire aux capteurs.
- [ ] Tailscale : HA joignable depuis l'iPhone à distance ✅/❌.
- [ ] WiCAN et capteurs se reconnectent après redémarrage du RUT240 et du RPi.
- [ ] Redémarrage propre → HA revient seul, sans blocage.

---

## Résultat de campagne

| Section | Statut | Notes |
|---------|--------|-------|
| 0. Prérequis | ⬜ | Zigbee à restaurer ; campagne locale requise |
| 1. Alarme | ⬜ | 🔒 capteurs portes P1 non commandés |
| 2. Températures | ⬜ | AirGuard Lupo appairé ; SNZB-02P frigo non commandé |
| 3. Alimentation | ⬜ | Identifier UPS/accus/boîtier et valider le DC-DC |
| 4. Cuves | ⬜ | 🔒 câblage et configuration à valider |
| 5. CAN bus | ⬜ | Aucun appareil WiCAN enregistré au 05/11 |
| 6. Connectivité | ⬜ | RUT240 non connecté au 05/11 |

**Go/no-go installation van :** décision après résultats consignés pour les sections 0, 2, 3 et 6, fonctionnement offline des scénarios critiques et traitement explicite des risques CAN/alimentation. Aucun « go » n'est déduit de cette mise à jour documentaire.

---

*Checklist recadrée le 2026-11-05 : matériel réel, capteur frigo corrigé et résultats non testés laissés ouverts.*

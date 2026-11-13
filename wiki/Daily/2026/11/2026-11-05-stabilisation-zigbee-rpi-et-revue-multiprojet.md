---
date: 2026-11-05
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-05 — stabilisation-zigbee-rpi-et-revue-multiprojet

## Session — 23:57 — stabilisation-zigbee-rpi-et-revue-multiprojet

### Contexte
- Modèle : kimi-code
- Projet : 11_IOT

### Résumé
Stabilisation du Zigbee RPi après changement de port USB, validation d’AirGuard Serre, Lupo toujours sans mesure fraîche et revue documentaire WildNexus/multiprojet sans réactivation.

### Actions
- Inventaire des installations Home Assistant visibles via Tailscale et mises à jour automatiques sélectives sur le RPi.
- Appairage et affectation des AirGuard Serre et Lupo ; diagnostic du dongle Zigbee et déplacement du port noyau 1-2 vers 3-2.
- Surveillance réussie de 20:52 à 21:02, puis contrôle à 23:50 : Zigbee2MQTT actif, dongle présent, aucune nouvelle coupure USB ni sous-tension ; Serre mesuré à 22,5 °C, 55,7 %, batterie 95 %, LQI 255/255 à 23:46.
- Recherche dans les journaux Lupo : dernière trame réelle à 13:01, 20,9 °C, 51,8 %, batterie 100 %, LQI 56/255 ; les publications ultérieures sont retenues et ne prouvent pas une mesure fraîche.
- Recherche documentaire sur les alarmes CO et les risques CO en van, sans achat ni installation.
- Revue fraîche WildNexus, clarification de son organisation et revue de cohérence transverse des projets actifs, sans reprise technique.
- Invocation utilisateur /save dans Kimi validée par cette sauvegarde ; le TUI Grok reste à tester.

### Décisions
- Conserver le dongle RPi sur le port noyau 3-2 et ne pas lancer de mise à jour firmware ou Zigbee2MQTT comme correctif.
- En cas de récidive USB, tester une courte rallonge USB2 puis une alimentation officielle directe, une variable à la fois.
- Reporter au 06/11 le réveil et la vérification d’AirGuard Lupo ; ne pas le déclarer en panne sans nouvelle mesure.
- Maintenir WildNexus gelé et SOP-10 suspendue ; la passe est documentaire et ne réactive ni firmware ni achats.
- Conserver FUTURE_INVEST archivé et Ghost/Instagram en pause, sans publication.

### Prochaines étapes
- Réveiller AirGuard Lupo le 06/11 et contrôler une mesure fraîche ainsi que son LQI à distance.
- Confirmer la réception du second ZBDongle-E, puis décider son affectation maison/serre et valider le coordinateur concerné.
- Traiter séparément le service Zigbee2MQTT du M5, toujours en échec faute de dongle local.
- Intégrer localement WiCAN Pro et RUT240 au HA du van, puis valider MQTT, les entités réelles, Exosfer et la consommation.
- Tester séparément le TUI Grok ; reprendre Ghost uniquement après réponse du support et décision explicite de JC.

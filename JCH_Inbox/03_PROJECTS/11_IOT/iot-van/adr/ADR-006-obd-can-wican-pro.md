# ADR-006 — Intégration données véhicule via OBD-II/CAN bus (WiCAN Pro)

**Date initiale :** 2026-07-09

**Révision :** 2026-11-05

**Statut :** choix matériel retenu et WiCAN reçu ; **intégration non validée**

**Domaines :** décision IOT / réseau / Home Assistant

## Contexte

Le van est un Westfalia Kelsey 2026 sur porteur Ford Transit Custom 170 CV 4x4 (« Lupo »). La cible est de consulter les données moteur et carrosserie disponibles via OBD-II et de les exposer à Home Assistant par MQTT.

Les bus, adresses ECU, PIDs et données effectivement accessibles doivent être vérifiés sur ce véhicule. La présence d'un dépôt communautaire Ford Transit ne prouve pas la compatibilité avec le Transit Custom 2026 ou l'aménagement Westfalia.

Un Exosfer OBD Protect est également reçu. Sa compatibilité mécanique et électrique avec le WiCAN Pro n'est pas validée ; il ne doit pas être contourné.

## Décision

**Retenir un WiCAN Pro pour une lecture CAN/OBD en consultation seule.** Le matériel a été reçu début août 2026 (~82 € historiques) et est documenté comme physiquement installé. La décision n'implique plus de commande ni de flash initial.

Architecture cible révisée :

```text
WiCAN Pro → Wi-Fi local RUT240 → Ethernet RPi 5 HAOS → Mosquitto → Home Assistant
```

Principes :

- **HS-CAN + MS-CAN** pour ne pas exclure par conception les données carrosserie ;
- **PIDs candidats du dépôt `WiCAN-Ford-Transit`**, à contrôler avant import et valider sur le véhicule ;
- **MQTT local** avec entités réellement découvertes, sans noms ou valeurs fictifs ;
- **veille et réveil configurables**, avec mesure de consommation et de l'effet sur les ECU ;
- **capteurs Zigbee conservés** pour les portes et scénarios de camping tant que le CAN n'est pas éprouvé ;
- **aucune écriture ECU**, aucun contournement Exosfer et aucun flash systématique.

## État au 2026-11-05

- WiCAN Pro : reçu, présence physique documentée mais non revérifiée lors du diagnostic distant.
- RUT240 : en stock, non connecté au RPi ; aucun réseau local van configuré.
- RPi `lupo` : actuellement au bureau sur Wi-Fi maison ; Ethernet désactivé et sans liaison.
- Registre HA : **126 entités, aucun appareil WiCAN ni entité CAN**.
- Les 17+ entités, la compatibilité Exosfer, les PIDs et la consommation réelle restent à tester localement.

## Alternatives considérées — historique

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| **WiCAN Pro** | HS/MS-CAN, MQTT, veille et firmware ouvert | Compatibilité véhicule et intégration à prouver | **Retenu et reçu** |
| WiCAN basic | Moins cher, MQTT | Ne répondait pas au besoin MS-CAN documenté | Écarté |
| DIY ESP32 + CAN | Matériel économique | Firmware, mapping et veille à développer | Écarté — complexité |
| OBDLink MX+ | Outil de diagnostic établi | Pas la chaîne MQTT/HA recherchée ; coût supérieur | Non retenu pour cette cible |
| Pas de CAN | Simplicité | Pas d'accès aux données véhicule recherchées | Écarté, mais capteurs autonomes conservés |

## Conséquences attendues — non acquises

- Les entités disponibles pourront enrichir vitesse, carburant, diagnostic, portes, pneus et batterie **si les données sont réellement exposées**.
- Les scénarios de sécurité conserveront une source indépendante éprouvée.
- La suppression éventuelle de capteurs TPMS/température et les économies historiques ne sont actées qu'après tests comparatifs.
- Le dépôt communautaire crée une dépendance de mapping : sauvegarder la configuration et documenter les écarts.
- Le polling et les réveils peuvent influencer le bus et la consommation : la veille `<1 mA` et le wake de 5 min sont des réglages cibles à mesurer, pas une garantie « sans risque batterie ».

## Critères de révision

Réévaluer l'approche si :

- les PIDs essentiels ne sont pas accessibles ou sont incohérents après diagnostic adapté ;
- l'Exosfer ne peut pas fonctionner avec le montage sans compromis de sécurité ;
- la consommation ou les réveils du bus dépassent le budget électrique accepté par JC ;
- la reconnexion locale n'est pas fiable après redémarrage ou perte réseau.

Dans ces cas, limiter le WiCAN aux PIDs réellement utiles, désactiver le réveil périodique ou conserver des capteurs dédiés plutôt que forcer la cible de 17+ entités.

## Références

- [Procédure de mise en service](../OPERATIONS-CAN-OBD.md)
- [Spécification CAN](../specs/SPEC-CAN-BUS.md)
- [Dépôt communautaire WiCAN-Ford-Transit](https://github.com/anthonysecco/WiCAN-Ford-Transit)

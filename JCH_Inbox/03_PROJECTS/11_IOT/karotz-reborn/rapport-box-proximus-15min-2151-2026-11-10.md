# Rapport technique — Box Proximus (relevé 15 min, soir #2)

- **Relevé** : 2026-11-10, de 21:51:08 à 22:06:08 (15 minutes continues)
- **Émetteur** : Jean-Claude Havaux (via Dobby 🦉)
- **Équipement surveillé** : box Proximus, passerelle `192.168.128.1`, réseau local `/23`
- **Poste de mesure** : Mac sur le même réseau local, sans interruption

## Méthode

Ping ICMP toutes les **2 secondes** vers deux cibles :

1. **`192.168.128.1`** (la box) → disponibilité du **LAN**.
2. **`8.8.8.8`** (Google DNS) → disponibilité du **WAN/internet**.

## Résultats

### 1. LAN (box) — stable

- **446 paquets transmis, 446 reçus, 0,0 % de perte**
- Latence : min 3,4 ms · **moy 7,5 ms** · max 89,8 ms
- **0 coupure sur 15 minutes.**

### 2. WAN (internet) — stable, 1 artefact de démarrage

- **441 transmis, 440 reçus, 0,2 % de perte** (1 paquet)
- Latence : min 19,0 ms · **moy 28,4 ms** · max 130,2 ms
- **1 coupure de 3,3 s** à 21:51:08 — c'est le tout premier ping du relevé (échec initial avant stabilisation), pas une vraie coupure de ligne.

## Constats

1. **Aucune** des coupures mesurées ce matin (16 LAN/h + 22 WAN/h, jusqu'à 76 s) ne s'est reproduite ce soir.
2. **Latence WAN en amélioration** : moyenne 28,4 ms contre 38,1 ms au relevé de 19h12, et plus de pointe à 1 418 ms.
3. **Le défaut reste épisodique** (pic le matin, calme le soir) — cohérent avec le relevé de 19h12.

## Conclusion / recommandation

Box stable sur cette fenêtre de 15 minutes. Le problème du matin ne se manifeste pas le soir. Pour le dossier Proximus, l'argument reste : défaut **intermittent** avec pic sur les fenêtres de pointe. Prochaine étape utile : relever **1 h sur une fenêtre de pointe (matin)** pour capturer l'épisode, comme le relevé de 11h57.

*Relevé généré automatiquement (ping 2 s, 15 min). Logs : `/tmp/box-monitor-15min-lan.log`, `/tmp/box-monitor-15min-wan.log`.*

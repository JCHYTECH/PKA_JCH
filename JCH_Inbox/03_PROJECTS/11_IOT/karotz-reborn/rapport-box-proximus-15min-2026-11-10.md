# Rapport technique — Box Proximus (relevé 15 min, soir)

- **Relevé** : 2026-11-10, de 19:12:50 à 19:27:51 (15 minutes continues)
- **Émetteur** : Jean-Claude Havaux
- **Équipement surveillé** : box Proximus, passerelle `192.168.128.1`, réseau local `/23`
- **Poste de mesure** : Mac sur le même réseau local, sans interruption

## Méthode

Ping ICMP toutes les **2 secondes** vers deux cibles distinctes :

1. **`192.168.128.1`** (la box) → disponibilité du **LAN**.
2. **`8.8.8.8`** (Google DNS) → disponibilité du **WAN/internet**.

## Résultats

### 1. LAN (box) — aucune coupure

- **450 paquets transmis, 450 reçus, 0,0 % de perte**
- Latence : min 2,2 ms · moy 4,4 ms · max 14,2 ms
- **0 coupure sur 15 minutes.**

### 2. WAN (internet) — aucune coupure, mais latence anormale

- **450 paquets transmis, 450 reçus, 0,0 % de perte** (1 paquet arrivé hors délai)
- **0 coupure sur 15 minutes.**
- Latence : min 14,6 ms · **moy 38,1 ms** · **max 1 418 ms** · écart-type 85,6 ms

## Constats

1. **La box est stable sur cette fenêtre** — aucune des 16 coupures LAN/h mesurées à midi (11:57–12:57) ne s'est reproduite ce soir.
2. **Le problème est intermittent dans le temps**, pas permanent : épisode aigu le matin, fenêtre propre le soir.
3. **Signal résiduel** : la latence internet reste anormale (moyenne 38 ms, pointes à 1,4 s). Sur une ligne saine on attendrait 10–20 ms stables. Cela suggère une ligne chargée ou une instabilité latente, même sans coupure franche.

## Conclusion / recommandation

- Pas de coupure mesurée ce soir ; l'incident du matin n'est pas continu.
- Pour Proximus : le défaut est **épisodique** (pic le matin, calme le soir) — un diagnostic doit être fait sur une fenêtre de pointe, pas à froid.
- Option : relancer un relevé long (1 h) à un moment où la ligne est en défaut, pour capturer l'épisode.

*Relevé généré automatiquement (ping 2 s, 15 min). Logs : `/tmp/box-monitor-15min-lan.log`, `/tmp/box-monitor-15min-wan.log`.*

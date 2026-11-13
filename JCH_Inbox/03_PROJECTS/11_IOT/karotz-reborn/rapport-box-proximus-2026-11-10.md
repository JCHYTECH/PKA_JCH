gauche ou on voit la# Rapport technique — Instabilité de la box Proximus

- **Relevé** : 2026-11-10, de 11:57:44 à 12:57:44 (60 minutes continues)
- **Émetteur** : Jean-Claude Havaux
- **Équipement surveillé** : box Proximus, passerelle `192.168.128.1`, réseau local /23
- **Poste de mesure** : Mac sur le même réseau local, sans interruption

## Méthode

Ping ICMP toutes les **2 secondes** vers deux cibles distinctes :

1. **`192.168.128.1`** (la box elle-même) → mesure la disponibilité du **LAN** de la box.
2. **`8.8.8.8`** (hôte public Google DNS) → mesure la disponibilité du **WAN/internet** en sortie de box.

Une coupure est comptée depuis l'échec des pings jusqu'au retour. Fenêtre de 60 minutes sans coupure du poste de mesure.

## Résultats

### 1. Coupures LAN — la box cesse de répondre en local

- **16 coupures en 1 heure**
- **Durée cumulée : 233 secondes (~3,9 min, soit ~6,5 % du temps)**
- Durées : minimum 3 s · médiane 8 s · moyenne 14,6 s · **maximum 76 s**

Chronologie (début → fin, durée) :

| # | Début | Fin | Durée |
|---|-------|-----|-------|
| 1 | 11:57:44 | 11:58:16 | 25 s (début sous-estimé : le relevé a démarré en pleine coupure) |
| 2 | 12:01:09 | 12:01:13 | 4 s |
| 3 | 12:05:05 | 12:05:10 | 5 s |
| 4 | 12:06:20 | 12:06:25 | 5 s |
| 5 | 12:09:23 | 12:09:28 | 5 s |
| 6 | 12:21:45 | 12:21:52 | 7 s |
| 7 | 12:40:41 | 12:40:49 | 8 s |
| 8 | 12:41:19 | 12:41:27 | 8 s |
| 9 | 12:41:52 | 12:42:14 | 22 s |
| 10 | 12:42:32 | 12:43:48 | **76 s** |
| 11 | 12:44:04 | 12:44:40 | 36 s |
| 12 | 12:45:21 | 12:45:31 | 10 s |
| 13 | 12:47:44 | 12:47:49 | 5 s |
| 14 | 12:51:18 | 12:51:22 | 4 s |
| 15 | 12:52:25 | 12:52:28 | 3 s |
| 16 | 12:54:59 | 12:55:09 | 10 s |

### 2. Coupures internet (WAN — 8.8.8.8 injoignable)

- **22 coupures en 1 heure**
- **Durée cumulée : 301 secondes (~5 min)**
- Durées : majoritairement 4–5 s, plus une coupure de **195 s (~3,25 min)** et une de 15 s

## Constats clés

1. **Deux modes de défaillance distincts** :
   - **Perte LAN (16×)** : la box ne répond plus même en local → signature d'un **hang ou redémarrage du processeur** de la box.
   - **Perte WAN seule** (plusieurs événements, LAN toujours joignable) : l'internet tombe alors que le réseau local tient → signature d'une **instabilité de ligne ou du routage** de la box.

2. **Épisode critique 12:40:41 → 12:46:08** : ~6 minutes d'instabilité intense, dont une coupure box de 76 s et une coupure internet de 195 s. C'est l'épisode le plus grave du relevé.

3. **Fréquence rédhibitoire** : 16 à 22 coupures par heure rendent tout usage continu impossible (visioconférence, télétravail, objets connectés, streaming).

## Conclusion / demande

La box présente une instabilité récurrente et mesurée : **~16 crashs LAN/h et ~22 coupures WAN/h, jusqu'à 76 s de coupure continue**. Demande : diagnostic de la ligne et/ou remplacement de la box.

*Relevé généré automatiquement (ping 2 s, 60 min). Fichier source : `/tmp/box-monitor.log`.*

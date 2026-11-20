# Rapport technique — Ligne Proximus dégradée (relevé 1 h + speed test)

- **Relevé** : 2026-11-14, de 12:48:19 à 13:48:46 (60 minutes continues)
- **Émetteur** : Jean-Claude Havaux (via Dobby 🦉)
- **Équipement surveillé** : box Proximus, passerelle `192.168.128.1`, réseau local `/23`
- **Poste de mesure** : Mac M5 (`192.168.129.14`, Ethernet `en0`), sans interruption
- **Complète** : `rapport-box-proximus-2026-11-10.md` (relevé du 10/11) — voir §Comparaison

## Méthode

1. Ping ICMP toutes les **1 seconde** (60 min) vers deux cibles :
   - **`192.168.128.1`** (la box) → disponibilité du **LAN**.
   - **`1.1.1.1`** (Cloudflare DNS) → disponibilité du **WAN/internet**.
2. Contre-tests (10 pings) vers **`8.8.8.8`** (Google) et **`9.9.9.9`** (Quad9) pour écarter un problème spécifique à Cloudflare.
3. **Speed test TCP** (`speedtest-cli`) pour mesurer le débit réel, indépendamment de la dépriorisation ICMP.

## Résultats

### 1. LAN (box) — parfaitement stable

- **3 600 paquets transmis, 3 600 reçus, 0,0 % de perte**
- Latence : min 2,5 ms · **moy 5,1 ms** · max 169,2 ms (un seul pic) · écart-type 9,1 ms
- **0 coupure sur 60 minutes.**

### 2. WAN (internet, `1.1.1.1`) — dégradation continue

- **3 600 transmis, 3 223 reçus → 10,5 % de perte réelle** (377 paquets jamais revenus)
- Latence : min 12 ms · **médiane ~2 064 ms** · moy 1 809 ms · max 2 762 ms · écart-type 744 ms
- Répartition des réponses : **76 % ≥ 1 s** (1 815 pings > 2 s, 941 entre 1–2 s), seulement 6 % < 50 ms
- **Aucune coupure franche** (plus longue interruption sans réponse : 4 s) → pas de « trou », mais une ligne saturée en continu

### 3. Contre-tests (généralité du défaut)

| Cible | Perte | Latence moy | Latence max |
|-------|-------|-------------|-------------|
| `8.8.8.8` (Google) | 0/10 | 788 ms | 2 638 ms |
| `9.9.9.9` (Quad9) | 2/10 (20 %) | 2 324 ms | 2 625 ms |

Les trois cibles externes confirment le même défaut → **toute la liaison WAN Proximus est atteinte**, pas un peering isolé.

### 4. Speed test TCP (`speedtest-cli`)

- **Serveur sélectionné** : Telefónica Germany (Leipzig) à **535 km** — ping 143 ms. Aucun serveur belge/proche n'a répondu plus vite → indice de routage dégradé.
- **Download : 6,15 Mbit/s**
- **Upload : 1,79 Mbit/s**

Sur une ligne saine, on attendrait 100–400 Mbit/s en download et 20–40 en upload, avec un serveur belge < 20 ms.

## Constats clés

1. **Signature différente du 10/11** : le 10/11 matin montrait une **box qui crashe** (16 coupures LAN/h + 22 WAN/h, jusqu'à 76 s). Le 14/11, la box est **stable** (0 crash) mais la **ligne WAN est dégradée en continu** : latence ×100 (~2 s au lieu de 20–30 ms) + ~10 % de perte + débit effondré (6 Mbit/s).
2. **Pas de coupures sèches** : contrairement au 10/11 (défaut épisodique, pic matinal), on observe ici une **saturation/dégradation permanente** de la liaison, pas des interruptions nettes.
3. **Routage suspect** : le speed test n'a trouvé que Leipzig à 143 ms comme « meilleur » serveur — les serveurs belges sont injoignables ou plus lents, ce qui suggère un problème de ligne ou de peering Proximus, pas la box.
4. **Vérifié hors VPN** : la route vers l'internet sort directement par la box (`192.168.128.1` via `en0`). Tailscale est actif mais n'est pas le chemin par défaut — le défaut est bien côté Proximus.

## Comparaison avec le relevé du 2026-11-10

| Mesure | 10/11 (matin, 60 min) | 10/11 (soir, 15 min) | **14/11 (midi, 60 min)** |
|--------|----------------------|----------------------|--------------------------|
| Coupures LAN (box) | 16 / h | 0 | **0** |
| Coupures WAN | 22 / h | 0 | **0 (mais latence continue)** |
| Latence WAN moy | ~38 ms | 28,4 ms | **1 809 ms** |
| Perte WAN | n.d. (coupures) | 0,2 % | **10,5 %** |
| Débit | n.d. | n.d. | **↓ 6,15 / ↑ 1,79 Mbit/s** |

Le défaut a **changé de nature** : d'une instabilité épisodique (crash box le matin du 10/11) vers une **dégradation continue de la ligne** le 14/11.

## Conclusion / demande

La box est saine ce jour ; le problème est la **liaison WAN Proximus**, dégradée en continu (~2 s de latence, 10 % de perte, 6 Mbit/s en download). Demande : diagnostic de ligne Proximus avec ces mesures datées (relevé ICMP 1 s + speed test TCP) et comparaison au relevé du 10/11.

*Relevé généré automatiquement (ping 1 s, 60 min + speedtest-cli). Logs : `/tmp/ping-proximus-box.log`, `/tmp/ping-proximus-wan.log`.*

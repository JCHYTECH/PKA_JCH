# Installation Bluetti — Elite 100 V2 + Charger 2 sur Lupo (Westfalia Kelsey 2026)

> Document technique — Dobby 🦉 — 2026-10-03
> Véhicule : **Lupo** 🐺 — Westfalia Kelsey 2026, porteur Ford Transit Custom Tourneo (V710), 2.0 EcoBlue 170 ch, 4×4, BVA8

---

## 1. Objectif

Ajouter une **source d'énergie portable** au van, indépendante du réseau CBE existant :

- **Bluetti Elite 100 V2** — station 1 024 Wh / 1 800 W (sortie), entrée solaire 1 000 W max.
- **Bluetti Charger 2** — chargeur DC-DC 1 200 W (alternateur + solaire combinés), 12/24 V.

Le Charger 2 recharge la station pendant la conduite via l'alternateur du porteur (et, en option, via un panneau solaire dédié).

---

## 2. Contexte électrique du véhicule (confirmé par le bon de commande)

| Composant | Détail |
|-----------|--------|
| Centrale cellule | CBE (standard Westfalia) |
| Batterie porteur (démarrage) | Ford standard (AGM/gel) |
| Batterie cellule série | AGM 92 Ah |
| Batterie cellule lithium | LiFePO4 100 Ah (Vanomobil, chargeur intelligent inclus) |
| Solaire | FLEX 150 W + régulateur MPPT (Vanomobil) |
| Chauffage | Webasto 2 000 W |
| Réseaux | **Deux réseaux distincts : porteur vs cellule** |

**Règle n°1** : le Charger 2 se branche côté **batterie porteur** (alternateur), jamais sur le circuit cellule géré par la centrale CBE. Les deux réseaux doivent rester isolés.

---

## 3. Matériel nécessaire

- Bluetti **Elite 100 V2** (station, amovible — vit dans l'habitacle).
- Bluetti **Charger 2** (variante de base « Included DC Cable » — le câble DC de sortie est fourni).
- Câble de puissance rouge (positif) et noir (négatif) — section à confirmer (§6).
- **Fusible ANL/MEGA** + porte-fusible (calibre à confirmer §6).
- Cosse à œil, gaine thermorétractable, gaine de protection (loom), passe-câbles (grommets), serre-câbles.
- Multimètre, pince à sertir, clés (10/13 mm), bornier masse.
- Application **BLUETTI** (Bluetooth/WiFi) pour la configuration.

---

## 4. Principe de câblage (schéma logique)

```
Batterie porteur (+) ──┬── FUSIBLE (ANL) ──► Charger 2 [entrée ALTERNATEUR]
                       │
Batterie porteur (−) ──┴──► MASSE CHÂSSIS (point propre, non via le capteur BMS)

Charger 2 [sortie DC] ──(câble DC fourni)──► Elite 100 V2 [entrée DC/charge]
```

- **Positif** : départ batterie porteur → fusible à ≤ 30 cm de la borne → Charger 2.
- **Négatif** : masse châssis nue (poncée, rondelle éventail), ou retour batterie **sans** passer par le capteur de courant négatif Ford.

---

## 5. Procédure pas à pas

### Étape 0 — Sécurité
1. Contact coupé, clé retirée.
2. Débrancher la borne **négative** de la batterie porteur en premier.
3. Batterie porteur **sous le capot** (compartiment moteur, à côté de la boîte à fusibles sous capot) — confirmé par le manuel Ford, section « Vue d'ensemble sous le capot », item « Batterie 12 V ».

### Étape 1 — Emplacement du Charger 2
- Monter le Charger 2 **dans l'habitacle** (sec, ventilé), jamais sous le capot : il n'est pas IP étanche moteur et possède un ventilateur actif.
- Privilégier un trajet de câble **court** entre la batterie porteur et le Charger 2.
- Laisser un dégagement ≥ 5 cm autour pour la circulation d'air.

### Étape 2 — Tirage du câble positif
1. Faire passer le câble rouge depuis la batterie porteur jusqu'à l'emplacement du Charger 2.
2. Traversée de cloison (pare-feu) : utiliser un **passe-câble (grommet)** existant ou percer proprement + grommet. Ne jamais laisser le câble frotter sur la tôle. Sur Transit Custom, le grommet de pare-feu se situe souvent côté passager — à repérer sur le véhicule.
3. Protéger tout le trajet sous gaine (loom) et fixer au châssis avec serre-câbles.

### Étape 3 — Fusible
1. Monter le porte-fusible sur le câble **positif**, à **moins de 30 cm** de la borne positive de la batterie porteur.
2. Insérer le fusible **en dernier** (après tout le câblage), pour éviter tout court-circuit pendant le montage.

### Étape 4 — Masse (négatif)
1. Créer un point de masse châssis : poncer la tôle jusqu'au métal nu, fixer la cosse avec une **rondelle éventail** + boulon, protéger (graisse/vernis) contre la corrosion.
2. **Important Ford** : ne pas raccorder le négatif du Charger 2 sur la cosse du **capteur de courant (BMS)** présent sur la borne négative de la batterie. La masse doit être côté châssis, en aval du capteur.

### Étape 5 — Sortie vers la station
1. Brancher le **câble DC fourni** (sortie du Charger 2) à l'**entrée DC/charge** de l'Elite 100 V2.
2. Ne pas brancher la station tant que la configuration (§6) n'est pas terminée.

### Étape 6 — Configuration dans l'app BLUETTI
1. Reconnecter la borne négative de la batterie porteur, insérer le fusible.
2. Appairer le Charger 2 dans l'app (Bluetooth/WiFi).
3. Régler :
   - **Type de batterie d'entrée** = AGM (batterie porteur).
   - **Tension de démarrage** (seuil de détection moteur) — voir note « alternateur intelligent » ci-dessous.
   - **Tension de coupure** (protection de la batterie porteur) — ne jamais descendre sous ~12,3 V pour ne pas vider la batterie de démarrage.
   - **Limite de courant** si le manuel le permet (pour ménager un petit alternateur).

### Étape 7 — Tests
1. Moteur arrêté : vérifier que le Charger 2 **ne charge pas** (aucune consommation parasite).
2. Démarrer le moteur : vérifier dans l'app que le courant monte progressivement.
3. Couper le contact : vérifier l'arrêt automatique de la charge.
4. Contrôler qu'aucune odeur de brûlé ni échauffement anormal sur les câbles/fusible après 20 min de charge.

---

## 6. Section de câble et fusible — ⚠️ à confirmer sur le manuel Charger 2

Le Charger 2 délivre **1 200 W combinés** (alternateur + solaire). Le dimensionnement ci-dessous est une **base de départ conservatrice** ; la valeur exacte fait foi depuis le manuel Bluetti :

| Paramètre | Recommandation de départ | Note |
|-----------|--------------------------|------|
| Fusible positif | **ANL 60 A** (80 A si le manuel l'indique) | ≤ 30 cm de la batterie |
| Câble (trajet ≤ 2 m) | **16 mm²** (≈ 6 AWG) minimum | |
| Câble (trajet > 2-3 m) | **25 mm²** (≈ 4 AWG) | pour limiter la chute de tension |
| Masse | même section que le positif | point châssis propre |

> Batterie sous capot → Charger 2 dans l'habitacle = trajet typique 2 à 4 m : **privilégier 25 mm²**. La batterie étant sous le capot, le trajet est plus long que prévu initialement.

> Je n'ai pas pu récupérer le manuel officiel pendant cette session (page produit derrière un redirect, moteurs de recherche bloqués par anti-bots). **Vérifier le fusible et la section exacts dans le manuel Charger 2 avant achat du matériel.**

---

## 7. Point critique : alternateur intelligent Ford

Le Transit Custom V710 est équipé d'un **alternateur intelligent** (régénération au freinage, tension variable ~12,3–15 V, start-stop). Conséquences :

- Une détection **purement par tension** du « moteur en marche » peut être trompée quand l'alternateur baisse la tension en croisière.
- Utiliser de préférence un **signal d'allumage (ACC / D+)** si le Charger 2 le supporte, ou régler finement le seuil de tension de démarrage dans l'app.
- Le Charger 2 possède une protection « auto on/off » pour ne pas vider la batterie porteur à l'arrêt — la laisser active.

---

## 8. Option solaire — à trancher

Le Kelsey a déjà un panneau **150 W + MPPT sur le réseau CBE**. Deux choix possibles :

1. **Ne pas utiliser l'entrée solaire du Charger 2** (recommandé au départ) : le solaire existant continue d'alimenter la cellule CBE, le Charger 2 ne fait que l'alternateur → station.
2. **Ajouter un panneau solaire dédié** sur l'entrée solaire du Charger 2, pour recharger la station au solaire en plus. Ne **pas** repiquer le panneau 150 W existant sur les deux régulateurs à la fois.

---

## 9. Récapitulatif sécurité

- Fusible côté batterie, en premier point du positif.
- Gaine + passe-câbles sur tout le trajet.
- Masse châssis propre, hors capteur BMS.
- Couper la batterie et insérer le fusible en dernier.
- Vérifier l'absence de consommation parasite à l'arrêt.

---

## 10. Références

- Fiche technique Lupo : `Lupo Itself/OLDIES/achat-van/fiche-technique-lupo-kelsey.md`
- Note deux réseaux électriques : `van technique/securite/camera-reolink-argus-magicam-lupo.md`
- Prix surveillés (alerte quotidienne) : `scripts/bluetti_price_watch.py` / `bin/pka-watch-bluetti`

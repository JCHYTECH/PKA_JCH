# Rapport Araignee — Audit IoT & Recommandations

**Auteur :** [[Araignee]]  
**Date :** 2026-06-06  
**Projets audites :** `11_IOT/iot-van/`, `03_WILDNEXUS/P0`, `11_IOT/iot-home/`

---

> **Note post-rapport (2026-06-06) :** JCH a corrige la R1 — le van est mobile, WildNexus est deploye en foret. La gateway LoRa ne peut pas etre mutualisee. Les recommandations ont ete ajustees en consequence.

## 1. Etonnements

### 1.1 WildNexus alimente par piles AA fournies par l'utilisateur

C'est la plus grosse surprise. Le modele "camera de chasse" (8 x AA, 4S2P, fournies par l'utilisateur) est un choix pragmatique pour un prototype, mais tres limite pour un produit IoT en 2026.

- L'utilisateur doit acheter et changer des piles — perception "gadget", pas "produit"
- Pas de monitoring de charge, pas de recharge integree, pas de BMS
- L'ADR-005 le justifie bien (zero BMS, supply chain, cout), mais c'est un choix qui ferme la porte au "produit" et garde le systeme dans la categorie "proto de recherche"

**Question ouverte :** Est-ce que le marche cible (ecologues, naturalistes) accepte des piles AA en 2026 ? Ou est-ce qu'un petit panneau solaire + LiFePO4 integre serait un meilleur standard produit ?

### 1.2 Van IoT et WildNexus partagent la meme pile mais ne sont pas connectes

Le van a 150 Ah LiFePO4 + 280W solaire, un RPi 5 permanent, Tailscale, LTE. WildNexus a des noeuds ESP32-S3 sur piles AA qui transmettent en LoRa.

**Les deux projets ne parlent pas entre eux.** Pourtant :
- Le RPi 5 du van pourrait etre la gateway LoRa WildNexus (au lieu d'un second ESP32-S3)
- Le LTE du van pourrait relayer les evenements WildNexus vers le cloud
- Le van pourrait servir de station de recharge pour les satellites WildNexus en P1

C'est la convergence la plus evidente et elle n'est documentee nulle part.

### 1.3 iot-home est une coquille vide

Le dossier iot-home/ est vide. La maison off-grid est citee dans MEMORY.md (60 m, autonome) mais personne n'a encore ecrit une ligne sur son infrastructure IoT. Le van a 8 fichiers, WildNexus a 150+ fichiers, la maison a zero.

### 1.4 Le BOM van IoT integre des lecons WildNexus... mais WildNexus n'integre pas les lecons van

Le cahier technique van cite WildNexus en reference (SSD obligatoire, USB-C PD 5A, API REST). Mais WildNexus ne cite jamais le van IoT comme source de lecons. Par exemple :
- Le van a identifie le testeur FNIRSI FNB58 comme outil diagnostic critique pour les problemes d'alimentation — WildNexus pourrait aussi en beneficier
- Le van utilise Home Assistant avec des capteurs Zigbee COTS — WildNexus pourrait envisager Zigbee comme alternative basse consommation pour certains capteurs environnementaux

### 1.5 Decision bloquee sur la garantie van

Le projet van IoT est bloque sur la validation garantie par [[Renard]]. Le brief date du 30/05 et il n'y a pas de livrable. C'est le chemin critique de la Phase 0.

---

## 2. Recommandations

### ~~R1 — Converger les deux infrastructures IoT~~ (INVALIDE)

~~Creer un schema d'architecture converge qui montre comment le van, la maison et WildNexus partagent la meme pile~~

**Raison :** Le van est mobile. WildNexus est deploye en foret, loin du van. Les deux infrastructures sont geographiquement independantes. La convergence reseau n'est pas possible sans un point de collecte fixe partage. :

```
[WildNexus Satellites] --- LoRa P2P ---> [Gateway van RPi 5 + SX1262]
                                           |
                                     [Home Assistant / Tailscale]
                                      |                       |
                               [Dashboard van]         [Cloud/Tailnet]
                                      |
                               [Maison off-grid]
```


Note : la convergence cloud (Tailscale, alertes, dashboard) reste possible via internet — chaque site a sa propre connectivite, mais partage le meme tailnet et le meme dashboard Home Assistant central.

### R2 — Reconsiderer l'energie WildNexus pour P1

Garder le modele AA pour P0 (c'est pragmatique et deja decide), mais documenter explicitement l'evolution P1 vers :
- Petite batterie LiFePO4 18650 integree + panneau solaire 5W
- Recharge via USB-C terrain (compatible power bank standard)
- Option "AA adapter" pour compatibilite descendante

Cela transforme le positionnement de "camera de chasse amelioree" a "produit IoT ecologique".

### R3 — Activer le dossier iot-home

Le dossier iot-home devrait contenir au minimum un [[INDEX]].md avec :
- Schema electrique existant de la maison (panneaux, batteries, onduleur)
- Points de collecte (compteur, temperature, humidite)
- Objectifs IoT (monitoring, automatisation, alertes)
- Convergence avec le van (partage Home Assistant, Tailscale)

Je peux m'en charger.

### R4 — Debloquer la validation garantie van

Le chemin critique du projet van est la validation garantie. [[Renard]] est mandate depuis le 30/05 sans livrable visible. Proposition : relancer [[Renard]] avec une deadline.

### R5 — Standardiser le stack MQTT

Ni le van ni WildNexus n'utilisent MQTT de maniere explicite (WildNexus utilise LoRa P2P, le van utilise Zigbee + Home Assistant). Pourtant, MQTT est le protocole IoT standard pour interconnecter des systemes heterogenes.

Recommandation : Ajouter un broker MQTT (Mosquitto) sur le RPi 5 du van (ou de la maison) comme bus de messages transverse. Les satellites WildNexus pourraient pousser leurs evenements via MQTT sur LoRa, et Home Assistant les consommerait nativement.

### R6 — Revoir le dimensionnement electrique du van

F3 du DS300 est un 10A. Le Pi 5 tire ~2A sous 12V, plus le Zigbee dongle, plus d'eventuels peripheriques USB. Avec le LTE modem, on approche de 3A. La marge est de 7A pour les prises 12V d'origine — suffisant mais a documenter explicitement.

Recommandation : Mesurer la consommation reelle du Pi 5 + peripheriques au FNB58 avant de souder. Si > 3A, envisager un circuit F3 bis ou un relais contacteur.

### R7 — Documenter les lecons croisees

Creer un fichier LEQONS_CROISEES.md dans 11_IOT/ qui centralise :
- Les lecons WildNexus utilisees par le van (deja fait dans les docs van)
- Les lecons van qui pourraient servir a WildNexus
- Les lecons terrain (quand elles arriveront) partageables

---

## 3. Synthese

| Priorite | Action | Projet | Impact |
|----------|--------|--------|--------|
| ~~P0~~ | ~~Schema convergence van + maison + WildNexus~~ | ~~INVALIDE~~ | ~~Van mobile ≠ foret~~ |
| P0 | Initialiser iot-home/[[INDEX]].md | 11_IOT/iot-home | Clarte projet |
| P1 | Migration WildNexus Li-ion + solaire | 03_WILDNEXUS | Positionnement produit |
| P1 | Broker MQTT transverse | 11_IOT + 03_WILDNEXUS | Interoperabilite |
| ~~P1~~ | ~~Gateway LoRa sur RPi van~~ | ~~INVALIDE~~ | ~~Van mobile ≠ foret~~ |
| Maintenant | Relancer [[Renard]] (garantie van) | 11_IOT/iot-van | Chemin critique |

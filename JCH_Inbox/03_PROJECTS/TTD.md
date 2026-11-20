# TTD — Vue consolidée (tous projets)

> **Fichier dérivé** — généré à chaque `/save` depuis les seuls blocs `TTD — Pending` des thread files. Ne pas éditer à la main hors `/save` : la source de vérité reste les thread files + `etat-projets.md`.
> `last_updated: 2026-11-20 · by: deepseek-v4-pro` — pivot WildLens « tout en français » (3 éditions FR) + clipper iPad→inbox

## 01_AI_IT_TOOLS

Source : `01_AI_IT_TOOLS/thread-ai-it-tools.md`

- [ ] **P2 · — · (Dobby)** Maintenance continue — `pka-thread-file` + boucle mémoire à chaque fin de session
- [ ] **P1 · — · (Dobby)** Ajouter un mode observation/dry-run aux watch loops (inspiré SuperAgent : évaluer le signal, enregistrer ce qu'il ferait, sans agir)
- [ ] **P2 · — · (JC + Dobby)** Essayer le TUI/double-clic Grok ; le rituel `/save` Kimi est terminé et ne fait plus partie de cet essai
- [ ] **P2 · — · (JC + Dobby)** ACL Tailscale — durcir l'accès réseau (reporté 13/11) : poser la politique ACL puis taguer `lupo` en `tag:van` (ports 8123/1883/22222).
- [x] **P2 · — · (Dobby)** Mot de passe VNC dédié appliqué (M5 + M1, 13/11) — plus l'admin

## 02_ARTEON

Source : `02_ARTEON/thread-arteon.md`

- [ ] **P1 · — · (JC)** Relire le brouillon Ghost « WildLens — Edition #4 » (slug `wildlens-edition-4`) puis donner le feu vert
- [ ] **P2 · — · (Dobby, après relecture)** Pousser les 3 autres éditions en brouillon via `scripts/ghost_import.py`
- [ ] **P3 · — · (JC + Forge)** Finir la migration WildLens : DNS A `wildlens` → `2.25.8.208`, `ghost setup ssl`, Mailgun, import contenu (VPS créé + Ghost installé 15/11)
- [ ] **P4 · — · (JC)** Allouer du temps créatif éditorial — blocage structurel : 8 étapes roadmap non closes
- [ ] **P5 · — · (Forge + Jade, après feu vert)** Traduire les éditions en FR + IT ; builder le changeur de langue Ghost (EN/FR/IT) avec détection géoloc IP
- [ ] **P6 · — · (Dobby)** Presets brique 3 : masques IA (sujet/œil/plumage/arrière-plan) ; brique 4 : endpoint `/recommend` (EXIF niveau 1 d'abord)
- [ ] **P7 · — · (JC)** Nettoyer le doublon de preset LRC (37 importés au lieu de 36) + galerie avant/après définitive (12 paires)

## 03_WILDNEXUS — INSECTNET

Source : `03_WILDNEXUS/INSECTNET/thread-insectnet.md`

**Gelé — dépend de la reprise de WILDNEXUS DEVICE.**

- [ ] **Au signal de JC seulement** Revérifier l'existence et le fonctionnement du pipeline, l'accès M1 et la pertinence de la migration avant de redéfinir responsable et échéance.

## 03_WILDNEXUS — NEXUS_ACOUSTIC

Source : `03_WILDNEXUS/NEXUS_ACOUSTIC/thread-nexus-acoustic.md`

**Gelé — dépend de la reprise de WILDNEXUS DEVICE.**

- [ ] **Au signal de JC seulement** Vérifier les datasets réellement présents et leur intégrité, contrôler l'installation TweetyBERT, puis reconstruire une roadmap et des responsabilités.

## 03_WILDNEXUS — WILDNEXUS_DEVICE

Source : `03_WILDNEXUS/WILDNEXUS_DEVICE/thread-wildnexus.md`

### Ordre de reprise proposé

**Repris (P0 engineering, dégel 12/11) — gate 1 inventaire en cours. Aucun montage ni achat avant levée des gates.**

- [ ] **P0 · gate 1 · (JC)** Exécuter la checklist d'inventaire au banc (`07_PROCUREMENT_BOM/INVENTAIRE-checklist-reprise-2026-11-12.md`) puis renvoyer à Dobby ; rapprocher factures, commandes et budget ; synchroniser Plane/kanban sans reprendre les anciennes échéances.
- [ ] Lever les points de sécurité électrique et confirmer micros, PIR et optique IR avant alimentation ou soudure.
- [ ] Reprendre les phases D/E, SOP-06, CAM-01/02, SOP-08/09 sur le matériel identifié.
- [ ] Exécuter SOP-13 puis SOP-14/15/17/18 ; tester les fichiers réellement produits dans les pipelines.
- [ ] Comparer les modèles d'IA avec CAM-03/SOP-11, y compris rappel humain, fausses alertes animales, RAM, latence et énergie.
- [ ] Après arbitrage d'achat, exécuter SOP-07 et livrer la gateway P0 : réception des deux types de paquets, journal et erreurs.
- [ ] Mesurer le système intégré en Wh, puis décider du boîtier et de l'EVT. Ne pas annoncer 60 jours, une portée ou IP67 avant mesure.
- [ ] Rédiger ADR-018 et finaliser les exigences RGPD/sécurité avant le terrain.

## Décisions récentes

| Date | Décision |
|---|---|
| 2026-11-05 | Firmware destiné à MIT + `ETHICS.md` et politique d'usage ; ce n'est pas une dual-licence. Autres objets de licence à traiter séparément. |
| 2026-11-05 | Prix FIELD 149–179 € et marge 40 % retirés provisoirement ; coût produit complet inconnu. |
| 2026-11-05 | 60 jours, IP67, portée et latence traités comme cibles ; preuves matérielles exigées. |
| 2026-07-05 | Double cycle caméra/audio, payload spectral et format audio définis dans ADR-014/016/017. |
| 2026-06-19 | Couche acoustique stéréo définie dans ADR-013. |
| 2026-06-14 | Wokwi retenu comme smoke test, sans valeur de validation matérielle. |

## 05_PHOTO_AI_JURY

Source : `05_PHOTO_AI_JURY/thread-photo-ai-jury.md`

- [ ] **P2 · — · (JCH + Argus)** Enregistrer des comparaisons A/B avec tutoriel et une validation sur image inédite ; aucune généralisation ou lot automatique avant ces données réelles
- [ ] **P2 · — · (Argus)** Prochaine fournée d'analyses seulement après décision de JC ; aucun appel IA payant effectué dans ce chantier

## 06_PHOTO_NATURE

Source : `06_PHOTO_NATURE/thread-photo-nature.md`

- [ ] **P2 · — · (Dobby)** Maintien — keyworder et presets ; valider le prochain traitement réel après le correctif `headline`

## 07_TRAVELS

Source : `07_TRAVELS/thread-travels.md`

- [ ] **P2 · — · (Cigogne + Dobby)** Traiter 36 `skipped` (OCR échoué → vision forcée) + 9 `parked_routes` + 5 `rejected`
- [ ] **P2 · — · (Cigogne)** Finaliser le meuble banquette (design 104×55×25)
- [ ] **P2 · — · (JC + Dobby)** Maquette boîte vélo pliant → marquer axes/boîtier/chainring → valider encoches

## 08_VETALYX

Source : `08_VETALYX/thread-vetalyx.md`

- [ ] **P0 · échéance initiale 28/10 dépassée · (JC/Renard/Jade)** Finaliser relecture et traduction de la réponse v4.1 EN préparée le 29/10, puis décider son envoi
- [ ] **P0 · — · (Notaire)** Mécanique libération 6 000 € (pro-rata ? dilution si non-libération ?) — le nœud du 40 %
- [ ] **P1 · — · (JC)** Nommer les 2 administrateurs fondateurs (Art. 33)
- [ ] **P1 · — · (Notaire)** Validation notaire (mécanique 6 000 €, ISC, exercice fiscal)
- [ ] **P1 · — · (Renard)** Verrouiller anti-dilution pro-rata + pas de véto DIAHO sur entrée investisseur (Art. 5 pacte)
- [ ] **P1 · — · (JC)** Seuil drag-along (75 % recommandé)
- [x] **P1 · — · (Renard)** Vérifier double qualité Peiwen QI (fondatrice 15 % + administratrice DIAHO)
- [ ] **P1 · — · (Jade)** Re-traduction EN des clauses ajoutées
- [ ] **P2 · — · (Clio)** Trancher qualification AFMPS/FAMHP (DM vétérinaire vs médicament)
- [ ] **P2 · — · (Dobby)** Export BP statique (PDF) pour tiers
- [ ] **P2 · — · (veille)** 7 briefs actifs en mode exploration (voir tableau ci-dessous)

## 11_IOT

Source : `11_IOT/thread-iot.md`

- [ ] **P2 · continu · (Dobby)** Surveiller que `binary_sensor.raspberry_pi_power_status` reste `off` ; ré-intervenir sur l'alimentation/câble si récidive.
- [ ] **P1 · — · (JC)** RPi Home résolu (Core port 80, SSH permanent, Z2M réinstallé healthy) ; re-appairer `vanne_serre` + `LuxSerre` (permit join + bouton physique).
- [ ] **P1 · après 03:17 · (Dobby)** Vérifier l'exécution automatique Time Machine et la rétention ; tester une restauration uniquement avec confirmation explicite de JC et prévoir une copie hors du RPi.
- [ ] **P2 · — · (JC + Dobby)** Reconnecter Claude ; résoudre séparément les modèles Codex refusés par le compte. Ne pas exposer HA publiquement pour ChatGPT Web.
- [ ] **P1 · si doute sur un capteur · (JC + Dobby)** Contrôler une mesure fraîche ; aucune entité LQI/linkquality/last_seen n'est exposée, donc ne pas conclure à une panne sur les seules valeurs retenues.
- [ ] **P1 · si nouvelle coupure USB · (JC + Dobby)** Tester une courte rallonge USB2 saine, puis l'alimentation officielle directe du RPi, une variable à la fois. Ne pas mettre à jour le firmware pour masquer une coupure USB.
- [ ] **P0 · M5 · (JC + Dobby)** Décider si le second dongle doit équiper le M5 ; ensuite corriger le pont série ou arrêter le service Zigbee2MQTT inutilisé. Ne pas laisser la boucle de redémarrage sans traitement.
- [ ] **P0 · avant achat · (Dobby + Forge)** Identifier physiquement le X1205 et ses accus, vérifier boîtier X1201-C1/X1200 et sélectionner le DC-DC USB-C PD 5 A ; obtenir les prix réels.
- [ ] **P0 · 15/12 · (JC + Dobby)** Revalider les 10 articles P1 (~121 € historiques), les silentblocs et le coating ; aucun total final tant que les prix manquent.
- [ ] **P0 · accès local van · (Dobby + Forge)** Brancher/configurer le RUT240, établir le réseau van puis valider WiCAN → MQTT → HA, les entités réelles et Exosfer. Aucun flash requis pour ce premier diagnostic.
- [ ] **P0 · avant flash · (Dobby + Forge)** Corriger le GPIO8 du DS300 Tap et valider la chaîne d'alimentation.
- [ ] **P0 · 15/12 · (Dobby + JC)** Installer et tester l'ensemble dans Lupo.
- [ ] **À réception · (JC + Dobby)** Confirmer le second ZBDongle-E puis documenter son installation ; ne pas rouvrir pour autant le gel serre/maison.
- [ ] **P2 · quand JC voudra · (JC + Dobby)** Installer le Cozmo d'Anki en compagnon IA : réutiliser les leçons du Karotz (compatibilité WiFi, flash, interface web) → `cozmo-reborn/README.md` (fichier de travail) + `karotz-reborn/resurrection-karotz-2026-11-09.md`.

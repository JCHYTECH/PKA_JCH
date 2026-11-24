# TTD — Vue consolidée (tous projets)
> **Fichier dérivé** — généré à chaque `/save` depuis les seuls blocs `TTD — Pending` des thread files. Ne pas éditer à la main hors `/save` : la source de vérité reste les thread files + `etat-projets.md`.
> `last_updated: 2026-11-25 · by: deepseek-v4-pro` — harnais PKA cartographié + routage consolidé (AI_IT_TOOLS) + WildLens 3 sections (ARTEON)

## 01_AI_IT_TOOLS

Source : `01_AI_IT_TOOLS/thread-ai-it-tools.md`

- [ ] **P1 · — · (Dobby)** Câbler le Hub JCH : snapshot → radar + 5 boutons self-service (inbox/route, transcript, imprimer, recherche, save) — reporté « tout à l'heure » par JC
- [ ] **P2 · — · (JC + Dobby)** M1 : brancher Ethernet (dialogue ASIX AX88179B) + finaliser rotation secrets (repo public)
- [ ] **P2 · — · (Dobby)** Maintenance continue — `pka-thread-file` + boucle mémoire à chaque fin de session
- [ ] **P1 · — · (Dobby)** Ajouter un mode observation/dry-run aux watch loops (inspiré SuperAgent : évaluer le signal, enregistrer ce qu'il ferait, sans agir)
- [ ] **P2 · — · (JC + Dobby)** Essayer le TUI/double-clic Grok ; le rituel `/save` Kimi est terminé et ne fait plus partie de cet essai
- [ ] **P2 · — · (JC + Dobby)** ACL Tailscale — durcir l'accès réseau (reporté 13/11) : (1) poser la politique ACL (filet `autogroup:admin`→`*:*` ; `autogroup:member`↔`autogroup:member` ; `autogroup:member`→`tag:van:8123/1883/22222`) ; (2) taguer `lupo` en `tag:van`. Procédure prête (cf. `tailscale status` + `credentials-central.md`).
- [x] **P2 · — · (Dobby)** Mot de passe VNC dédié appliqué sur M5 + M1 (13/11) — plus l'admin ; raccourcis + onglets à jour
- [x] **P1 · — · (JC)** FDA accordée à `sshd-keygen-wrapper` (13/11) → raccourcis Bureau `M5-ecran-novnc.webloc` + `M1-ecran-novnc.webloc` créés. **Reste** : Accessibilité (épinglage UI encore bloqué — System Events pend en SSH).
- [ ] **P1 · — · (JC)** Réserver l'IP de l'EPSON ET-8550 en DHCP (actuellement .75, instable .65→.71→.75) pour stabiliser la file d'impression réseau
- [x] **P1 · Graph + transfert arteon.be CLOS · (JC + Dobby)** ✅ Connexion Graph lecture seule validée ; doublons supprimés (Roman Dillen) ; transfert arteon.be → Gmail actif (copie conservée côté arteon.be), testé le 24/11
- [x] **P2 · Yahoo → Gmail CLOS · (JC + Dobby)** ✅ `jc_havaux@yahoo.com` ajouté à Gmail (OAuth ShuttleCloud), import en tâche de fond (~3 600 mails, jusqu'à 2 j) ; fréquence auto (pas de réglage manuel OAuth) ; 2FA + mot de passe renouvelés ; email jchytech.be retiré (forwarde vers arteon.be).

## 02_ARTEON

Source : `02_ARTEON/thread-arteon.md`

- [ ] **P1 · — · (JC + Dobby)** Édition #3 : combler la photo Cadre + le Constat (trous signalés) ; vérifier les URLs FAO/UNEP du Constat #2 (fou de Bassan)
- [ ] **P1 · 2026-12-12 · (JC)** Valider l'édition #4 (pigeon ramier) → `draft → scheduled` + poser la photo en feature image Ghost
- [x] **P1 · — · (JC + Miel)** Valider le test voix JC #4 — ✅ validé par JC 23/11 (marqueur comblé + règle de modestie)
- [ ] **P1 · — · (JC)** Valider les réécritures voix-jc #1/#2/#3 (marqueur #1 graines + registre #3 tutoriel) puis basculer statut → published/scheduled et réimporter dans Ghost
- [ ] **P1 · — · (Jade)** Traduire les 3 éditions en italien (FR livré, EN en réserve) — après traction FR
- [ ] **P2 · — · (Dobby)** Recoller le hashtag #photographyethics (coupé au collage Instagram)
- [ ] **P3 · — · (JC)** Renouveler le token Instagram avant le 04/01/2026 (60 j)
- [ ] **P4 · — · (JC)** Allouer du temps créatif éditorial — blocage structurel : 8 étapes roadmap non closes
- [ ] **P6 · — · (Forge)** Presets brique 3 : masques IA (sujet/œil/plumage/arrière-plan) — design `strategy/brique-3-masques-ia-design.md`, tâche `task_a60c239c` ; brique 4 : endpoint `/recommend` (EXIF niveau 1 d'abord, Dobby)
- [ ] **P7 · — · (JC)** Nettoyer le doublon de preset LRC (37 importés au lieu de 36) + galerie avant/après définitive (12 paires)
- [ ] **P8 · M1 test aveugle · (JC + Dobby)** Correction manuelle de 16 photos (sélection `strategy/m1-test-aveugle-selection.md`) + jugement en aveugle ~5 photographes — critère « pire+indifférent » ≤ 50 % sinon stop. Préalables : mapping `LrC to-NN` → RAW `~/Pictures/` (JC fournit, ou correction directe dans Lightroom) ; trancher Nocturne (absent du corpus) + Golden hour (partiel). Découle du conseil `TEAM_Inbox/2026-11-16_dobby_conseil_correction-photo.md` (NO-GO service, GO conditionnel).
- [ ] **P9 · — · (JC + Dobby)** Choisir le tireur (compétence impression) — JC : s'associer à un pro du tirage ; Dobby : fournisseur white-label maintenant (coût unitaire + clause défauts), association différée post-édition #1 + apport marché B2B. Gate trafic avant galerie (2 000 visites qualifiées / 60 j)
- [ ] **P10 · — · (Dobby)** Tester l'édition #1 en pré-vente bornée (coût ~300–400 €, kill criteria : ≥ 8 préventes = GO) — uniquement après presets + WildLens

## 05_PHOTO_AI_JURY

Source : `05_PHOTO_AI_JURY/thread-photo-ai-jury.md`

- [ ] **P2 · — · (JCH + Argus)** Enregistrer des comparaisons A/B avec tutoriel et une validation sur image inédite ; aucune généralisation ou lot automatique avant ces données réelles
- [ ] **P2 · — · (Argus)** Prochaine fournée d'analyses seulement après décision de JC ; aucun appel IA payant effectué dans ce chantier
- [ ] **P1 · — · (Dobby)** Résoudre l'application du crop dans LrC : piste sidecar `.xmp` à côté du CR3 (au lieu du preset) ; test à refaire demain matin
- [ ] **P2 · — · (Dobby)** Repasser `untitled-2643.CR3` pour lui donner son crop (nombre d'or)

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

- [ ] **P0 · — · (JC)** Envoyer le mail unique aux Chinois via Outlook — `legal/courriers/2026-11-24_email-vetalyx-documents-merged-EN.md` (statuts v3 + pacte v4 + statut contrat-cadre)
- [ ] **P1 · — · (Renard)** Relecture indépendante des statuts v3 + pacte v4 (traductions EN incluses) avant signature
- [ ] **P1 · — · (Notaire)** Validation notaire (ISC, exercice fiscal 8 jan 2027 → 30 juin 2027, plafond « 2 administrateurs » Art. 15)
- [ ] **P1 · — · (JC)** R3 garantie Dixun — trancher puis rédiger la v5 du contrat-cadre (à partir du rapport AB), suite au call Li Yan
- [ ] **P2 · — · (Clio)** Trancher qualification AFMPS/FAMHP (DM vétérinaire vs médicament)
- [ ] **P2 · — · (Dobby)** Export BP statique (PDF) pour tiers
- [ ] **P2 · — · (veille)** 7 briefs actifs en mode exploration (voir tableau ci-dessous)

## 11_IOT

Source : `11_IOT/thread-iot.md`

- [ ] **P2 · continu · (Dobby)** Surveiller que `binary_sensor.raspberry_pi_power_status` reste `off` ; ré-intervenir sur l'alimentation/câble si récidive.
- [ ] **P0 · — · (JC)** RPi Home : diagnostic physique (alimentation/LED, microSD flash `rpi5-64`, Ethernet) puis probable re-flash HAOS — non joignable au 10/11.
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

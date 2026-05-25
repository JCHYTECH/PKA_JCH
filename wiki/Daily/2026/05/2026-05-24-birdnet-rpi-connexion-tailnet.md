---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — birdnet-rpi-connexion-tailnet

## Session — 10:09 — birdnet-rpi-connexion-tailnet

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
Session centrée sur BirdNET-Pi sur Raspberry Pi : accès Tools, modèle BirdNET installé, accès Safari iPhone, IPs locales et Tailscale, besoin d'URL stable, et consignes d'alimentation batterie RPI.

### Actions
Création d'une fiche d'accès BirdNET-Pi ; création du fichier connexion RPI.md ; ajout d'une règle mémoire Dobby sur la sauvegarde des informations d'accès techniques ; sauvegarde des IPs Tailscale iPhone/RPI ; clarification des URLs Safari et SSH Mac/iPhone.

### Décisions
Ne pas stocker les mots de passe en clair dans PKA ; utiliser Tailscale/IP 100.84.45.93 comme accès stable prioritaire au RPI ; conserver birdnetpi.local et 192.168.1.48 comme accès locaux ; distinguer birdnet comme login Tools et jchavaux comme user SSH ; ne pas alimenter le RPI par batterie brute sans régulation 5V stable.

### Prochaines étapes
Tester depuis iPhone Safari http://100.84.45.93 puis http://100.84.45.93:8080 ; vérifier Tailscale sur RPI avec tailscale status et tailscale ip -4 ; confirmer le port web BirdNET-Pi réel ; si besoin activer MagicDNS pour une URL tailnet nommée ; documenter toute nouvelle IP/URL/commande dans connexion RPI.md et BIRDNET_PI_ACCESS.md.

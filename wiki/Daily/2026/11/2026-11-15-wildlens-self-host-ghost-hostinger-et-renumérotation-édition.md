---
date: 2026-11-15
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-15 — WildLens self-host Ghost Hostinger et renumérotation éditions

## Session — 15:45 — WildLens self-host Ghost Hostinger et renumérotation éditions

### Contexte
- Modèle : deepseek-v4-pro
- Projet : ARTEON

### Résumé
Session centrée sur ARTEON/WildLens. Renumérotation des 4 éditions (archivage du transcript brut 04-18 et du template 06-20, ajout Keywords et tone). Correction du prix Ghost (18 USD/mois, pas 9). Décision de migration vers self-host Ghost : achat du VPS Hostinger KVM 1 (86,97 euros TTC/an) et installation complète du serveur (sécurité + Ghost v6.77.0 opérationnel, Node 22). Recherche des mails Gandi/ARTEON : société orban45.be identifiée (contact Roman) qui gère les IT de JC. Arrêt du contrat Orban à venir. DNS de wildlens bloqué en attendant la récupération du compte Gandi.

### Actions
- Renumérotation des éditions WildLens en séquence 1-4 ; archivage de 04-18 (transcript) et 06-20 (template)
- Ajout du bloc Keywords et du frontmatter tone/edition sur les éditions 1, 2, 3
- Correction du prix Ghost (9 vers 18 USD/mois) dans 4 fichiers
- Chiffrage des alternatives Ghost (self-host Hostinger, Magic Pages, beehiiv)
- Achat du VPS Hostinger KVM 1 (86,97 euros/an, échéance 15/11/2027)
- Installation serveur : sécurité (deploy, clé SSH, ufw, fail2ban), Node 22, nginx, MySQL, Ghost v6.77.0
- Runbook déposé : runbook-ghost-selfhost-hostinger.md
- Recherche mails Gandi/ARTEON via Gmail ; identification de orban45.be (Roman)

### Décisions
- Self-host Ghost sur VPS Hostinger KVM 1 (abandon de Ghost Pro 18 USD/mois) — VPS = brique réutilisable PKA
- Renumérotation des éditions WildLens (04-18 et 06-20 archivés)
- Prix Ghost corrigé : 18 USD/mois (Starter)
- Attendre le contact avec orban45.be avant de rompre le contrat IT

### Prochaines étapes
- Contacter Orban (orban45.be, Roman) pour récupérer le compte Gandi arteon.be
- Pointer le DNS wildlens vers 2.25.8.208 chez Gandi
- Configurer nginx + SSL + Mailgun + migration des 4 éditions
- (Optionnel) configurer OAuth Microsoft pour rétablir l'accès jchytech.be

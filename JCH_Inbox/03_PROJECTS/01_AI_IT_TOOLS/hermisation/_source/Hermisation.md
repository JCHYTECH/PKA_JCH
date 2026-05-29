# [[Hermisation]] du système PKA_JCH

[[PKA_JCH]]
[[AI-system]]
[[Dobby]]
[[multi-agent]]
[[Obsidian]]

Date : 2026-05-25

---

# 1. Définition du concept de « [[Hermisation]] »

Le terme « [[Hermisation]] » désigne le processus consistant à transformer progressivement le système PKA_JCH en une infrastructure AI :

- persistante ;
- mémorielle ;
- orchestrée ;
- documentée ;
- gouvernable ;
- modulaire ;
- extensible.

L’objectif n’est pas de reproduire exactement Hermes Agent.

L’objectif est de :

> intégrer les fonctions réellement utiles d’un système type Hermes dans une architecture interne maîtrisée.

---

# 2. Philosophie générale

La [[Hermisation]] doit rester :

- pragmatique ;
- progressive ;
- contrôlée ;
- documentée ;
- réversible.

Le projet ne doit jamais dériver vers :

- une pseudo AGI ;
- une autonomie incontrôlée ;
- une architecture opaque ;
- une multiplication anarchique des agents ;
- une dépendance excessive aux frameworks externes.

La priorité reste :

> continuité opérationnelle + capitalisation du savoir.

---

# 3. Objectifs de la [[Hermisation]]

## 3.1 Continuité entre les sessions

Le système doit :

- conserver les décisions ;
- conserver les workflows validés ;
- conserver les conventions ;
- conserver les états projets ;
- réduire les pertes de contexte.

---

## 3.2 Mémoire procédurale

Le système doit progressivement apprendre :

- les méthodes validées ;
- les structures de documents ;
- les workflows répétitifs ;
- les procédures techniques ;
- les conventions [[Obsidian]] ;
- les méthodes de gestion projet.

---

## 3.3 Gouvernance documentaire

Le système doit éviter :

- doublons ;
- désorganisation ;
- corruption des notes ;
- renommages incohérents ;
- écritures incontrôlées.

---

## 3.4 Coordination multi-agents

Le système doit permettre :

- routage ;
- spécialisation ;
- supervision ;
- journalisation ;
- suivi d’état ;
- orchestration légère.

---

## 3.5 Infrastructure durable

Le système doit être :

- maintenable ;
- compréhensible ;
- scalable raisonnablement ;
- sécurisé ;
- documenté.

---

# 4. Principes fondamentaux

## 4.1 [[Dobby]] reste central

[[Dobby]] reste :

- coordinateur principal ;
- superviseur ;
- répartiteur ;
- couche décisionnelle.

PKA-Hermes ne remplace pas [[Dobby]].

---

## 4.2 Les agents restent spécialisés

Chaque agent doit :

- avoir un rôle unique ;
- avoir un périmètre limité ;
- avoir des permissions minimales ;
- avoir une mémoire contrôlée.

---

## 4.3 Le contrôle humain reste obligatoire

Les décisions critiques doivent toujours être validées humainement.

Exemples :

- suppression ;
- déplacement massif ;
- publication ;
- envoi externe ;
- renommage global ;
- archivage critique.

---

## 4.4 La simplicité prime

Toute fonctionnalité ajoutée doit être :

- utile ;
- documentée ;
- maintenable ;
- compréhensible.

---

# 5. Architecture cible

## 5.1 Couche humaine

### MacBook M5

Fonctions :

- [[Obsidian]] ;
- coordination ;
- supervision ;
- développement ;
- validation ;
- cockpit principal.

---

## 5.2 Couche orchestration persistante

### VPS

Fonctions :

- APIs ;
- mémoire runtime ;
- automatisations ;
- journalisation ;
- services permanents ;
- queue système ;
- workflows.

Technologies possibles :

- [[Docker]] ;
- [[PostgreSQL]] ;
- [[Redis]] ;
- [[Qdrant]] ;
- [[FastAPI]] ;
- [[n8n]] ;
- [[Tailscale]].

---

## 5.3 Couche stockage

### NAS

Fonctions :

- archives ;
- datasets ;
- audio ;
- photos ;
- vidéos ;
- sauvegardes ;
- exports.

---

## 5.4 Couche terrain

### Raspberry / [[ESP32]]

Fonctions :

- [[BirdNET]] ;
- capteurs ;
- bioacoustique ;
- météo ;
- acquisition terrain.

---

# 6. Mémoire du système

## 6.1 Mémoire active

Contenu :

- états agents ;
- tâches ;
- logs ;
- workflows récents ;
- contexte runtime.

Localisation :

- VPS ;
- [[PostgreSQL]] ;
- [[Redis]].

---

## 6.2 Mémoire longue durée

Contenu :

- procédures ;
- templates ;
- architectures ;
- connaissances validées ;
- historique décisions ;
- workflows stabilisés.

Localisation :

- [[Obsidian]] ;
- NAS ;
- [[Git]] privé.

---

# 7. Système documentaire

## 7.1 [[Obsidian]] comme mémoire humaine principale

Le vault principal reste :

- local ;
- structuré ;
- maîtrisé ;
- gouverné.

---

## 7.2 Zones d’écriture agents

Les agents ne peuvent écrire que dans :

- dossiers dédiés ;
- zones runtime ;
- dossiers temporaires.

---

## 7.3 Journalisation obligatoire

Chaque agent doit enregistrer :

- actions ;
- fichiers modifiés ;
- date ;
- objectif ;
- statut.

---

# 8. Capitalisation procédurale

## 8.1 Principe

Chaque workflow validé doit devenir :

- template ;
- procédure ;
- note technique ;
- skill interne ;
- documentation réutilisable.

---

## 8.2 Exemples

- génération fichier Markdown ;
- création commande Terminal ;
- création BOM ;
- workflow [[BirdNET]] ;
- installation Raspberry ;
- préparation VPS ;
- génération rapports ;
- classement documents.

---

# 9. Sécurité

## 9.1 Least privilege

Chaque agent :

- accès minimal ;
- permissions limitées ;
- APIs limitées ;
- dossiers limités.

---

## 9.2 Séparation des niveaux

### Sandbox
Tests.

### Opérationnel
Workflows validés.

### Sensible
Validation humaine obligatoire.

---

## 9.3 Protection réseau

Utilisation recommandée :

- [[Tailscale]] ;
- VPN ;
- accès privés ;
- zéro exposition inutile.

---

## 9.4 Sauvegardes

Sauvegardes automatiques obligatoires :

- [[Obsidian]] ;
- [[PostgreSQL]] ;
- workflows ;
- agents ;
- configurations.

---

# 10. Étapes de [[Hermisation]]

## Phase 1 — Cartographie

Objectif :

documenter le système existant.

Actions :

- lister agents ;
- définir rôles ;
- identifier dépendances ;
- définir flux.

---

## Phase 2 — Gouvernance documentaire

Objectif :

stabiliser l’environnement documentaire.

Actions :

- conventions ;
- arborescences ;
- permissions ;
- zones runtime ;
- logs.

---

## Phase 3 — Infrastructure minimale

Objectif :

mettre en place le socle technique.

Actions :

- VPS ;
- [[Docker]] ;
- [[PostgreSQL]] ;
- APIs ;
- monitoring.

---

## Phase 4 — Mémoire procédurale

Objectif :

capitaliser les workflows.

Actions :

- templates ;
- procédures ;
- skills internes ;
- bibliothèque méthodes.

---

## Phase 5 — Extension progressive

Objectif :

augmenter les capacités après validation.

Extensions possibles :

- [[BirdNET]] ;
- automatisations ;
- workflows terrain ;
- audio ;
- vision ;
- agents spécialisés supplémentaires.

---

# 11. Critères de réussite

Le système doit :

- rester compréhensible ;
- rester gouvernable ;
- améliorer la continuité ;
- éviter le chaos documentaire ;
- réduire les pertes de contexte ;
- capitaliser les méthodes ;
- rester stable ;
- rester sécurisé.

---

# 12. Conclusion

La [[Hermisation]] du système PKA_JCH consiste à :

> construire progressivement une infrastructure AI persistante, gouvernée et capitalisante.

Le projet ne vise pas :
- la complexité maximale ;
- l’autonomie totale ;
- l’imitation aveugle de frameworks externes.

Le projet vise :

- stabilité ;
- mémoire ;
- orchestration ;
- gouvernance ;
- continuité ;
- efficacité opérationnelle.

La réussite dépendra principalement :

- de la qualité de l’architecture ;
- de la discipline documentaire ;
- de la gouvernance des agents ;
- de la progressivité des déploiements.

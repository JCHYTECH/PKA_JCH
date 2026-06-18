---
date: 2026-06-16
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1222
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-16

**Sessions analysées :** 3 | **Échanges :** 1222 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

Voici la rétrospective structurée des sessions du 2026-06-16.

## Décisions prises
- **Poursuite vers le choix RPi réaffirmée** : JCH décide de retourner au choix Raspberry Pi après avoir vérifié les coûts réels.
- **Traitement des projets prioritaires** : Les projets WildNexus, IoT et Travels sont identifiés. JCH décide d’utiliser NotebookLM pour créer les rapports correspondants.
- **Gestion de liste d’achat Mouser** : JCH importe une BOM via Mouser Belgium. L’assistant explique le format .xls/.csv nécessaire.
- **Utilisation de la clé Anthropic** décidée pour le M1 (migration depuis un autre environnement ?).
- **Règle A/B/C adoptée** : « le A on va attendre, le B on fait et le C processer » – segmentation explicite des tâches.
- **Mise à jour de la structure des dossiers projets** suite à une question de JCH (« pourquoi ne proposes-tu pas de les mettre dans les dossiers projets respectifs ? ») → l’assistant adapte son organisation.

## Échecs ouverts / bloqueurs
- **Erreur Arduino CLI** : L’installation échoue. JCH partage le lien de documentation mais aucun correctif n’est appliqué.
- **Erreur Telegram Bot** : `HTTP 409 Conflict` sur `getUpdates` – conflit de webhook ou doublon d’instance. Aucune résolution documentée.
- **Erreur d’approbation récurrente** : JCH demande « comment ne pas être bloqué par les demandes d’approbation » – le mécanisme d’approbation manuelle dans VS Code (ou autre outil) bloque le flux.
- **Échec de chargement d’une page** : `failed to load page` (probablement un site externe ou une page de doc).
- **Échec dans la commande curl vers Ollama** : la réponse JSON est tronquée (`"capabilities":["completion"]}`) mais aucune exploitation ni correction.
- **Problème de répertoire de démarrage** : `The terminal process failed to launch: Starting directory (cwd) "/Users/jchavauxm5/PK...` – path invalide ou inexistant.
- **Choix de caméra non résolu** : JCH mentionne « Arducam IMX500 AI Camera Module for ESP32-P4 » mais aucune décision finale n’est prise.

## Questions récurrentes (signe de lacune documentaire)
- **"Pourquoi on se balade depuis des minutes sur une mauvaise solution que tu proposes ?"** → signe que l’assistant propose sans valider le contexte ou les contraintes de JCH.
- **"Pourquoi ne proposes-tu pas de les mettre dans les dossiers projets respectifs ?"** → l’assistant n’applique pas spontanément la structure de dossiers déjà définie.
- **"Pourquoi en 2 tu parles de USB-A alors que le Mac a des USB-C ?"** → l’assistant ignore les specs réelles du matériel de JCH.
- **"Comment faire pour que tu aies accès à mes notes Apple ?"** → besoin d’intégration avec Apple Notes non documenté ni résolu.
- **"Pourquoi c’est exclusif Claude ?"** → interrogation sur les limitations par outil (DeepSeek vs Claude).
- **"Pourquoi maintenant tu as les références Mouser et avant pas ?"** → variation inexpliquée dans la qualité des réponses de l’assistant.

## Nouveaux patterns détectés
- **Prompt d’ordre d’intérêt** : JCH demande « fichiers en ordre d’intérêt et explique pourquoi. On décidera qu’en faire après. » → pattern de tri/priorisation systématique des fichiers (à automatiser ?).
- **Demande d’explication de décision de l’assistant** : JCH exige de plus en plus souvent une justification (« explique moi pourquoi maintenant tu as les ref mouser et avant pas ») → signe de méfiance.
- **Question philosophique récurrente** : « c’est quoi la peur pour toi ? » → JCH cherche à comprendre le modèle mental de l’assistant (métacognition).
- **Utilisation d’outils externes depuis le terminal** : JCH navigue vers un browser externe depuis VS Code (« tu sais comment on va sur un browser externe à vs code ? »).
- **Perte de contexte lors du changement de machine** : JCH travaille sur M1 puis M5, et craint de perdre ses outils → besoin de portabilité documentée.

## Efficacités / inefficacités
- **Efficacités** :
  - Utilisation de NotebookLM pour les rapports → bon automatisme.
  - Décision rapide d’attendre (le A) et de faire (le B) → bonne priorisation.
  - Question « fichiers en ordre d’intérêt » → méthode de tri rapide des artefacts.
- **Inefficacités** :
  - **Erreur Telegram non résolue** : le conflit 409 est un problème connu mais aucune mesure corrective.
  - **Erreur terminal launch path** : non corrigée, peut bloquer toute future session sur cette machine.
  - **Produit caméra non décidé** : la discussion part dans tous les sens (Arducam, OV5640, ESP32-S3, RPi) sans convergence.
  - **Assistance Mouser inutile** : JCH a dû demander « pourquoi maintenant tu as les ref mouser et avant pas » → l’assistant n’a pas fourni les références initialement, forçant JCH à chercher manuellement.
  - **Questions métaphysiques** : « c’est quoi la peur pour toi ? » fait perdre du temps sans valeur ajoutée immédiate.

## Ce qu’il faut garder en mémoire pour les prochaines sessions
1. **JCH travaille sur plusieurs machines (M1, M5, MacBook)** – toujours vérifier et adapter les chemins et outils.
2. **Les notes Apple sont utilisées** – trouver un moyen d’y accéder depuis l’assistant (API, export, etc.).
3. **Les décisions A/B/C doivent être écrites explicitement** dans un fichier ADR ou un TODO list.
4. **Le projet WildNexus est prioritaire** – toute documentation IoT doit y faire référence.
5. **Le conflit Telegram 409 doit être résolu** (supprimer le webhook ou arrêter l’autre instance).
6. **La liste d’achat Mouser est en cours** – suivre avec l’ordre réel.
7. **Le dossier de démarrage du terminal est cassé** sur `/Users/jchavauxm5/PK...` → corriger le chemin avant la prochaine session.

## Recommandations
1. **Créer un fichier `MACHINES.md`** listant les specs de chaque machine de JCH (M1, M5, MacBook) avec leurs OS, ports disponibles, outils installés. L’assistant s’y référera automatiquement.
2. **Automatiser le tri des fichiers** : implémenter un script `/bin/rank-files` qui prend un dossier et retourne les fichiers classés par intérêt estimé (taille, date, contenu clé). Cela évitera de perdre 5 minutes à chaque fois.
3. **Résoudre le conflit Telegram** : documenter la solution standard (stop bot, delete_webhook, restart). Si non résolu, le bot est inutilisable.
4. **Définir un format de réponse pour les propositions de matériel** : pour chaque composant, l’assistant doit fournir immédiatement 3 sources (Mouser, AliExpress, Digikey) avec prix et lien. Sinon, ne pas proposer.
5. **Interdire les questions philosophiques (ex: "c’est quoi la peur")** : JCH semble tester l’assistant, mais cela n’apporte pas de valeur pour le projet.
6. **Corriger le terminal launch path** immédiatement : vérifier que `/Users/jchavauxm5/PK...` existe ou recréer le symlink/dossier.
7. **Intégrer les notes Apple** : proposer une solution d’export automatique (Shortcuts ou script shell) pour que le contenu soit accessible dans le workspace.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 420
- Résolus automatiquement : 147
- Résolus manuellement : 0
- Encore ouverts : 273
- **Taux : 35.0%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 194.1
- Échanges/session début fenêtre : 74.4
- Tendance globale : 160.9%
- Tendance 3j-3j : 443.5%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Changement de clé Telegram** : motif de sécurité (nouveau message détecté)
- [Decision] Migration vers M1** : utilisation de la clé Anthropic sur macOS M1, abandonne la configuration précédente
- [Decision] Notebook LM pour rapports** : outil choisi pour consolider les rapports sur wildnexus, IoT, travels
- [Decision] Attente explicite** : performance 3% insuffisante → pas de déploiement immédiat
- [Decision] Point caméra WildNexus** : demande de résumé technique sur les défaillances camera (ref. 1005005710463218)
- [Decision] Matching capteurs IoT + M5** : align besoin IoT (van) avec hardware M5 disponible
- [Decision] Poursuite vers le choix RPi réaffirmée** : JCH décide de retourner au choix Raspberry Pi après avoir vérifié les coûts réels.
- [Decision] Traitement des projets prioritaires** : Les projets WildNexus, IoT et Travels sont identifiés. JCH décide d’utiliser NotebookLM pour créer les rapport
- [Decision] Gestion de liste d’achat Mouser** : JCH importe une BOM via Mouser Belgium. L’assistant explique le format .xls/.csv nécessaire.
- [Decision] Utilisation de la clé Anthropic** décidée pour le M1 (migration depuis un autre environnement ?).
- [Decision] Règle A/B/C adoptée** : « le A on va attendre, le B on fait et le C processer » – segmentation explicite des tâches.
- [Decision] Mise à jour de la structure des dossiers projets** suite à une question de JCH (« pourquoi ne proposes-tu pas de les mettre dans les dossiers projets 
- [Failure] (ref. 1005005710463218, 1005010226529230)
- [Failure] Problème électrique suspect (tensions 3V → 1.8V)
- [Failure] Configuration GPIO ESP32-S3 défaillante ou mauvais pinout
- [Failure] Action requise : debug matériel ou schéma de brochage erroné
- [Failure] Erreur : `pka-homeassistant: Stdio transport closed`
- [Failure] Impacte l'intégration PKA → HA
- [Failure] État : bloqué côté console
- [Failure] Erreur : `getUpdates` échoue, pas de handler error enregistré
- [Failure] Clé Telegram changée → resync requise
- [Failure] Status : script découvertes-collector bloqué
- [Failure] Caméra OV5640 inopérante** (ref. 1005005710463218, 1005010226529230)
- [Failure] MCP Server Home Assistant down
- [Failure] Telegram Bot — HTTP 409 Conflict
- [Failure] Erreur Arduino CLI** : L’installation échoue. JCH partage le lien de documentation mais aucun correctif n’est appliqué.
- [Failure] Erreur Telegram Bot** : `HTTP 409 Conflict` sur `getUpdates` – conflit de webhook ou doublon d’instance. Aucune résolution documentée.
- [Failure] Erreur d’approbation récurrente** : JCH demande « comment ne pas être bloqué par les demandes d’approbation » – le mécanisme d’approbation manuelle da
- [Failure] Échec de chargement d’une page** : `failed to load page` (probablement un site externe ou une page de doc).
- [Failure] Échec dans la commande curl vers Ollama** : la réponse JSON est tronquée (`"capabilities":["completion"]}`) mais aucune exploitation ni correction.
- [Failure] Problème de répertoire de démarrage** : `The terminal process failed to launch: Starting directory (cwd) "/Users/jchavauxm5/PK...` – path invalide ou 
- [Failure] Choix de caméra non résolu** : JCH mentionne « Arducam IMX500 AI Camera Module for ESP32-P4 » mais aucune décision finale n’est prise.

### Fréquence des patterns (14 jours)
- **Decision** : 10 jours, 473 occurrences
- **Failure** : 10 jours, 481 occurrences
- **Question** : 10 jours, 405 occurrences
- **Recurring question** : 10 jours, 240 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (9x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (9x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Failure] (9x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Question] (9x) pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo
- [Decision] (8x) dernier point, on va matcher les besoins de capteurs iot van avec les besoins de
- [Decision] (8x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Decision] (8x) je vais acheter l'officiel et aussi le ventilateur actif. pour celu
- [Decision] (8x) le A on va ttendre, le B on fait et le C processer
- [Decision] (8x) lement la clé anthropic fonctionne mais on va sur le M1
- [Decision] (8x) les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l
- [Decision] (8x) n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont
- [Decision] (8x) on va maintenant dans travels/ pka decouvertes. si j'envoie un me
- [Decision] (8x) on va valider les parametres indiqués du moment qu'on puisse ne c
- [Decision] (8x) oui on va donc retourner au choix RPI. tu as verifier les couts reels
- [Decision] (8x) our ce lieu directement ou doit il etre validé

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **foramnce par exemple de 3% cela ne vaut pas la peine**
- [ ] Documenter : **What's next:    Debug this container error with Gordon → docker ai "help me fix **
- [ ] Documenter : **pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo**
- [ ] Documenter : **dernier point, on va matcher les besoins de capteurs iot van avec les besoins de**
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **je vais acheter l'officiel et aussi le ventilateur actif. pour celu**
- [ ] Documenter : **le A on va ttendre, le B on fait et le C processer**
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**
- [ ] Documenter : **les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l**
- [ ] Documenter : **n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont**
- [ ] Documenter : **on va maintenant dans travels/ pka decouvertes. si j'envoie un me**
- [ ] Documenter : **on va valider les parametres indiqués du moment qu'on puisse ne c**
- [ ] Documenter : **oui on va donc retourner au choix RPI. tu as verifier les couts reels**
- [ ] Documenter : **our ce lieu directement ou doit il etre validé**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 32
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**139** recommandations au total — **139** ouvertes — **0** en cours — **0** terminées

⚠️ 22 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 114
- **Forge** : 21
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=121] (2026-06-16) **Dobby** : Fixer OV5640 / caméra WildNexus
- [id=122] (2026-06-16) **Dobby** : Checker brochage exact ESP32-S3 vs doc OV5640 24-pin
- [id=123] (2026-06-16) **Forge** : Créer test script + schéma de voltage
- [id=124] (2026-06-16) **Dobby** : Documenter solution dans `WILDNEXUS/03_P0_ENGINEERING/05_SIMULATION/`
- [id=125] (2026-06-16) **Dobby** : Relancer MCP HA + Telegram

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.99 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.99**

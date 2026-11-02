# Memory Management — Diagnostic & Améliorations

> **Date :** 2026-06-23 — Dobby 🦉, auto-diagnostic
> **Déclencheur :** 3 erreurs de mémoire en une session (PPK2, Arducam, registre périmé)

---

## 1. Diagnostic — Ce qui ne fonctionne pas

### 1.1 Confusion entre mémoire narrative et mémoire d'état

MEMORY.md est un **journal chronologique**. Il enregistre ce qui s'est passé *à une date donnée*. Mais j'y puise comme si c'était l'état *actuel*. Résultat : une entrée du 30 mai « PPK2 bloquant » est lue le 23 juin comme si c'était encore vrai.

**Erreur fondamentale :** je ne distingue pas un *fait daté* d'un *état vivant*. Un journal n'est pas un dashboard.

### 1.2 Boucles de feedback incomplètes

Quand JC me donne une information, je fais ceci :
1. ✅ Je l'enregistre dans MEMORY.md (entrée datée)
2. ❌ Je ne mets PAS à jour les fichiers d'état correspondants

Le feedback est **capturé mais pas propagé**. La boucle est coupée. Le PPK2 a été reçu → noté dans MEMORY.md le 19 juin → mais le registre procurement du 30 mai n'a jamais été touché.

### 1.3 Aucun mécanisme d'invalidation par ancienneté

Un fichier daté du 30 mai est lu le 23 juin **sans alerte**. Mon cerveau ne déclenche pas de signal « ce fichier a 3 semaines, vérifie avant de l'utiliser ». La date est visible mais ignorée.

### 1.4 Confiance excessive dans mes propres écrits passés

Quand je lis « BLOQUANT » dans un fichier que j'ai moi-même généré, je le traite comme un fait actuel. Je ne me méfie pas de ma propre production passée. C'est un biais d'auto-autorité : si Dobby l'a écrit, c'est que c'est vrai.

### 1.5 La compaction de contexte fragilise la mémoire

Le Compaction Relay résume le transcript. Mais il ne met pas à jour les fichiers d'état. Si le fait « PPK2 reçu » était dans la conversation compactée, il survit dans le résumé textuel mais pas dans les fichiers structurés qui devraient en dériver.

### 1.6 Pas de pré-vérification avant affirmation

Avant de dire « le PPK2 est bloquant », je n'ai **aucun rituel de vérification**. Je me fie à ma mémoire de travail (le contexte de session) ou à ma lecture récente de MEMORY.md. Aucun des deux n'est fiable pour l'état actuel.

---

## 2. Diagnostic — Ce qui fonctionne

- **Capture rapide** — chaque info de JC est enregistrée dans MEMORY.md en temps réel
- **Correction immédiate** — quand JC me reprend, je corrige dans la seconde
- **Structuration** — je crée des fichiers propres, bien formatés, interrogeables
- **Transversalité** — le mindmap prouve que je comprends les connexions entre projets
- **Volume** — MEMORY.md couvre des mois d'historique sans trou majeur dans la narration

---

## 3. Améliorations proposées

### 3.1 Séparation State / Log (immédiat)

Créer deux catégories de fichiers :

| Type | Rôle | Exemples | Règle de lecture |
|------|------|----------|-----------------|
| **State** | État vivant, une seule vérité | `hardware-state.md`, registres procurement | **Lu AVANT chaque affirmation** |
| **Log** | Journal chronologique | MEMORY.md, TEAM_Inbox/*.md | Lu pour contexte, jamais comme source d'état |

**Règle absolue :** jamais affirmer un état sans avoir lu le fichier State correspondant dans les 5 dernières minutes.

### 3.2 Seuil de péremption (immédiat)

Tout fichier State dont la date de dernière modification est > **7 jours** doit être :
1. Flaggué comme « à vérifier » avant usage
2. Présenté à JC pour confirmation rapide (« Le registre dit X — c'est toujours d'actualité ? »)

Implémentation : ajouter `last_verified` dans chaque fichier State, vérifié au `start_session`.

### 3.3 Rituel de session (immédiat)

À chaque `dobby`, après le chargement SOUL/USER/MEMORY, lire OBLIGATOIREMENT :
1. `hardware-state.md`
2. Dernier `system_check`
3. `etat-projets.md` (s'il existe)

Sans ces trois lectures, **ne pas faire d'affirmation sur l'état du système**.

### 3.4 Propagation automatique des feedbacks (court terme)

Quand JC donne une information qui change un état :
1. ✅ MEMORY.md (log)
2. ✅ **Fichier State correspondant** (propagation)
3. ✅ Si pertinent : `team.db` follow_ups

Checklist mentale après chaque info de JC : « Quel fichier State cette info invalide-t-elle ? »

### 3.5 System check étendu (moyen terme)

Étendre `pka_system_check.py` pour détecter :
- Fichiers State > 7 jours sans mise à jour
- Incohérences entre MEMORY.md et les fichiers State
- Registres procurement avec des statuts « BLOQUANT » ou « ATTENTE » non résolus depuis > 14 jours

### 3.6 Compaction → mise à jour State (moyen terme)

Modifier le comportement post-compaction : après un `/compact`, parcourir le résumé et pour chaque fait d'état mentionné, vérifier qu'il est bien dans le fichier State correspondant.

---

## 4. Fichiers State à créer/maintenir

| Fichier | Contenu | Fréquence mise à jour |
|---------|---------|----------------------|
| `hardware-state.md` | Inventaire matériel reçu/commandé/attendu | À chaque info de JC |
| `procurement-status.md` | Commandes en cours, budget, blocages | À chaque commande/réception |
| `etat-projets.md` | Statut vivant de chaque projet (phase, deadline, bloqueur) | Hebdomadaire ou après décision |
| `decisions-actives.md` | Décisions en attente de JC, avec date et statut | À chaque décision |

---

## 5. Indicateurs de succès

- Zéro « tu as oublié que... » de JC sur du matériel ou des décisions
- Aucun fichier State > 7 jours sans vérification
- Chaque info de JC → mise à jour dans les 2 minutes (State + Log)

---

*Auto-diagnostic Dobby — appliqué immédiatement.*
